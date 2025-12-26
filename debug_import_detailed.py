# debug_import_fixed.py
import sys
import os

print("=" * 70)
print("DETAILED IMPORT DEBUG - FIXED")
print("=" * 70)

# Текущая директория
print(f"\nCurrent directory: {os.getcwd()}")
print(f"Script directory: {os.path.dirname(os.path.abspath(__file__))}")

# Добавляем пути
sys.path.insert(0, os.getcwd())
print("\nPython path (first 10):")
for i, p in enumerate(sys.path[:10]):
    print(f"  [{i}] {p}")

print("\n" + "-" * 70)
print("STEP 1: Importing freppledb")
print("-" * 70)

try:
    # Пробуем найти модуль
    import importlib.util
    
    # Ищем freppledb
    module_path = None
    for root, dirs, files in os.walk('.'):
        if 'freppledb' in dirs and '__init__.py' in os.listdir(os.path.join(root, 'freppledb')):
            module_path = os.path.join(root, 'freppledb')
            break
    
    if module_path:
        abs_path = os.path.abspath(module_path)
        print(f"Found freppledb at: {abs_path}")
        if os.path.dirname(abs_path) not in sys.path:
            sys.path.insert(0, os.path.dirname(abs_path))
        
    # Пробуем импортировать
    import freppledb
    print(f"✓ freppledb imported from: {freppledb.__file__}")
    
    # Что внутри?
    print(f"\nContents of freppledb module (non-private attributes):")
    for item in dir(freppledb):
        if not item.startswith('_'):
            print(f"  - {item}")
    
except ImportError as e:
    print(f"✗ ImportError: {e}")
    print("\nSearching for module structure...")
    
    # Ищем все Python файлы с freppledb в имени
    found_files = []
    for root, dirs, files in os.walk('.'):
        for file in files:
            if file.endswith('.py') and 'freppledb' in file.lower():
                full_path = os.path.join(root, file)
                found_files.append(full_path)
    
    if found_files:
        print(f"Found {len(found_files)} freppledb-related files:")
        for f in found_files[:10]:  # Покажем первые 10
            print(f"  - {f}")
    else:
        print("No freppledb-related Python files found!")

print("\n" + "-" * 70)
print("STEP 2: Django setup")
print("-" * 70)

django_ok = False
try:
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'freppledb.settings')
    print(f"Django settings module: {os.environ['DJANGO_SETTINGS_MODULE']}")
    
    import django
    print(f"✓ Django imported: {django.__version__}")
    
    django.setup()
    print("✓ Django setup complete")
    django_ok = True
    
except Exception as e:
    print(f"✗ Django setup failed: {e}")
    import traceback
    traceback.print_exc()

print("\n" + "-" * 70)
print("STEP 3: Celery import and setup")
print("-" * 70)

try:
    from celery import Celery
    print(f"✓ Celery imported")
    
    # Пробуем создать приложение
    app = Celery('test_app')
    print(f"✓ Celery app created: {app.main}")
    
    if django_ok:
        # Пробуем получить конфигурацию из freppledb
        try:
            from freppledb import celery_app
            print(f"✓ Found celery_app in freppledb: {celery_app}")
        except ImportError:
            print("✗ No celery_app in freppledb module")
            
            # Пробуем найти в настройках Django
            from django.conf import settings
            print(f"\nChecking Django settings for Celery...")
            
            # Ищем CELERY_ настройки
            celery_settings = []
            for attr in dir(settings):
                if attr.startswith('CELERY_'):
                    celery_settings.append(attr)
            
            if celery_settings:
                print(f"Found {len(celery_settings)} Celery settings:")
                for attr in celery_settings[:5]:  # Первые 5
                    print(f"  {attr}: {getattr(settings, attr)}")
            else:
                print("No Celery settings found in Django settings")
                
except Exception as e:
    print(f"✗ Celery setup failed: {e}")
    import traceback
    traceback.print_exc()

print("\n" + "-" * 70)
print("STEP 4: Testing minimal worker startup")
print("-" * 70)

try:
    # Создаём минимальное Celery приложение
    from celery import Celery
    
    app = Celery('minimal_test')
    
    # Базовая конфигурация
    app.conf.update(
        broker_url='memory://',  # Используем in-memory брокер для теста
        result_backend='cache',
        cache_backend='memory',
        task_serializer='json',
        accept_content=['json'],
        result_serializer='json',
        timezone='UTC',
        worker_pool='solo',
    )
    
    print(f"✓ Minimal Celery app configured")
    print(f"  Broker: {app.conf.broker_url}")
    print(f"  Result backend: {app.conf.result_backend}")
    
    # Простая задача
    @app.task
    def test():
        return "Test successful"
    
    print("\nAttempting to start worker for 5 seconds...")
    
    import threading
    import time
    
    def run_worker():
        try:
            app.worker_main(['worker', '--loglevel=info', '--pool=solo'])
        except Exception as e:
            print(f"Worker error in thread: {e}")
    
    worker_thread = threading.Thread(target=run_worker, daemon=True)
    worker_thread.start()
    
    # Даём время на запуск
    for i in range(1, 6):
        time.sleep(1)
        if worker_thread.is_alive():
            print(f"  [{i}s] Worker is running...")
        else:
            print(f"  [{i}s] Worker stopped")
            break
    
    if worker_thread.is_alive():
        print("\n✓ SUCCESS: Worker is running!")
        print("Waiting 3 seconds then stopping...")
        time.sleep(3)
        # Выходим из скрипта, worker остановится как daemon thread
    else:
        print("\n✗ FAILED: Worker stopped immediately")
        
except Exception as e:
    print(f"✗ Worker test failed: {e}")
    import traceback
    traceback.print_exc()

print("\n" + "=" * 70)
print("DEBUG COMPLETE")
print("=" * 70)

# Ждём ввод для отладки
input("\nPress Enter to exit...")