from django.dispatch import receiver
from django.dispatch import Signal
from freppledb.qm.models import ProductPassport
from freppledb.technology.models import ItemT
from freppledb.settings import MEDIA_ROOT, MEDIA_URL
from django.db.models.signals import pre_save, post_save
from freppledb.qm.models import QualityControl, ControlType

import svglue
import os
import re

import cairosvg
import tempfile
import win32print
import tempfile
import win32api

### Signals list ###
print_passport_label_signal = Signal()

@receiver(post_save)
def technology_post_save_receiver(sender, instance, **kwargs):
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
def technology_pre_save_receiver(sender, instance, **kwargs):
    # Your logic here, e.g., modify instance.field
    if sender == QualityControl: #Создан результат контроля качества
        if sender.type == ControlType.CONTINUITY: # Запускаем прозвонку
            # Сформировать план проверки и запустить проверку
            print('sender=QualityControl, sender.type=ControlType.CONTINUITY')
            pass
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

def svg_to_pdf(svg_content):
    """Конвертирует SVG в PDF для печати"""
    try:
        # Создаем временный SVG файл
        with tempfile.NamedTemporaryFile(mode='w', suffix='.svg', delete=False, encoding='utf8') as f:
            f.write(svg_content)
            svg_temp_path = f.name
        
        # Создаем временный PDF файл
        with tempfile.NamedTemporaryFile(suffix='.pdf', delete=False) as f:
            pdf_temp_path = f.name
        
        # Конвертируем SVG в PDF
        cairosvg.svg2pdf(
            url=svg_temp_path,
            write_to=pdf_temp_path
        )
        
        # Читаем PDF байты
        with open(pdf_temp_path, 'rb') as f:
            pdf_bytes = f.read()
        
        # Удаляем временные файлы
        os.unlink(svg_temp_path)
        os.unlink(pdf_temp_path)
        
        return pdf_bytes
        
    except Exception as e:
        print(f"Ошибка конвертации SVG в PDF: {e}")
        return None

def print_svg_direct_windows(svg_content, printer_name=None):
    """Прямая печать на Windows"""
    try:
        # Конвертируем SVG в PDF
        pdf_bytes = svg_to_pdf(svg_content)
        if not pdf_bytes:
            return False
        
        # Сохраняем во временный файл
        with tempfile.NamedTemporaryFile(delete=False, suffix='.pdf') as f:
            f.write(pdf_bytes)
            temp_pdf_path = f.name
        
        # Получаем принтер по умолчанию если не указан
        if not printer_name:
            printer_name = win32print.GetDefaultPrinter()
        
        # Печатаем через системную команду
        win32api.ShellExecute(
            0, 
            "print", 
            temp_pdf_path, 
            f'"{printer_name}"', 
            ".", 
            0
        )
        
        # Удаляем временный файл через некоторое время
        import threading
        def delete_temp_file():
            import time
            time.sleep(10)  # Ждем 10 секунд
            if os.path.exists(temp_pdf_path):
                os.unlink(temp_pdf_path)
        
        threading.Thread(target=delete_temp_file).start()
        
        return True
        
    except Exception as e:
        print(f"Ошибка печати: {e}")
        return False

def download_svg(request):
    """Скачивание SVG файла"""
    svg_content = generate_svg()
    response = HttpResponse(svg_content, content_type='image/svg+xml')
    response['Content-Disposition'] = 'attachment; filename="label.svg"'
    return response