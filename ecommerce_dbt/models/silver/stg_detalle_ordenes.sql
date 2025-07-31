-- Limpia y estandariza la tabla de detalle de ordenes
select
    detalleid as detalle_id,
    ordenid as orden_id,
    productoid as producto_id,
    cantidad,
    preciounitario::decimal(10, 2) as precio_unitario
from
    {{ source('ecommerce_db', 'detalleordenes') }}