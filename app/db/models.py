# app/db/models.py
from sqlalchemy import Column, Integer, String, Text, ForeignKey, DateTime, JSON
from sqlalchemy.sql import func
from app.db.session import Base

class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    github_id = Column(String(100), unique=True, nullable=False)
    level = Column(Integer, default=1)
    current_exp = Column(Integer, default=0)
    target_repo_url = Column(String(255))

class CSQuiz(Base):
    __tablename__ = "cs_quizzes"
    id = Column(Integer, primary_key=True, index=True)
    question = Column(Text, nullable=False)
    options = Column(JSON)
    answer = Column(String(255))
    category = Column(String(50))