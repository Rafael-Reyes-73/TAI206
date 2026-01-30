#importaciones 
from typing import Optional
from fastapi import FastAPI
import asyncio

#inicializacion del servidor
app = FastAPI(
    title='Mi primer API con FastAPI',
    description='Rafael de Jesús Reyes Chávez',
    version='1.0.0'
)

#BD ficticia
usuarios=[
    {"id":1,"nombre":"Rafael","edad":26,},
    {"id":2,"nombre":"Ivet","edad":22,},
    {"id":3,"nombre":"Miguel","edad":23,},
    ]


#agrupamiento de endpoints

#Endpoints
@app.get("/",tags=["Inicio"])
async def holamundo():
    return {"mensaje": "Hola Mundo FastAPI"}

@app.get("/bienvenidos",tags=["Inicio"])
async def bienvenido():
    return {"mensaje": "Bienvenidosa tu API REST"}

@app.get("/v1/calificaciones",tags=["Asincronia"])
async def calificaciones():
    await asyncio.sleep(6)  # Simula una operación asincrónica  
    return {"mensaje": "Tu calificación es TAI es 5"}


@app.get("/v1/usuario/{id}",tags=["Parametro obligatorio"])
async def consultaUsuarios(id:int):
    await asyncio.sleep(3)
    return {"Usuario encontrado":id}

@app.get("/v1/usuarios_op/", tags=["Parametro Opcional"])
async def consultaOp(id: Optional[int] = None):
    await asyncio.sleep(3)
    if id is not None:
        for usuario in usuarios:
            if usuario["id"] == id: 
                return {"usuario encontrado": id, "Datos": usuario}
        return {"mensaje": "Usuario no encontrado"}  
    else:
        return {"mensaje": "No se proporciono Id"}
