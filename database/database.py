import os
from sqlalchemy import create_engine
from sqlalchemy.orm.session import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

# Nombre del archivo SQLite
sqlite_name = os.getenv("SQLITE_NAME", "movies.sqlite")
# Directorio base para SQLite
base_dir = os.getenv("SQLITE_DIR", os.path.dirname(os.path.realpath(__file__)))
# URL de la base de datos
database_url = f"sqlite:///{os.path.join(base_dir, sqlite_name)}"

# Configurar SQLAlchemy
engine = create_engine(database_url, echo=True)
session = sessionmaker(bind=engine)

Base = declarative_base()
