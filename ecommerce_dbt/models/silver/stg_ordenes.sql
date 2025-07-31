-- Limpia y estandariza la tabla de ordenes
select
    ordenid as orden_id,
    usuarioid as usuario_id,
    fechaorden::timestamp as fecha_orden,
    estado as estado_orden
from
    {{ source('ecommerce_db', 'ordenes') }}