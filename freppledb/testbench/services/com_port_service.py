import asyncio
import serial_asyncio
import serial
import logging
from django.conf import settings

logger = logging.getLogger(__name__)

class TZ_04_Service:
    def __init__(self):
        self.reader = None
        self.writer = None
        self.is_connected = False
        self.synchro = b'\xa5'
        self.command = {'GetVersion':b'\x80\x0d', 'ClearTester':b'\x81\x0d', 'StartTest':b'\x82\x0d', 'StopTest':b'\x83\x0d', 'AbortTest':b'\x84\x0d', 'Repeat':b'\x85\x0d', 'EndTest':b'\x86\x0d', 'LoadChannels':b'\x87\x0d', 'InvalidCommand':b'\x55\x0d'}
        
    async def connect(self, port, baudrate):
        try:
            self.reader, self.writer = await serial_asyncio.open_serial_connection(
                url=port,
                baudrate=baudrate,
                parity=serial.PARITY_NONE,
                                stopbits=serial.STOPBITS_ONE,
                                bytesize=serial.EIGHTBITS,
                                timeout=0.5
            )
            version = await self.get_version()
            if version:
                self.is_connected = True
                logger.info(f"Connected to COM port {port}")
                return True
            else:
                return False 
        except Exception as e:
            logger.error(f"COM port connection error: {e}")
            return False
    
    async def read_data(self):
        while self.is_connected:
            try:
                data = await self.reader.readuntil(b'\n')
                await self.process_harness_data(data.decode().strip())
            except Exception as e:
                logger.error(f"COM port read error: {e}")
                await asyncio.sleep(0.1)

    async def write_data(self, data):
        while self.is_connected:
            try:
                await self.writer.write(data + b'\n')
            except Exception as e:
                logger.error(f"COM port write error: {e}")
                await asyncio.sleep(0.1)

    async def process_harness_data(self, data):
        # Обработка данных от тестера жгута
        # Отправка команд на ESP32 через REST API
        pass

    async def get_version(self):
        # Запрос и получение версии от тестера жгута
        while self.is_connected:
            try:
                await self.write_data(self.command['GetVersion'])
                data = await self.reader.readuntil(b'\n')
                self.sw_version = data[3:5]
                self.channels = str(int(data[5:])*64)
                logger.info(f"Get_version: {self.sw_version}")
                return self.sw_version
            except Exception as e:
                logger.error(f"Get_version: COM port read error: {e}")
                await asyncio.sleep(0.1)
                return False
    
    async def disconnect(self):
        self.is_connected = False
        if self.writer:
            self.writer.close()
            await self.writer.wait_closed()
