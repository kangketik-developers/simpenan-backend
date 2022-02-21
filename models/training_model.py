import uuid
import datetime
import motor.motor_asyncio

from typing import Optional
from pydantic import BaseModel

from utils.tfftd_util import find_classes

class TrainingOut(BaseModel):
    results: str