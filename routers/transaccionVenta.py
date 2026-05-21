# pyrefly: ignore [missing-import]
from fastapi import APIRouter, status
from database import dbDependency
from .auth import dependenciaUsuario
from models import TransaccionVenta
from responses import TransaccionVentaAdminResponse, IniciarTransaccionVentaResponse
from exceptions import (
    usuarioNoEncontradoException,
    noAutorizadoException,
    transaccionNoEncontradaException,
    transaccionCerradaException,
)


router = APIRouter(
    prefix="/transacciones-venta",
    tags=["transacciones-venta"],
)

@router.get("/admin/lista-transacciones-ventas", 
    status_code=status.HTTP_200_OK, 
    response_model=list[TransaccionVentaAdminResponse]
)
def obtenerTransaccionesVentas(
    db: dbDependency,
    usuario: dependenciaUsuario,
    skip: int=0,
    limit: int=10
):
    if usuario is None:
        raise usuarioNoEncontradoException
    if not usuario.get("admin"):
        raise noAutorizadoException
    return db.query(TransaccionVenta).offset(skip).limit(limit).all()

@router.post("/nueva-transaccion-venta", 
    status_code=status.HTTP_201_CREATED, 
    response_model=IniciarTransaccionVentaResponse
)
async def nuevaTransaccionVenta(
    db: dbDependency,
    usuario: dependenciaUsuario,
):
    if usuario is None:
        raise usuarioNoEncontradoException
    transaccionVenta = TransaccionVenta(
        id_usuario=usuario.get("id")
    )
    db.add(transaccionVenta)
    db.commit()
    db.refresh(transaccionVenta)
    return transaccionVenta

@router.put("/cerrar-transaccion-venta/{id_transaccion_venta}", status_code=status.HTTP_200_OK)
async def cerrarTransaccionVenta(
    db: dbDependency,
    usuario: dependenciaUsuario,
    id_transaccion_venta: int
):
    if usuario is None:
        raise usuarioNoEncontradoException
    transaccionVenta = db.query(TransaccionVenta).filter(TransaccionVenta.id == id_transaccion_venta).first()
    if transaccionVenta is None:
        raise transaccionNoEncontradaException
    if transaccionVenta.cerrada:
        raise transaccionCerradaException
    transaccionVenta.cerrada = True
    db.commit()
    db.refresh(transaccionVenta)
    return {"message": "Transaccion cerrada exitosamente"}