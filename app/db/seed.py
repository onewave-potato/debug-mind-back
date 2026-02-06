import json
import os
from sqlalchemy.orm import Session
from app.db.session import SessionLocal, engine, Base
from app.db.models import CSQuiz, SoftSkillQuestion

# 테이블 생성
Base.metadata.create_all(bind=engine)

def load_json_data(file_path):
    with open(file_path, 'r', encoding='utf-8') as f:
        return json.load(f)

def seed_from_json():
    db: Session = SessionLocal()
    try:
        # 1. CS 퀴즈 적재
        quiz_file = 'app/data/cs_quizzes.json'
        if os.path.exists(quiz_file):
            quizzes_data = load_json_data(quiz_file)
            quizzes = [CSQuiz(**item) for item in quizzes_data]
            db.bulk_save_objects(quizzes)
            print(f"CS 퀴즈 {len(quizzes)}개 적재 완료.")

        # 2. Soft Skill 질문 적재
        skill_file = 'app/data/soft_skills.json'
        if os.path.exists(skill_file):
            skills_data = load_json_data(skill_file)
            skills = [SoftSkillQuestion(**item) for item in skills_data]
            db.bulk_save_objects(skills)
            print(f"Soft Skill 질문 {len(skills)}개 적재 완료.")

        db.commit()
    except Exception as e:
        print(f"데이터 적재 중 오류 발생: {e}")
        db.rollback()
    finally:
        db.close()

if __name__ == "__main__":
    seed_from_json()