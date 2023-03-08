from fastapi import APIRouter

router = APIRouter()

@router.get("/")
async def default_route():
    return {"message": "This is the default route."}