from fastapi import APIRouter
from database.connection import get_db_connection

from schemas.courses_teachers import CT, CT_Create, CT_Update

router = APIRouter()

# Crear conexión a la base de datos
conn = get_db_connection()
cursor = conn.cursor()

# Create courses_teachers
@router.post("/")
async def create_courses_teachers(CT: CT_Create):
    cursor.execute("INSERT INTO estudiantes (id_curso, id_maestro, nota, fecha) VALUES (:1, :2, :3, :4)",
                   (CT.course, CT.id_teacher, CT.score, CT.date))
    conn.commit()
    return {"message": "courses_teachers created successfully"}


# Read all courses_teacherss
@router.get("/")
async def read_courses_teacherss():
    cursor.execute("SELECT id_curso, id_maestro, nota, fecha FROM cursos_maestros")
    results = cursor.fetchall()
    courses_teachers = []
    for result in results:
        course_teacher =  course_teacher(id_curso=result[0], id_maestro=result[1], nota=result[2], fecha=result[3])
        courses_teachers.append(course_teacher)
    return courses_teachers

# Read courses_teachers by id
@router.get("/{course_teacher_id}")
async def read_courses_teachers(courses_teachers_id: int):
    cursor.execute("SELECT id_curso, id_maestro, nota, fecha FROM cursos_maestros WHERE id_maestro=:1", (courses_teachers_id,))
    result = cursor.fetchone()
    if result:
        course_teacher =  course_teacher(id_curso=result[0], id_maestro=result[1], nota=result[2], fecha=result[3])
        return course_teacher

    else:
        return {"message": "courses_teachers not found"}

# Update courses_teachers
@router.put("/{courses_teachers_id}")
async def update_courses_teachers(courses_teachers_id: int, courses_teachers: CT_Update):
    # Consultar si existe el estudiante con el ID proporcionado
    cursor.execute("SELECT id_estudiante FROM estudiantes WHERE id_estudiante=:1", (courses_teachers_id,))
    result = cursor.fetchone()

    # Si no se encuentra el estudiante, retornar un mensaje de error
    if not result:
        return {"error": "courses_teachers not found"}

    # Si el estudiante existe, actualizar sus datos en la base de datos
    cursor.execute("UPDATE estudiantes SET nombre_completo=:1, correo=:2, telefono=:3 WHERE id_estudiante=:4",
                   (courses_teachers.name, courses_teachers.email, courses_teachers.phone, courses_teachers_id))
    conn.commit()

    return {"message": "courses_teachers updated successfully"}


# Delete courses_teachers
@router.delete("/{courses_teachers_id}")
async def delete_courses_teachers(courses_teachers_id: int):
    # Consultar si existe el estudiante con el ID proporcionado
    cursor.execute("SELECT id_estudiante FROM estudiantes WHERE id_estudiante=:1", (courses_teachers_id,))
    result = cursor.fetchone()

    # Si no se encuentra el estudiante, retornar un mensaje de error
    if not result:
        return {"error": "courses_teachers not found"}

    # Si el estudiante existe, eliminarlo de la base de datos
    cursor.execute("DELETE FROM cursos_maestros WHERE id_maestro=:1", (courses_teachers_id,))
    conn.commit()

    return {"message": "courses_teachers deleted successfully"}

