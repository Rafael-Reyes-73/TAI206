from fastapi import FastAPI, HTTPException, status, Request
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from pydantic import BaseModel, Field, EmailStr
from typing import List, Literal
from datetime import datetime

app = FastAPI()

@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    return JSONResponse(
        status_code=400,
        content={"detail": "Faltan datos o el nombre del libro no es válido"}
    )

current_year = datetime.now().year

class Usuario(BaseModel):
    nombre: str
    correo: EmailStr 

class Libro(BaseModel):
    nombre: str = Field(..., min_length=2, max_length=100) 
    anio: int = Field(..., gt=1450, le=current_year) 
    paginas: int = Field(..., gt=1) 
    estado: Literal["disponible", "prestado"] = "disponible" 

class Prestamo(BaseModel):
    id_prestamo: int
    nombre_libro: str
    correo_usuario: EmailStr

db_libros = []
db_prestamos = []

@app.post("/libros", status_code=status.HTTP_201_CREATED) 
def registrar_libro(libro: Libro):
    db_libros.append(libro)
    return {"mensaje": "Libro registrado exitosamente", "libro": libro}


@app.get("/libros/disponibles", response_model=List[Libro])
def listar_libros_disponibles():
    return [libro for libro in db_libros if libro.estado == "disponible"]


@app.get("/libros/{nombre}")
def buscar_libro(nombre: str):
    for libro in db_libros:
        if libro.nombre.lower() == nombre.lower():
            return libro
    raise HTTPException(status_code=400, detail="Nombre de libro no válido o no encontrado") 


@app.post("/prestamos")
def registrar_prestamo(nombre_libro: str, usuario: Usuario):
    for libro in db_libros:
        if libro.nombre == nombre_libro:
            if libro.estado == "prestado":
                raise HTTPException(status_code=409, detail="El libro ya está prestado")
            
            libro.estado = "prestado"
            nuevo_prestamo = Prestamo(
                id_prestamo=len(db_prestamos) + 1, 
                nombre_libro=libro.nombre, 
                correo_usuario=usuario.correo
            )
            db_prestamos.append(nuevo_prestamo)
            return {"mensaje": "Préstamo registrado", "prestamo": nuevo_prestamo}
    raise HTTPException(status_code=404, detail="Libro no encontrado")


@app.put("/prestamos/{id_prestamo}/devolver", status_code=status.HTTP_200_OK) 
def devolver_libro(id_prestamo: int):
    for prestamo in db_prestamos:
        if prestamo.id_prestamo == id_prestamo:
            for libro in db_libros:
                if libro.nombre == prestamo.nombre_libro:
                    libro.estado = "disponible"
            return {"mensaje": "Libro devuelto exitosamente"}
            
    raise HTTPException(status_code=409, detail="El registro de préstamo ya no existe")


@app.delete("/prestamos/{id_prestamo}")
def eliminar_prestamo(id_prestamo: int):
    for i, prestamo in enumerate(db_prestamos):
        if prestamo.id_prestamo == id_prestamo:
            db_prestamos.pop(i)
            return {"mensaje": "Registro de préstamo eliminado"}
            
    raise HTTPException(status_code=409, detail="El registro de préstamo ya no existe") 

