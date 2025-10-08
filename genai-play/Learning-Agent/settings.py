try:
    from pydantic_settings import BaseSettings
except ImportError:
    import os
    os.system('pip install pydantic-settings')
    from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    base_url: str
    API_KEY: str
    class Config:
        env_file = ".env"
