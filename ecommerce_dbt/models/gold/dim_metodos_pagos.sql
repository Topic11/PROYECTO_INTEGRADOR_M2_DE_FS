-- models/gold/dim_metodos_pago.sql
with stg_metodos_pago as (
    select * from {{ ref('stg_metodos_pago') }}
)

select
    metodo_pago_id,
    nombre_metodo_pago
from stg_metodos_pago