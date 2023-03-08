from fastapi import APIRouter
from routes import student_router, teacher_router, course_router, default_router, headquarter_router, faculty_router, school_router,area_router, courses_teachers_router, tuition_router, school_headquarter_router

api_router = APIRouter()
api_router.include_router(default_router.router, prefix="")
api_router.include_router(student_router.router, prefix="/students", tags=["Students"])
api_router.include_router(teacher_router.router, prefix="/teachers", tags=["Teachers"])
api_router.include_router(course_router.router, prefix="/courses", tags=["Courses"])
api_router.include_router(headquarter_router.router, prefix="/headquarters", tags=["Headquarters"])
api_router.include_router(faculty_router.router, prefix="/faculties", tags=["Faculties"])
api_router.include_router(school_router.router, prefix="/schools", tags=["Schools"])
api_router.include_router(area_router.router, prefix="/areas", tags=["Areas"])
api_router.include_router(courses_teachers_router.router, prefix="/Courses_teachers", tags=["Courses_teachers"])
api_router.include_router(tuition_router.router, prefix="/Tuition", tags=["Tuition"])
api_router.include_router(school_headquarter_router.router, prefix="/School_headquarter", tags=["School_headquarter"])