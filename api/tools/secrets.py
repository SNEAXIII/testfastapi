from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    APP_SECRET_STRING:str
    USER:str
    PASSWORD:str
    DATABASE:str
    DATABASE_HOST:str
    DATABASE_PORT:int

    model_config = SettingsConfigDict(env_file="api.env")

settings = Settings()