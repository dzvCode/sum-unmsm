from fastapi import FastAPI
from database.connection import get_db_connection
from routes.base_router import api_router
from fastapi.middleware.cors import CORSMiddleware


app = FastAPI(title="SUM Chiquito", description="La API backend realizada con FAST API del gestor de estudiantes y matrícula SUM Chiquito es un sistema que permite a los usuarios gestionar información relacionada con la matrícula y el seguimiento de estudiantes de la Universidad Nacional Mayor de San Marcos.")
# # Crear conexión a la base de datos
# conn = get_db_connection()

# cursor = conn.cursor()

# Configuración del middleware CORS
origins = ["*"]  # Permite solicitudes desde cualquier origen
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(api_router)

#uvicorn main:app --reload