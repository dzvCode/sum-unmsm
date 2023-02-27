from fastapi import APIRouter, HTTPException
from fastapi.responses import RedirectResponse

router = APIRouter()

@router.get("/")
async def default_route():
    return {"message": "This is the default route."}