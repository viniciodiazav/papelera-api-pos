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
from responses import IniciarTransaccionCompraResponse, TransaccionCompraAdminResponse


router = APIRouter(
    prefix="/transacciones-compras",
    tags=["transacciones-compras"],
)


@router.get("/admin/lista-transacciones-compras", 
    status_code=status.HTTP_200_OK, 
    response_model=list[TransaccionCompraAdminResponse]
)
def obtenerTransaccionesCompras(
    db: dbDependency,
    usuario: dependenciaUsuario,
    skip: int=0,
    limit: int=10
):
    if usuario is None:
        raise usuarioNoEncontradoException
    if not usuario.get("admin"):
        raise noAutorizadoException
    return db.query(TransaccionCompra).offset(skip).limit(limit).all()


@router.post("/nueva-transaccion-compra-mayoreo", 
    status_code=status.HTTP_201_CREATED, 
    response_model=IniciarTransaccionCompraResponse
)
async def nuevaTransaccionCompraMayoreo(
    db: dbDependency,
    usuario: dependenciaUsuario,
):
    if usuario is None:
        raise usuarioNoEncontradoException
    transaccionCompra = TransaccionCompra(
        tipo_compra="mayoreo",
        id_usuario=usuario.get("id")
    )
    db.add(transaccionCompra)
    db.commit()
    db.refresh(transaccionCompra)
    return transaccionCompra


@router.post("/nueva-transaccion-compra-menudeo", 
    status_code=status.HTTP_201_CREATED, 
    response_model=IniciarTransaccionCompraResponse
)
async def nuevaTransaccionCompraMenudeo(
    db: dbDependency,
    usuario: dependenciaUsuario,
):
    if usuario is None:
        raise usuarioNoEncontradoException
    transaccionCompra = TransaccionCompra(
        tipo_compra="menudeo",
        id_usuario=usuario.get("id")
    )
    db.add(transaccionCompra)
    db.commit()
    db.refresh(transaccionCompra)
    return transaccionCompra

@router.put("/cerrar-transaccion/{idTransaccion}", status_code=status.HTTP_200_OK)
async def cerrarTransaccionCompra(
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