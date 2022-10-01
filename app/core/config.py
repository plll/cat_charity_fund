from pydantic import BaseSettings


class Settings(BaseSettings):
    app_title: str = 'Проект по сбору средств для котиков'
    database_url: str = 'sqlite+aiosqlite:///./cat_charity.db'
    secret: str = 'SECRET'

    class Config:
        env_file = '.env'


settings = Settings()