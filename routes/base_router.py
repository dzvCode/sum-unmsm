from fastapi import APIRouter
from routes import student_router, default_router

api_router = APIRouter()
api_router.include_router(default_router.router, prefix="")
api_router.include_router(student_router.router, prefix="/students", tags=["Students"])