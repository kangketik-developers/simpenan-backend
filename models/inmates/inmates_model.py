import uuid
import datetime
import motor.motor_asyncio

from typing import Optional
from pydantic import BaseModel

class InmatesIn(BaseModel):
    name: str
    regsitration_code: str
    room_block: str
    article: str
    punishment: str
    work_post: str
    description: str

class InmatesLabelOut(BaseModel):
    name: str

class InmatesOut(BaseModel):
    id: str
    name: str
    regsitration_code: str
    room_block: str
    article: str
    punishment: str
    work_post: str
    description: str
    created_at: datetime.datetime
    updated_at: Optional[datetime.datetime]

class inmatesDB(BaseModel):
    id: str
    name: str
    regsitration_code: str
    room_block: str
    article: str
    punishment: str
    work_post: str
    description: str
    created_at: datetime.datetime
    updated_at: Optional[datetime.datetime]

client = motor.motor_asyncio.AsyncIOMotorClient("mongodb://localhost:27017")
database = client.simpenan
collection = database.inmates

async def fetch_all_inmates():
    inmates = []
    cursor = collection.find({})
    async for document in cursor:
        inmates.append(InmatesOut(**document))
    return inmates

async def fetch_all_inmates_label():
    inmates = []
    cursor = collection.find({})
    async for document in cursor:
        inmates.append(InmatesLabelOut(**document))
    return inmates

async def fetch_by_inmates_name(name):
    document = await collection.find_one({ "name": name })
    if document is None:
        return 0
    return InmatesOut(**document)

async def fetch_by_inmates_id(id):
    document = await collection.find_one({ "id": id })
    return document

async def post_inmates(inmates):
    document = inmates.dict()
    uid = str(uuid.uuid4())
    result = await collection.insert_one(
        inmatesDB(
            **document, 
            id=uid, 
            created_at=datetime.datetime.today()
        ).dict()
    )
    if result :
        return { "detail" : f"Data warga binaan berhasil dibuat dengan id {uid}!" }
    return 0

async def put_inmates(id, inmates):
    result = await collection.find_one({ "id": id })
    response = await collection.update_one(
        { "id": id }, 
        { 
            "$set": inmatesDB(
                **inmates.dict(),
                id=id,
                created_at=result["created_at"],
                updated_at=datetime.datetime.today()
            ).dict()
        }
    )
    if response :
        return { "detail" : "warga binaan berhasil diperbarui!"}
    return 0

async def delete_inmates(id):
    result = await collection.delete_one({ "id": id })
    if result :
        return { "detail" : "warga binaan berhasil dihapus!"}
    return 0