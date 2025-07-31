FROM python:3.10

# Crea el directorio del proyecto dbt
WORKDIR /app/

# Instala dbt y adaptador de postgres
RUN pip install dbt-postgres

