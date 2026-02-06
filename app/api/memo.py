from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import func
from app.db.session import SessionLocal
from app.db.models import SoftSkillQuestion, UserMemo, DailyArchive, User
from pydantic import BaseModel, Field
from datetime import date

router = APIRouter()

def get_db():
    db = SessionLocal()
    try: yield db
    finally: db.close()

class MemoCreate(BaseModel):
    user_id: int
    qid: int # 모델의 SoftSkillQuestion.qid 반영
    memo_txt: str = Field(..., max_length=200) # 모델의 String(200) 반영

@router.get("/question")
def get_soft_skill_question(db: Session = Depends(get_db)):
    question = db.query(SoftSkillQuestion).order_by(func.random()).first()
    if not question:
        raise HTTPException(status_code=404, detail="질문이 없습니다.")
    return question

@router.post("/save")
def save_memo(memo: MemoCreate, db: Session = Depends(get_db)):
    # 1. 유저 존재 확인 (FK 제약 조건 에러 방지)
    user = db.query(User).filter(User.id == memo.user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="사용자를 찾을 수 없습니다.")

    # 2. 메모 저장
    new_memo = UserMemo(
        user_id=memo.user_id,
        qid=memo.qid,
        memo_txt=memo.memo_txt
    )
    db.add(new_memo)
    
    # 3. Daily Archive 갱신
    today = date.today()
    archive = db.query(DailyArchive).filter(
        DailyArchive.user_id == memo.user_id,
        DailyArchive.date == today
    ).first()
    
    if not archive:
        archive = DailyArchive(user_id=memo.user_id, date=today, memo_done=True)
        db.add(archive)
    else:
        archive.memo_done = True
        
    db.commit()
    return {"status": "success"}