import os
import shutil

import aiofiles
from fastapi import APIRouter, HTTPException, File, UploadFile, exceptions
from fastapi_pagination import Page, add_pagination, paginate
from werkzeug.utils import secure_filename

from models.inmates.inmates_model import fetch_by_inmates_id
from models.inmates.inmates_video_model import *
from utils.generator_util import split_from_videos

router = APIRouter()

BASE_PATH = os.path.abspath(os.path.dirname("."))
VIDS_UPLOAD_PATH = os.path.join(BASE_PATH, "uploads/inmates_videos")
FACES_UPLOAD_PATH = os.path.join(BASE_PATH, "assets/faces")


@router.get("/", response_model=Page[VidInmatesOut])
async def show_all_inmates_document():
    response = await fetch_all_vid_inmates()
    return paginate(response)


@router.get("/{id}", response_model=VidInmatesOut)
async def show_one_inmates_document(id: str):
    response = await fetch_by_inmates_vid_id(id)
    if response:
        return response
    raise HTTPException(404, f"Tidak ada video dengan id {id}")


@router.post("/{id}", status_code=201)
async def create_inmates_document(id: str, file: UploadFile = File(...)):
    find_inmates = await fetch_by_inmates_id(id)
    if find_inmates is None:
        raise HTTPException(status_code=400, detail=f'Warga binaan dengan id {id} tidak ditemukan!')
    videoname = secure_filename(file.filename).lower()
    sampledirname = secure_filename(find_inmates["name"]).lower()
    find_video_inmates = await fetch_by_inmates_vid_inmates_id(id)
    if find_video_inmates:
        raise HTTPException(status_code=400, detail=f'Video untuk warga binaan dengan id {id} sudah terdaftar!')
    filename = secure_filename(videoname).lower()
    folder_berkas = os.path.join(VIDS_UPLOAD_PATH, filename)
    try:
        async with aiofiles.open(folder_berkas, 'wb') as out_file:
            content = await file.read()
            await out_file.write(content)
    except exceptions as e:
        raise HTTPException(status_code=400, detail=f'Terjadi kesalahan ketika menyimpan video! {e}')
    totalsample = split_from_videos(folder_berkas, sampledirname)
    response = await post_inmates_vid(id, videoname, sampledirname, totalsample)
    if response:
        return response
    raise HTTPException(status_code=400, detail='Terjadi kesalahan ketika menyimpan video!')


@router.delete("/{id}")
async def remove_inmates_document(id: str):
    find_vid_inmates = await fetch_by_inmates_vid_id(id)
    if find_vid_inmates is None:
        raise HTTPException(status_code=400, detail=f'Video dengan id {id} tidak ditemukan!')
    video_file = os.path.join(VIDS_UPLOAD_PATH, find_vid_inmates["videoname"])
    face_file = os.path.join(FACES_UPLOAD_PATH, find_vid_inmates["sampledirname"])
    if os.path.exists(video_file):
        os.remove(video_file)
    if os.path.exists(face_file):
        shutil.rmtree(face_file)
    response = await delete_inmates_vid(id)
    if response:
        return response
    raise HTTPException(status_code=400, detail='Terjadi kesalahan ketika menghapus video!')


add_pagination(router)
