from pydantic_settings import BaseSettings, SettingsConfigDict
import os

from dotenv import load_dotenv

load_dotenv()

class Settings(BaseSettings):
    DB_HOST: str
    DB_PORT: int
    DB_USER: str
    DB_PASS: str
    DB_NAME: str
    BOT_TOKEN: str
    API_KEY: str
    
    @property
    def DATABASE_URL_psycopg(self):
        return f"postgresql+psycopg://{self.DB_USER}:{self.DB_PASS}@{self.DB_HOST}:{self.DB_PORT}/{self.DB_NAME}"
    
    model_config = SettingsConfigDict(env_file="test_work/.env")  
    
settings = Settings()


