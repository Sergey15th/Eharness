"""Celery application for freppledb.

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
    app.conf.broker_url = getattr(settings, "BROKER_URL", None) or getattr(
        settings, "CELERY_BROKER_URL", None
    )
if not app.conf.result_backend:
    app.conf.result_backend = getattr(settings, "RESULT_BACKEND", None) or getattr(
        settings, "CELERY_RESULT_BACKEND", None
    )

# Autodiscover tasks from installed apps
app.autodiscover_tasks()


__all__ = ("app", "Celery")
