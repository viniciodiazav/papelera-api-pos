# pyrefly: ignore [missing-import]
from fastapi import APIRouter, status
from database import dbDependency
from .auth import dependenciaUsuario
from exceptions import (
    usuarioNoEncontradoException,
    transaccionNoEncontradaException,
    materialNoEncontradoException,
    noAutorizadoException,
    transaccionCerradaException
)
from models import OperacionCompra, TransaccionCompra, Material
from requests import OperacionCompraRequest
from service.operacionCompraService import crearOperacionCompra

router = APIRouter(
    prefix="/operaciones-compras",
    tags=["operaciones-compras"],
)


@router.post("/nueva-operacion", status_code=status.HTTP_201_CREATED)
async def nuevaOperacionCompra(
    db: dbDependency,
    usuario: dependenciaUsuario,
    operacion: OperacionCompraRequest,
):
    if usuario is None:
        raise usuarioNoEncontradoException
    transaccionCompra = db.query(TransaccionCompra).filter_by(id=operacion.id_transaccion).first()
    if transaccionCompra is None:
        raise transaccionNoEncontradaException
    material = db.query(Material).filter_by(id=operacion.id_material).first()
    if material is None:
        raise materialNoEncontradoException
    if transaccionCompra.cerrada:
        raise transaccionCerradaException

    operaciones = crearOperacionCompra(
        operacion=operacion,
        transaccionCompra=transaccionCompra,
        material=material
    )
    db.commit()
    db.refresh(operaciones["operacion"])
    db.refresh(operaciones["transaccion"])
    db.refresh(operaciones["material"])
    return {"mensaje": "Operacion de compra creada correctamente"}


@router.get("/lista", status_code=status.HTTP_200_OK)
def obtenerOperacionesCompras(
    db: dbDependency, 
    usuario: dependenciaUsuario, 
    skip: int = 0, 
    limit: int = 10
):
    if usuario is None:
        raise usuarioNoEncontradoException
    if not usuario.get("admin"):
        raise noAutorizadoException
    return db.query(OperacionCompra).offset(skip).limit(limit).all()


@router.get("/lista/{idTransaccion}", status_code=status.HTTP_200_OK)
def obtenerOperacionesComprasFiltradas(
    db: dbDependency,
    usuario: dependenciaUsuario,
    idTransaccion: int,
):
    if usuario is None:
        raise usuarioNoEncontradoException
    if not usuario.get("admin"):
        raise noAutorizadoException
    return db.query(OperacionCompra).filter_by(id_transaccion=idTransaccion).all()


@router.get("/lista/mayoreo", status_code=status.HTTP_200_OK)
def obtenerOperacionesComprasMayoreo(
    db: dbDependency,
    usuario: dependenciaUsuario,
    skip: int = 0,
    limit: int = 10,
):
    if usuario is None:
        raise usuarioNoEncontradoException
    if not usuario.get("admin"):
        raise noAutorizadoException
    return (
        db.query(OperacionCompra)
        .filter(OperacionCompra.tipo_compra == "mayoreo")
        .offset(skip)
        .limit(limit)
        .all()
    )


@router.get("/lista/menudeo", status_code=status.HTTP_200_OK)
def obtenerOperacionesComprasMenudeo(
    db: dbDependency, 
    usuario: dependenciaUsuario, 
    skip: int = 0, 
    limit: int = 10
):
    if usuario is None:
        raise usuarioNoEncontradoException
    if not usuario.get("admin"):
        raise noAutorizadoException
    return (
        db.query(OperacionCompra)
        .filter(OperacionCompra.tipo_compra == "menudeo")
        .offset(skip)
        .limit(limit)
        .all()
    )
