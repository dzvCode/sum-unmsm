from fastapi import APIRouter
from database.connection import get_db_connection
from schemas.courses import Course


router = APIRouter()

# Insertar un curso
@router.post("/")
async def create_course(course: Course):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("INSERT INTO CURSOS (ID_CURSO, NOMBRE, CREDITOS, CICLO) VALUES (:1, :2, :3, :4)", (course.id, course.name, course.weight, course.cycle))
    conn.commit()
    conn.close()
    return {"message": "Curso registrado correctamente"}

# Obtener todos los cursos
@router.get("/")
async def read_courses():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT ID_CURSO, NOMBRE, CREDITOS, CICLO FROM CURSOS")
    results = cursor.fetchall()
    courses = []

    for result in results:
        course = Course(id=result[0], name=result[1], weight=result[2], cycle=result[3])
        courses.append(course)

    conn.close()
    return courses

# Obtener curso por ciclo
@router.get("/{course_cycle}")
async def read_course(course_cycle: int):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT ID_CURSO, NOMBRE, CREDITOS, CICLO FROM CURSOS WHERE CICLO=:1", [course_cycle])
    results = cursor.fetchall()
    courses = []
    
    for result in results:
        course = Course(id=result[0], name=result[1], weight=result[2], cycle=result[3])
        courses.append(course)

    conn.close()
    return courses 