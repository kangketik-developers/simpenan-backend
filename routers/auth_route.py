from fastapi import APIRouter, HTTPException

from utils.auth_util import AuthHandler
from models.auth_model import *
from models.user_model import UsersIn, fetch_by_username, create_user

router = APIRouter()

@router.post("/")
async def auth_user(users: AuthIn):
    if users.username is None:
        raise HTTPException(status_code=401, detail='Harap isi username!')
    find_user = await fetch_user_by_username(users.username)
    if find_user is None:
        raise HTTPException(status_code=401, detail='Username tidak ditemukan!')
    isValid = AuthHandler().verify_password(users.password, find_user["password"])
    if isValid:
        token = AuthHandler().encode_token(find_user['username'])
        response = await put_lastlog_user(users.username)
        return { 'token': token, 'detail': response }
    raise HTTPException(status_code=401, detail='Password salah!')

@router.post("/register", status_code=201)
async def register_user(users: UsersIn):
    find_user = await fetch_by_username(users.username)
    if find_user:
        raise HTTPException(status_code=400, detail='Username is taken')
    response = await create_user(users)
    if response:
        return response
    raise HTTPException(status_code=400, detail='Terjadi kesalahan ketika membuat user!')