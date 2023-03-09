from fastapi import APIRouter
from database.connection import get_db_connection
from datetime import datetime
from schemas.tuition import Tuition, TuitionCreate, TuitionDelete,  TuitionUpdateScore,  VW_TuitionAll, VW_TuitionID

router = APIRouter()

# Create courses_teachers
@router.post("/")
async def create_Tuitions(Tuition: TuitionCreate):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.callproc("PKG_MATRICULAS.SP_MATRICULA_ESTUDIANTE_CURSO", [Tuition.id_student, Tuition.id_course, Tuition.id_teacher, Tuition.section])
    conn.commit()
    conn.close()
    return {"message": "Estudiante Matriculado correctamente"}


# Read all courses_teacherss
@router.get("/")
async def read_courses_teacherss():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT cod_estudiante, ciclo, cod_curso, asignatura, creditos, seccion, docente FROM vw_matriculas_all")
    results = cursor.fetchall()
    tns = []
    for result in results:
        tn =  VW_TuitionAll(cod_estudiante=result[0], ciclo=result[1], cod_curso=result[2], asignatura=result[3], creditos=result[4], seccion=result[5], docente=result[6])
        tns.append(tn)
    conn.close()
    return tns

# Read Tuitions by id
@router.get("/{Tuition_information_ByIdStudent}")
async def read_tuition(student_id: int):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT ciclo, cod_curso, asignatura, creditos, seccion, docente FROM vw_matriculas_all WHERE cod_estudiante=:1", (student_id,))
    results = cursor.fetchall()
    tns = []
    for result in results:
        tn =  VW_TuitionID(ciclo=result[0], cod_curso=result[1], asignatura=result[2], creditos=result[3], seccion=result[4], docente=result[5])
        tns.append(tn)
    conn.close()
    return tns

# Update Tuitions
@router.put("/{Update_Tuition_ByIdStudent_IdCourse}")
async def update_courses_teachers(student_id:int, course_id: str, Tuition: TuitionUpdateScore):
    conn = get_db_connection()
    cursor = conn.cursor()
    # Consultar si existe el estudiante con el ID proporcionado
    cursor.execute("SELECT id_estudiante, id_curso FROM matriculas WHERE id_estudiante =:1 and id_curso=:2", (student_id, course_id))
    result = cursor.fetchone()

    # Si no se encuentra el estudiante, retornar un mensaje de error
    if not result:
        conn.close()
        return {"error": "Matricula del curso no encontrada"}

    # Si el estudiante existe, actualizar sus datos en la base de datos
    cursor.execute("UPDATE matriculas SET nota=:1 WHERE id_estudiante=:2 and id_curso=:3", (Tuition.score, student_id, course_id))
    conn.commit()
    conn.close()

    return {"message": "La nota del curso con codigo "+course_id+" del alumno con codigo "+str(student_id)+" ha sido actualizada"}


# Delete Tuitions
@router.delete("/")
async def delete_tuition(Tuition: TuitionDelete):
    conn = get_db_connection()
    cursor = conn.cursor()
    # Consultar si existe el estudiante con el ID proporcionado
    cursor.execute("SELECT id_curso, id_estudiante FROM matriculas WHERE id_estudiante = :1 AND id_curso = :2", (Tuition.id_student, Tuition.id_course))
    result = cursor.fetchone()

    # Si no se encuentra el estudiante, retornar un mensaje de error
    if not result:
        conn.close()
        return {"error": "Matricula del curso no encontrada"}

    # Si el estudiante existe, eliminarlo de la base de datos
    cursor.callproc("PKG_MATRICULAS.SP_ANULAR_MATRICULA", [Tuition.id_student, Tuition.id_course])
    conn.commit()
    conn.close()

    return {"message": "Matricula al curso con codigo "+Tuition.id_course+" del alumno con codigo "+str(Tuition.id_student)+" eliminada"}
