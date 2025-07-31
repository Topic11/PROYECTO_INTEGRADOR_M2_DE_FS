-- models/marts/dim_fechas.sql

-- Genera un rango de fechas a partir de un inicio y un fin
with date_series as (
  select generate_series('2020-01-01'::date, '2026-12-31'::date, '1 day'::interval) as fecha_dia
)

-- Generamos los atributos de la dimensión de fechas a partir de la serie anterior
select
  (extract(year from fecha_dia) * 10000 + extract(month from fecha_dia) * 100 + extract(day from fecha_dia))::int as fecha_id,
  fecha_dia as fecha_completa,
  extract(year from fecha_dia)::int as anio,
  extract(month from fecha_dia)::int as mes,
  to_char(fecha_dia, 'Month') as nombre_mes,
  extract(day from fecha_dia)::int as dia_del_mes,
  extract(isodow from fecha_dia)::int as dia_de_la_semana,
  to_char(fecha_dia, 'Day') as nombre_dia_semana,
  extract(quarter from fecha_dia)::int as trimestre,
  case
    when extract(isodow from fecha_dia) in (6, 7) then true
    else false
  end as es_fin_de_semana
from
  date_series
order by
  fecha_dia