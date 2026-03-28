from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    supabase_url: str
    supabase_service_role_key: str
    supabase_jwt_secret: str
    storage_bucket: str = "posts"

    class Config:
        env_file = ".env"


settings = Settings()
