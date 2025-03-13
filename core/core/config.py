from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    SQLALCHEMY_DATABASE_URL: str
    REDIS_URL: str
    JWT_SECRET_KEY: str = "env_jwt_secret_token"

    model_config = SettingsConfigDict(env_file=".env")


settings = Settings()
