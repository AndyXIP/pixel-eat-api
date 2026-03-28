from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    supabase_url: str
    supabase_service_role_key: str
    supabase_jwt_secret: str
    storage_bucket: str = "posts"
    base_url: str = "http://127.0.0.1:8000"

    class Config:
        env_file = ".env"


settings = Settings()
