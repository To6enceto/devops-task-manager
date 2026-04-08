from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    database_url: str = "postgresql+asyncpg://postgres:postgres@localhost:5432/taskmanager"
    log_level: str = "INFO"
    app_name: str = "DevOps Task Manager"

    model_config = {"env_prefix": "", "case_sensitive": False}


settings = Settings()
