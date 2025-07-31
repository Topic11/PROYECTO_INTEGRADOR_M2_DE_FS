from sqlalchemy import (
    Column, Integer, String, DateTime, DECIMAL, ForeignKey, Text, CheckConstraint
)
from sqlalchemy.orm import declarative_base, relationship
from orm.db_connector    import engine  # importa tu engine existente

Base = declarative_base()

# Usuarios
class usuario(Base):
    __tablename__ = 'usuarios'

    id = Column('usuarioid', Integer, primary_key=True, autoincrement=True)
    nombre = Column('nombre', String(100), nullable=False)
    apellido = Column('apellido', String(100), nullable=False)
    dni = Column('dni', String(20), nullable=False, unique=True)
    email = Column('email', String(255), nullable=False, unique=True)
    contraseña = Column('contraseña', String(255), nullable=False)
    fecha_registro = Column('fecharegistro', DateTime)

# Categorías
class categoria(Base):
    __tablename__ = 'categorias'

    id = Column('categoriaid', Integer, primary_key=True, autoincrement=True)
    nombre = Column('nombre', String(100), nullable=False)
    descripcion = Column('descripcion', String(255))

# Productos
class producto(Base):
    __tablename__ = 'productos'

    id = Column('productoid', Integer, primary_key=True, autoincrement=True)
    nombre = Column('nombre', String(255), nullable=False)
    descripcion = Column('descripcion', Text)
    precio = Column('precio', DECIMAL(10, 2), nullable=False)
    stock = Column('stock', Integer, nullable=False)
    categoria_id = Column('categoriaid', Integer, ForeignKey('categorias.categoriaid'))

# Órdenes
class orden(Base):
    __tablename__ = 'ordenes'

    id = Column('ordenid', Integer, primary_key=True, autoincrement=True)
    usuario_id = Column('usuarioid', Integer, ForeignKey('usuarios.usuarioid'))
    fecha_orden = Column('fechaorden', DateTime)
    total = Column('total', DECIMAL(10, 2), nullable=False)
    estado = Column('estado', String(50))

# Detalle de Órdenes
class detalleorden(Base):
    __tablename__ = 'detalleordenes'

    id = Column('detalleid', Integer, primary_key=True, autoincrement=True)
    orden_id = Column('ordenid', Integer, ForeignKey('ordenes.ordenid'))
    producto_id = Column('productoid', Integer, ForeignKey('productos.productoid'))
    cantidad = Column('cantidad', Integer, nullable=False)
    precio_unitario = Column('preciounitario', DECIMAL(10, 2), nullable=False)

# Direcciones de Envío
class direccionenvio(Base):
    __tablename__ = 'direccionesenvio'

    id = Column('direccionid', Integer, primary_key=True, autoincrement=True)
    usuario_id = Column('usuarioid', Integer, ForeignKey('usuarios.usuarioid'))
    calle = Column('calle', String(255), nullable=False)
    ciudad = Column('ciudad', String(100), nullable=False)
    departamento = Column('departamento', String(100))
    provincia = Column('provincia', String(100))
    distrito = Column('distrito', String(100))
    estado = Column('estado', String(100))
    codigo_postal = Column('codigopostal', String(20))
    pais = Column('pais', String(100), nullable=False)

# Carrito de Compras
class carrito(Base):
    __tablename__ = 'carrito'

    id = Column('carritoid', Integer, primary_key=True, autoincrement=True)
    usuario_id = Column('usuarioid', Integer, ForeignKey('usuarios.usuarioid'))
    producto_id = Column('productoid', Integer, ForeignKey('productos.productoid'))
    cantidad = Column('cantidad', Integer, nullable=False)
    fecha_agregado = Column('fechaagregado', DateTime)

# Métodos de Pago
class metodopago(Base):
    __tablename__ = 'metodospago'

    id = Column('metodopagoid', Integer, primary_key=True, autoincrement=True)
    nombre = Column('nombre', String(100), nullable=False)
    descripcion = Column('descripcion', String(255))

# Ordenes Métodos de Pago
class ordenmetodopago(Base):
    __tablename__ = 'ordenesmetodospago'

    id = Column('ordenmetodoid', Integer, primary_key=True, autoincrement=True)
    orden_id = Column('ordenid', Integer, ForeignKey('ordenes.ordenid'))
    metodo_pago_id = Column('metodopagoid', Integer, ForeignKey('metodospago.metodopagoid'))
    monto_pagado = Column('montopagado', DECIMAL(10, 2), nullable=False)

# Reseñas de Productos
class resenaproducto(Base):
    __tablename__ = 'reseñasproductos'

    id = Column('resenaid', Integer, primary_key=True, autoincrement=True)
    usuario_id = Column('usuarioid', Integer, ForeignKey('usuarios.usuarioid'))
    producto_id = Column('productoid', Integer, ForeignKey('productos.productoid'))
    calificacion = Column('calificacion', Integer, CheckConstraint('calificacion >= 1 AND calificacion <= 5'))
    comentario = Column('comentario', Text)
    fecha = Column('fecha', DateTime)

# Historial de Pagos
class historialpago(Base):
    __tablename__ = 'historialpagos'

    id = Column('pagoid', Integer, primary_key=True, autoincrement=True)
    orden_id = Column('ordenid', Integer, ForeignKey('ordenes.ordenid'))
    metodo_pago_id = Column('metodopagoid', Integer, ForeignKey('metodospago.metodopagoid'))
    monto = Column('monto', DECIMAL(10, 2), nullable=False)
    fecha_pago = Column('fechapago', DateTime)
    estado_pago = Column('estadopago', String(50))
