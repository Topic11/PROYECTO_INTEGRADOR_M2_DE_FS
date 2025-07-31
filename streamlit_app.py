import streamlit as st
import pandas as pd
from sqlalchemy import create_engine, text
import os
from dotenv import load_dotenv
from pathlib import Path

# --- Configuración de la Página y Carga de Credenciales ---
st.set_page_config(
    page_title="Dashboard de Ventas E-Commerce",
    page_icon="📊",
    layout="wide"
)

# --- Carga de Variables de Entorno de forma robusta ---
project_root = Path(__file__).parent.parent
env_path = project_root / '.env'
load_dotenv(dotenv_path=env_path)

# --- Conexión a la Base de Datos ---
DB_HOST = os.getenv("DB_HOST", "localhost")
DB_PORT = os.getenv("DB_PORT", "5432")
DB_NAME = os.getenv("POSTGRES_DB")
DB_USER = os.getenv("POSTGRES_USER")
DB_PASSWORD = os.getenv("POSTGRES_PASSWORD")
DB_SCHEMA = os.getenv("DBT_TARGET_SCHEMA", "public")

if not all([DB_NAME, DB_USER, DB_PASSWORD]):
    st.error(f"Error: No se pudieron cargar las credenciales desde {env_path}. Asegúrate de que el archivo .env exista en la raíz del proyecto y contenga POSTGRES_DB, POSTGRES_USER y POSTGRES_PASSWORD.")
    st.stop()

DATABASE_URL = f"postgresql+psycopg2://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"

try:
    engine = create_engine(DATABASE_URL, connect_args={'options': f'-csearch_path={DB_SCHEMA}'})
    st.session_state.db_connection_status = "Conectado"
except Exception as e:
    st.session_state.db_connection_status = f"Error: {e}"

# --- Función para Cargar Datos (cacheada para mejorar performance) ---
@st.cache_data
def load_data(query):
    try:
        with engine.connect() as connection:
            df = pd.read_sql(text(query), connection)
            return df
    except Exception as e:
        st.error(f"Error al ejecutar la consulta: {e}")
        return pd.DataFrame()

# --- Título del Dashboard ---
st.title("📊 Dashboard de Ventas E-Commerce")
st.markdown("Este dashboard presenta los KPIs clave y análisis del rendimiento de ventas, consumiendo los datos directamente desde el Data Warehouse.")

if st.session_state.db_connection_status != "Conectado":
    st.error(f"No se pudo establecer conexión con la base de datos. Detalles: {st.session_state.db_connection_status}")
    st.stop()

# --- Carga de Datos para los KPIs y Gráficos ---
# CORRECCIÓN: Usamos 'fact_ventas' en lugar de 'fct_ventas'
query_kpi_aov = "select sum(monto_total_linea) / count(distinct orden_id) as ticket_promedio from fact_ventas"
query_kpi_categorias = """
    select
        dp.nombre_categoria,
        sum(fv.monto_total_linea) as total_vendido
    from fact_ventas fv
    left join dim_productos dp on fv.producto_id = dp.producto_id
    where dp.es_version_actual = true
    group by 1
    order by 2 desc
"""
# CORRECCIÓN: Usamos 'fact_ventas' y unimos con 'dim_fechas'
query_ventas_mensuales = """
    select
        date_trunc('month', df.fecha_completa)::date as mes,
        sum(fv.monto_total_linea) as ventas_mensuales
    from fact_ventas fv
    left join dim_fechas df on fv.fecha_orden_id = df.fecha_id
    group by 1
    order by 1
"""

df_aov = load_data(query_kpi_aov)
df_categorias = load_data(query_kpi_categorias)
df_ventas_mensuales = load_data(query_ventas_mensuales)

# --- Mostrar KPIs en Tarjetas ---
st.header("KPIs Principales")
if not df_aov.empty and not df_categorias.empty:
    total_ventas = df_categorias['total_vendido'].sum()
    ticket_promedio = df_aov['ticket_promedio'][0]

    col1, col2 = st.columns(2)
    col1.metric("Ventas Totales", f"${total_ventas:,.2f}")
    col2.metric("Ticket Promedio (AOV)", f"${ticket_promedio:,.2f}")
else:
    st.warning("No se pudieron calcular los KPIs.")

st.markdown("---")

# --- Visualizaciones ---
st.header("Análisis de Ventas")
col1, col2 = st.columns(2)

with col1:
    st.subheader("Ventas por Categoría de Producto")
    if not df_categorias.empty:
        st.bar_chart(df_categorias.set_index('nombre_categoria'))
    else:
        st.warning("No se pudieron cargar los datos de ventas por categoría.")

with col2:
    st.subheader("Evolución de Ventas Mensuales")
    if not df_ventas_mensuales.empty:
        st.line_chart(df_ventas_mensuales.set_index('mes'))
    else:
        st.warning("No se pudieron cargar los datos de ventas mensuales.")