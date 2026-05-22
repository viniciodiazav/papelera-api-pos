# pyrefly: ignore [missing-import]
from fastapi import APIRouter, status
import uuid
from database import dbDependency
from .auth import dependenciaUsuario
from models import Paca, Articulo, Usuario, Material
from exceptions import usuarioNoEncontradoException, noAutorizadoException, materialNoEncontradoException, materialInsuficienteException
from requests import PacaRequest
from responses import PacaResponse
from service.pacasService import validarCantidadPacas
router = APIRouter(prefix="/pacas", tags=["Pacas"])

@router.post("/crear", response_model=PacaResponse, status_code=status.HTTP_201_CREATED)
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

    for paca in pacas:
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