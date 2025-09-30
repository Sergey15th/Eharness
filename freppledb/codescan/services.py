from django.dispatch import receiver
from django.dispatch import Signal
from .models import Workstation
import logging

logger = logging.getLogger('DQ.admin')
logger.info('Запуск админки ' + __name__ + '...')

### Signals list ###
code_scanned_signal = Signal()

@receiver(code_scanned_signal)
def code_scanned_handler(sender, instance, request, **kwargs):
    return # ничего не совпало, ничего не делаем

def workstation_context(request):
    workstation_id = request.COOKIES.get('workstation_id')
    if not workstation_id:
        return {}
    try:
        workstation = Workstation.objects.get(short_name=workstation_id)
        return {'workstation': workstation}
    except Workstation.DoesNotExist:
        return {}
def last_scanned_item_context(request):
    last_scanned_item_id = request.COOKIES.get('item_id')
    if not last_scanned_item_id:
        return {}
    else:
        return {'item_id': last_scanned_item_id}