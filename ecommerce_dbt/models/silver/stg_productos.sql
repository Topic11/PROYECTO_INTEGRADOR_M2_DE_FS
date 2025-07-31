-- models/staging/stg_productos.sql

with source as (
    select * from {{ source('ecommerce_db', 'productos') }}
),

-- SIMULACIÓN DE DATOS HISTÓRICOS
-- Tomamos el producto_id = 1 real y le inventamos un historial de precios,
-- manteniendo todos sus otros datos originales.
simulated_history as (
    -- Versión actual de todos los productos
    select
        productoid as producto_id,
        nombre as nombre_producto,
        descripcion,
        precio::decimal(10, 2) as precio,
        stock,
        categoriaid as categoria_id,
        now()::timestamp as fecha_modificacion -- La data actual la marcamos con la fecha de hoy
    from source

    union all

    -- Versión histórica 1 del producto 1 (precio anterior)
    select
        productoid as producto_id,
        nombre as nombre_producto,
        descripcion,
        1150.75 as precio, -- Inventamos un precio anterior
        stock,
        categoriaid as categoria_id,
        (now() - interval '6 months')::timestamp as fecha_modificacion -- Inventamos una fecha de cambio
    from source
    where productoid = 1

)

select * from simulated_history