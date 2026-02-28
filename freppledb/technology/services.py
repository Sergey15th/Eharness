from django.db.models.signals import pre_save
from django.dispatch import receiver
from freppledb.technology.models import ConnectionList, ItemT
from freppledb.input.models.operationplan import ManufacturingOrder
from freppledb.qm.models import Batch, ProductPassport
from freppledb.codescan.models import *
from freppledb.qm.services import print_passport_label_signal

@receiver(pre_save)
def technology_pre_save_receiver(sender, instance, **kwargs):
    # Your logic here, e.g., modify instance.field
    if sender == ConnectionList:
        if instance.qr is None:
            try:
                current_qr = LastUsedQR.objects.get(model='8') # Карта резки
            except Exception as e:
                current_qr = LastUsedQR(model='8', qr='0000')
            current_qr.qr = current_qr._next_id()
            instance.qr = current_qr.model + current_qr.qr
            current_qr.save()
    if sender == ItemT: # Если сохраняем Номенклатуру:
        #if instance.image.name is None:
        #    instance.image = 'img/no_image.png'
        #    instance.imagef = 'img/no_image_F.png'
        if instance.qr is None: # Если QR кода нет
            try:
                current_qr = LastUsedQR.objects.get(model='6') # Номенклатура
            except Exception as e:
                current_qr = LastUsedQR(model='6', qr='0000')
            current_qr.qr = current_qr._next_id()
            new_qr = QR()
            new_qr.create_qr(current_qr.model + current_qr.qr)
            current_qr.save()
            new_qr.save()
            instance.qr = new_qr
        else: # Если QR код есть, то генерим картинку
            if not instance.qr.image: #QR есть, но нужно сгенерить картинку
                instance.qr.create_qr(instance.qr.qr)
                instance.qr.save()
        if instance.barcode_number is not None: # Если есть номер штрих-кода
            if instance.barcode is None: # проверяем, есть ли созданный штрих-код
                # Если нет, то создаём новый
                new_barcode = barcode()
                new_barcode.create_barcode(instance.barcode_number)
                new_barcode.save()
                instance.barcode = new_barcode
            pass
    if sender == ManufacturingOrder:
        # Необходимо определить, является ли заказ новым
        # создаем новую партию
        try: # Определим, не создана ли уже партия номенклатуры под наш заказ 
            bl = Batch.objects.get(manufacturing_order=instance)
            # Уже создана, ничего не делаем
            pass
        except:
            # Партии номенклатуры нет, создаём новую
            try: # Ищем все паспорта продукта и находим максимальный серийный номер
                batch_product_passports_last_serialnumber = ProductPassport.objects.filter(manufacturing_order__item=instance.operation.item).order_by("-serial_number").first().serial_number # последний серийный номер
                batch_product_passports_last_serialnumber += 1 # Будем создавать паспорта с серийными номерами, следующими за максимальным
            except:
                batch_product_passports_last_serialnumber = 0 # Паспортов вообще нет
            new_batch = Batch()            
            new_batch.manufacturing_order = instance
            new_batch.serie_no_start = batch_product_passports_last_serialnumber
            new_batch.save()
            pass
