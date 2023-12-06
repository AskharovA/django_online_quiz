from django.apps import AppConfig


class GameConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'app.game'

    def ready(self):
        import app.game.signals
