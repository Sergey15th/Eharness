from django.conf import settings
from django.contrib.admin.utils import unquote
from django.db.models.functions import Cast
from django.db.models import Q, IntegerField
from django.db.models.expressions import RawSQL
from django.template import Template
from django.utils.translation import gettext_lazy as _
from django.utils.encoding import force_str
from django.utils.text import format_lazy
from django.views.generic import DetailView

from freppledb.boot import getAttributeFields
from freppledb.technology.models import (
    MobileHanger, ItemT
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
            key=False,
            formatter="detail",
            extra='"role":"technology/itemt"',
            model=ItemT,
        ),
        GridFieldText("source", title=_("source")),
        GridFieldLastModified("lastmodified"),
    )

class MobileHangerView(DetailView):
    model = MobileHanger
    template_name = 'mobilehanger_view.html'
    context_object_name = 'mobilehanger'
