from fastapi import APIRouter, status
from database import dbDependency
from .auth import dependenciaUsuario
from exceptions import usuarioNoEncontradoException, noAutorizadoException
from models import TransaccionCompra
from requests import TransaccionCompraRequest


router = APIRouter(
    prefix="/transacciones-compras",
    tags=["transacciones-compras"],
)


@router.get("/")
def obtenerTransaccionesCompras(db: dbDependency, usuario: dependenciaUsuario):
    if usuario is None:
        raise usuarioNoEncontradoException
    if not usuario.get("admin"):
        raise noAutorizadoException
    return db.query(TransaccionCompra).all()


@router.post("/nueva-transaccion-compra", status_code=status.HTTP_201_CREATED)
async def nueva_transaccion_compra(
    db: dbDependency,
    usuario: dependenciaUsuario,
    transaccion: TransaccionCompraRequest,
):
    if usuario is None:
        raise usuarioNoEncontradoException
    transaccionCompra = TransaccionCompra(
        tipo_compra=transaccion.tipo_compra, id_usuario=usuario.get("id")
    )
    db.add(transaccionCompra)
    db.commit()
    db.refresh(transaccionCompra)
    return transaccionCompra
