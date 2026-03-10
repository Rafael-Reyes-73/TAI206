from typing import Optional
from fastapi import FastAPI, status, HTTPException, Depends
import asyncio
from pydantic import BaseModel, Field
from fastapi.security import HTTPBasic, HTTPBasicCredentials
import secrets

app = FastAPI(
    title='EXAMEN SEGUNDO PARCIAL',
    description='Rafael de Jesus Reyes Chavez',
    version='1.0'
)

pacientes = [
    {"id": 1, "nombre": "Karen", "edad": 21, "citas": 0},
    {"id": 2, "nombre": "Mely", "edad": 18, "citas": 0},
    {"id": 3, "nombre": "Maria", "edad": 24, "citas": 0},
]

citas = [
    {"id": 1, "fecha": "15/03/26", "motivo": "Me duele algo","confirmacion": False},
    {"id": 2, "fecha": "18/03/26", "motivo": "Me duele algo","confirmacion": False},
    {"id": 3, "fecha": "20/03/26", "motivo": "Me duele algo","confirmacion": False},
]

class PacienteBase(BaseModel):
    id: int = Field(..., gt=0, description="Identificador de paciente", example=1)
    nombre: str = Field(..., min_length=5, max_length=50, description="Nombre del paciente", example="Karen")
    edad: int = Field(..., ge=0, le=121, description="La edad de 0 a 121", example=21)
    
    
class CitasBase(BaseModel):
    id: int = Field(..., gt=0, description="Identificador de citas", example=1)
    fecha: str = Field(..., min_length=5, max_length=50, description="fecha de citas", example="15/03/26")
    motivo: int = Field(..., ge=15, le=100, description="motivo no debe de exceder 100 caracteres", example="Me duele algo")
    confirmacion: bool = Field(..., True, False, description="La confirmacion debe de ser bool", example=False)

security = HTTPBasic()

def verificar_paciente(credentials: HTTPBasicCredentials = Depends(security)):
    usuarioAuth = secrets.compare_digest(credentials.username, "root")
    contrasenaAuth = secrets.compare_digest(credentials.password, "1234")
    
    if not (usuarioAuth and contrasenaAuth):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Credenciales no validas",
        )
    return credentials.username


@app.get("/v1/parametroO/{id}", tags=['Parametros Obligatorios'])
async def ConsultaPacientesParam(id: int):
    await asyncio.sleep(3)
    return {"Paciente Encontrado": id}

@app.get("/v1/parametroOP/", tags=['Parametros Opcionales'])
async def ConsultaOp(id: Optional[int] = None):
    await asyncio.sleep(3)
    if id is not None:
        return {"Paciente Encontrado": id}
    return {"mensaje": "No se proporciono Id"}

#-----------------------------------------   PACIENTE
@app.get("/v1/paciente/{id}", tags=['Crud Pacientes'])
async def ConsultaUnPaciente(id: int):
    for paci in pacientes:
        if paci["id"] == id:
            return {"status": 200, "data": paci}
    raise HTTPException(status_code=404, detail="Paciente no encontrado")


@app.post("/v1/AgregarPaciente/", tags=['Crud Paciente'])
async def AgregarPacientes(paciente: PacienteBase):
    for usr in pacientes:
        if usr["id"] == paciente.id:
            raise HTTPException(
                status_code=400,
                detail="ID existente"
            )

    nuevo_paciente = paciente.model_dump() 
    pacientes.append(nuevo_paciente)
    return {
        "mensaje": "Paciente agregado correctamente",
        "datos": nuevo_paciente,
        "status": 200
    } 

@app.delete("/v1/EliminarPacientes/{id}", tags=['Crud Cita'])
async def eliminar_paciente(id: int, username: str = Depends(verificar_paciente)):
    for i, paci in enumerate(pacientes):
        if paci["id"] == id:
            paciente_eliminado = pacientes.pop(i)
            return {
                "mensaje": f"paciente eliminado correctamente por {username}",
                "datos": paciente_eliminado,
                "status": 200
            }
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail="Paciente no encontrado"
    )
#-----------------------------------------       

#-----------------------------------------   CITA
@app.get("/v1/paciente/{id}", tags=['Crud Pacientes'])
async def ConsultaUnPaciente(id: int):
    for paci in pacientes:
        if paci["id"] == id:
            return {"status": 200, "data": paci}
    raise HTTPException(status_code=404, detail="Paciente no encontrado")


@app.post("/v1/AgregarPaciente/", tags=['Crud Paciente'])
async def AgregarPacientes(paciente: PacienteBase):
    
    for usr in pacientes:
        if usr["id"] == paciente.id:
            raise HTTPException(
                status_code=400,
                detail="ID existente"
            )

    nuevo_paciente = paciente.model_dump() 
    pacientes.append(nuevo_paciente)
    return {
        "mensaje": "Usuario agregado correctamente",
        "datos": nuevo_paciente,
        "status": 200
    } 

@app.delete("/v1/EliminarCita/{id}", tags=['Crud Cita'])
async def eliminar_cita(id: int, username: str = Depends(verificar_paciente)):
    for i, ci in enumerate(citas):
        if ci["id"] == id:
            cita_eliminada = citas.pop(i)
            return {
                "mensaje": f"Cita eliminada correctamente por {username}",
                "datos": cita_eliminada,
                "status": 200
            } 
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail="Cita no encontrado"
    )
