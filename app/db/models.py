from sqlalchemy import Column, Integer, String, Text, ForeignKey, Date, Boolean, DateTime, CHAR, JSON
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.db import Base  

# 1. User table: users
class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    github_id = Column(String(100), unique=True, nullable=False)
    level = Column(Integer, default=1)
    current_exp = Column(Integer, default=0)
    target_repo_url = Column(String(255))

    # Relationships
    daily_archives = relationship("DailyArchive", back_populates="user")
    analyses = relationship("CodeAnalysis", back_populates="user")
    memos = relationship("UserMemo", back_populates="user")

# 2. Daily table: daily_archive
class DailyArchive(Base):
    __tablename__ = "daily_archive"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    date = Column(Date, default=func.current_date())
    quiz_done = Column(Boolean, default=False)
    memo_done = Column(Boolean, default=False)
    analysis_done = Column(Boolean, default=False)

    user = relationship("User", back_populates="daily_archives")

# 3. Quiz table: cs_quizzes
class CSQuiz(Base):
    __tablename__ = "cs_quizzes"

    id = Column(Integer, primary_key=True, index=True)
    question = Column(Text, nullable=False)
    options = Column(JSON, nullable=False)  # JSON 타입으로 선택지 저장
    answer = Column(String(255), nullable=False)
    category = Column(String(50))

# 4. Code Analysis table: code_analysis
class CodeAnalysis(Base):
    __tablename__ = "code_analysis"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    commit_sha = Column(String(40), nullable=False)
    rank = Column(CHAR(1))  # S, A, B, C 등급
    feedback = Column(String(150))  # 150자 이내 제한
    earned_exp = Column(Integer, default=0)

    user = relationship("User", back_populates="analyses")

# 5. Soft Skill table: soft_skill_questions
class SoftSkillQuestion(Base):
    __tablename__ = "soft_skill_questions"

    qid = Column(Integer, primary_key=True, index=True)
    question_txt = Column(String(100), nullable=False)
    category = Column(Integer)  # 카테고리 식별 번호

    memos = relationship("UserMemo", back_populates="question")

# 6. Memo table: user_memos
class UserMemo(Base):
    __tablename__ = "user_memos"

    mid = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    qid = Column(Integer, ForeignKey("soft_skill_questions.qid"), nullable=False)
    memo_txt = Column(String(200))  # 200자 이내 제한
    timestamp = Column(DateTime(timezone=True), server_default=func.now())

    user = relationship("User", back_populates="memos")
    question = relationship("SoftSkillQuestion", back_populates="memos")
