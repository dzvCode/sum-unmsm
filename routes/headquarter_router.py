from fastapi import APIRouter
from database.connection import get_db_connection

from schemas.headquarter import  Headquarter

router = APIRouter()

# Crear conexión a la base de datos
conn = get_db_connection()
cursor = conn.cursor()

#GET Headquarter
@router.get("/")
async def read_headquarter():
    cursor.execute("SELECT id_sede, nombre, direccion FROM sedes")
    results = cursor.fetchall()
    headquarters = []
    for result in results:
        headquarter = Headquarter(id=result[0], name=result[1], address=result[2])
        headquarters.append(headquarter)
    return headquarters