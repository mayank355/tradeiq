from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    # Postgres
    database_url: str = "postgresql://tradeiq_user:tradeiq_pass@localhost:5432/tradeiq_db"

    # Redis
    redis_url: str = "redis://localhost:6379/0"

    # Groq
    groq_api_key: str = "your_key_here"

    # Alpha Vantage
    alpha_vantage_api_key: str = "your_key_here"

    # App
    app_name: str = "TradeIQ"
    debug: bool = True

    class Config:
        env_file = ".env"


settings = Settings()
