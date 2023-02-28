from fastapi import APIRouter
from routes import student_router, default_router, headquarter_router, faculty_router, school_router,area_router

api_router = APIRouter()
api_router.include_router(default_router.router, prefix="")
api_router.include_router(student_router.router, prefix="/students", tags=["Students"])
api_router.include_router(headquarter_router.router, prefix="/headquarters", tags=["Headquarters"])
api_router.include_router(faculty_router.router, prefix="/faculties", tags=["Faculties"])
api_router.include_router(school_router.router, prefix="/schools", tags=["Schools"])
api_router.include_router(area_router.router, prefix="/areas", tags=["Areas"])