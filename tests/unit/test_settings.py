from media_bot.config.settings import BotSettings, DatabaseSettings


def test_bot_settings_load_bot_token():
    """BotSettings should load the bot token from the configured environment."""
    settings = BotSettings()

    assert settings.bot_token


def test_database_settings_load_test_database_url():
    """DatabaseSettings should load the database URL from `.env.test`.

    The test explicitly selects the test dotenv file instead of relying on
    process-wide environment variables. This keeps the test deterministic
    and makes it clear that integration tests are intentionally configured
    against the dedicated test database.
    """
    settings = DatabaseSettings(_env_file=".env.test")

    assert settings.database_url
