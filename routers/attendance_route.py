import os
import uuid
import pytz
import aiofiles
import datetime

from werkzeug.utils import secure_filename
from fastapi import APIRouter, HTTPException, File, UploadFile, exceptions
from fastapi_pagination import Page, add_pagination, paginate

from models.inmates.inmates_model import fetch_all_inmates_label, fetch_by_inmates_name
from models.inmates.inmates_score_model import *
from models.attendance_model import *

from utils.attendance_util import rules_absensi, hitung_hari
from utils.detector_util import detect

router = APIRouter()

total_hari = hitung_hari()

BASE_PATH = os.path.abspath(os.path.dirname("."))
ATT_CAP_PATH = os.path.join(BASE_PATH, "uploads/attendance_cap")

@router.get("/", response_model=Page[AttendancePostDb])
async def show_all_attendance():
    response = await fetch_all_atendance()
    return paginate(response)

@router.post("/masuk", response_model=AttendanceOut)
async def capture_sign_in_attendance(file: UploadFile = File(...)):
    labels = []
    filename = secure_filename(str(uuid.uuid4())).lower()
    folder_berkas = os.path.join(ATT_CAP_PATH, f"{filename}.jpeg")
    try:
        async with aiofiles.open(folder_berkas, 'wb') as out_file:
            content = await file.read()
            await out_file.write(content)
    except exceptions as e:
        raise HTTPException(status_code=400, detail=f'Terjadi kesalahan ketika menyimpan capture! {e}')
    inmates = await fetch_all_inmates_label()
    for inmate in inmates:
        labels.append(inmate.name)
    labels.sort()
    results = detect(labels, folder_berkas)
    # 
    find_inmates = await fetch_by_inmates_name(results[0])
    tanggal = datetime.datetime.now().date().strftime("%Y-%m-%d")
    month = datetime.datetime.now().date().strftime("%m")
    year = datetime.datetime.now().date().strftime("%Y")
    jam = datetime.datetime.now(pytz.timezone('Asia/Jakarta')).time().strftime("%H:%M:%S")
    nilai_absen = rules_absensi()
    nilai_kegiatan = 42
    nilai_total = nilai_absen+nilai_kegiatan
    # 
    if os.path.exists(folder_berkas):
        os.remove(folder_berkas)
    if find_inmates:
        find_attandance = await fetch_attendance_by_inmates_id_and_date(find_inmates.id, tanggal)
        if find_attandance is None:
            find_score = await fetch_inmates_score_by_args(find_inmates.id, int(month), int(year))
            if find_score is None:
                score = InmatesScoreIn(
                    inmates_id=find_inmates.id,
                    name=find_inmates.name,
                    month=month,
                    year=year,
                    total_score=nilai_total,
                    percentage_score=round(nilai_total/total_hari, 2)
                )
                await post_inmates_score(score)
            else:
                score = InmatesScoreIn(
                    inmates_id=find_inmates.id,
                    name=find_inmates.name,
                    month=month,
                    year=year,
                    total_score=find_score.total_score+nilai_total,
                    percentage_score=round((find_score.total_score+nilai_total)/total_hari, 2)
                )
                await put_inmates_score(find_score.id, score)
            await post_attendance_sign_in(find_inmates.id, find_inmates.name, tanggal, jam, nilai_absen, nilai_kegiatan, nilai_total)
        return {
            "id": find_inmates.id,
            "name": results[0],
            "confident": results[1],
            "messages": results[2]
        }
    raise HTTPException(status_code=400, detail=f'Terjadi kesalahan ketika menyimpan capture!')

@router.put("/pulang", response_model=AttendanceOut)
async def capture_sign_out_attendance(file: UploadFile = File(...)):
    labels = []
    print(total_hari)
    filename = secure_filename(str(uuid.uuid4())).lower()
    folder_berkas = os.path.join(ATT_CAP_PATH, f"{filename}.jpeg")
    try:
        async with aiofiles.open(folder_berkas, 'wb') as out_file:
            content = await file.read()
            await out_file.write(content)
    except exceptions as e:
        raise HTTPException(status_code=400, detail=f'Terjadi kesalahan ketika menyimpan capture! {e}')
    inmates = await fetch_all_inmates_label()
    for inmate in inmates:
        labels.append(inmate.name)
    labels.sort()
    results = detect(labels, folder_berkas)
    find_inmates = await fetch_by_inmates_name(results[0])
    if os.path.exists(folder_berkas):
        os.remove(folder_berkas)
    if find_inmates:
        find_attendance = await fetch_attendance_by_inmates_id(find_inmates.id)
        if find_attendance:
            jam = datetime.datetime.now(pytz.timezone('Asia/Jakarta')).time().strftime("%H:%M:%S")
            month = datetime.datetime.now().date().strftime("%m")
            year = datetime.datetime.now().date().strftime("%Y")
            nilai_absen = find_attendance.attendance_score + 2.5
            nilai_total = find_attendance.total_score+2.5
            if find_attendance.sign_out is None:
                find_score = await fetch_inmates_score_by_args(find_inmates.id, int(month), int(year))
                if find_score is None:
                    score = InmatesScoreIn(
                        inmates_id=find_inmates.id,
                        name=find_inmates.name,
                        month=month,
                        year=year,
                        total_score=nilai_total,
                        percentage_score=round(nilai_total/total_hari, 2)
                    )
                    await post_inmates_score(score)
                else:
                    score = InmatesScoreIn(
                        inmates_id=find_inmates.id,
                        name=find_inmates.name,
                        month=month,
                        year=year,
                        total_score=find_score.total_score+2.5,
                        percentage_score=round((find_score.total_score+2.5)/total_hari, 2)
                    )
                    await put_inmates_score(find_score.id, score)
                await put_attendance_sign_out(find_attendance.id, jam, nilai_absen, nilai_total)
            return {
                "id": find_attendance.id,
                "name": results[0],
                "confident": results[1],
                "messages": results[2]
            }
    raise HTTPException(status_code=400, detail=f'Terjadi kesalahan ketika menyimpan capture!')

@router.delete("/")
async def remove_all_attendance():
    attendances = await fetch_all_atendance()
    if attendances:
        for attendance in attendances:
            await delete_attendance(attendance.id)
        scores = await fetch_all_inmates_score()
        for score in scores:
            await delete_inmates_score(score.id)
        return { "detail" : "Seluruh absensi berhasil dihapus!"}
    raise HTTPException(status_code=400, detail='Terjadi kesalahan ketika menghapus absensi!')

@router.delete("/{id}")
async def remove_attendance(id: str):
    response = await delete_attendance(id)
    if response:
        return response
    raise HTTPException(status_code=400, detail='Terjadi kesalahan ketika menghapus user!')

add_pagination(router)