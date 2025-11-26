import psycopg2
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from typing import Optional

def get_db_connection():
    # os.getenv 사용 안 함 → 기본값을 직접 설정
    DB_HOST: Optional[str] = "db_postgresql"
    DB_PORT: Optional[str] = "5432"
    POSTGRES_DB: Optional[str] = "main_db"
    POSTGRES_USER: Optional[str] = "admin"
    POSTGRES_PASSWORD: Optional[str] = "admin123"
    conn = psycopg2.connect(
        host=DB_HOST,
        port=DB_PORT,
        dbname=POSTGRES_DB,
        user=POSTGRES_USER,
        password=POSTGRES_PASSWORD
    )
    return conn

SQLALCHEMY_DATABASE_URL = "postgresql://admin:admin123@db_postgresql:5432/main_db"

engine = create_engine(SQLALCHEMY_DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
