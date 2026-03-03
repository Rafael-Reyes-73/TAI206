#importaciones
from fastapi import FastAPI, status, HTTPException, Depends
import asyncio
from typing import Optional
from pydantic import BaseModel, Field
from fastapi.security import HTTPBasic, HTTPBasicCredentials
import secrets



#Inicializacion o Instacia de la API
app= FastAPI(
    title= 'Mi primer API',
    description='Rafael de Jesus Reyes Chavez',
    version='1,0'
)

#BD Ficticia
usuarios=[
    {"id":1,"Nombre":"sad","Edad":21},
    {"id":2,"Nombre":"ssd","Edad":15},
    {"id":3,"Nombre":"jm","Edad":28},
]

security = HTTPBasic()
def verifcar_Peticion(credentials: HTTPBasicCredentials = Depends(security)):
    usuarioAuth = secrets.compare_digest(credentials.username, "admin")
    contraAuth = secrets.compare_digest(credentials.password, "1234")
    if not (usuarioAuth and contraAuth):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Credenciales incorrectas"
        )
    return credentials.username

#Endpoints
@app.get("/",tags=['Inicio'])
async def comoandamosrasa():
    return {"mensaje":"Hola mundo FastAPI"}

@app.get("/v1/bienvenidos", tags=['Inicio'])
async def bienvenido():
    return {"mensaje":"Bienveidos a tu API REST"}

@app.get("/v1/calificaciones", tags=['Asincronia'])
async def calificaciones():
    await asyncio.sleep(6)
    return {"mensaje":"Tu calificacion en TAI es 10 "}

@app.get("/v1/parametroo/{id}", tags=['Parametro Obligatorio'])
async def consultaUsuarios(id:int):
    await asyncio.sleep(3)
    return { "usuario encontrado":id }


@app.get("/v1/ParametroOp/", tags=['Parametro Opcional'])
async def consultaOp(id: Optional[int]=None):
    await asyncio.sleep(3)
    if id is not None:
        for usuario in usuarios:
            if usuario["id"] == id:
                return { "Usuario encontrado":id,"Datos": usuario }
        return { "Mensaje":"Usuario no encontrado" }
    else:
        return { "Aviso":"No se proporciono ID" }

@app.get("/v1/usuarios/{id}", tags=['CRUD Usuarios'])
async def consultaUsuarios():
    return{
        "status":"200",
        "total": len(usuarios),
        "data":usuarios
    }
    
@app.post("/v1/usuarios/{id}", tags=['CRUD Usuarios'])
async def agregar_usuarios(usuario:dict):
    for usr in usuarios:
        if usr["id"] == usuario.get("id"):
            raise HTTPException(
                status_code=400,
                detail= "El id ya existe"
            )
    usuarios.append(usuario)
    return{
        "Mensaje": "Usuario agregado",
        "datos":usuario,
        "status":"200"
    }
    
@app.put("/v1/usuarios/{id}", tags=['CRUD Usuarios'])
async def actualizar_usuarios(id: int, usuario_actualizado: dict):
    for index, usr in enumerate(usuarios):
        if usr["id"] == id:
            usuarios[index] = usuario_actualizado
            return {
                "mensaje": "Usuario actualizado correctamente",
                "datos": usuario_actualizado
            }
    
    raise HTTPException(
        status_code=404,
        detail="Usuario no encontrado"
    )



@app.delete("/v1/usuarios/{id}", tags=['CRUD Usuarios'])
async def eliminar_usuario(id: int, usuarioAuth: str = Depends(verifcar_Peticion)):
    for usr in usuarios:
        if usr["id"] == id:
            usuarios.remove(usr)
            return {
                "mensaje": "Usuario eliminado correctamente",
                "datos": usr
            }
    
    raise HTTPException(
        status_code=404,
        detail="El Usuario no existe"
    )




