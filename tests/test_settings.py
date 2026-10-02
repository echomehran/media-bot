from music_bot.config.settings import Settings


def test_settings_load_bot_token():
    settings = Settings()

    assert settings.bot_token