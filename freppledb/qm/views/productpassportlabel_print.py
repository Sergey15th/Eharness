from django.http import HttpResponse, JsonResponse
from django.shortcuts import get_object_or_404
from django.views import View
from django.views.generic import TemplateView
from django.template.loader import get_template
from freppledb.qm.models import ProductPassport
import os
from freppledb.settings import MEDIA_ROOT, MEDIA_URL
from freppledb.qm.services import print_svg_direct_windows, generate_svg

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
