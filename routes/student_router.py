from fastapi import APIRouter
from database.connection import get_db_connection

from schemas.student import CreateStudent, Student, UpdateStudent


router = APIRouter()

# Crear conexión a la base de datos
conn = get_db_connection()
cursor = conn.cursor()

# Create student
@router.post("/")
async def create_student(student: CreateStudent):
    cursor.execute("INSERT INTO estudiantes (id_estudiante, nombre_completo, correo, telefono, id_escuela) VALUES (:1, :2, :3, :4, :5)",
                   (student.id,student.name, student.email, student.phone, student.id_school))
    conn.commit()
    return {"message": "Student created successfully"}


# Read all students
@router.get("/")
async def read_students():
    cursor.execute("SELECT id_escuela, nombre_completo, correo FROM estudiantes")
    results = cursor.fetchall()
    students = []
    for result in results:
        student = Student(id=result[0], name=result[1], email=result[2])
        students.append(student)
    return students

# Read student by id
@router.get("/{student_id}")
async def read_student(student_id: int):
    cursor.execute("SELECT id_estudiante,nombre_completo, correo FROM estudiantes WHERE id_estudiante=:1", (student_id,))
    result = cursor.fetchone()
    if result:
        student = Student(id=result[0], name=result[1], email=result[2])
        return student
    else:
        return {"message": "Student not found"}

# Update student
@router.put("/{student_id}")
async def update_student(student_id: int, student: UpdateStudent):
    # Consultar si existe el estudiante con el ID proporcionado
    cursor.execute("SELECT id_estudiante FROM estudiantes WHERE id_estudiante=:1", (student_id,))
    result = cursor.fetchone()

    # Si no se encuentra el estudiante, retornar un mensaje de error
    if not result:
        return {"error": "Student not found"}

    # Si el estudiante existe, actualizar sus datos en la base de datos
    cursor.execute("UPDATE estudiantes SET nombre_completo=:1, correo=:2, telefono=:3 WHERE id_estudiante=:4",
                   (student.name, student.email, student.phone, student_id))
    conn.commit()

    return {"message": "Student updated successfully"}


# Delete student
@router.delete("/{student_id}")
async def delete_student(student_id: int):
    # Consultar si existe el estudiante con el ID proporcionado
    cursor.execute("SELECT id_estudiante FROM estudiantes WHERE id_estudiante=:1", (student_id,))
    result = cursor.fetchone()

    # Si no se encuentra el estudiante, retornar un mensaje de error
    if not result:
        return {"error": "Student not found"}

    # Si el estudiante existe, eliminarlo de la base de datos
    cursor.execute("DELETE FROM estudiantes WHERE id_estudiante=:1", (student_id,))
    conn.commit()

    return {"message": "Student deleted successfully"}

