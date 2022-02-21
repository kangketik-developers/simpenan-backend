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

class AttendanceDB(BaseModel):
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

client = motor.motor_asyncio.AsyncIOMotorClient("mongodb://localhost:27017")
database = client.simpenan
collection = database.attendance_sign_in

async def post_attendance_sign_in(id, name, tanggal, jam, nilai_absen, nilai_kegiatan):
    result = await collection.insert_one(
        AttendanceDB(
            id=str(uuid.uuid4()), 
            inmates_id=id,
            name=name,
            date=tanggal,
            sign_in=jam,
            activity_score=nilai_kegiatan,
            attendance_score=nilai_absen,
            created_at=datetime.datetime.today()
        ).dict()
    )
    if result :
        return { "detail" : "Data warga binaan berhasil dibuat!" }
    return 0