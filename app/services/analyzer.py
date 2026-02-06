import os
import json
import re
import vertexai
from vertexai.generative_models import GenerativeModel, GenerationConfig
from dotenv import load_dotenv

# 1. [.env 로드 경로 수정]
# 현재 파일 위치(app/services)에서 두 단계 위(root)에 있는 .env를 찾습니다.
base_dir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
load_dotenv(os.path.join(base_dir, ".env"))

# 2. [GCP 초기화] 환경 변수에서 프로젝트 ID를 가져옵니다.
PROJECT_ID = os.getenv("PROJECT_ID")
LOCATION = "asia-northeast3"  # 서울 리전

vertexai.init(project=PROJECT_ID, location=LOCATION)


def analyze_code_with_ai(code_patch: str):
    """실제로 Vertex AI를 사용하여 코드 품질을 분석합니다."""
    try:
        # 모델 설정: Gemini 2.0 Flash (비용 효율적)
        model = GenerativeModel("gemini-2.0-flash")

        config = GenerationConfig(
            response_mime_type="application/json", temperature=0.2
        )

        prompt = f"""
        당신은 구글 출신의 테크 리드입니다. 
        취업 준비생이 제출한 다음 파이썬 코드를 분석하여 반드시 JSON으로 응답하세요.
        
        응답 형식:
        {{
            "rank": "S/A/B/C",
            "review": "냉철한 피드백 한마디",
            "improvements": ["개선점1", "개선점2"]
        }}

        분석할 코드:
        {code_patch}
        """

        response = model.generate_content(prompt, generation_config=config)

        # JSON 추출 안전 로직
        res_text = response.text.strip()
        json_match = re.search(r"\{.*\}", res_text, re.DOTALL)
        result = json.loads(json_match.group()) if json_match else json.loads(res_text)

        return result

    except Exception as e:
        print(f"🚨 [AI 에러] : {e}")
        # 에러 발생 시 서비스 중단을 막기 위한 기본값
        return {
            "rank": "B",
            "review": "AI 분석 중 일시적인 오류가 발생했습니다.",
            "improvements": ["코드가 정상적으로 실행되는지 확인해 보세요."],
        }
