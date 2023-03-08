from fastapi import APIRouter
from database.connection import get_db_connection
from datetime import datetime
from schemas.tuition import Tuition, TuitionCreate, TuitionUpdate,  VW_TuitionAll, VW_TuitionID

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
async def update_courses_teachers(course_id: int, student_id:int, Tuition: TuitionUpdate):
    conn = get_db_connection()
    cursor = conn.cursor()
    # Consultar si existe el estudiante con el ID proporcionado
    cursor.execute("SELECT id_curso, id_estudiante FROM matricula WHERE id_curso=:1 and id_estudiante =:2", (course_id, student_id))
    result = cursor.fetchone()

    # Si no se encuentra el estudiante, retornar un mensaje de error
    if not result:
        conn.close()
        return {"error": "Tuitions not found"}

    # Si el estudiante existe, actualizar sus datos en la base de datos
    cursor.execute("UPDATE matriculas SET nota=:3, fecha=:4 WHERE id_curso=:1 and id_estudiante =:2",
                   (course_id, student_id, Tuition.score, datetime.date.today()))
    conn.commit()
    conn.close()

    return {"message": "Tuition updated successfully"}


# Delete Tuitions
@router.delete("/{Delete_Tuition_ByIdStudent_IdCourse}")
async def delete_tuition(course_id: int, student_id:int):
    conn = get_db_connection()
    cursor = conn.cursor()
    # Consultar si existe el estudiante con el ID proporcionado
    cursor.execute("SELECT id_curso, id_estudiante FROM matricula WHERE id_curso=:1 and id_estudiante =:2", (course_id, student_id))
    result = cursor.fetchone()

    # Si no se encuentra el estudiante, retornar un mensaje de error
    if not result:
        conn.close()
        return {"error": "Tuitions not found"}

    # Si el estudiante existe, eliminarlo de la base de datos
    cursor.execute("DELETE FROM matricula WHERE id_curso=:1 and id_estudiante =:2", (course_id, student_id))
    conn.commit()
    conn.close()

    return {"message": "Tuitions deleted successfully"}