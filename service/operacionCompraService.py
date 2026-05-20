from decimal import Decimal
from models import TransaccionCompra, Material, OperacionCompra
from requests import OperacionCompraRequest

def crearOperacionCompra(operacion: OperacionCompraRequest, transaccionCompra: TransaccionCompra, material: Material):
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
    return {
        "operacion": operacionCompra,
        "material": material,
        "transaccion": transaccionCompra
    }

