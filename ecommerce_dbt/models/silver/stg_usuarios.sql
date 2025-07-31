-- Limpia y estandariza la tabla de usuarios
select
    usuarioid as usuario_id,
    nombre,
    apellido,
    email,
    fecharegistro::date as fecha_registro
from    
    {{source('ecommerce_db','usuarios')}}