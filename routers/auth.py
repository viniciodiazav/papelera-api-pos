# pyrefly: ignore [missing-import]
from fastapi import APIRouter, status, Depends
from requests import UsuarioRequest
from database import dbDependency
from models import Usuario
# pyrefly: ignore [missing-import]
from passlib.context import CryptContext
from exceptions import (
    usuarioYaExisteException,
    usuarioNoEncontradoException,
    contrasenaIncorrectaException,
    credentialException,
)
# pyrefly: ignore [missing-import]
from fastapi.security import OAuth2PasswordRequestForm, OAuth2PasswordBearer
# pyrefly: ignore [missing-import]
from typing import Annotated
from jose import jwt
from datetime import datetime, timedelta, timezone
from jose import JWTError
import os
# pyrefly: ignore [missing-import]
from dotenv import load_dotenv

load_dotenv()

router = APIRouter(prefix="/auth", tags=["Auth"])

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

oauth2Bearer = OAuth2PasswordBearer(tokenUrl="auth/login")

SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = os.getenv("ALGORITHM")


def obtenerUsuarioActual(request: Annotated[str, Depends(oauth2Bearer)]):
    try:
        payload = jwt.decode(request, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("username")
        id: int = payload.get("id")
        admin: bool = payload.get("admin")
        if username is None or id is None or admin is None:
            raise credentialException
        return {"username": username, "id": id, "admin": admin}
    except JWTError:
        raise credentialException


dependenciaUsuario = Annotated[dict, Depends(obtenerUsuarioActual)]


def verificarCredenciales(username: str, password: str, db: dbDependency):
    usuario = db.query(Usuario).filter(Usuario.username == username).first()
    if not usuario:
        raise usuarioNoEncontradoException
    if not pwd_context.verify(password, usuario.hashed_password):
        raise contrasenaIncorrectaException
    return usuario


def crearTokenUsuario(usuario: Usuario, expiracion: timedelta):
    payload = {
        "username": usuario.username,
        "admin": usuario.admin,
        "id": usuario.id,
        "exp": datetime.utcnow() + expiracion
        # "exp": datetime.now(timezone.utc) + expiracion,
    }
    return jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)


@router.post("/registrar_usuario", status_code=status.HTTP_201_CREATED)
async def registrarUsuario(usuarioRequest: UsuarioRequest, db: dbDependency):
    existeUsuario = (
        db.query(Usuario).filter(Usuario.username == usuarioRequest.username).first()
    )
    if existeUsuario is not None:
        raise usuarioYaExisteException

    nuevoUsuario = Usuario(
        nombre=usuarioRequest.nombre,
        apellido=usuarioRequest.apellido,
        username=usuarioRequest.username,
        hashed_password=pwd_context.hash(usuarioRequest.password),
        admin=usuarioRequest.admin,
    )
    db.add(nuevoUsuario)
    db.commit()
    db.refresh(nuevoUsuario)
    return nuevoUsuario


@router.post("/login", status_code=status.HTTP_200_OK)
async def login(
    formData: Annotated[OAuth2PasswordRequestForm, Depends()], db: dbDependency
):
    usuario = verificarCredenciales(formData.username, formData.password, db)
    if usuario is None:
        raise usuarioNoEncontradoException
    token = crearTokenUsuario(
        usuario, timedelta(minutes=10)
    )  # <---------- checar el tiempo
    return {"access_token": token, "token_type": "bearer"}
