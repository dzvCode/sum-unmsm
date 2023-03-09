from fastapi import APIRouter
from database.connection import get_db_connection

from schemas.courses_teachers import CT, CTGetCourse, CTGetTeacher, CTUpdate, VWProgrammingCourses

router = APIRouter()

# Programar un curso
@router.post("/")
async def create_courses_teachers(CT: CT):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.callproc("PKG_CURSOS_MAESTROS.SP_INSERTAR_CURSO_MAESTRO", [CT.id_course, CT.id_teacher, CT.section])
    conn.commit()
    conn.close()
    return {"message": "courses_teachers created successfully"}


# Obtener todos los cursos programados
@router.get("/")
async def read_courses_teachers():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT cod_curso, curso, creditos, seccion, cod_maestro, profesor, ciclo FROM vw_programacion_cursos")
    results = cursor.fetchall()
    courses_teachers = []
    for result in results:
        course_teacher =  VWProgrammingCourses(cod_course=result[0], course=result[1], credits=result[2], section=result[3], cod_teacher=result[4], teacher=result[5], cycle=result[6])
        courses_teachers.append(course_teacher)
    conn.close()
    return courses_teachers

# Obtener los codigos de los cursos distintos
@router.get("/get_courses")
async def read_courses_ids():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT DISTINCT id_curso FROM cursos_maestros")
    results = cursor.fetchall()
    courses_teachers = []
    for result in results:
        course_teacher =  CTUpdate(id_course=result[0])
        courses_teachers.append(course_teacher)
    print(courses_teachers)
    conn.close()
    return courses_teachers


@router.get("/{get_teacher}")
async def read_eachers_ids(id_course: str):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT id_maestro FROM cursos_maestros WHERE id_curso=:1", [id_course])
    results = cursor.fetchall()
    courses_teachers = []
    for result in results:
        course_teacher =  CTGetTeacher(id_teacher=result[0])
        courses_teachers.append(course_teacher)
    conn.close()
    return courses_teachers


# Actualizar una programacion de cursos
@router.put("/{courses_teachers_id}")
async def update_courses_teachers(teacher_id: int, course_id:int, CT: CTUpdate):
    conn = get_db_connection()
    cursor = conn.cursor()
    # Consultar si existe el estudiante con el ID proporcionado
    cursor.execute("SELECT id_curso, id_maestro FROM cursos_maestros WHERE id_maestro=:1 and id_curso=:2", (teacher_id, course_id,))
    result = cursor.fetchone()

    # Si no encuentra el curso programado con la asignacion del profesor
    if not result:
        conn.close()
        return {"error": "Curso programado con el profesor digitado no encontrado"}


    # Si el curso programado existe, actualizar sus datos en la base de datos
    cursor.execute("UPDATE cursos_maestros SET id_curso=:1, WHERE id_curso =:2 and id_maestro=:3",
                   (CT.id_course, course_id, teacher_id))
    conn.commit()
    conn.close()
    return {"message": "Curso programado actualizado"}



# Eliminar el curso programado
@router.delete("/{courses_teachers_id}")
async def delete_courses_teachers(course_id: int, teacher_id:int):
    conn = get_db_connection()
    cursor = conn.cursor()
    # Consultar si existe el curso programado
    cursor.execute("SELECT id_curso, id_maestro FROM cursos_maestros WHERE id_curso=:1 and id_maestro=:2", (course_id, teacher_id,))
    result = cursor.fetchone()

    # Si no encuentra el curso programado con la asignacion del profesor
    if not result:
        conn.close()
        return {"error": "Curso programado con el profesor digitado no encontrado"}


    # Si el estudiante existe, eliminarlo de la base de datos
    cursor.execute("DELETE FROM cursos_maestros WHERE id_maestro=:1 and id_curso=:2", (course_id, teacher_id,))
    conn.commit()
    conn.close()
    return {"message": "Curso programado eliminado"}

# Obtener los cursos
@router.get("/cursos")
async def get_cursos():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT DISTINCT COD_CURSO, CURSO FROM VW_PROGRAMACION_CURSOS")
    results = cursor.fetchall()
    courses = []
    for result in results:
        course = CTGetCourse(cod_course=result[0], course=result[1])
        courses.append(course)
    conn.close()
    return courses
