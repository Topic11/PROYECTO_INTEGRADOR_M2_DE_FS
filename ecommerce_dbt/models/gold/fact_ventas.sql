-- models/marts/fact_ventas.sql (v2)

with stg_detalle_ordenes as (
    select * from {{ ref('stg_detalle_ordenes') }}
),

stg_ordenes as (
    select * from {{ ref('stg_ordenes') }}
),

-- Referenciamos la nueva dim_fechas para poder unir por fecha_id
dim_fechas as (
    select * from {{ ref('dim_fechas') }}
)

select
    -- Claves Surrogadas y Foráneas
    od.detalle_id as venta_id,
    od.orden_id,
    od.producto_id,
    o.usuario_id as cliente_id,
    -- Reemplazamos la fecha_orden por la clave de la dimensión de fechas
    df.fecha_id as fecha_orden_id,

    -- Métricas
    od.cantidad,
    od.precio_unitario,
    (od.cantidad * od.precio_unitario) as monto_total_linea,
    
    -- Atributos degenerados
    o.estado_orden

from
    stg_detalle_ordenes od
left join
    stg_ordenes o on od.orden_id = o.orden_id
-- Unimos con la dimensión de fechas para obtener la clave fecha_id
left join
    dim_fechas df on o.fecha_orden::date = df.fecha_completa

