from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import Field
from functools import lru_cache

class Settings(BaseSettings):
    # App
    ENV: str = "development"
    DEBUG: bool = True
    APP_NAME: str = "AI Revenue Recovery Controller"
    # DB Engine Selection (postgres or sqlite)
    DB_ENGINE: str = Field(default="sqlite")

    # DB - Postgres
    POSTGRES_USER: str = Field(default="postgres")
    POSTGRES_PASSWORD: str = Field(default="postgres")
    POSTGRES_SERVER: str = Field(default="localhost")
    POSTGRES_PORT: str = Field(default="5432")
    POSTGRES_DB: str = Field(default="razorpay_recovery")
    
    # DB - Mongo
    MONGO_URL: str = Field(default="mongodb://localhost:27017")
    MONGO_DB: str = Field(default="razorpay_audit")
    
    # Redis
    REDIS_URL: str = Field(default="redis://localhost:6379/0")
    
    # API Keys
    RAZORPAY_KEY_ID: str = Field(default="")
    RAZORPAY_KEY_SECRET: str = Field(default="")
    
    # LLM
    GEMINI_API_KEY: str = Field(default="")
    
    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8", case_sensitive=True)
    
    @property
    def async_database_url(self) -> str:
        if self.DB_ENGINE == "sqlite":
            return self.sqlite_database_url
        return f"postgresql+asyncpg://{self.POSTGRES_USER}:{self.POSTGRES_PASSWORD}@{self.POSTGRES_SERVER}:{self.POSTGRES_PORT}/{self.POSTGRES_DB}"
        
    @property
    def sqlite_database_url(self) -> str:
        return "sqlite+aiosqlite:///./razorpay_recovery.db"
        
@lru_cache
def get_settings() -> Settings:
    return Settings()
