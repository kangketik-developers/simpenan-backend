from fastapi import APIRouter, HTTPException
from fastapi_pagination import Page, add_pagination, paginate

from utils.auth_util import AuthHandler
from models.user_model import *

router = APIRouter()

@router.get("/", response_model=Page[UsersOut])
async def show_all_users():
    response = await fetch_all_users()
    return paginate(response)

@router.get("/{id}", response_model=UsersOut)
async def show_one_user(id: str):
    response = await fetch_by_id(id)
    if response:
        return response
    raise HTTPException(404, f"tidak ada user dengan login {id}")

@router.post("/", status_code=201)
async def register_user(users: UsersIn):
    find_user = await fetch_by_username(users.username)
    if find_user:
        raise HTTPException(status_code=400, detail='Username is taken')
    response = await create_user(users)
    if response:
        return response
    raise HTTPException(status_code=400, detail='Terjadi kesalahan ketika membuat user!')

@router.put("/{id}/")
async def update_user(id, users: UsersIn):
    response = await put_user(id, users)
    if response:
        return response
    raise HTTPException(status_code=400, detail='Terjadi kesalahan ketika memperbarui user!')

@router.put("/change_password/{id}")
async def change_password(id, old_password: str, new_password):
    find_user = await fetch_by_id(id)
    if find_user is None:
        raise HTTPException(status_code=400, detail=f'User dengan id {id} tidak ditemukan!')
    isValid = AuthHandler().verify_password(old_password, find_user["password"])
    if isValid:
        return await put_new_password(id, new_password)
    raise HTTPException(status_code=400, detail='Pasword lama, salah!')

@router.delete("/{id}")
async def remove_user(id: str):
    response = await delete_user(id)
    if response:
        return response
    raise HTTPException(status_code=400, detail='Terjadi kesalahan ketika menghapus user!')

add_pagination(router)