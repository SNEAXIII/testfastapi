from pydantic_settings import BaseSettings, SettingsConfigDict
from os.path import join
class Settings(BaseSettings):
    APP_SECRET_STRING:str
    USER:str
    PASSWORD:str
    DATABASE:str
    DATABASE_HOST:str
    DATABASE_PORT:int
    BULK_INSERT_NUMBER:int
    DATA_PATH:str
    DATA_CSV:str
    DB_CONNECTION_RETRY:int
    DB_CONNECTION_TIMEOUT:int
    model_config = SettingsConfigDict(env_file="api.env")

settings = Settings()
BULK_INSERT_NUMBER = settings.BULK_INSERT_NUMBER
CSV_PATH = join(settings.DATA_PATH,settings.DATA_CSV)
DB_CONNECTION_RETRY = settings.DB_CONNECTION_RETRY
DB_CONNECTION_TIMEOUT = settings.DB_CONNECTION_TIMEOUT