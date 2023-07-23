from pydantic_settings import BaseSettings, SettingsConfigDict



class SettingsModel(BaseSettings):
    database_name: str
    database_file: str
    host:str
    user:str
    password:str
    secret_key:str
    access_token_expire_mins:int

    model_config = SettingsConfigDict(env_file=".env")



envvars = SettingsModel()