# pyrefly: ignore [missing-import]
from pydantic import BaseModel, Field
from typing import Optional
from decimal import Decimal


class UsuarioRequest(BaseModel):
    nombre: str = Field(min_length=3, max_length=40)
    apellido: str = Field(min_length=3, max_length=40)
    username: str = Field(min_length=3, max_length=30)
    password: str = Field(min_length=8)
    admin: Optional[bool] = Field(default=False)

    model_config = {
        "json_schema_extra": {
            "example": {
                "nombre": "nombre",
                "apellido": "apellido",
                "username": "username",
                "password": "password",
            }
        }
    }


class ProveedorRequest(BaseModel):
    nombre: str = Field(min_length=3, max_length=150)
    contacto: str = Field(min_length=10, max_length=200)

    model_config = {
        "json_schema_extra": {
            "example": {
                "nombre": "proveedor",
                "contacto": "5512345678",
            }
        }
    }


class MaterialRequest(BaseModel):
    nombre: str = Field(min_length=3, max_length=100)
    unidad_medida: str = Field(min_length=1, max_length=15)
    precio_compra: Decimal = Field(gt=0)
    precio_venta: Decimal = Field(gt=0)
    constante_paca: Optional[Decimal] = Field(default=600.00)

    model_config = {
        "json_schema_extra": {
            "example": {
                "nombre": "carton",
                "unidad_medida": "kg",
                "precio_compra": 1,
                "precio_venta": 2,
                "constante_paca": 600,
            }
        }
    }


class PrecioMaterialRequest(BaseModel):
    precio_compra: Decimal = Field(gt=0)
    precio_venta: Decimal = Field(gt=0)

    model_config = {
        "json_schema_extra": {
            "example": {
                "precio_compra": 1,
                "precio_venta": 2,
            }
        }
    }

class ConstantePacaRequest(BaseModel):
    constante_paca: Decimal = Field(gt=0)

    model_config = {
        "json_schema_extra": {
            "example": {
                "constante_paca": 600,
            }
        }
    }

class ClienteRequest(BaseModel):
    nombre: str = Field(min_length=3, max_length=40)
    contacto: str = Field(min_length=10, max_length=200)
    direccion: str = Field(min_length=10, max_length=200)

    model_config = {
        "json_schema_extra": {
            "example": {
                "nombre": "cliente",
                "contacto": "5512345678",
                "direccion": "direccion",
            }
        }
    }


class OperacionCompraRequest(BaseModel):
    id_transaccion: int = Field(gt=0)    
    id_material: int = Field(gt=0)
    peso_bruto_kgs: Decimal = Field(gt=0)
    tara_kgs: Decimal = Field(gt=0)
    descuento: Optional[Decimal] = Field(default=0.00)
    descripcion_descuento: Optional[str] = Field(max_length=150, default=None)

    model_config = {
        "json_schema_extra": {
            "example": {
                "id_transaccion": 1,
                "id_material": 1,
                "peso_bruto_kgs": 1,
                "tara_kgs": 1,
                "descuento": 0,
                "descripcion_descuento": "no aplico",
            }
        }
    }


class TransaccionCompraRequest(BaseModel):
    tipo_compra: str = Field(min_length=1, max_length=10)

    model_config = {
        "json_schema_extra": {
            "example": {
                "tipo_compra": "mayoreo",
            }
        }
    }


class CompraMayoreoRequest(BaseModel):
    id_proveedor: int = Field(gt=0)
    id_transaccion: int = Field(gt=0)
    placas: str = Field(max_length=15)
    bascula: int = Field(default=0)
    observaciones: Optional[str] = Field(max_length=150, default=None)

    model_config = {
        "json_schema_extra": {
            "example": {
                "id_proveedor": 1,
                "id_transaccion": 1,
                "placas": "ABC-123",
                "bascula": 1,
            }
        }
    }


class CompraMenudeoRequest(BaseModel):
    id_transaccion: int = Field(gt=0)
    observaciones: Optional[str] = Field(max_length=150, default=None)

    model_config = {
        "json_schema_extra": {
            "example": {
                "id_transaccion": 1,
            }
        }
    }
