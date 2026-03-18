from fastapi import FastAPI, status, HTTPException, Depends
from app.routers import usuarios, misc
from app.security.auth import verificar_usuario

app = FastAPI(
    title='Mi primera API',
    description='Rafael de Jesus Reyes Chavez',
    version='1.0'
)

app.include_router(usuarios.router)
app.include_router(misc.router)