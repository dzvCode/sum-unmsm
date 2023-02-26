from fastapi import APIRouter, FastAPI
from pydantic import BaseModel
import oracledb

from schemas.student import CreateStudent, Student

app = FastAPI(title="SUM chiquito")

conn=oracledb.connect(
     user="admin",
     password="GTA-5-elmejor",
     dsn="kb2tz61mq5de5n4y_low",
     config_dir="C:/Users/jj-08/Downloads/Wallet_KB2TZ61MQ5DE5N4Y",
     wallet_location="C:/Users/jj-08/Downloads/Wallet_KB2TZ61MQ5DE5N4Y",
     wallet_password="GTA-5-elmejor")

cursor = conn.cursor()

router = APIRouter(tags=["Users"])

# Create student
@router.post("/students/")
async def create_student(student: Student):
    cursor.execute("INSERT INTO estudiantes (id,nombre, apellido) VALUES (:1, :2, :3)",
                   (student.id,student.name, student.last_name))
    conn.commit()
    return {"message": "Student created successfully"}


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