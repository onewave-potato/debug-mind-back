# app/db/session.py
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from app.core.config import settings

# PostgreSQL 엔진 생성
engine = create_engine(settings.DATABASE_URL)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

# FastAPI의 Depends로 사용할 DB 세션 획득 함수
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()