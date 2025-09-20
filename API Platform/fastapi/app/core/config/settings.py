from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    litellm_base_url: str

    class Config:
        env_file = ".env"


settings = Settings()
