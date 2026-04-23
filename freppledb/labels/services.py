from django.dispatch import receiver
from django.dispatch import Signal
from freppledb.technology.models import ItemT
from freppledb.settings import MEDIA_ROOT, MEDIA_URL
from django.db.models.signals import pre_save, post_save

import os
import re

import tempfile
#import win32print
import tempfile
#import win32api

### Signals list ###
print_passport_label_signal = Signal()

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
    return filename

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