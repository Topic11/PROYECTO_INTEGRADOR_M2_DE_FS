-- Limpia y estandariza la tabla de metodos de pago
select
    metodopagoid as metodo_pago_id,
    nombre as nombre_metodo_pago
from
    {{ source('ecommerce_db', 'metodospago') }}