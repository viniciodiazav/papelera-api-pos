# pyrefly: ignore [missing-import]
from fastapi import APIRouter
from database import dbDependency
from models import Material
from .auth import dependenciaUsuario
from exceptions import (
    usuarioNoEncontradoException,
    materialYaExisteException,
    materialNoEncontradoException,
    noAutorizadoException,
)
from requests import MaterialRequest, PrecioMaterialRequest
from responses import MaterialResponse

router = APIRouter(prefix="/material", tags=["Material"])


@router.get("/")
async def obtenerMateriales(db: dbDependency, usuario: dependenciaUsuario):
    if usuario is None:
        raise usuarioNoEncontradoException
    if not usuario.get("admin"):
        raise noAutorizadoException
    return db.query(Material).all()


@router.get("/materiales", response_model=list[MaterialResponse])
async def materilaesParaCompraVenta(db: dbDependency, usuario: dependenciaUsuario):
    if usuario is None:
        raise usuarioNoEncontradoException
    return db.query(Material).filter(Material.activo == True).all()


@router.post("/nuevo-material")
async def crearMaterial(
    db: dbDependency, usuario: dependenciaUsuario, material: MaterialRequest
):
    if usuario is None:
        raise usuarioNoEncontradoException
    if not usuario.get("admin"):
        raise noAutorizadoException
    if db.query(Material).filter(Material.nombre == material.nombre).first():
        raise materialYaExisteException
    material = Material(**material.model_dump())
    db.add(material)
    db.commit()
    db.refresh(material)
    return material


@router.put("/precio/{id}")
async def actualizarPrecioMaterial(
    db: dbDependency,
    usuario: dependenciaUsuario,
    id: int,
    precio: PrecioMaterialRequest,
):
    if usuario is None:
        raise usuarioNoEncontradoException
    if not usuario.get("admin"):
        raise noAutorizadoException
    material = db.query(Material).filter_by(id=id).first()
    if material is None:
        raise materialNoEncontradoException
    material.precio_compra = precio.precio_compra
    material.precio_venta = precio.precio_venta
    db.commit()
    db.refresh(material)
    return material


@router.delete("/{id}")
async def eliminarMaterial(db: dbDependency, usuario: dependenciaUsuario, id: int):
    if usuario is None:
        raise usuarioNoEncontradoException
    if not usuario.get("admin"):
        raise noAutorizadoException
    materialEliminar = db.query(Material).filter_by(id=id).first()
    if materialEliminar is None:
        raise materialNoEncontradoException
    materialEliminar.activo = False
    db.commit()
    db.refresh(materialEliminar)
    return {"mensaje": "Material eliminado correctamente"}
