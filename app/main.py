import os
from fastapi import FastAPI
from pydantic import BaseModel  # BaseModel은 pydantic에서 가져와야 합니다!
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv

# 1. A 개발자님 DB/API 설정 임포트
from app.db.session import engine
from app.db import models
from app.api.quiz import router as quiz_router
from app.api.memo import router as memo_router

# 2. B 담당(팀장님) 성장 엔진 임포트
from app.services.analyzer import analyze_code_with_ai
from app.services.game import add_routine_xp, get_user_status

# .env 파일 로드
load_dotenv()

# 앱 시작 시 DB 테이블 자동 생성
models.Base.metadata.create_all(bind=engine)

app = FastAPI(title="Debug Mind API", description="취업 성공을 위한 백엔드 성장 엔진")

# ✅ CORS 설정 (A/B 통합 설정)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ✅ 라우터 등록 (기존 A 담당 API)
app.include_router(quiz_router, prefix="/api/quiz", tags=["Quiz"])
app.include_router(memo_router, prefix="/api/memo", tags=["Memo"])

# --- B 담당: AI 코드 분석 및 대시보드 로직 시작 ---


class CodeRequest(BaseModel):
    user_id: int = 1
    code: str


@app.get("/")
def health_check():
    return {"status": "ok", "message": "Debug Mind API is running and healthy"}


@app.post("/analyze")
async def analyze_code(request: CodeRequest):
    """B 담당 미션: AI 분석 결과에 따라 DB에 경험치 반영"""
    # 1. Vertex AI 분석 수행
    analysis_result = analyze_code_with_ai(request.code)

    # 2. 결과(Rank)에 따라 DB 경험치 업데이트 (game.py 연동)
    growth_data = add_routine_xp(
        user_id=request.user_id,
        mission_type="code_analysis",
        rank=analysis_result["rank"],
    )
    return {"status": "success", "analysis": analysis_result, "growth": growth_data}


@app.get("/total-dashboard")
async def get_dashboard(user_id: int = 1):
    """B 담당 미션: 유저 실시간 상태 및 캐릭터 외형 조회"""
    user_stats = get_user_status(user_id)
    return {
        "user_info": {
            "nickname": user_stats["nickname"],
            "level": user_stats["level"],
            "title": user_stats["title"],
            "avatar": user_stats["avatar_url"],
        },
        "xp_info": {
            "current_xp": user_stats["exp"],
            "next_level_xp": 100,
            "progress_rate": f"{user_stats['exp']}/100",
        },
        "mission_status": {
            "quiz": bool(user_stats["daily_quiz_done"]),
            "memo": bool(user_stats["daily_memo_done"]),
            "oss": bool(user_stats["oss_bonus_done"]),
        },
    }
