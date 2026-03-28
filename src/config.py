from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    supabase_url: str
    supabase_service_key: str
    storage_bucket: str = "posts"
    base_url: str = "http://127.0.0.1:8000"

    class Config:
        env_file = ".env"


settings = Settings()
