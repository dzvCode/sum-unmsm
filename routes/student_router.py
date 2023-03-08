from fastapi import APIRouter
from database.connection import get_db_connection

from schemas.student import CreateStudent, Student

router = APIRouter()

# Insertar un estudiante
@router.post("/")
async def create_student(student: CreateStudent):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.callproc("PKG_ESTUDIANTES.SP_INSERTAR_ESTUDIANTE", [student.id, student.name, student.email, student.phone, student.id_school])
    conn.commit()
    conn.close()
    return {"message": "Estudiante registrado correctamente"}

# Obtener todos los estudiantes
@router.get("/")
async def read_students():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT ID_ESTUDIANTE, NOMBRE_COMPLETO, CORREO FROM ESTUDIANTES")
    results = cursor.fetchall()
    students = []

    for result in results:
        student = Student(id=result[0], name=result[1], email=result[2])
        students.append(student)
    conn.close()
    return students

# Obtener estudiante por id
@router.get("/{student_id}")
async def read_student(student_id: int):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT ID_ESTUDIANTE,NOMBRE_COMPLETO, CORREO FROM ESTUDIANTES WHERE ID_ESTUDIANTE=:1", (student_id,))
    result = cursor.fetchone()

    if result:
        student = Student(id=result[0], name=result[1], email=result[2])
        conn.close()
        return student
    else:
        conn.close()
        return {"message": f'Estudiante con id: {student_id} no encontrado'}

# Actualizar estudiante
@router.put("/{student_id}")
async def update_student(student_id: int, student_phone: int):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT ID_ESTUDIANTE FROM ESTUDIANTES WHERE ID_ESTUDIANTE=:1", [student_id])
    result = cursor.fetchone()

    if not result:
        conn.close()
        return {"error": f'Estudiante con id: {student_id} no encontrado'}

    cursor.callproc("PKG_ESTUDIANTES.SP_EDITAR_ESTUDIANTE", [student_id, student_phone])
    conn.commit()
    conn.close()

    return {"message": "Estudiante actualizado correctamente"}

# Eliminar estudiante
@router.delete("/{student_id}")
async def delete_student(student_id: int):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT ID_ESTUDIANTE FROM ESTUDIANTES WHERE ID_ESTUDIANTE=:1", (student_id,))
    result = cursor.fetchone()

    if not result:
        return {"error": f'Estudiante con id: {student_id} no encontrado'}

    cursor.execute("DELETE FROM ESTUDIANTES WHERE ID_ESTUDIANTE=:1", [student_id])
    conn.commit()
    conn.close()

    return {"message": "Estudiante eliminado correctamente"}