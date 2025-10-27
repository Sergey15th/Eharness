from django.dispatch import receiver
from django.dispatch import Signal
from freppledb.qm.models import ProductPassport
from freppledb.technology.models import ItemT
from freppledb.settings import MEDIA_ROOT, MEDIA_URL

import svglue
import os
import re

### Signals list ###
print_passport_label_signal = Signal()

@receiver(print_passport_label_signal)
def print_passport_label_handler(sender, instance, request, **kwargs):
    svg_file = generate_svg(template=instance.label_path, instance=instance)
    base_name = f"{instance.id}-{instance.manufacturing_order.operation.item}-{instance.manufacturing_order.batch}-{instance.serial_number}"
    safe_name = re.sub(r'[^\w\-_.]', '_', base_name)
    save_svg_to_file(svg_file, os.path.join(MEDIA_ROOT, 'img', 'svg', safe_name, '.png'))
    return #

def generate_svg(template, instance):
    """Генерирует SVG шильдик на основе шаблона"""
    # Загружаем шаблон
    template = svglue.load(file=template)

    # Заменяем текстовые элементы
    for elem_key in template._tspan_subs: # Перебираем все текстовые template-id
        elem_key_clean = re.sub(r'\d+$', '', elem_key)
        try:
            parts = elem_key_clean.split('.')
            current_obj = instance
            for part in parts:
                if part == 'item': # Если обращение к аттрибуту объекта Item, то подменяем его ItemT для возможности доступа к расширенным данным
                    current_obj = ItemT.objects.get(item_ptr_id=getattr(current_obj, part))
                else:
                    current_obj = getattr(current_obj, part)
                if current_obj is None:
                    value = None
            value = current_obj
        except (AttributeError, ValueError):
            value = None
        if value is not None:
            template.set_text(elem_key, escape_text(str(value)))
    for elem_key in template._rect_subs: # Перебираем все прямоугольники template-id
        elem_key_clean = re.sub(r'\d+$', '', elem_key)
        try:
            parts = elem_key_clean.split('.')
            current_obj = instance
            for part in parts:
                if part == 'item': # Если обращение к аттрибуту объекта Item, то подменяем его ItemT для возможности доступа к расширенным данным
                    current_obj = ItemT.objects.get(item_ptr_id=getattr(current_obj, part))
                else:
                    current_obj = getattr(current_obj, part)
                if current_obj is None:
                    value = None
            value = current_obj
        except (AttributeError, ValueError):
            value = None
        if value is not None:
            path = os.path.join(MEDIA_ROOT, str(value)) # Берём файл из MEDIA_ROOT/img/qr/*.png
            template.set_image(elem_key, file=path, mimetype='image/png')
    src = template.__str__()
    # Рендерим финальный SVG
    return src

def escape_text(text):
    """Экранирует специальные символы"""
    if not text:
        return ""
    return (text.replace('&', '&amp;')
                .replace('<', '&lt;')
                .replace('>', '&gt;')
                .replace('"', '&quot;')
                .replace("'", '&apos;'))

def save_svg_to_file(svg_content, filename):
    """Сохраняет SVG в файл"""
    with open(os.path.join(filename), 'w', encoding='utf8') as svgout:
        svgout.write(svg_content)
