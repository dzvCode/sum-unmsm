from fastapi import APIRouter
from database.connection import get_db_connection

from schemas.teacher import CreateTeacher, Teacher
router = APIRouter()

# Insertar un maestro
@router.post("/")
async def create_teacher(teacher: CreateTeacher):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.callproc("PKG_MAESTROS.SP_INSERTAR_MAESTRO", [teacher.id, teacher.name, teacher.degree, teacher.email, teacher.phone, teacher.id_school])
    conn.commit()
    conn.close()

    return {"message": "Maestro registrado correctamente"}

# Obtener todos los maestros
@router.get("/")
async def read_teachers():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT ID_MAESTRO, NOMBRE_COMPLETO, GRADO, CORREO, TELEFONO FROM MAESTROS")
    results = cursor.fetchall()
    teachers = []

    for result in results:
        teacher = Teacher(id=result[0], name=result[1], degree=result[2], email=result[3], phone=result[4])
        teachers.append(teacher)
    conn.close()
    return teachers

# Actualizar maestro
@router.put("/{teacher_id}")
async def update_teacher(teacher_id: int, teacher_degree: str, teacher_phone: int):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT ID_MAESTRO FROM MAESTROS WHERE ID_MAESTRO=:1", [teacher_id])
    result = cursor.fetchone()

    if not result:
        conn.close()
        return {"error": f'Maestro con id: {teacher_id} no encontrado'}

    cursor.callproc("PKG_MAESTROS.SP_EDITAR_MAESTRO", [teacher_id, teacher_degree, teacher_phone])
    conn.commit()
    conn.close()

    return {"message": "Maestro actualizado correctamente"}

# Eliminar maestro
@router.delete("/{teacher_id}")
async def delete_teacher(teacher_id: int):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT ID_MAESTRO FROM MAESTROS WHERE ID_MAESTRO=:1", (teacher_id,))
    result = cursor.fetchone()

    if not result:
        conn.close()
        return {"error": f'Maestro con id: {teacher_id} no encontrado'}

    cursor.execute("DELETE FROM MAESTROS WHERE ID_MAESTRO=:1", [teacher_id])
    conn.commit()
    conn.close()

    return {"message": "Maestro eliminado correctamente"}