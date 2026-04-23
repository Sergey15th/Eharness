from django.dispatch import receiver
from django.dispatch import Signal
from freppledb.qm.models import ProductPassport
from freppledb.technology.models import ItemT
from freppledb.labels.models import CreatedLabel
from freppledb.settings import MEDIA_ROOT, MEDIA_URL
from django.db.models.signals import pre_save, post_save
from freppledb.qm.models import QualityControl, ControlType, Batch
from freppledb.codescan.models import *
from django.core.files import File
from datetime import datetime
 
import os

import svglue
import os
import re

import cairosvg
import tempfile
#import win32print
import tempfile
#import win32api

### Signals list ###
print_passport_label_signal = Signal()

@receiver(post_save)
def qm_post_save_receiver(sender, instance, **kwargs):
    # Your logic here, e.g., modify instance.field
    if sender == QualityControl: #Сохранён результат контроля качества
        if instance.control_result == 'СООТВЕТСТВУЕТ':
            controlled_item = ItemT.objects.get(item_ptr_id=instance.product_passport.manufacturing_order.operation.item)
            # Проверить, выполнены ли у продукта все контроли качества на 'СООТВЕТСТВУЕТ'
            for need_check in controlled_item.qm_control_types.all():
                try:
                    last_checks_maked = QualityControl.objects.filter(type=need_check).order_by('date').first().control_result
                    if last_checks_maked !='СООТВЕТСТВУЕТ':
                        return # Если последняя по дате проверка не отрицательная
                except:
                    # Или если проверок вообще не было, и текущая положительная проверка не требуемая
                    if need_check.type != instance.type.type:
                        return
            # Все проверки пройдены, нужно закрыть паспорт
            instance.product_passport.status = 'Закрыт'
            instance.product_passport.save()

            # TODO:
            pass
            # ВЫПУЩЕНА И ПРИНЯТА ГОТОВАЯ ПРОДУКЦИЯ,
            # СФОРМИРОВАТЬ ШИЛЬДИК ПРОДУКТА И РАСПЕЧАТАТЬ 
            #print_passport_label_signal.send(sender=QualityControl, instance=instance) #, request=request
            pass

@receiver(pre_save)
def qm_pre_save_receiver(sender, instance, **kwargs):
    if sender == QualityControl: #Создан результат контроля качества
        if sender.type == ControlType.CONTINUITY: # Запускаем прозвонку
            # Сформировать план проверки и запустить проверку
            print('sender=QualityControl, sender.type=ControlType.CONTINUITY')
            pass
    if sender == ProductPassport: #Обновился паспорт продукта
        pp_item = ItemT.objects.get(item_ptr_id=instance.manufacturing_order.operation.item) # Находим номенклатуру, для которой создан паспорт
        #instance.label_path = pp_item.passport_label_template.template #
        pass
    if sender == QualityControl: #Создан результат контроля качества
        if instance.control_result == 'СООТВЕТСТВУЕТ':
            controlled_item = ItemT.objects.get(item_ptr_id=instance.product_passport.manufacturing_order.operation.item)
            # Проверить, выполнены ли у продукта все контроли качества на 'СООТВЕТСТВУЕТ'
            for need_check in controlled_item.qm_control_types.all():
                try:
                    last_checks_maked = QualityControl.objects.filter(type=need_check).order_by('date').first().control_result
                    if last_checks_maked !='СООТВЕТСТВУЕТ':
                        return # Если последняя по дате проверка не отрицательная
                except:
                    # Или если проверок вообще не было, и текущая положительная проверка не требуемая
                    if need_check.type != instance.type.type:
                        return
            # Все проверки пройдены, нужно закрыть паспорт
            instance.product_passport.status = 'Закрыт'
            instance.product_passport.save()

            # TODO:
            # ВЫПУЩЕНА И ПРИНЯТА ГОТОВАЯ ПРОДУКЦИЯ,
            # СФОРМИРОВАТЬ ШИЛЬДИК ПРОДУКТА И РАСПЕЧАТАТЬ 
            print_passport_label_signal.send(sender=QualityControl, instance=instance)
            pass
    if sender == Batch: #Партия номенклатуры создаёт этикетки изделий
        # Проверяем, есть ли уже паспорта для созданной партии:
        if not instance.serials_created:
            # Если на партию номенклатуры еще не созданы паспорта, то создаём:
            for i in range(int(instance.serie_no_start), int(instance.serie_no_start) + int(instance.manufacturing_order.quantity)):
                Passport = ProductPassport()
                Passport.manufacturing_order = instance.manufacturing_order
                Passport.serial_number = i
                #Passport.product = ItemT.objects.get(item_ptr_id=instance.manufacturing_order.operation.item)
                try:
                    current_qr = LastUsedQR.objects.get(model='B') # Паспорт изделия
                except Exception as e:
                    current_qr = LastUsedQR(model='B', qr='0000')
                current_qr.qr = current_qr._next_id()
                new_qr = QR()
                new_qr.create_qr(current_qr.model + current_qr.qr)
                current_qr.save()
                new_qr.save()
                Passport.product_qrcode = new_qr
                Passport.date = datetime.now()
                pp_item = ItemT.objects.get(item_ptr_id=Passport.manufacturing_order.operation.item) # Находим номенклатуру ItemT, для которой создан паспорт
                # Создаём этикетку паспорта
                if not Passport.label: # Этикетки нет, создаём её
                    Passport.label = CreatedLabel()
                    Passport.label.template = pp_item.passport_label_template
                    Passport.label.file = Passport.label.template.generate_svg(Passport, f"passport-{Passport.product_qrcode.qr}")
                    Passport.label.name = f"passport-{Passport.product_qrcode.qr}"
                    Passport.label.save()
                Passport.save()
            instance.serials_created = True

        pass

@receiver(print_passport_label_signal)
def print_passport_label_handler(sender, instance, **kwargs):
    # ЗАГЛУШКА
    return
    svg_file = generate_svg(template=instance.label_path, instance=instance)
    base_name = f"{instance.id}-{instance.manufacturing_order.operation.item}-{instance.manufacturing_order.batch}-{instance.serial_number}"
    safe_name = re.sub(r'[^\w\-_.]', '_', base_name)
    save_svg_to_file(svg_file, os.path.join(MEDIA_ROOT, 'img', 'svg', safe_name, '.png'))
    return #