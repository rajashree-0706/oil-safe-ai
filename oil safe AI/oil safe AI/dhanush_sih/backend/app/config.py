import os

class Settings:
    PROJECT_NAME: str = "OIL-SAFE AI"
    VERSION: str = "1.0.0"
    API_V1_STR: str = "/api"
    SECRET_KEY: str = os.getenv("SECRET_KEY", "oilsafe_super_secret_jwt_key_2026_refinery_safety_command_center")
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 24 # 24 hours
    DATABASE_URL: str = os.getenv("DATABASE_URL", "sqlite:///./oil_safe_ai.db")
    USE_PGVECTOR: bool = os.getenv("USE_PGVECTOR", "false").lower() == "true"
    ENVIRONMENT: str = os.getenv("ENVIRONMENT", "development")
    CORS_ORIGINS: list = ["*"]
    STATIC_DIR: str = os.getenv("STATIC_DIR", os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "static"))

settings = Settings()
