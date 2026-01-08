# news_app/apps.py
from django.apps import AppConfig


class NewsAppConfig(AppConfig):
    """
    Docstring for NewsAppConfig
    """
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'news_app'

    def ready(self):
        import news_app.signals  # ensures signals are registered
