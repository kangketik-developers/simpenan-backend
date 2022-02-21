from datetime import datetime, time
from fastapi import APIRouter, HTTPException, File, UploadFile, exceptions
from fastapi_pagination import Page, add_pagination, paginate

from models.report_model import *
from models.inmates.inmates_score_model import *

router = APIRouter()

@router.get("/", response_model=Page[InmatesScoreOut])
async def show_report():
    responses = await fetch_all_inmates_score()
    return paginate(responses)

@router.get("/{month}/{year}", response_model=Page[reportOut])
async def show_report_monthly(month: int, year: int):
    responses = await fetch_atendance()
    this_date = datetime.datetime.strptime(f"{year}-{month}", "%Y-%m")
    responses = [response for response in responses if response.created_at >= this_date]
    return paginate(responses)

add_pagination(router)