import settings

from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

SQLALCHEMY_CONNECTION_STRING = f"mysql+pymysql://{settings.envvars.user}:{settings.envvars.password}@{settings.envvars.host}/{settings.envvars.database_name}?charset=utf8mb4"

engine = create_engine(SQLALCHEMY_CONNECTION_STRING)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()


# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()