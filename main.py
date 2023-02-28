<<<<<<< HEAD
from fastapi import APIRouter, FastAPI #Documentacion
from pydantic import BaseModel #Validad datos en la DB
import oracledb #Conección en BD OCI
from dotenv import load_dotenv #Credenciales
import os

from schemas.student import CreateStudent, Student
=======
from fastapi import FastAPI
from database.connection import get_db_connection
from routes.base_router import api_router
>>>>>>> dev

app = FastAPI(title="SUM chiquito")

# # Crear conexión a la base de datos
# conn = get_db_connection()

# cursor = conn.cursor()


<<<<<<< HEAD
# Read all students
@router.get("/students/")
async def read_students():
    cursor.execute("SELECT id,nombre, apellido FROM estudiantes")
    results = cursor.fetchall()
    students = []
    for result in results:
        student = Student(id=result[0], name=result[1], last_name=result[2])
        students.append(student)
    return students

# Read student by id
@router.get("/students/{student_id}")
async def read_student(student_id: int):
    cursor.execute("SELECT id,nombre, apellido FROM estudiantes WHERE id=:1", (student_id,))
    result = cursor.fetchone()
    if result:
        student = Student(id=result[0], name=result[1], last_name=result[2])
        return student
    else:
        return {"message": "Student not found"}

# Update student
@router.put("/students/{student_id}")
async def update_student(student_id: int, student: Student):
    cursor.execute("UPDATE estudiantes SET nombre=:1, apellido=:2 WHERE id=:3",
                   (student.name, student.last_name, student_id))
    conn.commit()
    return {"message": "Student updated successfully"}

# Delete student
@router.delete("/students/{student_id}")
async def delete_student(student_id: int):
    cursor.execute("DELETE FROM estudiantes WHERE id=:1", (student_id,))
    conn.commit()
    return {"message": "Student deleted successfully"}

app.include_router(router)

#uvicorn main:app --reload
=======
app.include_router(api_router)
>>>>>>> dev
