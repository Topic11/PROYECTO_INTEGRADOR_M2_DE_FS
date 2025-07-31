-- Base de datos: ecommercedb_new
-- Este script crea todas las tablas necesarias en PostgreSQL

-- Tabla: Usuarios
CREATE TABLE usuarios (
    usuarioid SERIAL PRIMARY KEY,
    nombre VARCHAR(100) NOT NULL,
    apellido VARCHAR(100) NOT NULL,
    dni VARCHAR(20) UNIQUE NOT NULL,
    email VARCHAR(255) UNIQUE NOT NULL,
    contraseña VARCHAR(255) NOT NULL,
    fecharegistro TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);


-- Tabla: Categorías
CREATE TABLE categorias (
    categoriaid SERIAL PRIMARY KEY,
    nombre VARCHAR(100) NOT NULL,
    descripcion VARCHAR(255)
);

-- Tabla: Productos
CREATE TABLE productos (
    productoid SERIAL PRIMARY KEY,
    nombre VARCHAR(255) NOT NULL,
    descripcion TEXT,
    precio DECIMAL(10,2) NOT NULL,
    stock INT NOT NULL,
    categoriaid INT REFERENCES categorias(categoriaid) ON DELETE SET NULL
);

-- Tabla: Órdenes
CREATE TABLE ordenes (
    ordenid SERIAL PRIMARY KEY,
    usuarioid INT REFERENCES usuarios(usuarioid) ON DELETE CASCADE,
    fechaorden TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    total DECIMAL(10,2) NOT NULL,
    estado VARCHAR(50) DEFAULT 'Pendiente'
);

-- Tabla: Detalle de Órdenes
CREATE TABLE detalleordenes (
    detalleid SERIAL PRIMARY KEY,
    ordenid INT REFERENCES ordenes(ordenid) ON DELETE CASCADE,
    productoid INT REFERENCES productos(productoid) ON DELETE CASCADE,
    cantidad INT NOT NULL,
    preciounitario DECIMAL(10,2) NOT NULL
);

-- Tabla: Direcciones de Envío
CREATE TABLE direccionesenvio (
    direccionid SERIAL PRIMARY KEY,
    usuarioid INT REFERENCES usuarios(usuarioid) ON DELETE CASCADE,
    calle VARCHAR(255) NOT NULL,
    ciudad VARCHAR(100) NOT NULL,
    departamento VARCHAR(100),
    provincia VARCHAR(100),
    distrito VARCHAR(100),
    estado VARCHAR(100),
    codigopostal VARCHAR(20),
    pais VARCHAR(100) NOT NULL
);

-- Tabla: Carrito de Compras
CREATE TABLE carrito (
    carritoid SERIAL PRIMARY KEY,
    usuarioid INT REFERENCES usuarios(usuarioid) ON DELETE CASCADE,
    productoid INT REFERENCES productos(productoid) ON DELETE CASCADE,
    cantidad INT NOT NULL,
    fechaagregado TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Tabla: Métodos de Pago
CREATE TABLE metodospago (
    metodopagoid SERIAL PRIMARY KEY,
    nombre VARCHAR(100) NOT NULL,
    descripcion VARCHAR(255)
);

-- Tabla: Ordenes Métodos de Pago
CREATE TABLE ordenesmetodospago (
    ordenmetodoid SERIAL PRIMARY KEY,
    ordenid INT REFERENCES ordenes(ordenid) ON DELETE CASCADE,
    metodopagoid INT REFERENCES metodospago(metodopagoid) ON DELETE CASCADE,
    montopagado DECIMAL(10,2) NOT NULL
);

-- Tabla: Reseñas de Productos
CREATE TABLE reseñasproductos (
    reseñaid SERIAL PRIMARY KEY,
    usuarioid INT REFERENCES usuarios(usuarioid) ON DELETE CASCADE,
    productoid INT REFERENCES productos(productoid) ON DELETE CASCADE,
    calificacion INT CHECK (calificacion >= 1 AND calificacion <= 5),
  comentario TEXT,
  fecha TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);


-- Tabla: Historial de Pagos

   CREATE TABLE historialpagos (
  pagoid SERIAL PRIMARY KEY,
  ordenid INT REFERENCES ordenes(ordenid) ON DELETE CASCADE,
  metodopagoid INT REFERENCES metodospago(metodopagoid) ON DELETE CASCADE,
  monto DECIMAL(10,2) NOT NULL,
  fechapago TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  estadopago VARCHAR(50) DEFAULT 'Procesando'
);


