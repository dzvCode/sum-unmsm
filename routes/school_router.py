from fastapi import APIRouter
from database.connection import get_db_connection
from schemas.school import CreateSchool, School, SchoolUpdate

router = APIRouter()

# Create school
@router.post("/")
async def create_school(school: CreateSchool):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("INSERT INTO escuelas (id_escuela, nombre, id_facultad) VALUES (:1, :2, :3)",
                   (school.id, school.name, school.id_facultad))
    conn.commit()
    conn.close()
    return {"message": "Escuela creada exitosamente"}


# Read all schools
@router.get("/")
async def read_schools():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT nombre FROM escuelas")
    results = cursor.fetchall()
    schools = []
    for result in results:
        school = School(name=result[0])
        schools.append(school)
    conn.close()
    return schools


# Update school
@router.put("/{school_id}")
async def update_school(school_id: int, school: SchoolUpdate):
    conn = get_db_connection()
    cursor = conn.cursor()
    # Consultar si existe la escuela con el ID proporcionado
    cursor.execute("SELECT id_escuela FROM escuelas WHERE id_escuela=:1", (school_id,))
    result = cursor.fetchone()

    # Si no se encuentra la escuela, retornar un mensaje de error
    if not result:
        conn.close()
        return {"error": "Escuela no encontrada"}

    # Si la escuela existe, actualizar sus datos en la base de datos
    cursor.execute("UPDATE escuelas SET nombre=:1 WHERE id_escuela=:2",
                   (school.name, school_id))
    conn.commit()
    conn.close()
    return {"message": "Escuela actualizada exitosamente"}

# Delete school
@router.delete("/{school_id}")
async def delete_school(school_id: int):
    conn = get_db_connection()
    cursor = conn.cursor()
    # Consultar si existe el escuela con el ID proporcionado
    cursor.execute("SELECT id_escuela FROM escuelas WHERE id_escuela=:1", (school_id,))
    result = cursor.fetchone()

    # Si no se encuentra el escuela, retornar un mensaje de error
    if not result:
        conn.close()
        return {"error": "Escuela no encontrada"}

    # Si el escuela existe, eliminarlo de la base de datos
    cursor.execute("DELETE FROM escuelas WHERE id_escuela=:1", (school_id,))
    conn.commit()
    conn.close()
    return {"message": "Escuela eliminada exitosamente"}