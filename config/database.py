from flask_sqlalchemy import SQLAlchemy
import psycopg2
from config.settings import Config

db = SQLAlchemy()

def create_database():
    """Verifica si la base de datos existe, si no, la crea."""
    db_url = Config.SQLALCHEMY_DATABASE_URI
    db_name = db_url.rsplit('/', 1)[-1]  # Extraer el nombre de la base de datos
    db_url_without_db = db_url.rsplit('/', 1)[0]  # URL sin el nombre de la base de datos

    try:
        conn = psycopg2.connect(db_url)
        conn.close()
        print(f"✔ La base de datos '{db_name}' ya existe.")
    except:
        print(f"⚠ La base de datos '{db_name}' no existe. Creándola...")
        conn = psycopg2.connect(db_url_without_db + "/postgres")  # Conectar a la base de datos por defecto
        conn.autocommit = True
        cursor = conn.cursor()
        cursor.execute(f"CREATE DATABASE {db_name};")
        cursor.close()
        conn.close()
        print(f"✅ Base de datos '{db_name}' creada exitosamente.")
