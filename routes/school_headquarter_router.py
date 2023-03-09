from fastapi import APIRouter
from database.connection import get_db_connection

from schemas.school_headquarter import SHR, SHRUpdate, VW_SHR

router = APIRouter()

# Create Schools_headquarters
@router.post("/")
async def create_schools_headquarters(SHR: SHR):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("INSERT INTO escuela_sede (id_escuela, id_sede) VALUES (:1, :2)",
                   (SHR.id_school, SHR.id_headquarter))
    conn.commit()
    conn.close()
    return {"message": "fila escuela_sede creada con exito"}


# Read all courses_teacherss
@router.get("/")
async def read_school_headquarter():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT ESCUELA,SEDE FROM VW_ESCUELAS_SEDES")
    results = cursor.fetchall()
    schools_headquarters = []
    for result in results:
        school_headquarter =  VW_SHR(school=result[0], headquarter=result[1])
        schools_headquarters.append(school_headquarter)
    conn.close()
    return schools_headquarters

# Read Schools_headquarters by id
@router.get("/{School_headquarter}")
async def read_school_headquarter_ids(school_id:int , id_headquarter:int):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT id_escuela, id_sede FROM escuela_sede WHERE id_escuela=:1 and id_sede=:2", (school_id, id_headquarter,))
    result = cursor.fetchone()
    if result:
        school_headquarter =  SHR(id_school=result[0], id_headquarter=result[1])
        conn.close()
        return school_headquarter

    else:
        conn.close()
        return {"message": "No se encontro esa fila en escuela_sede"}

# Update school_headquarter
@router.put("/{school_headquarter_ids}")
async def update_school_headquarter(school_id:int, headquarter_id:int, SHR: SHRUpdate):
    conn = get_db_connection()
    cursor = conn.cursor()
    # Consultar si existe el estudiante con el ID proporcionado
    cursor.execute("SELECT id_escuela, id_sede FROM escuela_sede WHERE id_escuela=:1 and id_sede=:2", (school_id, headquarter_id,))
    result = cursor.fetchone()

    # Si no se encuentra el estudiante, retornar un mensaje de error
    if not result:
        conn.close()
        return {"error": "Escuela_sede no encontrada"}

    # Si el estudiante existe, actualizar sus datos en la base de datos
    cursor.execute("UPDATE escuela_sede SET id_sede=:1 WHERE id_escuela=:2 and id_sede=:3",
                   (SHR.id_headquarter, school_id, headquarter_id))
    conn.commit()
    conn.close()
    return {"message": "La cambio la id de sede "+str(headquarter_id)+" a " + str(SHR.id_headquarter) + " en la escuela "+ str(school_id) + " de manera exitosa"}


# Delete school_headquarter
@router.delete("/{school_headquarter_ids}")
async def delete_school_headquarter(school_id:int, headquarter_id:int):
    conn = get_db_connection()
    cursor = conn.cursor()
    # Consultar si existe el estudiante con el ID proporcionado
    cursor.execute("SELECT id_escuela, id_sede FROM escuela_sede WHERE id_escuela=:1 and id_sede=:2", (school_id, headquarter_id,))
    result = cursor.fetchone()

    # Si no se encuentra el estudiante, retornar un mensaje de error
    if not result:
        conn.close()
        return {"error": "school_headquarter not found"}

    # Si el estudiante existe, eliminarlo de la base de datos
    cursor.execute("DELETE FROM escuela_sede WHERE id_escuela=:1 and id_sede=:2", (school_id, headquarter_id,))
    conn.commit()
    conn.close()
    return {"message": "se eliminó la fila con id_escuela "+ str(school_id) +" y con id_sede "+ str(headquarter_id)+ " de manera exitosa"}

