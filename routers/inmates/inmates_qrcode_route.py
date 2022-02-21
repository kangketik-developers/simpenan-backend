from fastapi import APIRouter, HTTPException

router = APIRouter()

@router.get("/")
async def show_report():
    pass

@router.post("/")
async def show_report_monthly():
    pass