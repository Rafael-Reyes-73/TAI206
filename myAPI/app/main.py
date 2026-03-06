from typing import Optional
from fastapi import FastAPI,status,HTTPException, Depends
import asyncio
from pydantic import BaseModel, Field
from fastapi.security import HTTPBasic, HTTPBasicCredentials
import secrets


#tiempo de espera de una peticion es de prueba 

usuarios=[
    {"id":1,"nombre":"Miguel","edad":21},
    {"id":2,"nombre":"Ivet","edad":22},
    {"id":3,"nombre":"Isaac","edad":20},
]
#modelo de validacion pydantic
class UsuarioBase(BaseModel):
    id :int =  Field(...,gt=0,description="identificador de usuario",example="1")
    nombre : str = Field(...,min_length=3,max_length=50,description="Nombre del usuario",example="axel")
    edad : int = Field(...,ge=0,gt=121,description="la edad de 0 a 121",example="21")
    
    

    # seguridad con HTTPBasic
security = HTTPBasic()

def verificar_usuario(credentials: HTTPBasicCredentials = Depends(security)):
    usuarioAuth= secrets.compare_digest(credentials.username, "admin")
    contrasenaAuth= secrets.compare_digest(credentials.password, "1234")
    
    if not(usuarioAuth and contrasenaAuth):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Credenciales no validas",
        )
        
    return credentials.username

#inicialiacion 
app= FastAPI(
    title= 'mi primera api',
    description='Rafael de Jesús Reyes Chávez',
    version='1.0'
)
#mostramos ladescripcion de documentacion

#endpoints
@app.get("/", tags=['inicio'])
async def helloworld():
    return {"mensaje":" hello world FastAPI"} 


@app.get("/bienvenidos", tags=['inicio'])
async def bienvenida():
    return {"mensaje":" bienvenido a mi primerita API"}



#27/01/26
@app.get("/v1/calificaciones", tags=['Asincronia'])
#tags nos ayuda a seccionar las partes de nuestra documentacion por apartados
async def calificaciones():
    await asyncio.sleep(7)
    #se muestra la peticion pero con una demora de tiempo pero en cuanto se libere se recibira la peticion 
    return {"mensaje":" Tu calificacion en TAI es 10"} 

#obligatorio
@app.get("/v1/prametroO/{id}", tags=['Parametros Obligatorios'])
async def ConsultaUsuarios(id:int):
    await asyncio.sleep(3)
    return {"Usuario Encontrado":id}

#opcional
@app.get("/v1/parametroOP/", tags=['Parametros opcionales'])
async def ConsultaOp(id: Optional[int]=None):
    await asyncio.sleep(3)
    if id is not None:
        return {"Usuario Encontrado":id}


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
    
#verbos http tarea put, delete
@app.get("/v1/usuario/{id}", tags=['Crud Usuario'])
async def ConsultaUsuarios():
    return{
        "status":"200",
        "total":len(usuarios),
        "data":usuarios
    }

@app.post("/v1/AgregarUsuario/{id}", tags=['Crud Usuario'])
async def AgregarUsuarios(usuario:UsuarioBase):
    for usr in usuarios:
        if usr["id"] == usuario.id("id"):
            raise HTTPException(
                status_code=400,
                detail="ID existente"
            )
    usuarios.append(usuario)
    return{
        "mensaje":"usuario agregado correctamente",
        "datos":usuario,
        "status":200
    } 
    
# put
@app.put("/v1/ActualizarUsuario/{id}", tags=['Crud Usuario'])
async def actualizar_usuario(id: int, usuario_actualizado: dict):
    # Buscar el usuario por id
    for usr in usuarios:
        if usr["id"] == id:
            # Actualizar solo los campos proporcionados (nombre, edad)
            if "nombre" in usuario_actualizado:
                usr["nombre"] = usuario_actualizado["nombre"]
            if "edad" in usuario_actualizado:
                usr["edad"] = usuario_actualizado["edad"]
            return {
                "mensaje": "Usuario actualizado correctamente",
                "datos": usr,
                "status": 200
            }
    # Si no se encuentra el id, lanzar excepción 404
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail="Usuario no encontrado"
    )


#delete 
@app.delete("/v1/EliminarUsuario/{id}", tags=['Crud Usuario'])
async def eliminar_usuario(id: int, username: str = Depends(verificar_usuario)):
    # Buscar el índice del usuario por id
    for i, usr in enumerate(usuarios):
        if usr["id"] == id:
            usuario_eliminado = usuarios.pop(i)
            return {
                
                
                "mensaje": "Usuario eliminado correctamente por {usuarioAuth}",
                "datos " : usuario_eliminado,
                "status": 200
            }
    # Si no se encuentra el id, lanzar excepción 404
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail="Usuario no encontrado"
    )