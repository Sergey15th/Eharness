from django.http import HttpResponse, JsonResponse
from django.shortcuts import get_object_or_404
from django.views import View
from django.views.generic import TemplateView
from django.template.loader import get_template
from freppledb.qm.models import ProductPassport
import os
from freppledb.settings import MEDIA_ROOT, MEDIA_URL
import requests
import base64
import tempfile
import json

import win32print
import win32api

import cairosvg
import tempfile

class ProductLabelPreviewView(View): # Предварительный просмотр шильдика паспорта
    """Предварительный просмотр шильдика"""
    def get(self, request):
        product_id = request.GET.get('id')
        product_passport = get_object_or_404(ProductPassport, id=product_id)
        # Если шильдик уже существует, используем его
        svg_path = product_passport.label.file.path
        if hasattr(product_passport, 'label') and svg_path:
            # Читаем содержимое SVG файла
            with open(svg_path, 'r', encoding='utf-8') as f:
                svg_content = f.read()
        html_content = f"""
            <!DOCTYPE html>
                <html>
                <head>
                    <title>Просмотр этикетки</title>
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
                            //setTimeout(function() {{ window.close();  }}, 3000);
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
        return HttpResponse(html_content)
    