-- models/gold/dim_clientes.sql

with stg_usuarios as (
    select * from {{ ref('stg_usuarios') }}
)

select
    usuario_id as cliente_id,
    nombre,
    apellido,
    email,
    fecha_registro
from stg_usuarios