# app/core/config.py
from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    # Cloud SQL (PostgreSQL) 접속 정보
    DATABASE_URL: str
    
    # GitHub Webhook 검증용 시크릿
    GITHUB_WEBHOOK_SECRET: str
    
    # Pydantic이 .env 파일을 읽어오도록 설정
    model_config = SettingsConfigDict(env_file=".env")

settings = Settings()