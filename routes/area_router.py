from fastapi import APIRouter
from database.connection import get_db_connection
from schemas.areas import Area, AreaUpdate, CreateArea

router = APIRouter()

# Create area
@router.post("/")
async def create_area(areas: CreateArea):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("INSERT INTO areas (id_area, nombre) VALUES (:1, :2)",
                   (areas.id, areas.name))
    conn.commit()
    conn.close()
    return {"message": "Area creada exitosamente"}


# Read all areas
@router.get("/")
async def read_areas():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT nombre FROM areas")
    results = cursor.fetchall()
    areas = []
    for result in results:
        area = Area(name=result[0])
        areas.append(area)
    conn.close()
    return areas

# Update area
@router.put("/{area_id}")
async def update_area(area_id: int, areas: AreaUpdate):
    conn = get_db_connection()
    cursor = conn.cursor()
    # Consultar si existe la escuela con el ID proporcionado
    cursor.execute("SELECT id_area FROM areas WHERE id_area=:1", (area_id,))
    result = cursor.fetchone()

    # Si no se encuentra la escuela, retornar un mensaje de error
    if not result:
        return {"error": "Area no encontrada"}

    # Si la escuela existe, actualizar sus datos en la base de datos
    cursor.execute("UPDATE areas SET nombre=:1 WHERE id_area=:2",
                   (areas.name, area_id))
    conn.commit()
    conn.close()
    return {"message": "Area actualizada exitosamente"}

# Delete area
@router.delete("/{area_id}")
async def delete_area(area_id: int):
    conn = get_db_connection()
    cursor = conn.cursor()
    # Consultar si existe el area con el ID proporcionado
    cursor.execute("SELECT id_area FROM areas WHERE id_area=:1", (area_id,))
    result = cursor.fetchone()

    # Si no se encuentra el area, retornar un mensaje de error
    if not result:
        return {"error": "Area no encontrada"}

    # Si el area existe, eliminarlo de la base de datos
    cursor.execute("DELETE FROM areas WHERE id_area=:1", (area_id,))
    conn.commit()
    conn.close()
    return {"message": "Area actualizada exitosamente"}