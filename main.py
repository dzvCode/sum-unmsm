from fastapi import APIRouter, FastAPI
from pydantic import BaseModel
import cx_Oracle

from schemas.student import CreateStudent, Student

app = FastAPI(title="SUM chiquito")

# Configuracion de base de datos
db_username = 'g3_dzavala' # Cambian segun su nombre de usuario
db_password = 'admin' # Contrasena
db_dsn = cx_Oracle.makedsn('localhost', '1521', 'xe') # Dejar por defecto
db = cx_Oracle.connect(db_username, db_password, db_dsn)
cursor = db.cursor()

router = APIRouter(tags=["Users"])

# Create student
@router.post("/students/")
async def create_student(student: CreateStudent):
    cursor.execute("INSERT INTO students (name, last_name) VALUES (:1, :2)",
                   (student.name, student.last_name))
    db.commit()
    return {"message": "Student created successfully"}

# Read all students
@router.get("/students/")
async def read_students():
    cursor.execute("SELECT id, name, last_name FROM students")
    results = cursor.fetchall()
    students = []
    for result in results:
        student = Student(id=result[0], name=result[1], last_name=result[2])
        students.append(student)
    return students

# Read student by id
@router.get("/students/{student_id}")
async def read_student(student_id: int):
    cursor.execute("SELECT id, name, last_name FROM students WHERE id=:1", (student_id,))
    result = cursor.fetchone()
    if result:
        student = Student(id=result[0], name=result[1], last_name=result[2])
        return student
    else:
        return {"message": "Student not found"}

# Update student
@router.put("/students/{student_id}")
async def update_student(student_id: int, student: Student):
    cursor.execute("UPDATE students SET name=:1, last_name=:2 WHERE id=:3",
                   (student.name, student.last_name, student_id))
    db.commit()
    return {"message": "Student updated successfully"}

# Delete student
@router.delete("/students/{student_id}")
async def delete_student(student_id: int):
    cursor.execute("DELETE FROM students WHERE id=:1", (student_id,))
    db.commit()
    return {"message": "Student deleted successfully"}

app.include_router(router)