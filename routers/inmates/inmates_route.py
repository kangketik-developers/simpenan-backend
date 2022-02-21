import os, shutil

from fastapi import APIRouter, HTTPException
from fastapi_pagination import Page, add_pagination, paginate

from models.inmates.inmates_model import *
from models.inmates.inmates_video_model import fetch_all_vid_inmates_by_inmates_id, delete_inmates_vid
from models.inmates.inmates_document_model import fetch_all_doc_inmates_by_inmates_id, delete_inmates_doc

router = APIRouter()

BASE_PATH = os.path.abspath(os.path.dirname("."))
DOCS_UPLOAD_PATH = os.path.join(BASE_PATH, "uploads/inmates_files")
VIDS_UPLOAD_PATH = os.path.join(BASE_PATH, "uploads/inmates_videos")
FACES_UPLOAD_PATH = os.path.join(BASE_PATH, "assets/faces")

@router.get("/", response_model=Page[InmatesOut])
async def show_all_inmates():
    response = await fetch_all_inmates()
    return paginate(response)

@router.get("/{id}", response_model=InmatesOut)
async def show_one_inmates(id: str):
    response = await fetch_by_inmates_id(id)
    if response:
        return response
    raise HTTPException(404, f"tidak ada warga binaan dengan id {id}")

@router.post("/", status_code=201)
async def create_inmates(inmates: InmatesIn):
    find_inmates = await fetch_by_inmates_name(inmates.name)
    if find_inmates:
        raise HTTPException(status_code=400, detail='warga binaan sudah terdaftar!')
    response = await post_inmates(inmates)
    if response:
        return response
    raise HTTPException(status_code=400, detail='Terjadi kesalahan ketika membuat warga binaan!')


@router.put("/{id}/")
async def update_inmates(id, inmates: InmatesIn):
    response = await put_inmates(id, inmates)
    if response:
        return response
    raise HTTPException(status_code=400, detail='Terjadi kesalahan ketika memperbarui warga binaan!')

@router.delete("/{id}")
async def remove_inmates(id: str):
    response = await delete_inmates(id)
    if response:
        documents = await fetch_all_doc_inmates_by_inmates_id(id)
        for doc in documents:
            await delete_inmates_doc(doc.id)
            documents_file = os.path.join(DOCS_UPLOAD_PATH, doc.filename)
            if os.path.exists(documents_file):
                os.remove(documents_file)
        videos = await fetch_all_vid_inmates_by_inmates_id(id)
        for video in videos:
            await delete_inmates_vid(video.id)
            video_file = os.path.join(VIDS_UPLOAD_PATH, video.videoname)
            if os.path.exists(video_file):
                os.remove(video_file)
            face_file = os.path.join(FACES_UPLOAD_PATH, video.sampledirname)
            if os.path.exists(face_file):
                shutil.rmtree(face_file)
        return response
    raise HTTPException(status_code=400, detail='Terjadi kesalahan ketika menghapus warga binaan!')

@router.delete("/")
async def remove_all_inmates():
    inmates = await fetch_all_inmates()
    if inmates:
        for inmate in inmates:
            await delete_inmates(inmate.id)
            documents = await fetch_all_doc_inmates_by_inmates_id(inmate.id)
            for doc in documents:
                await delete_inmates_doc(doc.id)
                documents_file = os.path.join(DOCS_UPLOAD_PATH, doc.filename)
                if os.path.exists(documents_file):
                    os.remove(documents_file)
            videos = await fetch_all_vid_inmates_by_inmates_id(inmate.id)
            for video in videos:
                await delete_inmates_vid(video.id)
                video_file = os.path.join(VIDS_UPLOAD_PATH, video.videoname)
                if os.path.exists(video_file):
                    os.remove(video_file)
                face_file = os.path.join(FACES_UPLOAD_PATH, video.sampledirname)
                if os.path.exists(face_file):
                    shutil.rmtree(face_file)
        return { "detail" : "Seluruh warga binaan berhasil dihapus!"}
    raise HTTPException(status_code=400, detail='Terjadi kesalahan ketika menghapus warga binaan!')



add_pagination(router)