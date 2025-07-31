# Informe del Proyecto: Optimización de una Plataforma de E-Commerce

## 1. Resumen

Este documento detalla el proceso de diseño e implementación de una solución de datos para una empresa emergente de e-commerce. El proyecto partió de un conjunto de datos desestructurado y culminó con la creación de un Data Warehouse dimensional, siguiendo la metodología de modelado Kimball.

El objetivo principal fue transformar los datos crudos en una fuente de información centralizada, confiable y optimizada para el análisis de negocio, permitiendo responder preguntas críticas y monitorear KPIs clave para la toma de decisiones estratégicas.

El desarrollo se estructuró en las siguientes fases clave, que se detallan a continuación:
1.  **Carga y Entendimiento de los Datos:** Se configuró el entorno de datos y se realizó un Análisis Exploratorio para evaluar la calidad de las fuentes originales.
2.  **Diseño del Modelo Dimensional:** Se diseñó un modelo en esquema de estrella para responder a las preguntas de negocio, incluyendo una estrategia para el manejo de datos históricos (SCD).
3.  **Implementación con dbt:** Se construyó el pipeline de transformaciones para limpiar los datos y materializar el modelo dimensional final.
4.  **Análisis y KPIs:** Se definieron métricas clave y se propuso una solución de visualización para explotar los datos y generar insights.

---

## 2. Estructura del Repositorio

El proyecto está organizado en las siguientes carpetas principales, cada una con una responsabilidad clara:

```text
├── data/                 # Carpeta generada por Pgadmin.
├── dbt_profile/          # Configuración del perfil de conexión para dbt.
├── docs/                 # Documentación del modelo de datos y screenshots de validacion.
├── ecommerce_dbt/        # Proyecto principal de dbt con los modelos de transformación.
├── init_scripts/         # Scripts .sql para la creación inicial de las tablas (DDL).
├── logs/                 # Logs generados por dbt.
├── orm/                  # Notebook de exploración script de carga de datos y conectores de db.
├── pgadmin-data/         # Datos persistentes de la configuración de pgAdmin.
├── .env                  # Archivo de configuración con las credenciales.
├── .gitignore            # Archivos y carpetas a ignorar por Git.
├── docker-compose.yml    # Orquestador de los servicios de Docker (PostgreSQL, pgAdmin y dbt).
├── dockerfile            # Definición de la imagen de Docker para el entorno de dbt.
├── requirements.txt      # Dependencias de Python para el proyecto.
└── streamlit_app.py      # Script.py para visualizacion de KPIS.
```


---

## 3. Desarrollo del Proyecto Paso a Paso

A continuación, se detalla cada fase del proyecto, el requerimiento que busca resolver y los archivos asociados a su implementación.

### Paso 1: Carga y Entendimiento de los Datos (Avance #1)

-   **Enunciado del Desafío:** "Configurar una base de datos relacional, cargar los archivos, explorar los datos para detectar inconsistencias y evaluar su calidad."
-   **Descripción de la Implementación:** Se orquestó un entorno de datos reproducible utilizando Docker. El proceso de carga se dividió en dos etapas:
    1.  **Creación de Estructuras (DDL):** Al iniciar el contenedor de PostgreSQL, se ejecuta automáticamente el script `Create_ddl.sql` para crear el esquema y todas las tablas vacías.
    2.  **Población de Datos (DML):** Posteriormente, se ejecuta el script en Python `load_data.py`, que utiliza SQLAlchemy para leer los archivos `.sql` restantes y poblar las tablas con los registros correspondientes.
    
    Una vez cargados los datos, se realizó un Análisis Exploratorio que reveló una alta integridad estructural (claves primarias únicas y sin registros huérfanos).

-   **Archivos Utilizados:**
    -   `docker-compose.yml`: Define y orquesta los servicios de PostgreSQL, pgAdmin y DBT.
    -   `init_scripts/Create_ddl.sql`: Script SQL para la creación de la estructura de las 11 tablas.
    -   `orm/load_data.py`: Script de Python responsable de la inserción de datos en las tablas.
    -   `orm/explorer.ipynb`: Notebook con el código y los resultados del Análisis Exploratorio de Datos.
    -   `docs/validation.docx': imagen 1 y 2 donde se levantan los contenedores y se carga la data.

### Paso 2: Diseño del Modelo Dimensional (Avance #2)

-   **Enunciado del Desafío:** "Analizar las preguntas de negocio, definir hechos y dimensiones según la metodología Kimball, diseñar el modelo y generar un diagrama entidad-relación (ERD)."
-   **Descripción de la Implementación:** Para traducir las preguntas de negocio en un modelo analítico, se aplicó la metodología Kimball, resultando en un **esquema en estrella**. Este diseño fue elegido por su simplicidad y alto rendimiento para las consultas que realizan los analistas de negocio.

    -   **Definición de la Tabla de Hechos (`fact_ventas')  ** El corazón del modelo es la tabla de hechos. Se definió que representaría el proceso de negocio más importante: las **ventas**. La granularidad se estableció en el nivel más detallado posible: **un registro por cada ítem de producto dentro de una orden**. Esta decisión, aunque genera una tabla grande, es la más potente, ya que nos permite "subir" y analizar los datos desde cualquier ángulo (por producto, por categoría, por día, por cliente) sin perder información.

    -   **Definición de las Dimensiones:** Las dimensiones proveen el contexto que describe a los hechos. Se crearon para responder a las preguntas "quién, qué, cuándo y cómo" de cada venta:
        -   `dim_clientes`: Responde al **"quién"** compró.
        -   `dim_productos`: Responde al **"qué"** se vendió.
        -   `dim_fechas`: Responde al **"cuándo"** ocurrió la venta, permitiendo análisis de tendencias.
        -   `dim_metodos_pago`: Responde al **"cómo"** se pagó la orden.

    -   **Justificación de Slowly Changing Dimension (SCD) Tipo 2:** Se identificó que los atributos de la dimensión `dim_productos` (como el precio) no son estáticos y pueden cambiar con el tiempo. Para analizar las ventas históricas con la información correcta del momento en que ocurrieron, era crucial no perder este historial. Por ello, se implementó una estrategia **SCD Tipo 2**, que permite mantener múltiples versiones de un mismo producto, cada una con su período de validez. Esto es fundamental para que, por ejemplo, un análisis de rentabilidad de hace seis meses use el precio de ese momento y no el actual.
-   
    **Archivos Utilizados:**
    -   `docs/erd.png`: Imagen del Diagrama Entidad-Relación que representa visualmente el esquema en estrella final.
    -   `README.md` (este mismo archivo): Esta sección contiene la justificación detallada del diseño del modelo.


### Paso 3: Implementación de Transformaciones con dbt (Avance #3)

-   **Enunciado del Desafío:** "Construir el modelo físico implementando las transformaciones en dbt. Crear tablas de hechos y dimensiones, incluyendo el manejo de SCDs y organizando las capas de modelado."
-   **Descripción de la Implementación:** Se utilizó **dbt** para construir el pipeline que transforma los datos desde las tablas crudas hasta el modelo dimensional final. Se siguió la **arquitectura de medallón** de tres capas:
    1.  **Capa Bronce:** Se declararon las tablas crudas (cargadas en el Paso 1) como *fuentes* en dbt. Esta capa representa el punto de entrada de los datos al pipeline, sin transformaciones.
    2.  **Capa Plata:** Se crearon modelos de staging para cada fuente. En esta capa se realizaron las tareas de limpieza y estandarización: Renombrado de columnas  y otras normalizaciones menores. El objetivo es tener una base limpia y consistente para la siguiente capa.
    3.  **Capa Oro:** En esta capa final se construyeron las tablas de hechos y dimensiones (`fact_` y `dim_`) que conforman el modelo en estrella. Estos modelos contienen la lógica de negocio, los joins entre las tablas de staging y las agregaciones necesarias para el análisis directo.
    
    Adicionalmente, se implementaron **tests de datos** en dbt para garantizar la integridad del modelo final, validando claves primarias (únicas y no nulas) y la integridad referencial entre las tablas de hechos y dimensiones.
-   **Archivos Utilizados:**
    -   `ecommerce_dbt/models/bronze/sources.yml`: Define las tablas de la capa Bronce.
    -   `ecommerce_dbt/models/silver/: Contiene los modelos SQL para la capa Plata.
    -   `ecommerce_dbt/models/gold/:  Contiene los modelos SQL para la capa Oro.
    -   `ecommerce_dbt/models/gold/schema.yml:  Contiene los test de dbt.
    -   `dbt_project.yml`: Archivo principal de configuración del proyecto dbt.
    -   `docs/validation`: imagen 3, 4 y 5 donde se levantan el contenedor dbt (se inicializa al mismo tiempo que los otros contenedores pero para fines demostrativos lo separé), se corren los modelos y se ejecutan los test.

### Paso 4: Análisis de KPIs y Propuesta de Visualización

-   **Enunciado del Desafío:** "Diseñar e Implementar KPIs y métricas para identificar patrones que ayuden a responder las preguntas de negocio."
-   **Descripción de la Implementación:** Se definieron 3 KPIs clave para el negocio, calculables a partir de nuestro modelo dimensional:
    1.  **Ticket Promedio por Orden (AOV):** Para medir el valor promedio de compra.
    2.  **Crecimiento Mensual de Ventas (MoM Growth):** Para medir la tendencia y salud del negocio.
    3.  **Valor Total de Venta por Categoría:** Para identificar las categorías de productos más rentables.
    Como propuesta de visualización, se planteó la creación de un dashboard en **Streamlit**.
-   **Archivos Utilizados:**
    -   `docs/validation`: Carpeta destinada a contener las consultas SQL que calculan los KPIs (KPI 1,2 y 3) + apartado de Visualizacion.
    -   `streamlit_app.py`: Script para construir el dashboard.
