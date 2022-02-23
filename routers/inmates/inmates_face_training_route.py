from fastapi import APIRouter

from models.inmates.inmates_face_training_model import *
from models.inmates.inmates_model import fetch_all_inmates_label
from utils.training_util import start_training

router = APIRouter()


@router.get("/", response_model=FaceTrainingOut)
async def training_face_capture():
    classes = []
    inmates = await fetch_all_inmates_label()
    for inmate in inmates:
        classes.append(inmate.name)
    response = start_training(classes)
    return response
