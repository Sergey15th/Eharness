"""Celery application for freppledb.
Start worker:
celery -A freppledb worker -E --loglevel=debug -P eventlet -c 5 --hostname=worker1@%h
 
This follows the Django recommended setup. It reads broker/backend
configuration from Django settings (BROKER_URL/BROKER or CELERY_ prefix)
and exposes the app as `app` and `celery_app`.
"""
from __future__ import annotations

import os
from celery import Celery

# set the default Django settings module for the 'celery' program.
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "freppledb.settings")

from django.conf import settings

# Create the Celery app instance
app = Celery("freppledb")

# Load configuration from Django settings. Prefer `CELERY_` prefixed keys
# but also support a `BROKER_URL`/`RESULT_BACKEND` style.
app.config_from_object("django.conf:settings", namespace="CELERY")

# Fallbacks for older style names
if not app.conf.broker_url:
    app.conf.broker_url = getattr(settings, "BROKER_URL", None) or getattr(settings, "CELERY_BROKER_URL", None)
if not app.conf.result_backend:
    app.conf.result_backend = getattr(settings, "RESULT_BACKEND", None) or getattr(settings, "CELERY_RESULT_BACKEND", None)

# Autodiscover tasks from installed apps

app.conf.update(
    task_serializer='json',
    accept_content=['json'],
    result_serializer='json',
    timezone='Europe/Moscow',
    enable_utc=True,
    task_routes={
        'mqtt_tasks.publish_mqtt_message': {'queue': 'default'},
        'mqtt_tasks.publish_mqtt_batch': {'queue': 'default'},
    },
    task_acks_late=True,
    worker_prefetch_multiplier=1,
    task_default_queue='default',
    worker_max_tasks_per_child=1000,  # Перезапуск воркера после 1000 задач
)

from celery.schedules import crontab

app.conf.beat_schedule = {
    # Проверка здоровья каждые 5 минут
    'mqtt-health-check-every-30-sec': {
        'task': 'freppledb.mqtt.mqtt_tasks.health_check',  # Полный путь к задаче
        'schedule': 30.0,  # Каждые 30 секунд (0.5 минут)
        'options': {'queue': 'monitoring'},  # Опционально: отправлять в очередь monitoring
    },
    # Более сложный пример: проверка каждый день в 9 утра
    #'daily-morning-check': {
    #    'task': 'your_project.tasks.health_check',
    #    'schedule': crontab(hour=9, minute=0),
    #    'args': (),  # Можно передать аргументы, если функция их принимает
    #},
}

app.autodiscover_tasks()
__all__ = ("app", "Celery")