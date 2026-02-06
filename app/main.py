import os
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv
from app.db.session import engine, Base
from app.db import models
from app.api.quiz import router as quiz_router
from app.api.memo import router as memo_router

# 앱 시작 시 Cloud SQL에 테이블이 없다면 자동 생성
models.Base.metadata.create_all(bind=engine)

# .env 파일 로드
load_dotenv()

app = FastAPI()

# 프론트엔드와 통신을 위한 CORS 설정
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(quiz_router, prefix="/api/quiz", tags=["Quiz"])
app.include_router(memo_router, prefix="/api/memo", tags=["Memo"])

@app.get("/")
def health_check():
    return {"status": "ok", "message": "Debug Mind API is running"}
