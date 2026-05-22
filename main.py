# pyrefly: ignore [missing-import]
from fastapi import FastAPI
from database import engine, Base
from routers import (
    auth,
    proveedor,
    material,
    cliente,
    transaccionCompra,
    operacionCompra,
    compra,
    transaccionVenta,
    usuarios,
    pacas,
)

app = FastAPI()

app.include_router(auth.router)
app.include_router(usuarios.router)
app.include_router(proveedor.router)
app.include_router(material.router)
app.include_router(cliente.router)
app.include_router(transaccionCompra.router)
app.include_router(operacionCompra.router)
app.include_router(compra.router)
app.include_router(transaccionVenta.router)
app.include_router(pacas.router)

Base.metadata.create_all(bind=engine)
