import os
import uuid
import pytz
import aiofiles

from datetime import date
from werkzeug.utils import secure_filename
from fastapi import APIRouter, HTTPException, File, UploadFile, exceptions

from models.inmates.inmates_model import fetch_all_inmates_label, fetch_by_inmates_name
from models.attendance.sign_in_attendance_model import *
from models.attendance.sign_out_attendance_model import *

from utils.attendance_util import rules_absensi
from utils.detector_util import detect

router = APIRouter()

BASE_PATH = os.path.abspath(os.path.dirname("."))
ATT_CAP_PATH = os.path.join(BASE_PATH, "uploads/attendance_cap")

@router.post("/", response_model=AttendancePostOut)
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
    find_inmates = await fetch_by_inmates_name(results[0])
    if os.path.exists(folder_berkas):
        os.remove(folder_berkas)
    if find_inmates:
        find_attendance = await fetch_by_inmates_id(find_inmates.id)
        if find_attendance:
            jam = datetime.datetime.now(pytz.timezone('Asia/Jakarta')).time().strftime("%H:%M:%S")
            nilai_absen = find_attendance.attendance_score + 2.5
            response = await put_attendance_sign_out(find_attendance.id, jam, nilai_absen)
            if response:
                return {
                    "id": find_attendance.id,
                    "name": results[0],
                    "confident": results[1],
                    "messages": results[2]
                }
    raise HTTPException(status_code=400, detail=f'Terjadi kesalahan ketika menyimpan capture!')
