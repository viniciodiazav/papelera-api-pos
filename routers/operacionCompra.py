# pyrefly: ignore [missing-import]
from fastapi import APIRouter, status
from database import dbDependency
from .auth import dependenciaUsuario
from exceptions import (
    usuarioNoEncontradoException,
    transaccionNoEncontradaException,
    materialNoEncontradoException,
    noAutorizadoException,
)
from models import OperacionCompra, TransaccionCompra, Material
from requests import OperacionCompraRequest
from decimal import Decimal

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

    pesoNeto = operacion.peso_bruto_kgs - operacion.tara_kgs
    descuentoKgs = Decimal("0.0")
    if operacion.descuento != Decimal("0.0"):
        descuentoKgs = pesoNeto * (operacion.descuento / Decimal("100.0"))
    kgsReales = pesoNeto - descuentoKgs

    operacionCompra = OperacionCompra(
        id_transaccion=operacion.id_transaccion,
        id_material=operacion.id_material,
        peso_bruto_kgs=operacion.peso_bruto_kgs,
        tara_kgs=operacion.tara_kgs,
        peso_neto_kgs=pesoNeto,
        descuento=operacion.descuento,
        descuento_kgs=descuentoKgs,
        descripcion_descuento=operacion.descripcion_descuento,
        kgs_reales=kgsReales,
        precio_unitario=material.precio_compra,
        tipo_compra=transaccionCompra.tipo_compra,
    )
    material.kgs_en_inventario += kgsReales
    material.pacas_estimadas = material.kgs_en_inventario / material.constante_paca
    transaccionCompra.monto += operacionCompra.kgs_reales * operacionCompra.precio_unitario
    db.add(operacionCompra)
    db.commit()
    db.refresh(operacionCompra)
    db.refresh(transaccionCompra)
    db.refresh(material)
    return operacionCompra


@router.get("/lista", status_code=status.HTTP_200_OK)
def obtenerOperacionesCompras(db: dbDependency, usuario: dependenciaUsuario):
    if usuario is None:
        raise usuarioNoEncontradoException
    if not usuario.get("admin"):
        raise noAutorizadoException
    return db.query(OperacionCompra).all()


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
def obtenerOperacionesComprasMayoreo(db: dbDependency, usuario: dependenciaUsuario):
    if usuario is None:
        raise usuarioNoEncontradoException
    if not usuario.get("admin"):
        raise noAutorizadoException
    return (
        db.query(OperacionCompra).filter(OperacionCompra.tipo_compra == "mayoreo").all()
    )


@router.get("/lista/menudeo", status_code=status.HTTP_200_OK)
def obtenerOperacionesComprasMenudeo(db: dbDependency, usuario: dependenciaUsuario):
    if usuario is None:
        raise usuarioNoEncontradoException
    if not usuario.get("admin"):
        raise noAutorizadoException
    return (
        db.query(OperacionCompra).filter(OperacionCompra.tipo_compra == "menudeo").all()
    )
