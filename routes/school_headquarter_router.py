from fastapi import APIRouter
from database.connection import get_db_connection

from schemas.school_headquarter import SHR, SHRUpdate

router = APIRouter()

# Crear conexión a la base de datos
conn = get_db_connection()
cursor = conn.cursor()

# Create Schools_headquarters
@router.post("/")
async def create_schools_headquarters(SHR: SHR):
    cursor.execute("INSERT INTO escuela_sede (id_escuela, id_sede) VALUES (:1, :2)",
                   (SHR.id_school, SHR.id_headquarter))
    conn.commit()
    return {"message": "school_headquarter created successfully"}


# Read all courses_teacherss
@router.get("/")
async def read_school_headquarter():
    cursor.execute("SELECT id_escuela, id_sede FROM escuela_sede")
    results = cursor.fetchall()
    schools_headquarters = []
    for result in results:
        school_headquarter =  SHR(id_escuela=result[0], id_sede=result[1])
        schools_headquarters.append(school_headquarter)
    return schools_headquarters

# Read Schools_headquarters by id
@router.get("/{School_headquarter}")
async def read_school_headquarter_ids(school_id:int , id_headquarter:int):
    cursor.execute("SELECT id_escuela, id_sede FROM escuela_sede WHERE id_escuela=:1 and id_sede=:2", (school_id, id_headquarter,))
    result = cursor.fetchone()
    if result:
        school_headquarter =  SHR(id_escuela=result[0], id_sede=result[1])
        return school_headquarter

    else:
        return {"message": "school_headquarter not found"}

# Update school_headquarter
@router.put("/{school_headquarter_ids}")
async def update_school_headquarter(school_id:int, headquarter_id:int, SHR: SHRUpdate):
    # Consultar si existe el estudiante con el ID proporcionado
    cursor.execute("SELECT id_escuela, id_sede FROM escuela_sede WHERE id_escuela=:1 and id_sede=:2", (school_id, headquarter_id,))
    result = cursor.fetchone()

    # Si no se encuentra el estudiante, retornar un mensaje de error
    if not result:
        return {"error": "school_headquarter not found"}

    # Si el estudiante existe, actualizar sus datos en la base de datos
    cursor.execute("UPDATE id_sede SET id_sede=:1 WHERE id_escuela=:2 and id_sede=:3",
                   (SHR.id_headquarter, school_id, headquarter_id))
    conn.commit()

    return {"message": "school_headquarter updated successfully"}


# Delete school_headquarter
@router.delete("/{school_headquarter_ids}")
async def delete_school_headquarter(school_id:int, headquarter_id:int):
    # Consultar si existe el estudiante con el ID proporcionado
    cursor.execute("SELECT id_escuela, id_sede FROM escuela_sede WHERE id_escuela=:1 and id_sede=:2", (school_id, headquarter_id,))
    result = cursor.fetchone()

    # Si no se encuentra el estudiante, retornar un mensaje de error
    if not result:
        return {"error": "school_headquarter not found"}

    # Si el estudiante existe, eliminarlo de la base de datos
    cursor.execute("DELETE FROM escuela_sede WHERE id_escuela=:1 and id_sede=:2", (school_id, headquarter_id,))
    conn.commit()

    return {"message": "school_headquarter deleted successfully"}

