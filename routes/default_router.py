from fastapi import APIRouter

router = APIRouter()

@router.get("/")
async def default_route():
    return {"message": "Estas en la ruta por defecto"}