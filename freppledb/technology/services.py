from django.db.models.signals import pre_save
from django.dispatch import receiver
from freppledb.technology.models import ConnectionList, ItemT
from freppledb.codescan.models import LastUsedQR

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
    if sender == ItemT:
        if instance.qr is None:
            try:
                current_qr = LastUsedQR.objects.get(model='6') # Карта резки
            except Exception as e:
                current_qr = LastUsedQR(model='6', qr='0000')
            current_qr.qr = current_qr._next_id()
            instance.qr = current_qr.model + current_qr.qr
            current_qr.save()
        if instance.image is not None:
          if instance.image.name is None: instance.image = 'img/no_image.png'
          instance.imagef.name = instance.image.name[:-4] + '_F' + instance.image.name[-4:] # путь относительно MEDIA_ROOT
          instance.imagef_height = instance.image_height
          instance.imagef_width = instance.image_width
