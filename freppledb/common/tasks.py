"""Example Celery tasks for freppledb.common."""
from __future__ import annotations

from . import models
from datetime import datetime

try:
    from freppledb.celery import app
except Exception:
    # Celery not available in this environment; create a dummy decorator
    def task(*args, **kwargs):
        def _f(f):
            return f

        return _f

    app = None


@app.task(bind=True, name="freppledb.common.example_add")
def example_add(self, a, b):
    """Simple example task: adds two numbers and logs a timestamp.

    This demonstrates how to define a task in the project.
    """
    now = datetime.now().isoformat()
    return {"result": a + b, "when": now}
