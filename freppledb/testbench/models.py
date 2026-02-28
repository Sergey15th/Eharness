from django.db import models
from freppledb.common.models import HierarchyModel, AuditModel
from freppledb.technology.models import ItemT
from django.utils.translation import gettext as _
import serial.tools.list_ports
import serial
import logging


logger = logging.getLogger(__name__)
# класс quality_control, в котором создаются экземпляры контроля качества
class BenchConnectors(AuditModel):
    # почему то не работает
    def formfield_for_foreignkey(self, db_field, request, **kwargs): # Фильтруем выбор разъёмов, только из списка opposite_item
            if db_field.name == "connector":
                # Показываем только ItemT из списка opposite_item
                kwargs["queryset"] = ItemT.objects.filter(
                    opposite_item__isnull=False,
                ).distinct()
            return super().formfield_for_foreignkey(db_field, request, using=request.database, **kwargs)
    def __str__(self):
        return (str(id) + '-' + str(self.connector_name) + '-' + str(self.connector_designation)) 
    id = models.AutoField(_("identifier"), primary_key=True)
    # Наименование разъёма
    connector_name = models.CharField(max_length=50, null=True, blank=True)
    # Обозначение разъёма
    connector_designation = models.CharField(max_length=10, null=False, blank=False, unique=True)
    # Разъём
    connector = models.ForeignKey('technology.ItemT', verbose_name=_("Разъём стенда"), on_delete=models.PROTECT, db_index=False, related_name='item_testbench_connectors', blank=False, null=False, )
    # Количество контактов у разъёма
    connector_pins_no = models.IntegerField(blank=False, null=False)
    # MQTT адрес лампочки разъёма
    light_led_mqtt_id = models.CharField(max_length=50, null=True, blank=True, verbose_name=_("MQTT ID светодиода"))
    class Meta(AuditModel.Meta):
        db_table = 'testbench_connectors'                 # Name of the database table
        verbose_name = _('Разъём стенда')          # A translatable name for the entity
        verbose_name_plural = _('Разъёмы стенда')  # Plural name

# модель "Подключения стенда"
# Разъём - контакт - канал тестера ТЖ-04
class BenchChannels(AuditModel):
    def __str__(self):
        return (str(id) + '-' + str(self.bench_connector) + '-' + str(self.bench_pin_no))
    id = models.AutoField(_("identifier"), primary_key=True)
    bench_connector = models.ForeignKey(BenchConnectors, verbose_name=_("Разъём стенда"), on_delete=models.PROTECT, db_index=False, related_name='channels', blank=False, null=False, )
    bench_pin_no = models.IntegerField(verbose_name=_("Контакт разъёма"), blank=False, null=False)
    channel = models.IntegerField(verbose_name=_("Канал тестера"), blank=False, null=False)
    class Meta(AuditModel.Meta):
        db_table = 'testbench_channels'                 # Name of the database table
        verbose_name = _('Подключение стенда')          # A translatable name for the entity
        verbose_name_plural = _('Подключения стенда')   # Plural name
        unique_together = [
            ['bench_connector', 'bench_pin_no'],  # Комбинация 'bench_connector' и 'bench_pin_no' должна быть уникальной
        ]

class TZ_04: # Тестер жгутов ТЖ-04
    def __new__(cls, port:str, *args, **kwargs):
        try:# Open the COM port
            ser = None
            ser = serial.Serial(port, baudrate=9600,
                                parity=serial.PARITY_NONE,
                                stopbits=serial.STOPBITS_ONE,
                                bytesize=serial.EIGHTBITS,
                                timeout=0.5)
            instance = super().__new__(cls)
            instance.connection = ser
            return instance
        except Exception as e:
            # serial.SerialException:
            logger.error(f"Error opening port: {e}")
            return None
    def __init__(self, port:str, *args, **kwargs):
        if not hasattr(self, 'connection'):  # если __new__ не задал connection
            logger.error(f"Error: no connection attr")
            raise RuntimeError("Device not initialized")
        self.port = port
        self.synchro = b'\xa5'
        self.command = {'GetVersion':b'\x80\x0d', 'ClearTester':b'\x81\x0d', 'StartTest':b'\x82\x0d', 'StopTest':b'\x83\x0d', 'AbortTest':b'\x84\x0d', 'Repeat':b'\x85\x0d', 'EndTest':b'\x86\x0d', 'LoadChannels':b'\x87\x0d', 'InvalidCommand':b'\x55\x0d'}
        self.connection.write(self.synchro+self.command['GetVersion'])
        line = self.connection.read(7).decode('utf-8')
        if not line:
            self.connection.close()
            logger.error(f"Device did not respond")
            raise RuntimeError("Device did not respond")
        self.sw_version = line[3:5]
        self.channels = str(int(line[5:])*64)

    def get_com_ports(self)->list:
        return serial.tools.list_ports.comports()

    def load_channels(self, channels:list):
        self.connection.write(self.synchro+self.command['LoadChannels'])
        logger.info(self.synchro+self.command['LoadChannels'])
        self.connection.write(b':FF0000FF\x0d')
        logger.info(':FF0000FF')
        for channel in channels:
            # Отправляем список каналов в формате NEX
            self.connection.write(b':'+f'{channel:X}'.encode('utf-8')+f'{channel:02X}'.encode('utf-8')+b'\x0d')
            logger.info(":"+f'{channel:X}'+f'{channel:02X}')
        self.connection.write(b':0001FF\x0d')
        logger.info(':0001FF')
        line = self.connection.read(10).decode('utf-8').replace("\r", "")
        logger.info('<-'+ line)
        if line == ':87000000':
            return True
        else:
            return False
    def check_channels(self, channels:list) -> list:
        result = {}
        if self.load_channels(channels=channels):
            while True:
                # Отправляем команду начала проверки
                self.connection.write(self.synchro+self.command['StartTest'])
                line = self.connection.read(14).decode('utf-8').replace("\r", "")
                logger.info(line)
                if line[:3] == ':85' and line[7:-2]=='FFFF': # Ошибка: канал не связан ни с какими другими каналами
                    result[int(line[3:-6],16)]='NotUsed'
                if line==b':86' or line =='':
                    logger.info('Test completed')
                    break
        #result.append()
        return (result)