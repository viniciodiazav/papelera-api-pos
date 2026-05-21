# pyrefly: ignore [missing-import]
from decimal import Decimal
from pydantic import BaseModel
# pyrefly: ignore [missing-import]
from typing import Optional
# pyrefly: ignore [missing-import]
from datetime import datetime
from models import CompraMayoreo, CompraMenudeo


class UsuarioResponse(BaseModel):
    id: int
    nombre: str
    apellido: str
    username: str
    admin: bool

    model_config = {
        "from_attributes": True
    }

class MaterialesAdminResponse(BaseModel):
    id: int
    nombre: str
    unidad_medida: str
    precio_compra: Decimal
    precio_venta: Decimal
    kgs_en_inventario: Decimal
    constante_paca: int
    pacas_estimadas: Decimal

    model_config = {
        "from_attributes": True
    }
    

class MaterialResponse(BaseModel):
    id: int
    nombre: str
    constante_paca: int
    precio_compra: float
    precio_venta: float

    model_config = {
        "from_attributes": True
    }

class ProveedorResponse(BaseModel):
    id: int
    nombre: str
    contacto: str
    
    model_config = {
        "from_attributes": True
    }

class ClienteResponse(BaseModel):
    id: int
    nombre: str
    contacto: str
    direccion: str

    model_config = {
        "from_attributes": True
    }

class TransaccionCompraAdminResponse(BaseModel):
    id: int
    id_usuario: int
    monto: Decimal
    tipo_pago: str
    observaciones: str
    tipo_compra: str
    cerrada: bool
    
    model_config = {
        "from_attributes": True
    }

class IniciarTransaccionCompraResponse(BaseModel):
    id: int
    id_usuario: int
    tipo_compra: str

    model_config = {
        "from_attributes": True
    }

class OperacionCompraAdminResponse(BaseModel):
    id: int
    id_transaccion: int
    id_material: int
    peso_bruto_kgs: Decimal
    tara_kgs: Decimal
    peso_neto_kgs: Decimal
    descuento: Decimal
    descripcion_descuento: str
    descuento_kgs: Decimal
    kgs_reales: Decimal
    precio_unitario: Decimal
    tipo_compra: str

    model_config = {
        "from_attributes": True
    }

class CompraMayoreoResponse(BaseModel):
    id: int
    id_proveedor: int
    id_transaccion: int
    placas: str
    bascula: int
    observaciones: str
    fecha: datetime

    model_config = {
        "from_attributes": True
    }

class CompraMenudeoResponse(BaseModel):
    id: int
    id_transaccion: int
    observaciones: str
    fecha: datetime

    model_config = {
        "from_attributes": True
    }

class TodasLasComprasResponse(BaseModel):
    compras_mayoreo: list[CompraMayoreoResponse]
    compras_menudeo: list[CompraMenudeoResponse]

class TransaccionVentaAdminResponse(BaseModel):
    id: int
    id_usuario: int
    monto: Decimal
    tipo_cobro: str
    observaciones: str
    cerrada: bool
    
    model_config = {
        "from_attributes": True
    }

class IniciarTransaccionVentaResponse(BaseModel):
    id: int
    id_usuario: int

    model_config = {
        "from_attributes": True
    }