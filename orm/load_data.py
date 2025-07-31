import os
from sqlalchemy import create_engine, text
from dotenv import load_dotenv

# --- 1. Carga de Variables de Entorno ---
# Busca el archivo .env en la misma carpeta que el script (orm/.env)
load_dotenv()

DB_HOST = os.getenv("DB_HOST", "localhost")
DB_PORT = os.getenv("DB_PORT", "5432")
DB_NAME = os.getenv("DB_NAME")
DB_USER = os.getenv("DB_USER")
DB_PASSWORD = os.getenv("DB_PASSWORD")

# --- 2. Configuración de la Conexión con SQLAlchemy ---
DATABASE_URL = f"postgresql+psycopg2://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"

# --- 3. Definición de la Lógica de Carga ---

# Orden de carga manual para respetar las dependencias (claves foráneas)
SQL_LOAD_ORDER = [
    "1.usuarios.sql",
    "2.categorias.sql",
    "3.metodos_pago.sql",
    "4.productos.sql",
    "5.ordenes.sql",
    "6.direcciones_envio.sql",
    "7.carrito.sql",
    "8.detalle_ordenes.sql",
    "9.ordenes_metodospago.sql",
    "10.historial_pagos.sql",
    "11.resenas_productos.sql"
]

def execute_sql_from_file(engine, file_path):
    """
    Lee un archivo .sql y ejecuta su contenido usando una conexión de SQLAlchemy.
    """
    print(f"Ejecutando archivo: {os.path.basename(file_path)}...")
    with open(file_path, 'r', encoding='utf-8') as f:
        sql_script = f.read()
        with engine.connect() as connection:
            with connection.begin() as transaction:
                try:
                    connection.execute(text(sql_script))
                    transaction.commit()
                    print(f"    -> Finalizado exitosamente.")
                except Exception as e:
                    print(f"    -> ERROR durante la ejecución: {e}")
                    transaction.rollback()
                    raise

def main():
    """
    Función principal que se conecta a la base de datos
    y ejecuta los archivos .sql en el orden predefinido.
    """
    try:
        engine = create_engine(DATABASE_URL)
        
        # --- ESTA ES LA LÍNEA CORREGIDA ---
        # Ahora busca la carpeta 'data' DENTRO de la carpeta 'orm'
        sql_files_path = os.path.join(os.path.dirname(__file__), 'data')
        
        print("--- Iniciando carga de datos desde archivos .sql ---")
        
        for sql_file in SQL_LOAD_ORDER:
            file_path = os.path.join(sql_files_path, sql_file)
            if os.path.exists(file_path):
                execute_sql_from_file(engine, file_path)
            else:
                print(f"    -> ADVERTENCIA: No se encontró el archivo {sql_file}. Saltando.")
        
        print("\n¡Carga de todos los archivos completada exitosamente!")

    except Exception as e:
        print(f"\nOcurrió un error crítico durante el proceso de carga y se ha detenido.")
    finally:
        if 'engine' in locals() and engine:
            engine.dispose()
            print("Conexión del motor de SQLAlchemy cerrada.")

# --- Punto de Entrada del Script ---
if __name__ == "__main__":
    main()