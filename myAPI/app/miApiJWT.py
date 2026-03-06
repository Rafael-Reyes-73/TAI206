from typing import Optional
from fastapi import FastAPI, status, HTTPException, Depends
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from pydantic import BaseModel, Field
import asyncio
from jose import JWTError, jwt
from datetime import datetime, timedelta
import secrets


SECRET_KEY = "mi_super_secreta_clave_para_jwt" 
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 1 


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


usuarios = [
    {"id": 1, "nombre": "Miguel", "edad": 21},
    {"id": 2, "nombre": "Ivet", "edad": 22},
    {"id": 3, "nombre": "Isaac", "edad": 20},
]


class UsuarioBase(BaseModel):
    id: int = Field(..., gt=0, description="Identificador de usuario", example=1)
    nombre: str = Field(..., min_length=3, max_length=50, description="Nombre del usuario", example="axel")
    edad: int = Field(..., ge=0, le=121, description="La edad de 0 a 121", example=21)

def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


async def get_current_user(token: str = Depends(oauth2_scheme)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="No se pudieron validar las credenciales"
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
    except JWTError: 
        raise credentials_exception
    return username


app = FastAPI(
    title='miApiJWT',
    description='Rafael de Jesús Reyes Chávez - API con JWT',
    version='1.0'
)


@app.post("/token", tags=['Autenticación'])
async def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends()):
    usuarioAuth = secrets.compare_digest(form_data.username, "admin")
    contrasenaAuth = secrets.compare_digest(form_data.password, "1234")
    
    if not (usuarioAuth and contrasenaAuth):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Usuario o contraseña incorrectos"
        )
    
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": form_data.username}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}


@app.get("/", tags=['inicio'])
async def helloworld():
    return {"mensaje": "Rafael Reyes"} 

@app.get("/v1/usuario/{id}", tags=['Crud Usuario'])
async def ConsultaUsuarios():
    return {
        "status": "200",
        "total": len(usuarios),
        "data": usuarios
    }

@app.post("/v1/AgregarUsuario/", tags=['Crud Usuario'])
async def AgregarUsuarios(usuario: UsuarioBase):
    for usr in usuarios:
        if usr["id"] == usuario.id:
            raise HTTPException(status_code=400, detail="ID existente")
    usuarios.append(usuario.dict())
    return {"mensaje": "usuario agregado correctamente", "datos": usuario, "status": 200} 



@app.put("/v1/ActualizarUsuario/{id}", tags=['Crud Usuario'])
async def actualizar_usuario(id: int, usuario_actualizado: dict, current_user: str = Depends(get_current_user)):
    for usr in usuarios:
        if usr["id"] == id:
            if "nombre" in usuario_actualizado:
                usr["nombre"] = usuario_actualizado["nombre"]
            if "edad" in usuario_actualizado:
                usr["edad"] = usuario_actualizado["edad"]
            return {"mensaje": "Usuario actualizado", "datos": usr, "usuario_auth": current_user}
            
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Usuario no encontrado")

@app.delete("/v1/EliminarUsuario/{id}", tags=['Crud Usuario'])
async def eliminar_usuario(id: int, current_user: str = Depends(get_current_user)):
    for i, usr in enumerate(usuarios):
        if usr["id"] == id:
            usuario_eliminado = usuarios.pop(i)
            return {"mensaje": f"Usuario eliminado correctamente por {current_user}", "datos": usuario_eliminado}
            
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Usuario no encontrado")