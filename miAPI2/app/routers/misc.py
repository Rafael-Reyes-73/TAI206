
from fastapi import APIRouter, HTTPException, status, Depends
from typing import Optional
from app.models.usuario import UsuarioBase
from app.security.auth import verificar_usuario
from app.data.database import usuarios
import asyncio

router = APIRouter(tags="Miscelaniua")


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