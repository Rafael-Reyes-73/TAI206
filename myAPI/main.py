#importaciones 
from fastapi import FastAPI

#inicializacion del servidor
app = FastAPI()

#Endpoints
@app.get("/")
async def holamundo():
    return {"mensaje": "Hola Mundo FastAPI"}

@app.get("/bienvenidos")
async def bienvenido():
    return {"mensaje": "Bienvenidosa tu API REST"}