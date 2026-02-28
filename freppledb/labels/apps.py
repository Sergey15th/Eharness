# labels/apps.py
from django.apps import AppConfig

class MyAppConfig(AppConfig):
    name = 'freppledb.labels'

    def ready(self):
        # Импортируем сигналы здесь, чтобы избежать circular imports
        from . import services