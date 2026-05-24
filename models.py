from database import Base
# pyrefly: ignore [missing-import]
from sqlalchemy import (
    Column,
    Integer,
    String,
    Boolean,
    ForeignKey,
    Numeric,
    TIMESTAMP,
)
# pyrefly: ignore [missing-import]
from sqlalchemy.orm import relationship


class Usuario(Base):
    __tablename__ = "usuarios"

    id = Column(Integer, primary_key=True, index=True)
    nombre = Column(String(40), nullable=False)
    apellido = Column(String(40), nullable=False)
    username = Column(String(30), nullable=False, unique=True, index=True)
    hashed_password = Column(String, nullable=False)
    admin = Column(Boolean, default=False)
    activo = Column(Boolean, nullable=False, default=True)


class Material(Base):
    __tablename__ = "materiales"

    id = Column(Integer, primary_key=True, index=True)
    nombre = Column(String(40), nullable=False, unique=True)
    unidad_medida = Column(String(15), nullable=False)
    precio_compra = Column(Numeric(10, 2), nullable=False)
    precio_venta = Column(Numeric(10, 2), nullable=False)
    kgs_en_inventario = Column(Numeric(10, 2), nullable=False, default=0.00)
    estimado_kg_pacas = Column(Numeric(10,2), nullable=False, default=0.00)
    constante_paca = Column(Numeric(10, 2), nullable=False, default=600.00)
    pacas_estimadas = Column(Numeric(10, 2), nullable=False, default=0.00)
    pacas_reales = Column(Integer, nullable=False, default=0)
    activo = Column(Boolean, nullable=False, default=True)


class Paca(Base):
    __tablename__ = "pacas"

    id = Column(Integer, primary_key=True, index=True)
    id_material = Column(Integer, ForeignKey("materiales.id"), nullable=False)
    peso_estimado = Column(Numeric(10, 2), nullable=False)
    codigo = Column(String(200), nullable=False, unique=True)
    en_inventario = Column(Boolean, nullable=False, default=True)


class Proveedor(Base):
    __tablename__ = "proveedores"

    id = Column(Integer, primary_key=True, index=True)
    nombre = Column(String(150), nullable=False)
    contacto = Column(String(200), nullable=True, unique=True)
    concurrencia = Column(Integer, nullable=False, default=0)
    activo = Column(Boolean, nullable=False, default=True)


class Cliente(Base):
    __tablename__ = "clientes"

    id = Column(Integer, primary_key=True, index=True)
    nombre = Column(String(100), nullable=False)
    contacto = Column(String(200), nullable=False)
    direccion = Column(String(200), nullable=False)
    concurrencia = Column(Integer, nullable=False, default=0)
    activo = Column(Boolean, nullable=False, default=True)


class TransaccionCompra(Base):
    __tablename__ = "transacciones_compras"

    id = Column(Integer, primary_key=True, index=True)
    id_usuario = Column(Integer, ForeignKey("usuarios.id"), nullable=False)
    monto = Column(Numeric(10, 2), nullable=False, default=0.00)
    tipo_pago = Column(String(30), nullable=True, default=None)
    observaciones = Column(String(150), nullable=True, default=None)
    tipo_compra = Column(String(30), nullable=False, default="mayoreo")
    cerrada = Column(Boolean, nullable=False, default=False)

    operaciones = relationship(
        "OperacionCompra", back_populates="transaccion", cascade="all, delete-orphan"
    )


class OperacionCompra(Base):
    __tablename__ = "operaciones_compras"

    id = Column(Integer, primary_key=True, index=True)
    id_transaccion = Column(
        Integer, ForeignKey("transacciones_compras.id"), nullable=False
    )
    id_material = Column(Integer, ForeignKey("materiales.id"), nullable=False)
    peso_bruto_kgs = Column(Numeric(10, 2), nullable=False)
    tara_kgs = Column(Numeric(10, 2), nullable=True, default=0.00)
    peso_neto_kgs = Column(Numeric(10, 2), nullable=False)
    descuento = Column(Numeric(10, 2), nullable=True, default=0.00)
    descripcion_descuento = Column(String(150), nullable=True, default=None)
    descuento_kgs = Column(Numeric(10, 2), nullable=True, default=0.00)
    kgs_reales = Column(Numeric(10, 2), nullable=False)
    precio_unitario = Column(Numeric(10, 2), nullable=False)
    tipo_compra = Column(String(30), nullable=False, default="mayoreo")
    transaccion = relationship("TransaccionCompra", back_populates="operaciones")


class TransaccionVenta(Base):
    __tablename__ = "transacciones_venta"

    id = Column(Integer, primary_key=True, index=True)
    id_cliente = Column(Integer, ForeignKey("clientes.id"), nullable=False)
    id_usuario = Column(Integer, ForeignKey("usuarios.id"), nullable=False)
    monto_bruto = Column(Numeric(10, 2), nullable=False, default=0.00)
    iva = Column(Numeric(10,2), nullable=False, default=16.00)
    envio = Column(Numeric(10,2), nullable=True)
    monto_bruto_envio = Column(Numeric(10,2), nullable=False, default=0.00)
    impuesto = Column(Numeric(10,2), nullable=False, default=0.00)
    monto_neto = Column(Numeric(20, 2), nullable=False, defualt=0.00)
    tipo_cobro = Column(String(30), nullable=True)
    observaciones = Column(String(150), nullable=True)
    cerrada = Column(Boolean, nullable=False, default=False)
    operaciones = relationship(
        "OperacionVenta", back_populates="transaccion", cascade="all, delete-orphan"
    )


class OperacionVenta(Base):
    __tablename__ = "detalles_venta"

    id = Column(Integer, primary_key=True, index=True)
    id_transaccion = Column(Integer, ForeignKey("transacciones_venta.id"), nullable=False)
    id_paca = Column(Integer, ForeignKey("pacas.id"), nullable=False, unique=True) 
    precio_unitario = Column(Numeric(10, 2), nullable=False) 

    transaccion = relationship("TransaccionVenta", back_populates="detalles")
    paca = relationship("Paca")


class CompraMayoreo(Base):
    __tablename__ = "compras_mayoreo"

    id = Column(Integer, primary_key=True, index=True)
    id_proveedor = Column(Integer, ForeignKey("proveedores.id"), nullable=False)
    id_usuario = Column(Integer, ForeignKey("usuarios.id"), nullable=False)
    id_transaccion = Column(
        Integer,
        ForeignKey("transacciones_compras.id"),
        nullable=False,
        unique=True,
        index=True,
    )
    fecha = Column(TIMESTAMP, nullable=False)
    placas = Column(String(15), nullable=False)
    bascula = Column(Integer, nullable=False)
    observaciones = Column(String(150), nullable=True, default=None)


class CompraMenudeo(Base):
    __tablename__ = "compras_menudeo"

    id = Column(Integer, primary_key=True, index=True)
    id_usuario = Column(Integer, ForeignKey("usuarios.id"), nullable=False)
    id_transaccion = Column(
        Integer,
        ForeignKey("transacciones_compras.id"),
        nullable=False,
        unique=True,
        index=True,
    )
    fecha = Column(TIMESTAMP, nullable=False)
    observaciones = Column(String(150), nullable=True)


class Venta(Base):
    __tablename__ = "ventas"

    id = Column(Integer, primary_key=True, index=True)
    id_usuario = Column(Integer, ForeignKey("usuarios.id"), nullable=False)
    id_transaccion = Column(
        Integer, 
        ForeignKey("transacciones_venta.id"), 
        nullable=True, 
        unique=True, 
        index=True
    )
    fecha = Column(TIMESTAMP, nullable=False)
    observaciones = Column(String(150), nullable=True)