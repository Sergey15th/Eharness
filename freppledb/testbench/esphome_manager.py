import aiohttp
import asyncio
import logging
from django.conf import settings
from asgiref.sync import sync_to_async

logger = logging.getLogger(__name__)

class ESPHOMEManager:
    def __init__(self):
        self.session = None
        self.base_url = None
        self.is_connected = False
        self.connection_lock = asyncio.Lock()
        
    async def initialize(self, base_url):
        self.base_url = base_url
        await self._ensure_connection()
        
    async def _ensure_connection(self):
        async with self.connection_lock:
            if not self.is_connected:
                await self._connect()
    
    async def _connect(self):
        try:
            if self.session is None or self.session.closed:
                timeout = aiohttp.ClientTimeout(total=10)
                self.session = aiohttp.ClientSession(timeout=timeout)
            
            # Проверка подключения
            async with self.session.get(f"{self.base_url}/light_bar/status") as response:
                if response.status == 200:
                    self.is_connected = True
                    logger.info("Connected to ESPHOME")
                else:
                    self.is_connected = False
                    
        except Exception as e:
            logger.warning(f"ESPHOME connection failed: {e}")
            self.is_connected = False
            await asyncio.sleep(2)  # Пауза перед повторной попыткой
    
    async def send_command(self, endpoint, data=None):
        max_retries = 3
        for attempt in range(max_retries):
            try:
                await self._ensure_connection()
                
                if not self.is_connected:
                    await self._connect()
                    if not self.is_connected:
                        continue
                
                url = f"{self.base_url}/{endpoint}"
                async with self.session.post(url, json=data) as response:
                    if response.status == 200:
                        return await response.json()
                    else:
                        logger.warning(f"ESPHOME command failed: {response.status}")        
            except Exception as e:
                logger.error(f"ESPHOME command error (attempt {attempt+1}): {e}")
                self.is_connected = False
                await asyncio.sleep(1)
        return None
    
    async def keep_alive(self):
        while True:
            if not self.is_connected:
                await self._connect()
            else:
                # Периодическая проверка соединения
                try:
                    await self.send_command("light_bar_section_10/turn_on?transition_length=0.2&r=10&g=10&b=255")
                except:
                    self.is_connected = False
            await asyncio.sleep(30)  # Проверка каждые 30 секунд
