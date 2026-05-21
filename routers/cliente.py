# pyrefly: ignore [missing-import]
from fastapi import APIRouter, status
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
from responses import ClienteResponse

router = APIRouter(
    prefix="/cliente",
    tags=["Cliente"]
)


@router.get("/lista-clientes", response_model=list[ClienteResponse], status_code=status.HTTP_200_OK)
def obtener_clientes(
        db: dbDependency,
        usuario: dependenciaUsuario,
        skip: int = 0,
        limit: int = 10
    ):
    if usuario is None:
        raise usuarioNoEncontradoException
    return db.query(Cliente).filter(Cliente.activo == True).offset(skip).limit(limit).all()


@router.post("/nuevo-cliente", status_code=status.HTTP_201_CREATED, response_model=ClienteResponse)
def crear_cliente(
    db: dbDependency, usuario: dependenciaUsuario, cliente: ClienteRequest
):
    if usuario is None:
        raise usuarioNoEncontradoException
    if db.query(Cliente).filter(Cliente.contacto == cliente.contacto).first() is not None:
        raise contactoYaExisteException
    cliente = Cliente(**cliente.model_dump())
    db.add(cliente)
    db.commit()
    db.refresh(cliente)
    return cliente


@router.put("/admin/{id}", response_model=ClienteResponse, status_code=status.HTTP_200_OK)
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


@router.delete("/admin/{id}", status_code=status.HTTP_200_OK)
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
