import uuid
import datetime
import motor.motor_asyncio

from typing import Optional
from pydantic import BaseModel

from utils.auth_util import AuthHandler

class UsersIn(BaseModel):
    fullname: str
    username: str

class UsersOut(BaseModel):
    id: str
    fullname: str
    username: str
    lastlog: Optional[datetime.datetime]
    created_at: datetime.datetime
    updated_at: Optional[datetime.datetime]

class UsersDB(BaseModel):
    id: str
    fullname: str
    username: str
    password: str
    lastlog: Optional[datetime.datetime]
    created_at: datetime.datetime
    updated_at: Optional[datetime.datetime]

client = motor.motor_asyncio.AsyncIOMotorClient("mongodb://localhost:27017")
database = client.simpenan
collection = database.users

async def fetch_all_users():
    users = []
    cursor = collection.find({})
    async for document in cursor:
        users.append(UsersOut(**document))
    return users

async def fetch_by_id(id):
    document = await collection.find_one({ "id": id })
    return document

async def fetch_by_username(username):
    document = await collection.find_one({ "username": username })
    return document

async def create_user(user):
    document = user.dict()
    random_pass = AuthHandler().pwd_gen()
    hashed_password = AuthHandler().get_password_hash(random_pass)
    result = await collection.insert_one(
        UsersDB(
            **document, 
            id=str(uuid.uuid4()), 
            password=hashed_password,
            created_at=datetime.datetime.today()
        ).dict()
    )
    if result :
        return { "detail" : f"User berhasil disimpan dengan password {random_pass}!"}
    return 0

async def put_user(id, user):
    result = await collection.find_one({ "id": id })
    response = await collection.update_one(
        { "id": id }, 
        { 
            "$set": UsersDB(
                **user.dict(),
                id=id,
                password=result["password"],
                created_at=result["created_at"],
                updated_at=datetime.datetime.today()
            ).dict()
        }
    )
    if response :
        return { "detail" : "User berhasil diperbarui!"}
    return 0

async def put_new_password(id, password):
    hashed_password = AuthHandler().get_password_hash(password)
    await collection.update_one(
        { "id": id }, 
        { 
            "$set": {"password": hashed_password } 
        }
    )
    await collection.update_one(
        { "id": id }, 
        { 
            "$set": {"updated_at": datetime.datetime.today() } 
        }
    )
    result = await collection.find_one({ "id": id })
    if result :
        return { "detail" : "Password berhasil diperbarui!"}
    return 0

async def delete_user(id):
    result = await collection.delete_one({ "id": id })
    if result :
        return { "detail" : "User berhasil dihapus!"}
    return 0