from django.conf import settings
from django.template import Template
from django.utils.translation import gettext_lazy as _
from django.views.generic import DetailView
from freppledb.technology.models import (
    ItemT, SolderingScheme,
)
from freppledb.common.report import (
    GridReport,
    GridFieldLastModified,
    GridFieldDateTime,
    GridFieldText,
    GridFieldHierarchicalText,
    GridFieldNumber,
    GridFieldInteger,
    GridFieldCurrency,
    GridFieldChoice,
    GridFieldDuration,
    GridFieldBool,
    GridField,
)
import logging

logger = logging.getLogger(__name__)


class SolderingSchemeList(GridReport):
    title = _("Схемы пайки")
    basequeryset = SolderingScheme.objects.all()
    model = SolderingScheme
    frozenColumns = 0
    editable = False
    help_url = "help/solderingscheme.html"
    message_when_empty = Template( # TODO: СДЕЛАТЬ WIZARD ДЛЯ ЗАГРУЗКИ CUTLIST, ПОД ШАГОМ №11
        """
        <h3>Создайте схемы пайки</h3>
        <br>
        Схема пайки представляет собой список номенклатуры и изображений схем пайки, которые
        необходимо отображать<br>
        <br>
        <br><br>
        <div role="group" class="btn-group.btn-group-justified">
        <a href="{{request.prefix}}/data/technology/solderingscheme/add/" class="btn btn-primary">Create a single item<br>in a form</a>
        <a href="{{request.prefix}}/wizard/load/production/?currentstep=12" class="btn btn-primary">Wizard to upload solderingscheme<br>from a spreadsheet</a>
        </div>
        <br>
        """
    )
    rows = (
        GridFieldText("id", title=_("ID"), formatter="detail", model=SolderingScheme, extra='"role":"technology/solderingscheme"',),
        GridFieldHierarchicalText(
            "item",
            title=_("Номенклатура"),
            field_name="item",
            key=False,
            formatter="detail",
            extra='"role":"technology/itemt"',
            model=ItemT,
        ),
        GridFieldText(
            "image",
            title=_("Схема пайки"),
            formatter="imagenew",
            key=False,
        ),
    )

class SolderingSchemeDetailView(DetailView):
    model = SolderingScheme
    template_name = 'soldering_scheme_detail.html'
    context_object_name = 'scheme'