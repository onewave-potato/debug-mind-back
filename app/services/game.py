import sqlite3
import os

# 1. DB 경로 설정 (프로젝트 루트의 debug_mind.db를 정확히 가리킵니다)
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
# app/services 위치에서 상위(app), 그 상위(root)로 이동
DB_PATH = os.path.abspath(os.path.join(BASE_DIR, "..", "..", "debug_mind.db"))

# 2. 레벨 데이터 정의 (B 담당 미션: 성장 수치 및 캐릭터 외형)
LEVEL_DATA = {
    1: {"title": "코딩 독학러", "avatar": "lv1_home.png"},
    2: {"title": "전공 학부생", "avatar": "lv2_univ.png"},
    3: {"title": "부트캠프 수료생", "avatar": "lv3_camp.png"},
    4: {"title": "주니어 개발자", "avatar": "lv4_office.png"},
    5: {"title": "시니어 개발자", "avatar": "lv5_lead.png"},
}


def add_routine_xp(user_id: int, mission_type: str, rank: str = None):
    """
    유저의 미션(퀴즈, 코드 분석 등) 완료에 따른 경험치를 지급하고 레벨업을 계산합니다.
    """
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()

    # 경험치 산정 로직
    if mission_type == "code_analysis":
        # 랭크별 경험치: S(50), A(30), B(15), C(5)
        xp_map = {"S": 50, "A": 30, "B": 15, "C": 5}
        earned_xp = xp_map.get(rank, 10)
    elif mission_type == "cs":
        earned_xp = 8  # 퀴즈 정답 시 8점
    else:
        earned_xp = 10  # 기타(메모 등) 10점

    try:
        # 1. 현재 유저 정보 조회
        cursor.execute("SELECT level, exp FROM users WHERE id = ?", (user_id,))
        user = cursor.fetchone()

        if not user:
            return {"status": "error", "message": "유저를 찾을 수 없습니다."}

        current_level = user["level"]
        new_exp = user["exp"] + earned_xp
        new_level = current_level

        # 2. 레벨업 로직 (100점당 1레벨업)
        while new_exp >= 100:
            new_level += 1
            new_exp -= 100

        # 3. DB 업데이트 (미션 타입에 따라 완료 여부 체크)
        done_column = "daily_quiz_done" if mission_type == "cs" else "daily_memo_done"
        if (
            mission_type == "code_analysis"
        ):  # 코드 분석은 별도 컬럼이 없으므로 경험치만 업데이트
            update_query = f"UPDATE users SET exp = ?, level = ? WHERE id = ?"
            cursor.execute(update_query, (new_exp, new_level, user_id))
        else:
            update_query = (
                f"UPDATE users SET exp = ?, level = ?, {done_column} = 1 WHERE id = ?"
            )
            cursor.execute(update_query, (new_exp, new_level, user_id))

        conn.commit()

        return {
            "status": "success",
            "earned_xp": earned_xp,
            "current_level": new_level,
            "current_exp": new_exp,
            "title": LEVEL_DATA.get(new_level, LEVEL_DATA[5])["title"],
            "is_levelup": new_level > current_level,
        }

    except Exception as e:
        conn.rollback()
        return {"status": "error", "message": str(e)}
    finally:
        conn.close()


def get_user_status(user_id: int):
    """
    DB에서 유저의 현재 스탯을 조회하여 대시보드용 데이터를 반환합니다.
    """
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM users WHERE id = ?", (user_id,))
    user = cursor.fetchone()
    conn.close()

    if not user:
        return None

    current_level = user["level"]
    avatar_info = LEVEL_DATA.get(current_level, LEVEL_DATA[1])

    return {
        "nickname": user["github_id"],  # ✅ 'nickname' 대신 'github_id'를 사용합니다.
        "level": current_level,
        "exp": user["current_exp"],  # ✅ 'exp' 대신 'current_exp'를 사용합니다.
        "title": avatar_info["title"],
        "avatar_url": avatar_info["avatar"],
        "daily_quiz_done": False,  # 일단 기본값
        "daily_memo_done": False,
        "oss_bonus_done": False,
    }
