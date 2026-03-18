
from typing import Optional
from fastapi import FastAPI, status, HTTPException, Depends, APIRouter  
import asyncio
from pydantic import BaseModel, Field
from fastapi.security import HTTPBasic, HTTPBasicCredentials
import secrets
from app.models.usuario import UsuarioBase
from app.security.auth import verificar_usuario
from app.data.database import usuarios

router = APIRouter(
    prefix="/v1/usuarios",
    tags=["CRUD HTTP"]
)

@router.get("/v1/calificaciones", tags=['Asincronia'])
async def calificaciones():
    await asyncio.sleep(7)
    return {"mensaje": "Tu calificacion en TAI es 10"} 

@router.get("/v1/parametroO/{id}", tags=['Parametros Obligatorios'])
async def ConsultaUsuariosParam(id: int):
    await asyncio.sleep(3)
    return {"Usuario Encontrado": id}

@router.get("/v1/parametroOP/", tags=['Parametros Opcionales'])
async def ConsultaOp(id: Optional[int] = None):
    await asyncio.sleep(3)
    if id is not None:
        return {"Usuario Encontrado": id}
    return {"mensaje": "No se proporciono Id"}

@router.get("/v1/usuarios_op/", tags=["Parametro Opcional"])
async def consultaOpBusqueda(id: Optional[int] = None):
    await asyncio.sleep(3)
    if id is not None:
        for usuario in usuarios:
            if usuario["id"] == id: 
                return {"usuario encontrado": id, "Datos": usuario}
        return {"mensaje": "Usuario no encontrado"}  
    else:
        return {"mensaje": "No se proporciono Id"} 
    

@router.get("/v1/usuario/{id}", tags=['Crud Usuario'])
async def ConsultaUnUsuario(id: int):
    for usr in usuarios:
        if usr["id"] == id:
            return {"status": 200, "data": usr}
    raise HTTPException(status_code=404, detail="Usuario no encontrado")


@router.post("/v1/AgregarUsuario/", tags=['Crud Usuario'])
async def AgregarUsuarios(usuario: UsuarioBase):
    for usr in usuarios:
        if usr["id"] == usuario.id:
            raise HTTPException(
                status_code=400,
                detail="ID existente"
            )

    nuevo_usuario = usuario.model_dump() 
    usuarios.append(nuevo_usuario)
    return {
        "mensaje": "Usuario agregado correctamente",
        "datos": nuevo_usuario,
        "status": 200
    } 
    

@router.put("/v1/{id}", status_code=200)
async def actualizar_usuario(id: int, usuario_actualizado: UsuarioUpdate):
    for usr in usuarios:
        if usr["id"] == id:
            if usuario_actualizado.nombre is not None:
                usr["nombre"] = usuario_actualizado.nombre
            if usuario_actualizado.edad is not None:
                usr["edad"] = usuario_actualizado.edad
                
            return {
                "mensaje": "Usuario actualizado correctamente",
                "datos": usr,
                "status": 200
            }
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail="Usuario no encontrado"
    )


@router.delete("/v1/{id}", status_code=status.HTTP_200_OK)
async def eliminar_usuario(id: int, username: str = Depends(verificar_usuario)):
    for i, usr in enumerate(usuarios):
        if usr["id"] == id:
            usuario_eliminado = usuarios.pop(i)
            return {
                "mensaje": f"Usuario eliminado correctamente por {username}",
                "datos": usuario_eliminado,
                "status": 200
            }
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail="Usuario no encontrado"
    )