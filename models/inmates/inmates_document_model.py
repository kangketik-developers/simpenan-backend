import uuid
import datetime
import motor.motor_asyncio

from typing import Optional
from pydantic import BaseModel
from utils.connection_util import DB_URL


class DocInmatesIn(BaseModel):
    description: str


class DocInmatesOut(BaseModel):
    id: str
    inmates_id: str
    description: str
    filepath: str
    created_at: datetime.datetime
    updated_at: Optional[datetime.datetime]


class DocInmatesOutDelete(BaseModel):
    id: str
    filename: str


class DocInmatesDB(BaseModel):
    id: str
    inmates_id: str
    description: str
    filename: str
    filepath: str
    created_at: datetime.datetime
    updated_at: Optional[datetime.datetime]


client = motor.motor_asyncio.AsyncIOMotorClient(DB_URL)
database = client.simpenan
collection = database.inmates_docs


async def fetch_all_doc_inmates():
    inmates_doc = []
    cursor = collection.find({})
    async for document in cursor:
        inmates_doc.append(DocInmatesOut(**document))
    return inmates_doc


async def fetch_all_doc_inmates_by_inmates_id(inmates):
    inmates_doc = []
    cursor = collection.find({"inmates_id": inmates})
    async for document in cursor:
        inmates_doc.append(DocInmatesOutDelete(**document))
    return inmates_doc


async def fetch_by_inmates_doc_id(id):
    document = await collection.find_one({"id": id})
    return document


async def fetch_inmates_doc_by_inmates_id(inmates):
    inmates_doc = []
    cursor = collection.find({"inmates_id": inmates})
    async for document in cursor:
        inmates_doc.append(DocInmatesOut(**document))
    return inmates_doc


async def fetch_by_inmates_doc_desc(description):
    document = await collection.find_one({"description": description})
    return document


async def post_inmates_doc(inmates_doc, id, filename):
    document = inmates_doc.dict()
    result = await collection.insert_one(
        DocInmatesDB(
            **document,
            id=str(uuid.uuid4()),
            inmates_id=id,
            filename=filename,
            filepath=f"/uploads/inmates_files/{filename}",
            created_at=datetime.datetime.today()
        ).dict()
    )
    if result:
        return {"detail": "Data dokumen warga binaan berhasil dibuat!"}
    return 0


async def put_inmates_doc(id, inmates_doc):
    result = await collection.find_one({"id": id})
    response = await collection.update_one(
        {"id": id},
        {
            "$set": DocInmatesDB(
                **inmates_doc.dict(),
                id=id,
                created_at=result["created_at"],
                updated_at=datetime.datetime.today()
            ).dict()
        }
    )
    if response:
        return {"detail": "Dokumen warga binaan berhasil diperbarui!"}
    return 0


async def delete_inmates_doc(id):
    result = await collection.delete_one({"id": id})
    if result:
        return {"detail": "Dokumen warga binaan berhasil dihapus!"}
    return 0
