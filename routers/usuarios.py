# pyrefly: ignore [missing-import]
from fastapi import APIRouter, status
from database import dbDependency
from .auth import dependenciaUsuario
from models import Usuario
from exceptions import usuarioNoEncontradoException, noAutorizadoException
from responses import UsuarioResponse

router = APIRouter(prefix="/usuarios", tags=["Usuarios"])

@router.get("/admin/lista-usuarios", response_model=list[UsuarioResponse], status_code=status.HTTP_200_OK)
async def obtenerUsuarios(
    db: dbDependency, 
    usuario: dependenciaUsuario, 
    skip: int = 0, 
    limit: int = 10
):
    if usuario is None:
        raise usuarioNoEncontradoException
    if not usuario.get("admin"):
        raise noAutorizadoException
    return db.query(Usuario).offset(skip).limit(limit).all()