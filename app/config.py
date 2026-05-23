from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    BOT_TOKEN: str
    OPENAI_API_KEY: str

    # Модель ИИ. Значение зададим на Bothost в переменных окружения.
    OPENAI_MODEL: str = "gpt-4o-mini"

    # Данные для входа в Tilda
    TILDA_LOGIN: str | None = None
    TILDA_PASSWORD: str | None = None

    # Ссылка на проект Tilda
    # Пример: https://tilda.cc/projects/?projectid=1234567
    TILDA_PROJECT_URL: str | None = None

    # На сервере браузер должен запускаться без окна
    HEADLESS: bool = True

    class Config:
        env_file = ".env"


settings = Settings()
