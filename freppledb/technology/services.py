from django.db.models.signals import pre_save
from django.dispatch import receiver
from freppledb.technology.models import ConnectionList, ItemT
from freppledb.input.models.operationplan import ManufacturingOrder
from freppledb.qm.models import BatchList

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
        if instance.image.name is None:
            instance.image = 'img/no_image.png'
            instance.imagef = 'img/no_image_F.png'
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
        if instance.barcode_number is not None:
            #new_barcode = barcode()
            #new_barcode.create_barcode(instance.barcode_number)
            #new_barcode.save()
            #instance.barcode = new_barcode
            pass
    if sender == ManufacturingOrder:
        # Необходимо определить, является ли заказ новым
        try: # Определим, не создана ли уже партия номенклатуры под наш заказ 
            bl = BatchList.objects.get(manufacturing_order=instance)
            # Уже создана, ничего не делаем
            pass
        except:
            # Партии номенклатуры нет, создаём новую
            pass