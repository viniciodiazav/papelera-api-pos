# pyrefly: ignore [missing-import]
from fastapi import APIRouter
from database import dbDependency
from models import Cliente
from .auth import dependenciaUsuario
from exceptions import (
    usuarioNoEncontradoException,
    contactoYaExisteException,
    clienteNoEncontradoException,
    noAutorizadoException,
)
from requests import ClienteRequest

router = APIRouter(prefix="/cliente", tags=["Cliente"])


@router.get("/")
def obtener_clientes(db: dbDependency, usuario: dependenciaUsuario):
    if usuario is None:
        raise usuarioNoEncontradoException
    return db.query(Cliente).all()


@router.post("/nuevo-cliente")
def crear_cliente(
    db: dbDependency, usuario: dependenciaUsuario, cliente: ClienteRequest
):
    if usuario is None:
        raise usuarioNoEncontradoException
    if db.query(Cliente).filter(Cliente.contacto == cliente.contacto).first():
        raise contactoYaExisteException
    cliente = Cliente(**cliente.model_dump())
    db.add(cliente)
    db.commit()
    db.refresh(cliente)
    return cliente


@router.put("/{id}")
def actualizar_cliente(
    db: dbDependency,
    usuario: dependenciaUsuario,
    id: int,
    cliente: ClienteRequest,
):
    if usuario is None:
        raise usuarioNoEncontradoException
    if not usuario.get("admin"):
        raise noAutorizadoException
    if (
        db.query(Cliente)
        .filter(Cliente.contacto == cliente.contacto, Cliente.id != id)
        .first()
    ):
        raise contactoYaExisteException
    clienteActualizar = db.query(Cliente).filter_by(id=id).first()
    if clienteActualizar is None:
        raise clienteNoEncontradoException
    clienteActualizar.nombre = cliente.nombre
    clienteActualizar.contacto = cliente.contacto
    clienteActualizar.direccion = cliente.direccion
    db.commit()
    db.refresh(clienteActualizar)
    return clienteActualizar


@router.delete("/{id}")
def eliminar_cliente(db: dbDependency, usuario: dependenciaUsuario, id: int):
    if usuario is None:
        raise usuarioNoEncontradoException
    if not usuario.get("admin"):
        raise noAutorizadoException
    clienteEliminar = db.query(Cliente).filter_by(id=id).first()
    if clienteEliminar is None:
        raise clienteNoEncontradoException
    clienteEliminar.activo = False
    db.commit()
    db.refresh(clienteEliminar)
    return {"mensaje": "Cliente eliminado correctamente"}
