import json
import random
import re
from vertexai.generative_models import GenerativeModel, GenerationConfig


def generate_cs_quiz(user_level: int):
    print(f"\n>>> [QUIZ] Lv.{user_level} 맞춤형 퀴즈 생성 시도...")

    try:
        # 1. 모델 설정: 응답 형식을 JSON으로 고정
        model = GenerativeModel("gemini-2.0-flash")
        config = GenerationConfig(response_mime_type="application/json")

        # 난이도 조절을 위한 가이드 추가
        difficulty = "기초" if user_level < 3 else "심화"

        prompt = f"""
        당신은 IT 기업의 면접관입니다. 
        Lv.{user_level} ({difficulty} 수준) 개발자에게 적합한 CS 면접 문제 1개를 내주세요.
        반드시 아래 JSON 형식으로만 답변하세요.
        형식: {{"question": "문제", "options": ["1번", "2번", "3번", "4번"], "answer_idx": 정답인덱스(0-3)}}
        """

        response = model.generate_content(prompt, generation_config=config)
        res_text = response.text.strip()

        # JSON만 추출하는 안전 로직
        json_match = re.search(r"\{.*\}", res_text, re.DOTALL)
        if json_match:
            return json.loads(json_match.group())
        return json.loads(res_text)

    except Exception as e:
        print(f"🚨 [QUIZ] AI 생성 실패(사유: {e}), 로컬 퀴즈로 대체합니다.")

        # 레벨별 퀴즈 뱅크 예시 (확장성 고려)
        quiz_bank = {
            "low": [
                {
                    "question": "HTTP 프로토콜에서 '403 Forbidden' 에러의 의미는?",
                    "options": [
                        "페이지 없음",
                        "권한 없음",
                        "서버 과부하",
                        "잘못된 요청",
                    ],
                    "answer_idx": 1,
                },
                {
                    "question": "파이썬의 'List'와 'Tuple'의 가장 큰 차이점은?",
                    "options": [
                        "속도 차이",
                        "데이터 타입 제한",
                        "가변성(Mutable) 여부",
                        "인덱싱 가능 여부",
                    ],
                    "answer_idx": 2,
                },
            ],
            "high": [
                {
                    "question": "OS에서 '데드락(Deadlock)' 발생 조건이 아닌 것은?",
                    "options": ["상호 배제", "점유와 대기", "선점 가능", "환형 대기"],
                    "answer_idx": 2,
                },
                {
                    "question": "B-Tree와 Binary Search Tree의 주요 차이점은?",
                    "options": [
                        "정렬 여부",
                        "노드당 자식 수",
                        "탐색 속도",
                        "데이터 저장 방식",
                    ],
                    "answer_idx": 1,
                },
            ],
        }

        category = "high" if user_level >= 3 else "low"
        return random.choice(quiz_bank[category])
