import uuid
import datetime
import motor.motor_asyncio

from typing import Optional
from pydantic import BaseModel
from utils.connection_util import DB_URL

class AttendanceOut(BaseModel):
    id: str
    name: str
    confident: float
    messages: str

class AttendancePutDbOut(BaseModel):
    id: str
    sign_out: Optional[datetime.time]
    attendance_score: float
    total_score: float

class AttendancePostDb(BaseModel):
    id: str
    inmates_id: str
    name: str
    date: str
    sign_in: str
    sign_out: Optional[datetime.time]
    activity_score: float
    attendance_score: float
    total_score: float
    created_at: datetime.datetime
    updated_at: Optional[datetime.datetime]

class AttendancePutDb(BaseModel):
    sign_out: str
    attendance_score: float
    total_score: float
    updated_at: datetime.datetime

client = motor.motor_asyncio.AsyncIOMotorClient(DB_URL)
database = client.simpenan
collection = database.attendance

async def fetch_all_atendance():
    inmates = []
    cursor = collection.find({})
    async for document in cursor:
        inmates.append(AttendancePostDb(**document))
    return inmates

async def fetch_attendance_by_inmates_id(id):
    document = await collection.find_one({ "inmates_id": id })
    if document is None:
        return 0
    return AttendancePutDbOut(**document)

async def fetch_attendance_by_inmates_id_and_date(id, date):
    document = await collection.find_one({ "inmates_id": id, "date": date })
    if document is None:
        return None
    return AttendancePutDbOut(**document)

async def post_attendance_sign_in(id, name, tanggal, jam, nilai_absen, nilai_kegiatan, nilai_total):
    result = await collection.insert_one(
        AttendancePostDb(
            id=str(uuid.uuid4()), 
            inmates_id=id,
            name=name,
            date=tanggal,
            sign_in=jam,
            activity_score=nilai_kegiatan,
            attendance_score=nilai_absen,
            total_score=nilai_total,
            created_at=datetime.datetime.today()
        ).dict()
    )
    if result :
        return { "detail" : "Absensi berhasil di simpan!" }
    return 0

async def put_attendance_sign_out(id, sign_out, attendance_score, total_score):
    response = await collection.update_one(
        { "id": id }, 
        { 
            "$set": AttendancePutDb(
                sign_out=sign_out,
                attendance_score=attendance_score,
                total_score=total_score,
                updated_at=datetime.datetime.today()
            ).dict()
        }
    )
    if response :
        return { "detail" : "Absen pulang berhasil diperbarui!"}
    return 0

async def delete_attendance(id):
    result = await collection.delete_one({ "id": id })
    if result :
        return { "detail" : "Data absensi berhasil dihapus seluruhnya!"}
    return 0