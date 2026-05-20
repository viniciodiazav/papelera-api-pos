# pyrefly: ignore [missing-import]
from fastapi import APIRouter, status
from database import dbDependency
from .auth import dependenciaUsuario
from exceptions import (
    usuarioNoEncontradoException,
    noAutorizadoException,
    transaccionNoEncontradaException,
    transaccionCerradaException,
)
from models import TransaccionCompra
from requests import TransaccionCompraRequest
from responses import IniciarTrasaccionCompraResponse


router = APIRouter(
    prefix="/transacciones-compras",
    tags=["transacciones-compras"],
)


@router.get("/")
def obtenerTransaccionesCompras(
    db: dbDependency, usuario: dependenciaUsuario, skip: int=0, limit: int=10
):
    if usuario is None:
        raise usuarioNoEncontradoException
    if not usuario.get("admin"):
        raise noAutorizadoException
    return db.query(TransaccionCompra).offset(skip).limit(limit).all()


@router.post("/nueva-transaccion-compra", status_code=status.HTTP_201_CREATED, response_model=IniciarTrasaccionCompraResponse)
async def nueva_transaccion_compra(
    db: dbDependency,
    usuario: dependenciaUsuario,
    transaccion: TransaccionCompraRequest,
):
    if usuario is None:
        raise usuarioNoEncontradoException
    transaccionCompra = TransaccionCompra(
        tipo_compra=transaccion.tipo_compra, id_usuario=usuario.get("id")
    )
    db.add(transaccionCompra)
    db.commit()
    db.refresh(transaccionCompra)
    return transaccionCompra


@router.put("/cerrar-transaccion/{idTransaccion}", status_code=status.HTTP_200_OK)
async def cerrar_transaccion_compra(
    db: dbDependency,
    usuario: dependenciaUsuario,
    idTransaccion: int,
):
    if usuario is None:
        raise usuarioNoEncontradoException
    transaccion = db.query(TransaccionCompra).filter_by(id=idTransaccion).first()
    if transaccion is None:
        raise transaccionNoEncontradaException
    if transaccion.cerrada:
        raise transaccionCerradaException
    transaccion.cerrada = True
    db.commit()
    db.refresh(transaccion)
    return {"mensaje": "Transaccion cerrada correctamente"}