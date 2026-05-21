# pyrefly: ignore [missing-import]
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

class IniciarTrasaccionCompraResponse(BaseModel):
    id: int
    id_usuario: int
    tipo_compra: str

    model_config = {
        "from_attributes": True
    }

class OperacionCompraRepsonse(BaseModel):
    id: int
    peso_bruto_kgs: int
    id_transaccion: int
    id_material: int
    peso_neto_kgs: int
    descripcion_descuento: str
    kgs_reales: int
    tipo_compra: str
    tara_kgs: int
    descuento: int
    descuento_kgs: int
    precio_unitario: int

    model_config = {
        "from_attributes": True
    }

class CompraMayoreoReponse(BaseModel):
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
    compras_mayoreo: list[CompraMayoreoReponse]
    compras_menudeo: list[CompraMenudeoResponse]