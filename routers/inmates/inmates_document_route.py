import os
import aiofiles

from werkzeug.utils import secure_filename
from fastapi import APIRouter, HTTPException, File, Form, UploadFile, exceptions
from fastapi_pagination import Page, add_pagination, paginate

from models.inmates.inmates_document_model import *
from models.inmates.inmates_model import fetch_by_inmates_id

router = APIRouter()

BASE_PATH = os.path.abspath(os.path.dirname("."))
DOCS_UPLOAD_PATH = os.path.join(BASE_PATH, "uploads/inmates_files")

@router.get("/", response_model=Page[DocInmatesOut])
async def show_all_inmates_document():
    response = await fetch_all_doc_inmates()
    return paginate(response)

@router.get("/{id}", response_model=DocInmatesOut)
async def show_one_inmates_document(id: str):
    response = await fetch_by_inmates_doc_id(id)
    if response:
        return response
    raise HTTPException(404, f"Tidak ada dokumen dengan id {id}")

@router.post("/{id}", status_code=201)
async def create_inmates_document(id: str, description: str = Form(...), file: UploadFile = File(...)):
    find_inmates = await fetch_by_inmates_id(id)
    if find_inmates is None:
        raise HTTPException(status_code=400, detail=f'Warga binaan dengan id {id} tidak ditemukan!')
    find_doc_inmates = await fetch_by_inmates_doc_desc(description)
    if find_doc_inmates:
        raise HTTPException(status_code=400, detail='Dokumen sudah terdaftar!')
    extensi = file.filename.rsplit(".", 1)[1]
    filename = secure_filename(description + "." + extensi).lower()
    folder_berkas = os.path.join(DOCS_UPLOAD_PATH, filename)
    try: 
        async with aiofiles.open(folder_berkas, 'wb') as out_file:
            content = await file.read()
            await out_file.write(content)
    except exceptions as e:
        raise HTTPException(status_code=400, detail=f'Terjadi kesalahan ketika menyimpan dokumen! {e}')
    inmates_doc = DocInmatesIn(description=description)
    response = await post_inmates_doc(inmates_doc, id, filename)
    if response:
        return response
    raise HTTPException(status_code=400, detail='Terjadi kesalahan ketika menyimpan dokumen!')
    

@router.delete("/{id}")
async def remove_inmates_document(id: str):
    find_doc_inmates = await fetch_by_inmates_doc_id(id)
    if find_doc_inmates is None:
        raise HTTPException(status_code=400, detail=f'Dokumen dengan id {id} tidak ditemukan!')
    documents_file = os.path.join(DOCS_UPLOAD_PATH, find_doc_inmates["filename"])
    if os.path.exists(documents_file):
        os.remove(documents_file)
    response = await delete_inmates_doc(id)
    if response:
        return response
    raise HTTPException(status_code=400, detail='Terjadi kesalahan ketika menghapus dokumen!')

add_pagination(router)