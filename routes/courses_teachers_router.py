from fastapi import APIRouter
from database.connection import get_db_connection

from schemas.courses_teachers import CT, CTUpdate

router = APIRouter()

# Crear conexión a la base de datos
conn = get_db_connection()
cursor = conn.cursor()

# Create courses_teachers
@router.post("/")
async def create_courses_teachers(CT: CT):
    cursor.execute("INSERT INTO estudiantes (id_curso, id_maestro) VALUES (:1, :2)",
                   (CT.course, CT.id_teacher))
    conn.commit()
    return {"message": "courses_teachers created successfully"}


# Read all courses_teacherss
@router.get("/")
async def read_courses_teachers():
    cursor.execute("SELECT id_curso, id_maestro FROM cursos_maestros")
    results = cursor.fetchall()
    courses_teachers = []
    for result in results:
        course_teacher =  CT(id_course=result[0], id_teacher=result[1])
        courses_teachers.append(course_teacher)
    return courses_teachers

# Read courses_teachers by id
@router.get("/{course_teacher_information}")
async def read_courses_teachers_ids(teacher_id: int, course_id:int):
    cursor.execute("SELECT id_curso, id_maestro FROM cursos_maestros WHERE id_maestro=:1 and id_curso=:2", (teacher_id, course_id,))
    result = cursor.fetchone()
    if result:
        course_teacher =  CT(id_curso=result[0], id_maestro=result[1])
        return course_teacher

    else:
        return {"message": "courses_teachers not found"}

# Update courses_teachers
@router.put("/{courses_teachers_id}")
async def update_courses_teachers(teacher_id: int, course_id:int, CT: CTUpdate):
    # Consultar si existe el estudiante con el ID proporcionado
    cursor.execute("SELECT id_curso, id_maestro FROM cursos_maestros WHERE id_maestro=:1 and id_curso=:2", (teacher_id, course_id,))
    result = cursor.fetchone()

    # Si no se encuentra el estudiante, retornar un mensaje de error
    if not result:
        return {"error": "courses_teachers not found"}

    # Si el estudiante existe, actualizar sus datos en la base de datos
    cursor.execute("UPDATE courses_teachers SET id_couse=:1, WHERE id_curso =:2 and id_maestro=:3",
                   (CT.id_course, course_id, teacher_id))
    conn.commit()

    return {"message": "id_course updated successfully"}


# Delete courses_teachers
@router.delete("/{courses_teachers_id}")
async def delete_courses_teachers(course_id: int, teacher_id:int):
    # Consultar si existe el estudiante con el ID proporcionado
    cursor.execute("SELECT id_curso, id_maestro FROM cursos_maestros WHERE id_curso=:1 and id_maestro=:2", (course_id, teacher_id,))
    result = cursor.fetchone()

    # Si no se encuentra el estudiante, retornar un mensaje de error
    if not result:
        return {"error": "course_id, teacher_id not found"}

    # Si el estudiante existe, eliminarlo de la base de datos
    cursor.execute("DELETE FROM cursos_maestros WHERE id_maestro=:1 and id_curso=:2", (course_id, teacher_id,))
    conn.commit()

    return {"message": "course_id, teacher_id deleted successfully"}
