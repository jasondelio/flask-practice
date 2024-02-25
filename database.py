from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from base import Base


DATABASE_URL = "postgresql://postgres:admin@localhost:5432/practice_db"

engine = create_engine(DATABASE_URL)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def getDB():
    return SessionLocal()
def createTables():
    Base.metadata.create_all(engine)