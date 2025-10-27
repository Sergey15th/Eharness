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
#import cups
import tempfile
import json

class ProductLabelPreviewView(View):
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
        
        response = HttpResponse(svg_content, content_type='image/svg+xml')
        #response['Content-Disposition'] = f'inline; filename="label_{product.sku}.svg"'
        return response