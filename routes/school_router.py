from fastapi import APIRouter
from database.connection import get_db_connection
from schemas.school import CreateSchool, School, SchoolUpdate

router = APIRouter()

# Crear conexión a la base de datos
conn = get_db_connection()
cursor = conn.cursor()

# Create school
@router.post("/")
async def create_school(school: CreateSchool):
    cursor.execute("INSERT INTO escuelas (id_escuela, nombre, id_facultad) VALUES (:1, :2, :3)",
                   (school.id, school.name, school.id_facultad))
    conn.commit()
    return {"message": "School created successfully"}


# Read all schools
@router.get("/")
async def read_schools():
    cursor.execute("SELECT nombre FROM escuelas")
    results = cursor.fetchall()
    schools = []
    for result in results:
        school = School(name=result[0])
        schools.append(school)
    return schools


# Update school
@router.put("/{school_id}")
async def update_school(school_id: int, school: SchoolUpdate):
    # Consultar si existe la escuela con el ID proporcionado
    cursor.execute("SELECT id_escuela FROM escuelas WHERE id_escuela=:1", (school_id,))
    result = cursor.fetchone()

    # Si no se encuentra la escuela, retornar un mensaje de error
    if not result:
        return {"error": "School not found"}

    # Si la escuela existe, actualizar sus datos en la base de datos
    cursor.execute("UPDATE escuelas SET nombre=:1 WHERE id_escuela=:2",
                   (school.name, school_id))
    conn.commit()

    return {"message": "School updated successfully"}

# Delete school
@router.delete("/{school_id}")
async def delete_school(school_id: int):
    # Consultar si existe el escuela con el ID proporcionado
    cursor.execute("SELECT id_escuela FROM escuelas WHERE id_escuela=:1", (school_id,))
    result = cursor.fetchone()

    # Si no se encuentra el escuela, retornar un mensaje de error
    if not result:
        return {"error": "School not found"}

    # Si el escuela existe, eliminarlo de la base de datos
    cursor.execute("DELETE FROM escuelas WHERE id_escuela=:1", (school_id,))
    conn.commit()

    return {"message": "School deleted successfully"}