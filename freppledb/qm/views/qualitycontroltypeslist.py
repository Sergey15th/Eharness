from django.conf import settings
from django.contrib.admin.utils import unquote
from django.template import Template
from django.utils.translation import gettext_lazy as _
from django.utils.encoding import force_str
from django.utils.text import format_lazy

from freppledb.boot import getAttributeFields
from freppledb.input.models import (
    ManufacturingOrder,
)
from freppledb.input.models import (
    ManufacturingOrder,
)
from freppledb.qm.models import (
    QualityControl,
    QualityControlTypes,
)
from freppledb.technology.models import (
    ItemT,
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

class QualityControlTypesList(GridReport):
    title = _("Виды контроля качества")
    basequeryset = QualityControlTypes.objects.all()
    model = QualityControlTypes
    frozenColumns = 0
    editable = True
    help_url = "help/qualitycontroltypeslist.html"
    message_when_empty = Template( # TODO: СДЕЛАТЬ WIZARD ДЛЯ ЗАГРУЗКИ, ПОД ШАГОМ №xx
        """
        <h3>Создайте запись видов контроля качества</h3>
        <br>
        Записи видов контроля качества создаются для каждой номенклатуры для каждого вида контроля.
        <br>
        <br><br>
        <div role="group" class="btn-group.btn-group-justified">
        <a href="{{request.prefix}}/data/qm/qualitycontroltypeslist/add/" class="btn btn-primary">Create a qualitycontroltypes<br>in a form</a>
        <a href="{{request.prefix}}/wizard/load/qualitycontroltypeslist/?currentstep=88" class="btn btn-primary">Wizard to upload qualitycontroltypeslist<br>from a spreadsheet</a>
        </div>
        <br>
        """
    )
    rows = (
        GridFieldText("id", title=_("ID"), formatter="detail", model=QualityControlTypes, extra='"role":"qm/qualitycontroltypes"',),
        GridFieldHierarchicalText(
            "item",
            title=_("Объект контроля"),
            field_name="item",
            key=False,
            formatter="detail",
            extra='"role":"technology/itemt"',
            model=ItemT,
        ),
        GridFieldText("type", title=_("Вид контроля"), field_name="type", ),
        GridFieldText("source", title=_("source"), initially_hidden=True),
        GridFieldLastModified("lastmodified", initially_hidden=True),
    )