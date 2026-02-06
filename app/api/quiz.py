from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import func
from app.db.session import SessionLocal
from app.db.models import CSQuiz, User, DailyArchive
from pydantic import BaseModel
from datetime import date

router = APIRouter()

def get_db():
    db = SessionLocal()
    try: yield db
    finally: db.close()

class QuizSubmit(BaseModel):
    user_id: int
    quiz_id: int
    is_correct: bool

@router.get("/today")
def get_today_quiz(db: Session = Depends(get_db)):
    # 무작위로 퀴즈 1건 추출
    quiz = db.query(CSQuiz).order_by(func.random()).first()
    if not quiz:
        raise HTTPException(status_code=404, detail="퀴즈 데이터가 없습니다.")
    return quiz

@router.post("/submit")
def submit_quiz(submission: QuizSubmit, db: Session = Depends(get_db)):
    # 1. 유저 경험치 업데이트 (정답일 경우 10 EXP 가산 예시)
    if submission.is_correct:
        user = db.query(User).filter(User.id == submission.user_id).first()
        if user:
            user.current_exp += 10
    
    # 2. Daily Archive 갱신
    today = date.today()
    archive = db.query(DailyArchive).filter(
        DailyArchive.user_id == submission.user_id,
        DailyArchive.date == today
    ).first()
    
    if not archive:
        archive = DailyArchive(user_id=submission.user_id, date=today, quiz_done=True)
        db.add(archive)
    else:
        archive.quiz_done = True
        
    db.commit()
    return {"status": "success", "earned_exp": 10 if submission.is_correct else 0}