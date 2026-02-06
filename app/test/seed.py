from sqlalchemy.orm import Session
from app.db.session import SessionLocal, engine, Base
from app.db.models import CSQuiz
import json

def seed_data():
    Base.metadata.create_all(bind=engine)
    db: Session = SessionLocal()
    
    # 중복 삽입 방지를 위해 기존 데이터 확인
    if db.query(CSQuiz).first():
        print("Seed data already exists.")
        return

    quizzes = [
        CSQuiz(
            question="가상 메모리 시스템에서 페이지 폴트(Page Fault)란 무엇입니까?",
            options=json.dumps(["프로세스가 물리 메모리에 없는 페이지에 접근할 때 발생", "CPU가 고장 났을 때 발생", "디스크 용량이 부족할 때 발생", "네트워크 연결이 끊겼을 때 발생"]),
            answer="프로세스가 물리 메모리에 없는 페이지에 접근할 때 발생",
            category="OS"
        ),
        CSQuiz(
            question="TCP와 UDP의 주요 차이점은 무엇입니까?",
            options=json.dumps(["TCP는 연결 지향적이고 신뢰성을 보장함", "UDP는 데이터 순서를 보장함", "TCP가 UDP보다 속도가 빠름", "UDP는 3-way handshake를 사용함"]),
            answer="TCP는 연결 지향적이고 신뢰성을 보장함",
            category="Network"
        )
    ]

    try:
        db.add_all(quizzes)
        db.commit()
        print("Seed data inserted successfully!")
    except Exception as e:
        db.rollback()
        print(f"Error seeding data: {e}")
    finally:
        db.close()

if __name__ == "__main__":
    seed_data()