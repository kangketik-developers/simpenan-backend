import datetime
import datetime
from typing import Optional

import motor.motor_asyncio
from pydantic import BaseModel

from utils.connection_util import DB_URL


class ReportIn(BaseModel):
    month: int
    year: int


class ReportOut(BaseModel):
    name: str
    date: str
    sign_in: str
    sign_out: Optional[datetime.time]
    activity_score: float
    attendance_score: float
    total_score: float
    percentage_score: float
    created_at: datetime.datetime
    updated_at: Optional[datetime.datetime]


client = motor.motor_asyncio.AsyncIOMotorClient(DB_URL)
database = client.simpenan
collection = database.attendance


async def fetch_atendance():
    inmates = []
    cursor = collection.find({})
    async for document in cursor:
        inmates.append(ReportOut(**document))
    return inmates
