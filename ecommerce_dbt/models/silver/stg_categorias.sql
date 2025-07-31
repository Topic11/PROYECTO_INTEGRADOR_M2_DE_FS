-- Limpia y estandariza la tabla de categorias
select
    categoriaid as categoria_id,
    nombre as nombre_categoria
from
    {{ source('ecommerce_db', 'categorias') }}