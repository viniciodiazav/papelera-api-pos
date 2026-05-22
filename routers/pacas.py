# pyrefly: ignore [missing-import]
from fastapi import APIRouter, status
import uuid
from database import dbDependency
from .auth import dependenciaUsuario
from models import Paca, Material
from exceptions import usuarioNoEncontradoException, noAutorizadoException, materialNoEncontradoException, materialInsuficienteException
from requests import PacaRequest
from responses import PacaAdminResponse
from service.pacasService import validarCantidadPacas
router = APIRouter(prefix="/pacas", tags=["Pacas"])

@router.post("/guardar", status_code=status.HTTP_201_CREATED)
async def crearPaca(
    db: dbDependency, 
    usuario: dependenciaUsuario,
    pacas: PacaRequest 
):
    if usuario is None:
        raise usuarioNoEncontradoException
    
    material = db.query(Material).filter(Material.activo == True, Material.id == pacas.id_material).first()
    if material is None:
        raise materialNoEncontradoException

    validacion = validarCantidadPacas(db, material, pacas.cantidad_pacas)
    if not validacion:
        raise materialInsuficienteException

    for i in range(0, pacas.cantidad_pacas):
        id_unico = str(uuid.uuid4())
        paca = Paca(
            id_material = material.id,
            peso_estimado = material.constante_paca,
            codigo = id_unico
        )
        db.add(paca)
        db.commit()
        db.refresh(paca)

    return {f"mensaje":f"Se guardaron {len(pacas)} pacas de {material.nombre} exitosamente"}    

@router.get("/admin/obtener-pacas", response_model=list[PacaAdminResponse], status_code=status.HTTP_200_OK)
async def obtenerPacas(
    db: dbDependency, 
    usuario: dependenciaUsuario,
    skip: int = 0, 
    limit: int = 10
):
    if usuario is None:
        raise usuarioNoEncontradoException
    if not usuario.get("admin"):
        raise noAutorizadoException
    return db.query(Paca).filter(Paca.en_inventario == True).offset(skip).limit(limit).all()

@router.get("/obtener-pacas-filtar-por-material/{id}", response_model=list[PacaAdminResponse], status_code=status.HTTP_200_OK)
async def obtenerPacasFiltrarPorMaterial(db: dbDependency, usuario: dependenciaUsuario, id: int):
    if usuario is None:
        raise usuarioNoEncontradoException
    if not usuario.get("admin"):
        raise noAutorizadoException
    if db.query(Material).filter(Material.id == id, Material.activo == True).first() is None:
        raise materialNoEncontradoException
    return db.query(Paca).filter(Paca.en_inventario == True, Paca.id_material == id).all()
