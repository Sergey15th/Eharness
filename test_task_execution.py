import os
import sys
import logging

# Включаем подробное логирование
logging.basicConfig(level=logging.DEBUG)

print("=" * 70)
print("Testing task execution")
print("=" * 70)

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'freppledb.settings')

import django
django.setup()

from freppledb.celery import app as celery_app

# Находим задачу
task_name = 'freppledb.testbench.tasks.publish_led_command'
task_func = celery_app.tasks.get(task_name)

if not task_func:
    print(f"✗ Task {task_name} not found!")
    print(f"Available tasks: {list(celery_app.tasks.keys())}")
    sys.exit(1)

print(f"✓ Task found: {task_name}")

# Проверяем, есть ли зависимости
print("\nChecking imports...")
try:
    import importlib
    
    # Пробуем импортировать модуль задачи
    module_name = 'freppledb.testbench.tasks'
    module = importlib.import_module(module_name)
    print(f"✓ Module imported: {module_name}")
    
    # Проверяем импорт paho.mqtt
    try:
        import paho.mqtt.publish as mqtt_publish
        print("✓ paho.mqtt is available")
    except ImportError:
        print("✗ paho.mqtt is NOT available")
        print("Install with: pip install paho-mqtt")
        
except Exception as e:
    print(f"✗ Import error: {e}")
    import traceback
    traceback.print_exc()

# Запускаем задачу синхронно (не через Celery)
print("\n" + "=" * 70)
print("Testing task execution DIRECTLY (not through Celery)")
print("=" * 70)

try:
    # Получаем оригинальную функцию (без celery декоратора)
    if hasattr(task_func, '__wrapped__'):
        original_func = task_func.__wrapped__
        print("✓ Got original function")
        
        # Пробуем выполнить
        print("Executing function directly...")
        result = original_func("test_led", "on")
        print(f"✓ Direct execution result: {result}")
    else:
        print("✗ Cannot get original function")
        
except Exception as e:
    print(f"✗ Direct execution failed: {e}")
    import traceback
    traceback.print_exc()

# Тестируем через Celery
print("\n" + "=" * 70)
print("Testing task execution via Celery")
print("=" * 70)

try:
    # Отправляем задачу
    print("Sending task to Celery...")
    result = task_func.delay("test_led", "on")
    print(f"✓ Task sent. ID: {result.id}")
    
    # Ждем результат (с ignore_result=True результат будет None)
    import time
    for i in range(1, 11):
        time.sleep(1)
        if result.ready():
            print(f"✓ Task completed in {i} seconds")
            # Даже с ignore_result=True можем проверить состояние
            print(f"  Task state: {result.state}")
            break
        else:
            print(f"  [{i}s] Task still pending...")
    
    if not result.ready():
        print("✗ Task timed out after 10 seconds")
        
except Exception as e:
    print(f"✗ Celery task submission failed: {e}")
    import traceback
    traceback.print_exc()