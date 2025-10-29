from django.http import HttpResponse, JsonResponse
from django.shortcuts import get_object_or_404
from django.views import View
from django.views.generic import TemplateView
from django.template.loader import get_template
from freppledb.qm.models import ProductPassport
from freppledb.qm.services import generate_svg
import os
from freppledb.settings import MEDIA_ROOT, MEDIA_URL
import requests
import base64
import tempfile
import json

import win32print
import tempfile
import win32api

import cairosvg
import tempfile

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

class ProductLabelPrintView(View):
    """Предварительный просмотр шильдика"""
    def get(self, request):
        product_id = request.GET.get('id')
        product_passport = get_object_or_404(ProductPassport, id=product_id)
        # Если шильдик уже существует, используем его
        if hasattr(product_passport, 'label_path'):
            svg_content = generate_svg(os.path.join(MEDIA_ROOT, product_passport.label_path), product_passport)
        else:
           # Иначе генерируем новый
            pass
        html_content = f"""
            <!DOCTYPE html>
                <html>
                <head>
                    <title>Печать этикетки</title>
                    <style>
                        @media print {{
                            body {{ margin: 0; padding: 0; }}
                            .no-print {{ display: none; }}
                        }}
                        @page {{ size: auto; margin: 0mm; }}
                        svg {{ width: auto; height: auto; }}
                    </style>
                    <script>
                        window.onload = function() {{
                            // window.print();
                            // Закрыть окно после печати (опционально)
                            setTimeout(function() {{ window.close();  }}, 3000);
                        }};
                    </script>
                </head>
                <body>
                    {svg_content}
                    <div class="no-print" style="text-align: center; margin: 20px;">
                        <button onclick="window.print()">Печать</button>
                        <button onclick="window.close()">Закрыть</button>
                    </div>
                </body>
                </html>
        """
        #response = HttpResponse(svg_content, content_type='image/svg+xml')
        #return response
        print_svg_direct_windows(svg_content)
        return HttpResponse(html_content)
    
def download_svg(request):
    """Скачивание SVG файла"""
    svg_content = generate_svg()
    response = HttpResponse(svg_content, content_type='image/svg+xml')
    response['Content-Disposition'] = 'attachment; filename="label.svg"'
    return response