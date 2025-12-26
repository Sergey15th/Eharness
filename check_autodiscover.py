# check_autodiscover.py
import os
import sys

print("=" * 70)
print("Checking Celery Autodiscover")
print("=" * 70)

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'freppledb.settings')

import django
django.setup()

from freppledb.celery import app as celery_app

print(f"Celery app: {celery_app.main}")

# Проверим autodiscover_tasks
print("\nTrying autodiscover_tasks()...")
try:
    celery_app.autodiscover_tasks()
    print("✓ autodiscover_tasks() executed")
except Exception as e:
    print(f"✗ autodiscover_tasks() failed: {e}")

# Проверим с указанием пакетов
print("\nTrying autodiscover_tasks with packages...")
try:
    celery_app.autodiscover_tasks(['freppledb'])
    print("✓ autodiscover_tasks(['freppledb']) executed")
except Exception as e:
    print(f"✗ Failed: {e}")

# Проверим задачи
print(f"\nTasks after autodiscover: {len(celery_app.tasks)}")
frepple_tasks = [t for t in celery_app.tasks.keys() if 'freppledb' in t]
print(f"frePPLe tasks: {len(frepple_tasks)}")
for task in frepple_tasks:
    print(f"  - {task}")

if len(frepple_tasks) == 0:
    print("\n⚠️ No frePPLe tasks found. Manually importing...")
    
    # Вручную импортируем модули
    modules = [
        'freppledb.testbench',
        'freppledb.execute',
        'freppledb.common',
        'freppledb.input',
        'freppledb.output',
    ]
    
    for module_name in modules:
        try:
            __import__(f'{module_name}.tasks')
            print(f"✓ Imported {module_name}.tasks")
        except ImportError:
            try:
                __import__(module_name)
                print(f"✓ Imported {module_name}")
            except ImportError as e:
                print(f"✗ Cannot import {module_name}: {e}")
    
    print(f"\nTasks after manual import: {len(celery_app.tasks)}")
    for task in celery_app.tasks:
        if 'freppledb' in task:
            print(f"  - {task}")