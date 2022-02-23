from fastapi import APIRouter
from fastapi_pagination import Page, add_pagination, paginate

from models.inmates.inmates_score_model import InmatesScoreOut, fetch_all_inmates_score, fetch_inmates_score_by_filtered

router = APIRouter()


@router.get("/", response_model=Page[InmatesScoreOut])
async def show_report():
    responses = await fetch_all_inmates_score()
    return paginate(responses)


@router.get("/{month}/{year}", response_model=Page[InmatesScoreOut])
async def show_report_monthly(month: int, year: int):
    responses = await fetch_inmates_score_by_filtered(month, year)
    return paginate(responses)


add_pagination(router)
