from django.apps import AppConfig

class TestbenchConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'freppledb.mqtt'
    def ready(self):
        # Импортируем сигналы здесь, чтобы избежать circular imports
        from . import services
        # Импортируем mqtt_tasks
        from . import mqtt_tasks
