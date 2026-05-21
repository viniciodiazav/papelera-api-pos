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
    transaccionNoCerradaException
)
from models import CompraMayoreo, CompraMenudeo, Proveedor, TransaccionCompra
from requests import CompraMayoreoRequest, CompraMenudeoRequest
from datetime import datetime
from responses import CompraMayoreoResponse, CompraMenudeoResponse, TodasLasComprasResponse

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

    if not transaccion.cerrada:
        raise transaccionNoCerradaException

    proveedor = db.query(Proveedor).filter(
        Proveedor.id == compraMayoreo.id_proveedor,
        Proveedor.activo == True
    ).first()
    if proveedor is None:
        raise proveedorNoEncontradoCompraException

    proveedor.concurrencia += 1
    compra = CompraMayoreo(
        id_proveedor=proveedor.id,
        id_usuario=transaccion.id_usuario,
        id_transaccion=transaccion.id,
        fecha=datetime.utcnow(),
        placas=compraMayoreo.placas,
        bascula=compraMayoreo.bascula,
        observaciones=compraMayoreo.observaciones,
    )
    db.add(compra)
    db.commit()
    db.refresh(compra)
    return {"mensaje": "Compra de mayoreo creada correctamente"}


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

    if not transaccion.cerrada:
        raise transaccionNoCerradaException


    compra = CompraMenudeo(
        id_usuario=transaccion.id_usuario,
        id_transaccion=compraMenudeo.id_transaccion,
        fecha=datetime.utcnow(),
    )
    db.add(compra)
    db.commit()
    db.refresh(compra)
    return {"mensaje": "Compra de menudeo creada correctamente"}


@router.get("/admin/todas-las-compras", status_code=status.HTTP_200_OK, response_model=TodasLasComprasResponse)
def obtenerCompras(
    db: dbDependency, 
    usuario: dependenciaUsuario, 
    limit: int = 5,
    skip: int = 0,
):
    if usuario is None:
        raise usuarioNoEncontradoException
    if not usuario.get("admin"):
        raise noAutorizadoException
    compras_mayoreo = db.query(CompraMayoreo).offset(skip).limit(limit).all()
    compras_menudeo = db.query(CompraMenudeo).offset(skip).limit(limit).all()
    return {"compras_mayoreo": compras_mayoreo, "compras_menudeo": compras_menudeo}


@router.get("/admin/compras-mayoreo", status_code=status.HTTP_200_OK, response_model=list[CompraMayoreoResponse])
def obtenerComprasMayoreo(
    db: dbDependency, 
    usuario: dependenciaUsuario, 
    limit: int = 10,
    skip: int = 0,
):
    if usuario is None:
        raise usuarioNoEncontradoException
    if not usuario.get("admin"):
        raise noAutorizadoException
    return db.query(CompraMayoreo).offset(skip).limit(limit).all()


@router.get("/admin/compras-menudeo", status_code=status.HTTP_200_OK, response_model=list[CompraMenudeoResponse])
def obtenerComprasMenudeo(
    db: dbDependency, 
    usuario: dependenciaUsuario, 
    limit: int = 10,
    skip: int = 0,
):
    if usuario is None:
        raise usuarioNoEncontradoException
    if not usuario.get("admin"):
        raise noAutorizadoException
    return db.query(CompraMenudeo).offset(skip).limit(limit).all()
