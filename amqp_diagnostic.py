# amqp_diagnostic_fixed.py
import os
import sys
import pika

print("=" * 70)
print("RabbitMQ/AMQP Diagnostic - Fixed")
print("=" * 70)

# 1. Проверяем RabbitMQ соединение
print("\n1. Testing RabbitMQ connection...")

broker_url = 'amqp://celery:yfB-h84-4tF-6uH@localhost:5672/celery'
print(f"URL: {broker_url}")

try:
    credentials = pika.PlainCredentials('celery', 'yfB-h84-4tF-6uH')
    parameters = pika.ConnectionParameters(
        host='localhost',
        port=5672,
        virtual_host='celery',
        credentials=credentials,
        socket_timeout=5,
        heartbeat=600
    )
    
    connection = pika.BlockingConnection(parameters)
    print("✓ Connection successful!")
    
    # Проверяем канал
    channel = connection.channel()
    print("✓ Channel created")
    
    # Пробуем объявить очередь (как делает Celery)
    try:
        result = channel.queue_declare(
            queue='celery',  # Имя очереди по умолчанию
            durable=True,
            exclusive=False,
            auto_delete=False
        )
        print(f"✓ Queue 'celery' declared")
    except Exception as e:
        print(f"✗ Queue declaration failed: {e}")
        # Пробуем временную очередь
        result = channel.queue_declare(queue='', exclusive=True)
        print(f"✓ Temporary queue created: {result.method.queue}")
    
    connection.close()
    print("✓ Connection closed properly")
    
except Exception as e:
    print(f"✗ Connection failed: {e}")
    import traceback
    traceback.print_exc()

# 2. Тестируем Celery конфигурацию
print("\n2. Testing Celery configuration...")

try:
    sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'freppledb.settings')
    
    import django
    django.setup()
    
    from freppledb import celery_app
    
    print(f"✓ Celery app loaded: {celery_app.main}")
    print(f"  Broker URL in app: {celery_app.conf.broker_url}")
    print(f"  Result backend: {celery_app.conf.result_backend}")
    
    # Проверяем задачи
    print(f"\n3. Checking registered tasks...")
    task_count = len(celery_app.tasks)
    print(f"  Total tasks registered: {task_count}")
    
    if task_count > 0:
        print("  First 5 tasks:")
        for i, task_name in enumerate(list(celery_app.tasks.keys())[:5]):
            print(f"    {i+1}. {task_name}")
    
except Exception as e:
    print(f"✗ Celery setup failed: {e}")
    import traceback
    traceback.print_exc()

# 3. Тест минимального Celery worker
print("\n4. Testing minimal Celery worker startup...")

try:
    from celery import Celery
    
    # Создаем тестовое приложение
    test_app = Celery('test_app')
    
    test_app.conf.update(
        broker_url='amqp://celery:yfB-h84-4tF-6uH@localhost:5672/celery',
        result_backend='rpc://',
        task_serializer='json',
        result_serializer='json',
        accept_content=['json'],
        timezone='UTC',
        broker_connection_timeout=30,
        broker_heartbeat=10,
    )
    
    print(f"✓ Test app created")
    print(f"  Broker: {test_app.conf.broker_url}")
    
    # Простая тестовая задача
    @test_app.task
    def test_task(x, y):
        return x + y
    
    print("✓ Test task registered")
    
    # Пробуем запустить worker на 5 секунд
    print("\nAttempting to start test worker for 5 seconds...")
    
    import threading
    import time
    
    def run_test_worker():
        try:
            test_app.worker_main([
                'worker',
                '--loglevel=info',
                '--pool=solo',
                '--hostname=test_worker@%h',
                '--without-mingle',
                '--without-gossip'
            ])
        except Exception as e:
            print(f"Test worker error: {e}")
    
    worker_thread = threading.Thread(target=run_test_worker, daemon=True)
    worker_thread.start()
    
    # Ждем
    for i in range(1, 6):
        time.sleep(1)
        if worker_thread.is_alive():
            print(f"  [{i}s] Test worker is running...")
        else:
            print(f"  [{i}s] Test worker stopped")
            break
    
    if worker_thread.is_alive():
        print("\n✓ SUCCESS! Test worker is running with AMQP")
        # Можно остановить тут
    else:
        print("\n✗ Test worker failed to start")
        
except Exception as e:
    print(f"✗ Test failed: {e}")
    import traceback
    traceback.print_exc()

print("\n" + "=" * 70)
print("Diagnostic complete")
print("=" * 70)