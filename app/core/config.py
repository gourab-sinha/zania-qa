from pydantic_settings import BaseSettings
from functools import lru_cache

class Settings(BaseSettings):
    API_V1_STR: str = "/api/v1"
    PROJECT_NAME: str = "Question-Answering Bot API"
    OPENAI_API_KEY: str
    MODEL_NAME: str = "gpt-3.5-turbo"
    TEMPERATURE: float = 0
    CHUNK_SIZE: int = 1000
    CHUNK_OVERLAP: int = 200
    VECTOR_SEARCH_K: int = 3

    class Config:
        env_file = ".env"

@lru_cache()
def get_settings():
    return Settings()