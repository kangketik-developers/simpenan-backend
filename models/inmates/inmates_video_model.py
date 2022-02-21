import uuid
import datetime
import motor.motor_asyncio

from typing import Optional
from pydantic import BaseModel
from utils.connection_util import DB_URL

class VidInmatesOut(BaseModel):
    id: str
    inmates_id: str
    videopath: str
    samplepath: str
    totalsample: int
    created_at: datetime.datetime
    updated_at: Optional[datetime.datetime]

class VidInmatesOutDelete(BaseModel):
    id: str
    videoname: str
    sampledirname: str

class VidInmatesDB(BaseModel):
    id: str
    inmates_id: str
    videoname: str
    videopath: str
    sampledirname: str
    samplepath: str
    totalsample: int
    created_at: datetime.datetime
    updated_at: Optional[datetime.datetime]

client = motor.motor_asyncio.AsyncIOMotorClient(DB_URL)
database = client.simpenan
collection = database.inmates_videos

async def fetch_all_vid_inmates():
    inmates_vid = []
    cursor = collection.find({})
    async for document in cursor:
        inmates_vid.append(VidInmatesOut(**document))
    return inmates_vid

async def fetch_all_vid_inmates_by_inmates_id(inmates):
    inmates_vid = []
    cursor = collection.find({"inmates_id": inmates})
    async for document in cursor:
        inmates_vid.append(VidInmatesOutDelete(**document))
    return inmates_vid

async def fetch_by_inmates_vid_id(id):
    document = await collection.find_one({ "id": id })
    return document

async def fetch_by_inmates_vid_inmates_id(inmates_id):
    document = await collection.find_one({ "inmates_id": inmates_id })
    return document

async def post_inmates_vid(id, videoname, sampledirname, totalsample):
    result = await collection.insert_one(
        VidInmatesDB(
            id=str(uuid.uuid4()), 
            inmates_id=id,
            videoname=videoname,
            videopath=f"/uploads/inmates_videos/{videoname}",
            sampledirname=sampledirname,
            samplepath=f"/assets/faces/{sampledirname}",
            totalsample=totalsample,
            created_at=datetime.datetime.today()
        ).dict()
    )
    if result :
        return { "detail" : "Data video sampel warga binaan berhasil dibuat!" }
    return 0

async def delete_inmates_vid(id):
    result = await collection.delete_one({"id": id})
    if result :
        return { "detail" : "Video sampel warga binaan berhasil dihapus!"}
    return 0