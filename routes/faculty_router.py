from fastapi import APIRouter
from database.connection import get_db_connection
from schemas.faculty import CreateFaculty, Faculty, FacultyUpdate

router = APIRouter()

# Crear conexión a la base de datos
conn = get_db_connection()
cursor = conn.cursor()

# Create faculty
@router.post("/")
async def create_faculty(faculty: CreateFaculty):
    cursor.execute("INSERT INTO facultades (id_facultad, nombre, id_area) VALUES (:1, :2, :3)",
                   (faculty.id, faculty.name, faculty.id_area))
    conn.commit()
    return {"message": "Faculty created successfully"}


# Read all faculties
@router.get("/")
async def read_faculties():
    cursor.execute("SELECT nombre FROM facultades")
    results = cursor.fetchall()
    faculties = []
    for result in results:
        faculty = Faculty(name=result[0])
        faculties.append(faculty)
    return faculties


# Update faculty
@router.put("/{faculty_id}")
async def update_faculty(faculty_id: int, faculty: FacultyUpdate):
    # Consultar si existe la facultad con el ID proporcionado
    cursor.execute("SELECT id_facultad FROM facultades WHERE id_facultad=:1", (faculty_id,))
    result = cursor.fetchone()

    # Si no se encuentra la facultad, retornar un mensaje de error
    if not result:
        return {"error": "Faculty not found"}

    # Si la facultad existe, actualizar sus datos en la base de datos
    cursor.execute("UPDATE facultades SET nombre=:1 WHERE id_facultad=:2",
                   (faculty.name, faculty_id))
    conn.commit()

    return {"message": "Faculty updated successfully"}

# Delete faculty
@router.delete("/{faculty_id}")
async def delete_faculty(faculty_id: int):
    # Consultar si existe el facultad con el ID proporcionado
    cursor.execute("SELECT id_facultad FROM facultades WHERE id_facultad=:1", (faculty_id,))
    result = cursor.fetchone()

    # Si no se encuentra el facultad, retornar un mensaje de error
    if not result:
        return {"error": "Faculty not found"}

    # Si el facultad existe, eliminarlo de la base de datos
    cursor.execute("DELETE FROM facultades WHERE id_facultad=:1", (faculty_id,))
    conn.commit()

    return {"message": "Faculty deleted successfully"}