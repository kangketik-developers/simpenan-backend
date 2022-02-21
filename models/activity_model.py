import uuid
import datetime
import motor.motor_asyncio

from typing import Optional
from pydantic import BaseModel
from utils.connection_util import DB_URL

class ActivityIn(BaseModel):
    description: str

class ActivityOut(BaseModel):
    id: str
    description: str
    created_at: datetime.datetime
    updated_at: Optional[datetime.datetime]

class ActivityDB(BaseModel):
    id: str
    description: str
    created_at: datetime.datetime
    updated_at: Optional[datetime.datetime]

client = motor.motor_asyncio.AsyncIOMotorClient(DB_URL)
database = client.simpenan
collection = database.activities

async def fetch_all_activities():
    activities = []
    cursor = collection.find({})
    async for document in cursor:
        activities.append(ActivityOut(**document))
    return activities

async def fetch_by_activity_desc(description):
    document = await collection.find_one({ "description": description })
    return document

async def fetch_by_activity_id(id):
    document = await collection.find_one({ "id": id })
    return document

async def post_activity(activity):
    document = activity.dict()
    result = await collection.insert_one(
        ActivityDB(
            **document, 
            id=str(uuid.uuid4()), 
            created_at=datetime.datetime.today()
        ).dict()
    )
    if result :
        return { "detail" : "Data kegiatan berhasil dibuat!" }
    return 0

async def put_activity(id, activity):
    result = await collection.find_one({ "id": id })
    response = await collection.update_one(
        { "id": id }, 
        { 
            "$set": ActivityDB(
                **activity.dict(),
                id=id,
                created_at=result["created_at"],
                updated_at=datetime.datetime.today()
            ).dict()
        }
    )
    if response :
        return { "detail" : "Kegiatan berhasil diperbarui!"}
    return 0

async def delete_activity(id):
    result = await collection.delete_one({"id": id})
    if result :
        return { "detail" : "Kegiatan berhasil dihapus!"}
    return 0