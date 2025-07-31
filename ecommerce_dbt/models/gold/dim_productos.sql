-- models/gold/dim_productos.sql
-- Implementación de Dimensión Lentamente Cambiante (SCD) Tipo 2

with stg_productos_con_historia as (
    select * from {{ ref('stg_productos') }}
),

stg_categorias as (
    select * from {{ ref('stg_categorias') }}
),

-- Usamos funciones de ventana para calcular los rangos de fechas
productos_con_periodos as (
    select
        producto_id,
        nombre_producto,
        descripcion,
        precio,
        stock,
        categoria_id,
        fecha_modificacion as fecha_inicio_validez,
        lead(fecha_modificacion) over (partition by producto_id order by fecha_modificacion) as fecha_fin_validez
    from stg_productos_con_historia
),

final as (
    select
        p.producto_id,
        p.nombre_producto,
        p.descripcion,
        c.nombre_categoria,
        p.precio,
        p.stock,
        p.fecha_inicio_validez,
        coalesce(p.fecha_fin_validez, '9999-12-31') as fecha_fin_validez,
        case
            when p.fecha_fin_validez is null then true
            else false
        end as es_version_actual
    from productos_con_periodos p
    left join stg_categorias c on p.categoria_id = c.categoria_id
)

select * from final