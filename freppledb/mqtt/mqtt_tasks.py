# Celery tasks для асинхронной публикации сообщений и поддержке 
from __future__ import annotations

import json
import logging
import os
from typing import Optional

from freppledb.celery import app
from celery.utils.log import get_task_logger
from celery.signals import worker_init, worker_shutdown
from freppledb.mqtt.mqtt_client import MQTTPublisherSingleton

logger = get_task_logger(__name__)
celery_logger = logging.getLogger('celery')

mqtt_publisher = MQTTPublisherSingleton()

@worker_init.connect
def setup_mqtt(sender, **kwargs):
    """
    Инициализация MQTT Publisher при старте Celery worker.
    Вызывается автоматически при конфигурации.
    """
    logger.info("Инициализация MQTT Publisher при старте Celery worker ...")
    celery_logger.info("Инициализация MQTT Publisher при старте Celery worker ...")
    print("Инициализация MQTT Publisher при старте Celery worker ...")
    try:
        # Конфигурация из настроек mqtt_publisher
        mqtt_publisher.initialize()
        print(f"MQTT Publisher инициализирован в процессе {os.getpid()}")
        frequency = 1000  # Частота в герцах  
        duration = 300  # Продолжительность в миллисекундах  
    except Exception as e:
        print(f"Ошибка инициализации MQTT в процессе {os.getpid()}: {e}")
        logger.error(f"Ошибка инициализации MQTT в процессе {os.getpid()}: {e}")

@app.task(bind=True, name='mqtt_tasks.publish_mqtt_message', max_retries=3, default_retry_delay=5, acks_late=True, queue='default')
def publish_mqtt_message(self, topic: str, payload: Any, qos: int = 0, retain: bool = False,  metadata: Optional[Dict] = None):
    """
    Задача Celery для публикации одного MQTT сообщения
    
    Args:
        topic: MQTT topic
        payload: Данные для отправки
        qos: Quality of Service (0, 1, 2)
        retain: Retain flag
        metadata: Дополнительные метаданные
    """
    try:
        # Добавляем метаданные если нужно
        if metadata and isinstance(payload, dict):
            payload_with_meta = payload.copy()
            payload_with_meta['_metadata'] = {
                **metadata,
                'task_id': self.request.id,
                'timestamp': datetime.now().isoformat()
            }
            payload_to_send = payload_with_meta
        else:
            payload_to_send = payload
        
        # Публикуем сообщение (синхронно в задаче)
        success = mqtt_publisher.publish(
            topic=topic,
            payload=payload_to_send,
            qos=qos,
            retain=retain,
            async_mode=False  # Синхронно, так как уже в фоновой задаче
        )
        
        if not success:
            raise Exception("Не удалось опубликовать MQTT сообщение")
        
        logger.info(f"Опубликовано в {topic}: {payload_to_send}")
        return {
            'success': True,
            'topic': topic,
            'task_id': self.request.id
        }
        
    except Exception as exc:
        logger.error(f"Ошибка публикации MQTT: {exc}")
        # Повторяем задачу при ошибке
        raise self.retry(exc=exc, countdown=2 ** self.request.retries)

@app.task(bind=True, name='mqtt_tasks.publish_mqtt_batch', max_retries=3, default_retry_delay=10, acks_late=True, queue='default')
def publish_mqtt_batch(self, messages: List[Dict[str, Any]], max_concurrent: int = 10):
    """
    Задача Celery для пакетной публикации MQTT сообщений
    
    Args:
        messages: Список сообщений в формате:
                  [{'topic': '...', 'payload': ..., 'qos': 0, 'retain': False}, ...]
        max_concurrent: Максимальное количество одновременных публикаций
    """
    try:
        results = []
        errors = []
        
        for i, msg in enumerate(messages):
            try:
                success = mqtt_publisher.publish(
                    topic=msg.get('topic'),
                    payload=msg.get('payload'),
                    qos=msg.get('qos', 0),
                    retain=msg.get('retain', False),
                    async_mode=False
                )
                
                results.append({
                    'index': i,
                    'topic': msg.get('topic'),
                    'success': success
                })
                
                # Небольшая задержка для регулирования скорости
                if i % max_concurrent == 0:
                    time.sleep(0.01)
                    
            except Exception as e:
                errors.append({
                    'index': i,
                    'topic': msg.get('topic'),
                    'error': str(e)
                })
                logger.error(f"Ошибка публикации сообщения {i}: {e}")
        
        # Если есть ошибки, логируем
        if errors:
            logger.warning(f"Ошибки при пакетной публикации: {len(errors)}/{len(messages)}")
            if len(errors) > len(messages) * 0.5:  # Если более 50% ошибок
                raise Exception(f"Много ошибок при публикации: {len(errors)}/{len(messages)}")
        
        return {
            'total': len(messages),
            'successful': len(results) - len(errors),
            'errors': len(errors),
            'task_id': self.request.id
        }
        
    except Exception as exc:
        logger.error(f"Ошибка пакетной публикации MQTT: {exc}")
        raise self.retry(exc=exc, countdown=5)

@app.task(name='mqtt_tasks.publish_async_fire_and_forget', queue='mqtt_fast')
def publish_async_fire_and_forget( topic: str, payload: Any, qos: int = 0):
    """
    Асинхронная публикация без ожидания результата (fire and forget)
    Использует внутреннюю очередь publisher'а
    """
    try:
        mqtt_publisher.publish(
            topic=topic,
            payload=payload,
            qos=qos,
            async_mode=True  # Через очередь publisher'а
        )
        return True
    except Exception as e:
        logger.error(f"Fire-and-forget ошибка: {e}")
        return False

@app.task(name='mqtt_tasks.health_check', queue='monitoring')
def health_check():
    """Проверка здоровья MQTT подключения"""
    print("Проверка здоровья MQTT подключения: публикация тестового сообщения...")
    try:
        # Публикуем тестовое сообщение
        success = mqtt_publisher.publish(
            topic="system/health",
            payload={"status": "check", "timestamp": datetime.now().isoformat()},
            qos=1,
            async_mode=False
        )
        health = {
            'mqtt_connected': mqtt_publisher.connected,
            'queue_size': mqtt_publisher.message_queue.qsize(),
            'last_check': datetime.now().isoformat(),
            'publish_success': success
        }
        print("Опубликовано: " + health)
        return health
    except Exception as e:
        logger.error(f"Health check failed: {e}")
        print(f"Health check failed: {e}")
        return {
            'error': str(e),
            'mqtt_connected': False
        }

@worker_shutdown.connect
def shutdown_mqtt(sender=None, **kwargs):
    logger.info(f"Завершение работы MQTT Publisher в процессе {os.getpid()}")
    mqtt_publisher.shutdown()