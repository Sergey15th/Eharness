#MQTT клиент для передачи сообщений
import paho.mqtt.client as mqtt
import threading
import time
import logging
import json
from queue import Queue
from typing import Optional, Dict, Any
from django.conf import settings

logger = logging.getLogger(__name__)

class MQTTPublisherSingleton:
    """
    Singleton для управления MQTT подключением в Celery worker.
    Создается один экземпляр на процесс worker'а.
    """
    _instance = None
    _lock = threading.Lock()
    
    def __new__(cls):
        with cls._lock:
            if cls._instance is None:
                cls._instance = super(MQTTPublisherSingleton, cls).__new__(cls)
                cls._instance._initialized = False
            return cls._instance
    
    def __init__(self):
        if not self._initialized:
            self.client: Optional[mqtt.Client] = None
            self.connected = False
            self.connection_lock = threading.Lock()
            self.publish_lock = threading.Lock()
            self.message_queue = Queue(maxsize=10000)
            self._stop_event = threading.Event()
            self.publisher_thread: Optional[threading.Thread] = None
            self._initialized = True
    
    def initialize(
        self,
        host: str = getattr(settings, "MQTT_BROKER_URL", "localhost"),
        port: int = getattr(settings, "MQTT_BROKER_PORT", 1883),
        username: Optional[str] = getattr(settings, "MQTT_BROKER_USERNAME", None),
        password: Optional[str] = getattr(settings, "MQTT_BROKER_PASSWORD", None),
        client_id: Optional[str] = None
    ):
        """Инициализация MQTT клиента"""
        with self.connection_lock:
            if self.client is not None:
                return
            client_id = client_id or f"mqtt_{int(time.time())}"
            print("client_id:" + client_id)
            self.client = mqtt.Client(
                client_id=client_id,
                clean_session=True,
                protocol=mqtt.MQTTv311
            )
            print("host:" + host)
            print("port:" + str(port))
            print("username:" + username)
            print("password:" + password)
            if username and password:
                self.client.username_pw_set(username, password)
            
            # Callbacks
            self.client.on_connect = self._on_connect
            self.client.on_disconnect = self._on_disconnect
            self.client.on_publish = self._on_publish
            
            try:
                if username is None:
                    raise ValueError("Имя пользователя не указано в settings (MQTT_BROKER_USERNAME)")
                if password is None:
                    raise ValueError("Пароль пользователя не указан в settings (MQTT_BROKER_PASSWORD)")
                self.client.connect(host, port, 60)
                print("after connect")
                self.client.loop_start()
                # Ждем подключения 1 секунду
                for _ in range(10): 
                    if self.connected: break
                    time.sleep(0.1)
                # Запускаем поток для публикации из очереди
                self.publisher_thread = threading.Thread(target=self._queue_publisher, daemon=True)
                self.publisher_thread.start()
                logger.info(f"MQTT Publisher инициализирован для {host}:{port}")
            except Exception as e:
                logger.error(f"Ошибка инициализации MQTT: {e}")
                self.client = None
    
    def _on_connect(self, client, userdata, flags, rc):
        if rc == 0:
            self.connected = True
            logger.info("MQTT подключен успешно")
        else:
            self.connected = False
            logger.error(f"Ошибка подключения MQTT: {rc}")
    
    def _on_disconnect(self, client, userdata, rc):
        self.connected = False
        logger.warning(f"MQTT отключен: {rc}")
    
    def _on_publish(self, client, userdata, mid):
        logger.debug(f"Сообщение опубликовано, mid: {mid}")
    
    def _queue_publisher(self):
        """Фоновый поток для публикации из очереди"""
        while not self._stop_event.is_set():
            try:
                # Блокирующее получение с таймаутом
                try:
                    topic, payload, qos, retain = self.message_queue.get(timeout=1)
                except Exception:
                    continue
                
                # Пытаемся опубликовать
                success = self._publish_sync(topic, payload, qos, retain)
                
                if not success and not self._stop_event.is_set():
                    # Возвращаем в очередь для повторной попытки
                    self.message_queue.put((topic, payload, qos, retain))
                    time.sleep(0.1)
                
                self.message_queue.task_done()
                
            except Exception as e:
                logger.error(f"Ошибка в queue_publisher: {e}")
                time.sleep(0.5)
    
    def _publish_sync(self, topic: str, payload: Any, qos: int = 0, retain: bool = False):
        """Синхронная публикация с проверкой соединения"""
        with self.publish_lock:
            if not self.connected or self.client is None:
                return False
            
            try:
                # Преобразуем данные
                if isinstance(payload, (dict, list)):
                    payload_str = json.dumps(payload, ensure_ascii=False)
                else:
                    payload_str = str(payload)
                
                # Публикуем
                result = self.client.publish(
                    topic=topic,
                    payload=payload_str,
                    qos=qos,
                    retain=retain
                )
                
                # Для QoS > 0 ждем подтверждения
                if qos > 0:
                    result.wait_for_publish(timeout=2)
                
                return result.rc == mqtt.MQTT_ERR_SUCCESS
                
            except Exception as e:
                logger.error(f"Ошибка публикации: {e}")
                return False
    
    def publish(
        self,
        topic: str,
        payload: Any,
        qos: int = 0,
        retain: bool = False,
        async_mode: bool = True
    ) -> bool:
        """
        Публикация сообщения
        
        Args:
            async_mode: True - через очередь (асинхронно),
                       False - напрямую (синхронно)
        """
        if self.client is None:
            logger.error("MQTT клиент не инициализирован")
            return False
        
        if async_mode:
            # Асинхронно через очередь
            try:
                self.message_queue.put_nowait((topic, payload, qos, retain))
                return True
            except Exception as e:
                logger.error(f"Ошибка добавления в очередь: {e}")
                return False
        else:
            # Синхронная публикация
            return self._publish_sync(topic, payload, qos, retain)
    
    def shutdown(self):
        """Корректное завершение работы"""
        self._stop_event.set()
        
        if self.publisher_thread:
            self.publisher_thread.join(timeout=5)
        
        if self.client:
            self.client.loop_stop()
            self.client.disconnect()
        
        logger.info("MQTT Publisher остановлен")