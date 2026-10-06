from pydantic_settings import BaseSettings, SettingsConfigDict


class BotSettings(BaseSettings):
    """Application settings required by the Telegram bot.

    This settings model intentionally contains only bot-related
    configuration. Keeping configuration domain-specific prevents
    unrelated components from requiring environment variables they
    do not actually use.

    Pydantic Settings reads values from environment variables and,
    when configured below, from the local `.env` file. Environment
    variables take precedence over values loaded from the dotenv file.
    """

    bot_token: str
    """Telegram Bot API token used to authenticate the bot."""

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
    )


class DatabaseSettings(BaseSettings):
    """Application settings required for database access.

    Database configuration is kept separate from bot configuration so
    database infrastructure and database tests can be initialized
    without requiring unrelated bot credentials.

    The `.env` file is the default configuration source. Tests can
    provide a different dotenv file at construction time, for example:

        DatabaseSettings(_env_file=".env.test")

    This uses Pydantic Settings' built-in environment-file override
    rather than modifying process-wide environment variables.
    """

    database_url: str
    """SQLAlchemy database URL used to create the async engine."""

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
    )
