import uuid
import datetime
import motor.motor_asyncio

from typing import Optional
from pydantic import BaseModel

class AttendancePostOut(BaseModel):
    id: str
    name: str
    confident: float
    messages: str

class AttendancePostDbOut(BaseModel):
    id: str
    inmates_id: str
    name: str
    date: str
    sign_in: str
    sign_out: Optional[datetime.time]
    activity_score: float
    attendance_score: float
    created_at: datetime.datetime
    updated_at: Optional[datetime.datetime]
    
class AttendanceDB(BaseModel):
    sign_out: str
    attendance_score: float
    updated_at: datetime.datetime

client = motor.motor_asyncio.AsyncIOMotorClient("mongodb://localhost:27017")
database = client.simpenan
collection = database.attendance_sign_in

async def fetch_by_inmates_id(id):
    document = await collection.find_one({ "inmates_id": id })
    if document is None:
        return 0
    return AttendancePostDbOut(**document)

async def put_attendance_sign_out(id, sign_out, attendance_score):
    response = await collection.update_one(
        { "id": id }, 
        { 
            "$set": AttendanceDB(
                sign_out=sign_out,
                attendance_score=attendance_score,
                updated_at=datetime.datetime.today()
            ).dict()
        }
    )
    if response :
        return { "detail" : "Absen pulang berhasil diperbarui!"}
    return 0