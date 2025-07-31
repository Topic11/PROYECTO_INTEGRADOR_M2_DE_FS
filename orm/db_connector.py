import os
from dotenv import load_dotenv
from sqlalchemy.orm import sessionmaker, declarative_base
from sqlalchemy import create_engine

load_dotenv()

DB_HOST=os.getenv("DB_HOST")
DB_PORT=os.getenv("DB_PORT")
DB_NAME=os.getenv("DB_NAME")
DB_USER=os.getenv("DB_USER")
DB_PASSWORD=os.getenv("DB_PASSWORD")

DATABASE_URL = f"postgresql+pg8000://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"

try:
    engine = create_engine(DATABASE_URL, echo=False, client_encoding='utf8')

    print("Motor db SQLAlchemy creado exitosamente para Docker")
except Exception as e:
    print(f"Error al crear db: {e}")
    raise

base = declarative_base()
DBSession = sessionmaker(bind=engine)

def get_db_engine():
    return engine


def get_db_session():
    return DBSession


def get_db_connection():
    return engine.connect()