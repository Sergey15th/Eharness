import logging
logger = logging.getLogger(__name__)

try:
    # Local import so it doesn't break environments without celery installed
    from freppledb.celery import app as celery_app  # noqa: F401
        # Вручную импортируем модули
    logger.info("\n⚠️ Manually importing tasks...")
    modules = [
        'freppledb.testbench',
    ]
    
    for module_name in modules:
        try:
            __import__(f'{module_name}.tasks')
            logger.info(f"✓ Imported {module_name}.tasks")
        except ImportError:
            try:
                __import__(module_name)
                logger.info(f"✓ Imported {module_name}")
            except ImportError as e:
                logger.info(f"✗ Cannot import {module_name}: {e}")
    
    logger.info(f"\nTasks after manual import: {len(celery_app.tasks)}")
    for task in celery_app.tasks:
        if 'freppledb' in task:
            logger.info(f"  - {task}")
    logger.info(f"Available tasks: {list(celery_app.tasks.keys())}")
except Exception as e:
    logger.info('EXCEPTION:' + str(e))
    celery_app = None