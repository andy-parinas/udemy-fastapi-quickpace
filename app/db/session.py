from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.settings import settings
# SQLALCHEMY_DATABASE_URI = "sqlite:///example.db"
SQLALCHEMY_DATABASE_URI = "postgresql://dbuser:password@localhost:5432/udemy_fastapi"


# engine = create_engine(SQLALCHEMY_DATABASE_URI, connect_args={"check_same_thread": False})
engine = create_engine(settings.SQLALCHEMY_DATABASE_URI, echo=True)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()