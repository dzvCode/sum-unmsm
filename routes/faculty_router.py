from fastapi import APIRouter
from database.connection import get_db_connection
from schemas.faculty import CreateFaculty, Faculty, FacultyUpdate

router = APIRouter()

# Create faculty
@router.post("/")
async def create_faculty(faculty: CreateFaculty):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("INSERT INTO facultades (id_facultad, nombre, id_area) VALUES (:1, :2, :3)",
                   (faculty.id, faculty.name, faculty.id_area))
    conn.commit()
    conn.close()
    return {"message": "Facultad creada exitosamente"}


# Read all faculties
@router.get("/")
async def read_faculties():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT nombre FROM facultades")
    results = cursor.fetchall()
    faculties = []
    for result in results:
        faculty = Faculty(name=result[0])
        faculties.append(faculty)
    conn.close()
    return faculties


# Update faculty
@router.put("/{faculty_id}")
async def update_faculty(faculty_id: int, faculty: FacultyUpdate):
    conn = get_db_connection()
    cursor = conn.cursor()
    # Consultar si existe la facultad con el ID proporcionado
    cursor.execute("SELECT id_facultad FROM facultades WHERE id_facultad=:1", (faculty_id,))
    result = cursor.fetchone()

    # Si no se encuentra la facultad, retornar un mensaje de error
    if not result:
        conn.close()
        return {"error": "Facultad no encontrada"}

    # Si la facultad existe, actualizar sus datos en la base de datos
    cursor.execute("UPDATE facultades SET nombre=:1 WHERE id_facultad=:2",
                   (faculty.name, faculty_id))
    conn.commit()
    conn.close()
    return {"message": "Facultad actualizada exitosamente"}

# Delete faculty
@router.delete("/{faculty_id}")
async def delete_faculty(faculty_id: int):
    conn = get_db_connection()
    cursor = conn.cursor()
    # Consultar si existe el facultad con el ID proporcionado
    cursor.execute("SELECT id_facultad FROM facultades WHERE id_facultad=:1", (faculty_id,))
    result = cursor.fetchone()

    # Si no se encuentra el facultad, retornar un mensaje de error
    if not result:
        conn.close()
        return {"error": "Facultad no encontrada"}

    # Si el facultad existe, eliminarlo de la base de datos
    cursor.execute("DELETE FROM facultades WHERE id_facultad=:1", (faculty_id,))
    conn.commit()
    conn.close()

    return {"message": "Facultad eliminada exitosamente"}