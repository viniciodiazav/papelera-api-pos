# pyrefly: ignore [missing-import]
from fastapi import APIRouter, status
from database import dbDependency
from .auth import dependenciaUsuario
from exceptions import (
    usuarioNoEncontradoException,
    transaccionYaExisteException,
    proveedorNoEncontradoCompraException,
    transaccionNoEncontradaException,
    noAutorizadoException,
)
from models import CompraMayoreo, CompraMenudeo, Proveedor, TransaccionCompra
from requests import CompraMayoreoRequest, CompraMenudeoRequest
from datetime import datetime

router = APIRouter(
    prefix="/compras",
    tags=["compras"],
)


@router.post("/nueva-compra-mayoreo", status_code=status.HTTP_201_CREATED)
async def nuevaCompraMayoreo(
    db: dbDependency,
    usuario: dependenciaUsuario,
    compraMayoreo: CompraMayoreoRequest,
):
    if usuario is None:
        raise usuarioNoEncontradoException
    if (
        db.query(CompraMayoreo).filter_by(id_transaccion=compraMayoreo.id_transaccion).first()
        is not None
        or db.query(CompraMenudeo).filter_by(id_transaccion=compraMayoreo.id_transaccion).first()
        is not None
    ):
        raise transaccionYaExisteException

    transaccion = db.query(TransaccionCompra).filter_by(id=compraMayoreo.id_transaccion).first()
    if transaccion is None or transaccion.tipo_compra != "mayoreo":
        raise transaccionNoEncontradaException

    if db.query(Proveedor).filter_by(id=compraMayoreo.id_proveedor).first() is None:
        raise proveedorNoEncontradoCompraException
    compra = CompraMayoreo(
        id_proveedor=compraMayoreo.id_proveedor,
        id_usuario=transaccion.id_usuario,
        id_transaccion=compraMayoreo.id_transaccion,
        fecha=datetime.utcnow(),
        placas=compraMayoreo.placas,
        bascula=compraMayoreo.bascula,
        observaciones=compraMayoreo.observaciones,
    )
    db.add(compra)
    db.commit()
    db.refresh(compra)
    return compra


@router.post("/nueva-compra-menudeo", status_code=status.HTTP_201_CREATED)
async def nuevaCompraMenudeo(
    db: dbDependency,
    usuario: dependenciaUsuario,
    compraMenudeo: CompraMenudeoRequest,
):
    if usuario is None:
        raise usuarioNoEncontradoException
    if (
        db.query(CompraMayoreo).filter_by(id_transaccion=compraMenudeo.id_transaccion).first()
        is not None
        or db.query(CompraMenudeo).filter_by(id_transaccion=compraMenudeo.id_transaccion).first()
        is not None
    ):
        raise transaccionYaExisteException

    transaccion = db.query(TransaccionCompra).filter_by(id=compraMenudeo.id_transaccion).first()
    if transaccion is None or transaccion.tipo_compra != "menudeo":
        raise transaccionNoEncontradaException

    compra = CompraMenudeo(
        id_usuario=transaccion.id_usuario,
        id_transaccion=compraMenudeo.id_transaccion,
        fecha=datetime.utcnow(),
    )
    db.add(compra)
    db.commit()
    db.refresh(compra)
    return compra


@router.get("/todas-las-compras", status_code=status.HTTP_200_OK)
def obtenerCompras(db: dbDependency, usuario: dependenciaUsuario):
    if usuario is None:
        raise usuarioNoEncontradoException
    if not usuario.get("admin"):
        raise noAutorizadoException
    compras_mayoreo = db.query(CompraMayoreo).all()
    compras_menudeo = db.query(CompraMenudeo).all()
    return {"compras_mayoreo": compras_mayoreo, "compras_menudeo": compras_menudeo}


@router.get("/compras-mayoreo", status_code=status.HTTP_200_OK)
def obtenerComprasMayoreo(db: dbDependency, usuario: dependenciaUsuario):
    if usuario is None:
        raise usuarioNoEncontradoException
    if not usuario.get("admin"):
        raise noAutorizadoException
    return db.query(CompraMayoreo).all()


@router.get("/compras-menudeo", status_code=status.HTTP_200_OK)
def obtenerComprasMenudeo(db: dbDependency, usuario: dependenciaUsuario):
    if usuario is None:
        raise usuarioNoEncontradoException
    if not usuario.get("admin"):
        raise noAutorizadoException
    return db.query(CompraMenudeo).all()
