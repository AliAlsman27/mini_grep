from pydantic_settings import BaseSettings

class settings(BaseSettings):

    


    App_name: str 
    App_version: str

    FILE_ALLOWED_EXTENSIONS: list
    FILE_MAX_SIZE: int
    FILE_DEFAULT_CHUNK_SIZE: int
    


    class Config:
        env_file = "src/.env"


def get_settings():
    return settings()