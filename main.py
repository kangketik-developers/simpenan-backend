from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles

from routers import auth_route, user_route, activity_route, attendance_route, report_route
from routers.inmates import inmates_route, inmates_document_route, inmates_video_route, inmates_face_training_route, \
    inmates_qrcode_route

app = FastAPI()
app.mount("/uploads", StaticFiles(directory="uploads/"), name="uploads")
app.mount("/assets", StaticFiles(directory="assets/"), name="assets")

origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(
    auth_route.router,
    prefix="/auth",
    tags=["Auth"]
)
app.include_router(
    user_route.router,
    prefix="/users",
    tags=["Kelola Pengguna"],
    # dependencies=[Depends(AuthHandler().auth_wrapper)]
)
app.include_router(
    activity_route.router,
    prefix="/activity",
    tags=["Kelola Kegiatan"],
    # dependencies=[Depends(AuthHandler().auth_wrapper)]
)

app.include_router(
    inmates_route.router,
    prefix="/inmates",
    tags=["Kelola Warga Binaan"],
    # dependencies=[Depends(AuthHandler().auth_wrapper)]
)

app.include_router(
    inmates_qrcode_route.router,
    prefix="/inmates/qrcode",
    tags=["Kelola QRCode"],
    # dependencies=[Depends(AuthHandler().auth_wrapper)]
)

app.include_router(
    inmates_document_route.router,
    prefix="/inmates/document",
    tags=["Kelola Dokumen Warga Binaan"],
    # dependencies=[Depends(AuthHandler().auth_wrapper)]
)

app.include_router(
    inmates_video_route.router,
    prefix="/inmates/capture",
    tags=["Kelola Capture Video Warga Binaan"],
    # dependencies=[Depends(AuthHandler().auth_wrapper)]
)

app.include_router(
    inmates_face_training_route.router,
    prefix="/inmates/training",
    tags=["Melatih Capture Wajah Warga Binaan"],
    # dependencies=[Depends(AuthHandler().auth_wrapper)]
)

app.include_router(
    attendance_route.router,
    prefix="/attendance",
    tags=["Kelola Absensi"],
    # dependencies=[Depends(AuthHandler().auth_wrapper)]
)

app.include_router(
    report_route.router,
    prefix="/report",
    tags=["Kelola Laporan"],
    # dependencies=[Depends(AuthHandler().auth_wrapper)]
)
