from fastapi import APIRouter
from database.connection import get_db_connection
from datetime import datetime
from schemas.tuition import Tuition, TuitionCreate, TuitionUpdate

router = APIRouter()

# Crear conexión a la base de datos
conn = get_db_connection()
cursor = conn.cursor()

# Create courses_teachers
@router.post("/")
async def create_Tuitions(Tuition: TuitionCreate):
    cursor.execute("INSERT INTO matriculas (id_curso, id_maestro, nota, fecha) VALUES (:1, :2, :3, :4)",
                   (Tuition.id_student, Tuition.id_course, Tuition.score, datetime.date.today()))
    conn.commit()
    return {"message": "Tuitions created successfully"}


# Read all courses_teacherss
@router.get("/")
async def read_courses_teacherss():
    cursor.execute("SELECT id_curso, id_maestro, nota, fecha FROM matriculas")
    results = cursor.fetchall()
    tns = []
    for result in results:
        tn =  Tuition(id_curso=result[0], id_maestro=result[1], nota=result[2], fecha=result[3])
        tns.append(tn)
    return tns

# Read Tuitions by id
@router.get("/{Tuition_information}")
async def read_tuition(student_id: int, curso_id: int):
    cursor.execute("SELECT id_curso, id_estudiante, nota, fecha FROM matriculas WHERE id_estudiante=:1", (student_id, curso_id,))
    result = cursor.fetchone()
    if result:
        tn =  Tuition(id_course=result[0], id_student=result[1], score=result[2], date=result[3])
        return tn

    else:
        return {"message": "Tuitions not found"}

# Update Tuitions
@router.put("/{courses_teachers_id}")
async def update_courses_teachers(course_id: int, student_id:int, Tuition: TuitionUpdate):
    # Consultar si existe el estudiante con el ID proporcionado
    cursor.execute("SELECT id_curso, id_estudiante FROM matricula WHERE id_curso=:1 and id_estudiante =:2", (course_id, student_id))
    result = cursor.fetchone()

    # Si no se encuentra el estudiante, retornar un mensaje de error
    if not result:
        return {"error": "Tuitions not found"}

    # Si el estudiante existe, actualizar sus datos en la base de datos
    cursor.execute("UPDATE matriculas SET nota=:3, fecha=:4 WHERE id_curso=:1 and id_estudiante =:2",
                   (course_id, student_id, Tuition.score, datetime.date.today()))
    conn.commit()

    return {"message": "Tuition updated successfully"}


# Delete Tuitions
@router.delete("/{courses_teachers_id}")
async def delete_tuition(course_id: int, student_id:int):
    # Consultar si existe el estudiante con el ID proporcionado
    cursor.execute("SELECT id_curso, id_estudiante FROM matricula WHERE id_curso=:1 and id_estudiante =:2", (course_id, student_id))
    result = cursor.fetchone()

    # Si no se encuentra el estudiante, retornar un mensaje de error
    if not result:
        return {"error": "Tuitions not found"}

    # Si el estudiante existe, eliminarlo de la base de datos
    cursor.execute("DELETE FROM matricula WHERE id_curso=:1 and id_estudiante =:2", (course_id, student_id))
    conn.commit()

    return {"message": "Tuitions deleted successfully"}

#a