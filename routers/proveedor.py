# pyrefly: ignore [missing-import]
from fastapi import APIRouter, status
from database import dbDependency
from models import Proveedor
from .auth import dependenciaUsuario
from exceptions import (
    usuarioNoEncontradoException,
    proveedorYaExisteException,
    contactoYaExisteException,
    proveedorNoEncontradoException,
    noAutorizadoException,
)
from requests import ProveedorRequest
from responses import ProveedorResponse

router = APIRouter(prefix="/proveedor", tags=["Proveedor"])


@router.get("/proveedores", response_model=list[ProveedorResponse], status_code=status.HTTP_200_OK)
def obtener_proveedores(db: dbDependency, usuario: dependenciaUsuario):
    if usuario is None:
        raise usuarioNoEncontradoException
    return db.query(Proveedor).filter(Proveedor.activo == True).all()


@router.post("/nuevo-proveedor", status_code=status.HTTP_201_CREATED, response_model=ProveedorResponse)
def crear_proveedor(
    db: dbDependency, usuario: dependenciaUsuario, proveedor: ProveedorRequest
):
    if usuario is None:
        raise usuarioNoEncontradoException
    if db.query(Proveedor).filter(Proveedor.nombre == proveedor.nombre, Proveedor.activo == True).first():
        raise proveedorYaExisteException
    if db.query(Proveedor).filter(Proveedor.contacto == proveedor.contacto, Proveedor.activo == True).first():
        raise contactoYaExisteException
    proveedor = Proveedor(**proveedor.model_dump())
    db.add(proveedor)
    db.commit()
    db.refresh(proveedor)
    return proveedor


@router.put("/admin/{id}", status_code=status.HTTP_200_OK, response_model=ProveedorResponse)
def actualizar_proveedor(
    db: dbDependency, usuario: dependenciaUsuario, id: int, proveedor: ProveedorRequest
):
    if usuario is None:
        raise usuarioNoEncontradoException
    if not usuario.get("admin"):
        raise noAutorizadoException
    proveedorEditar = db.query(Proveedor).filter_by(id=id).first()
    if proveedorEditar is None:
        raise proveedorNoEncontradoException
    if (
        db.query(Proveedor)
        .filter(Proveedor.nombre == proveedor.nombre, Proveedor.id != id, Proveedor.activo == True)
        .first()
    ):
        raise proveedorYaExisteException
    if (
        db.query(Proveedor)
        .filter(Proveedor.contacto == proveedor.contacto, Proveedor.id != id, Proveedor.activo == True)
        .first()
    ):
        raise contactoYaExisteException
    proveedorEditar.nombre = proveedor.nombre
    proveedorEditar.contacto = proveedor.contacto
    db.commit()
    db.refresh(proveedorEditar)
    return proveedorEditar


@router.delete("/admin/{id}", status_code=status.HTTP_200_OK)
def eliminar_proveedor(db: dbDependency, usuario: dependenciaUsuario, id: int):
    if usuario is None:
        raise usuarioNoEncontradoException
    if not usuario.get("admin"):
        raise noAutorizadoException
    proveedorEliminar = db.query(Proveedor).filter_by(id=id).first()
    if proveedorEliminar is None:
        raise proveedorNoEncontradoException
    proveedorEliminar.activo = False
    db.commit()
    db.refresh(proveedorEliminar)
    return {"mensaje": "Proveedor eliminado correctamente"}
