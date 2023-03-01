from fastapi import FastAPI
from database.connection import get_db_connection
from routes.base_router import api_router

app = FastAPI(title="SUM chiquito")

# # Crear conexión a la base de datos
# conn = get_db_connection()

# cursor = conn.cursor()


app.include_router(api_router)

#uvicorn main:app --reload