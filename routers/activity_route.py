from fastapi import APIRouter, HTTPException
from fastapi_pagination import Page, add_pagination, paginate

from models.activity_model import *

router = APIRouter()


@router.get("/", response_model=Page[ActivityOut])
async def show_all_activity():
    response = await fetch_all_activities()
    return paginate(response)


@router.get("/{id}", response_model=ActivityOut)
async def show_one_activity(id: str):
    response = await fetch_by_activity_id(id)
    if response:
        return response
    raise HTTPException(404, f"tidak ada kegiatan dengan id {id}")


@router.post("/", status_code=201)
async def create_activity(activity: ActivityIn):
    find_activity = await fetch_by_activity_desc(activity.description)
    if find_activity:
        raise HTTPException(status_code=400, detail='Kegiatan sudah terdaftar!')
    response = await post_activity(activity)
    if response:
        return response
    raise HTTPException(status_code=400, detail='Terjadi kesalahan ketika membuat kegiatan!')


@router.put("/{id}/")
async def update_activity(id, activity: ActivityIn):
    response = await put_activity(id, activity)
    if response:
        return response
    raise HTTPException(status_code=400, detail='Terjadi kesalahan ketika memperbarui kegiatan!')


@router.delete("/{id}")
async def remove_user(id: str):
    response = await delete_activity(id)
    if response:
        return response
    raise HTTPException(status_code=400, detail='Terjadi kesalahan ketika menghapus kegiatan!')


add_pagination(router)
