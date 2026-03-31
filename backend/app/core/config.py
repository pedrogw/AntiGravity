from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    PROJECT_NAME: str = "Logistics Manager API"
    DATABASE_URL: str = "postgresql+asyncpg://user:password@db:5432/logistics"
    SECRET_KEY: str = "logistics_secret_key_tcc_only"
    ALGORITHM: str = "HS256"

    class Config:
        case_sensitive = True
        env_file = ".env"

settings = Settings()
