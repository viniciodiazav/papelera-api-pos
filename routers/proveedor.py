# pyrefly: ignore [missing-import]
from fastapi import APIRouter
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

router = APIRouter(prefix="/proveedor", tags=["Proveedor"])


@router.get("/")
def obtener_proveedores(db: dbDependency, usuario: dependenciaUsuario):
    if usuario is None:
        raise usuarioNoEncontradoException
    return db.query(Proveedor).all()


@router.post("/nuevo-proveedor")
def crear_proveedor(
    db: dbDependency, usuario: dependenciaUsuario, proveedor: ProveedorRequest
):
    if usuario is None:
        raise usuarioNoEncontradoException
    if db.query(Proveedor).filter(Proveedor.nombre == proveedor.nombre).first():
        raise proveedorYaExisteException
    if db.query(Proveedor).filter(Proveedor.contacto == proveedor.contacto).first():
        raise contactoYaExisteException
    proveedor = Proveedor(**proveedor.model_dump())
    db.add(proveedor)
    db.commit()
    db.refresh(proveedor)
    return proveedor


@router.put("/{id}")
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
        .filter(Proveedor.nombre == proveedor.nombre, Proveedor.id != id)
        .first()
    ):
        raise proveedorYaExisteException
    if (
        db.query(Proveedor)
        .filter(Proveedor.contacto == proveedor.contacto, Proveedor.id != id)
        .first()
    ):
        raise contactoYaExisteException
    proveedorEditar.nombre = proveedor.nombre
    proveedorEditar.contacto = proveedor.contacto
    db.commit()
    db.refresh(proveedorEditar)
    return proveedorEditar


@router.delete("/{id}")
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
