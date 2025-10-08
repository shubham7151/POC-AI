try:
    from pydantic_settings import BaseSettings
except ImportError:
    import os
    os.system('pip install pydantic-settings')
    from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    db_name: str
    db_port: int
    db_user: str
    db_password: str
    db_host: str = "localhost"

    class Config:
        env_file = ".env"
