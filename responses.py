# pyrefly: ignore [missing-import]
from pydantic import BaseModel
# pyrefly: ignore [missing-import]
from typing import Optional
# pyrefly: ignore [missing-import]
from datetime import datetime


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

