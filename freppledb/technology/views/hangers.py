from django.conf import settings
from django.contrib.admin.utils import unquote
from django.db.models.functions import Cast
from django.db.models import Q, IntegerField
from django.db.models.expressions import RawSQL
from django.template import Template
from django.utils.translation import gettext_lazy as _
from django.utils.encoding import force_str
from django.utils.text import format_lazy
from django.views import View
from freppledb.boot import getAttributeFields
from freppledb.technology.models import (
    MobileHanger, ItemT
)
from django.http import HttpResponse
from django.shortcuts import get_object_or_404
from freppledb.common.report import (
    GridReport,
    GridFieldLastModified,
    GridFieldText,
    GridFieldHierarchicalText,
)

import logging

logger = logging.getLogger(__name__)

class MobileHangerList(GridReport):
    title = _("Мобильные вешала")
    basequeryset = MobileHanger.objects.all()
    model = MobileHanger
    frozenColumns = 0
    editable = True
    help_url = "help/mobilehanger.html"
    message_when_empty = Template( # TODO: СДЕЛАТЬ WIZARD ДЛЯ ЗАГРУЗКИ CUTLIST, ПОД ШАГОМ №16
        """
        <h3>Создайте мобильные вешала</h3>
        <br>
        <br>
        <br><br>
        <div role="group" class="btn-group.btn-group-justified">
        <a href="{{request.prefix}}/data/technology/mobilehanger/add/" class="btn btn-primary">Create a single item<br>in a form</a>
        <a href="{{request.prefix}}/wizard/load/production/?currentstep=16" class="btn btn-primary">Wizard to upload cutlist<br>from a spreadsheet</a>
        </div>
        <br>
        """
    )
    rows = (
        GridFieldText("id", title=_("id"), formatter="detail", model=MobileHanger, extra='"role":"technology/mobilehanger"',),
        GridFieldText("number", title=_("№"), ),
        GridFieldHierarchicalText(
            "Привязанная номенклатура",
            title=_("Привязанная номенклатура"),
            field_name="current_item",
            model=ItemT,
        ),
        GridFieldText("qr__image", title=_("QR_"), formatter="imagenew2", key=False, ),
        GridFieldText("labeltemplate", title=_("Шаблон этикетки"), field_name="label_template__name", key=False, formatter="showlink",
                      extra = ('"formatoptions": {"baseLinkUrl":"/data/technology/hangerlabel/", "showaction ":"255", "target":"_blank"}'), #, "addParam": "?source=grid"
                      editable=False),
        GridFieldText("source", title=_("source")),
        GridFieldLastModified("lastmodified"),

    )
'''
        GridFieldText("label", title=_("этикетка"), field_name="label__file", key=False, formatter="showlink",
                      extra = ('"formatoptions": {"baseLinkUrl":"/data/qm/productpassportlabel/", "showaction ":"255", "target":"_blank"}'), #, "addParam": "?source=grid"
                      editable=False),
'''

''' FOR DETAIL VIEW
class MobileHangerView(DetailView):
    model = MobileHanger
    template_name = 'mobilehanger_view.html'
    context_object_name = 'mobilehanger'
    pk_url_kwarg = 'pk'
'''

class MobileHangerLabelPreviewView(View): # Предварительный просмотр шильдика мобильного вешала
    """Предварительный просмотр шильдика"""
    def get(self, request):
        hanger_id = request.GET.get('id')
        mobile_hanger = get_object_or_404(MobileHanger, id=hanger_id)
        # Если шильдик уже существует, используем его
        svg_path = mobile_hanger.label.file.path
        if hasattr(mobile_hanger, 'label') and svg_path:
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
    