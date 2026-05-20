# pyrefly: ignore [missing-import]
from fastapi import APIRouter, status
# pyrefly: ignore [missing-import]
from database import dbDependency
from models import Material
from .auth import dependenciaUsuario
from exceptions import (
    usuarioNoEncontradoException,
    materialYaExisteException,
    materialNoEncontradoException,
    noAutorizadoException,
    constantePacaException,
)
# pyrefly: ignore [missing-import]
from requests import MaterialRequest, PrecioMaterialRequest, ConstantePacaRequest
# pyrefly: ignore [missing-import]
from responses import MaterialResponse

router = APIRouter(prefix="/material", tags=["Material"])


@router.get("/", status_code=status.HTTP_200_OK)
async def obtenerMateriales(db: dbDependency, usuario: dependenciaUsuario):
    if usuario is None:
        raise usuarioNoEncontradoException
    if not usuario.get("admin"):
        raise noAutorizadoException
    return db.query(Material).filter(Material.activo == True).all()


@router.get("/materiales", response_model=list[MaterialResponse], status_code=status.HTTP_200_OK)
async def materilaesParaCompraVenta(db: dbDependency, usuario: dependenciaUsuario):
    if usuario is None:
        raise usuarioNoEncontradoException
    return db.query(Material).filter(Material.activo == True).all()


@router.post("/nuevo-material", status_code=status.HTTP_201_CREATED)
async def crearMaterial(
    db: dbDependency, usuario: dependenciaUsuario, material: MaterialRequest
):
    if usuario is None:
        raise usuarioNoEncontradoException
    if not usuario.get("admin"):
        raise noAutorizadoException
    if db.query(Material).filter(Material.nombre == material.nombre, Material.activo == True).first():
        raise materialYaExisteException
    material = Material(**material.model_dump())
    db.add(material)
    db.commit()
    db.refresh(material)
    return material


@router.put("/precio/{id}", status_code=status.HTTP_200_OK, response_model=MaterialResponse)
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
    material = db.query(Material).filter(Material.id == id, Material.activo == True).first()
    if material is None:
        raise materialNoEncontradoException
    material.precio_compra = precio.precio_compra
    material.precio_venta = precio.precio_venta
    db.commit()
    db.refresh(material)
    return material

@router.put("/contante-paca/{id}", status_code=status.HTTP_200_OK)
async def actualizarConstantePaca(
    db: dbDependency,
    usuario: dependenciaUsuario,
    id: int,
    constante: ConstantePacaRequest
):
    if usuario is None:
        raise usuarioNoEncontradoException
    if not usuario.get("admin"):
        raise noAutorizadoException
    material = db.query(Material).filter(Material.id == id, Material.activo == True).first()
    if material is None:
        raise materialNoEncontradoException
    if material.constante_paca == constante.constante_paca:
        raise constantePacaException
    material.constante_paca = constante.constante_paca
    db.commit()
    db.refresh(material)
    return material


@router.delete("/{id}", status_code=status.HTTP_200_OK)
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
