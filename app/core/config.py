from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    database_url: str = "sqlite+aiosqlite:///./app.db"
    title_app: str = "API hitalent"


    class Config:
        env_file = ".env"


settings = Settings()