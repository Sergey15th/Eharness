# technology/apps.py
from django.apps import AppConfig

class MyAppConfig(AppConfig):
    name = 'freppledb.qm'

    def ready(self):
        # Импортируем сигналы здесь, чтобы избежать circular imports
        from . import services