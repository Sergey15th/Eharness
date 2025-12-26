# find_task.py
import os
import sys

print("=" * 70)
print("Finding frePPLe tasks")
print("=" * 70)

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

# Ищем все файлы с задачами
for root, dirs, files in os.walk('.'):
    for file in files:
        if file.endswith('.py') and 'task' in file.lower():
            filepath = os.path.join(root, file)
            try:
                with open(filepath, 'r', encoding='utf-8', errors='ignore') as f:
                    content = f.read()
                    if 'publish_led_command' in content:
                        print(f"Found 'publish_led_command' in: {filepath}")
                        
                        # Покажем контекст
                        lines = content.split('\n')
                        for i, line in enumerate(lines):
                            if 'publish_led_command' in line:
                                start = max(0, i-3)
                                end = min(len(lines), i+4)
                                print(f"\nContext (lines {start+1}-{end+1}):")
                                for j in range(start, end):
                                    print(f"{j+1:4}: {lines[j]}")
                                print()
            except:
                pass

# Проверим структуру модулей
print("\n" + "=" * 70)
print("Checking module structure")
print("=" * 70)

try:
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'freppledb.settings')
    import django
    django.setup()
    
    # Пробуем импортировать testbench
    try:
        import freppledb.testbench
        print(f"✓ freppledb.testbench imported from: {freppledb.testbench.__file__}")
        
        # Проверим содержимое
        if hasattr(freppledb.testbench, '__all__'):
            print(f"  __all__: {freppledb.testbench.__all__}")
            
        # Проверим есть ли tasks
        try:
            import freppledb.mqtt.mqtt_tasks
            print(f"✓ freppledb.testbench.tasks imported from: {freppledb.mqtt.mqtt_tasks.__file__}")
            
            # Посмотрим что в модуле
            import inspect
            members = inspect.getmembers(freppledb.mqtt.mqtt_tasks)
            print(f"  Members in tasks module:")
            for name, obj in members:
                if not name.startswith('_'):
                    print(f"    - {name}: {type(obj).__name__}")
                    
        except ImportError as e:
            print(f"✗ Cannot import freppledb.testbench.tasks: {e}")
            
    except ImportError as e:
        print(f"✗ Cannot import freppledb.testbench: {e}")
        
except Exception as e:
    print(f"Error: {e}")
    import traceback
    traceback.print_exc()