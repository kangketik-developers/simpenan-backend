import uuid
import datetime
import motor.motor_asyncio

from typing import Optional
from pydantic import BaseModel
from utils.connection_util import DB_URL


class InmatesScoreIn(BaseModel):
    inmates_id: str
    name: str
    month: int
    year: int
    total_score: float
    percentage_score: float


class InmatesScoreOut(BaseModel):
    id: str
    inmates_id: str
    name: str
    month: int
    year: int
    total_score: float
    percentage_score: Optional[float]
    created_at: datetime.datetime
    updated_at: Optional[datetime.datetime]


class InmatesScoreDb(BaseModel):
    id: str
    inmates_id: str
    name: str
    month: int
    year: int
    total_score: float
    percentage_score: Optional[float]
    created_at: datetime.datetime
    updated_at: Optional[datetime.datetime]


client = motor.motor_asyncio.AsyncIOMotorClient(DB_URL)
database = client.simpenan
collection = database.inmates_score


async def fetch_all_inmates_score():
    inmates_score = []
    cursor = collection.find({})
    async for document in cursor:
        inmates_score.append(InmatesScoreOut(**document))
    return inmates_score


async def fetch_inmates_score_by_filtered(month, year):
    inmates_score = []
    cursor = collection.find({"month": month, "year": year})
    async for document in cursor:
        inmates_score.append(InmatesScoreOut(**document))
    return inmates_score


async def fetch_inmates_score_by_args(inmates_id, month, year):
    document = await collection.find_one({"inmates_id": inmates_id, "month": month, "year": year})
    if document is None:
        return None
    return InmatesScoreOut(**document)


async def post_inmates_score(inmates_score):
    document = inmates_score.dict()
    uid = str(uuid.uuid4())
    result = await collection.insert_one(
        InmatesScoreDb(
            **document,
            id=uid,
            created_at=datetime.datetime.today()
        ).dict()
    )
    if result:
        return {"detail": f"Data warga binaan berhasil dibuat dengan id {uid}!"}
    return 0


async def put_inmates_score(id, inmates_score):
    result = await collection.find_one({"id": id})
    response = await collection.update_one(
        {"id": id},
        {
            "$set": InmatesScoreDb(
                **inmates_score.dict(),
                id=id,
                created_at=result["created_at"],
                updated_at=datetime.datetime.today()
            ).dict()
        }
    )
    if response:
        return {"detail": "warga binaan berhasil diperbarui!"}
    return 0


async def delete_inmates_score(id):
    result = await collection.delete_one({"id": id})
    if result:
        return {"detail": "Data absensi berhasil dihapus seluruhnya!"}
    return 0
