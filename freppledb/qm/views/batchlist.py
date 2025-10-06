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
    ManufacturingOrder
)
from freppledb.qm.models import (
    BatchList,
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

class BatchListList(GridReport):
    title = _("Партии номенклатуры")
    basequeryset = BatchList.objects.all()
    model = BatchList
    frozenColumns = 0
    editable = True
    help_url = "help/batchlist.html"
    message_when_empty = Template( # TODO: СДЕЛАТЬ WIZARD ДЛЯ ЗАГРУЗКИ BATCHLIST, ПОД ШАГОМ №xx
        """
        <h3>Создайте партии номенклатуры</h3>
        <br>
        Партии номенклатуры создаются автоматически при создании заказа на производство.
        Номер партии присваивается автоматически счётчиком для каждого вида номенклатуры.
        При автоматическом создании, партии номенклатуры автоматически присваивается диапазон серийных номеров<br>
        <br>
        <br><br>
        <div role="group" class="btn-group.btn-group-justified">
        <a href="{{request.prefix}}/data/qm/batchlist/add/" class="btn btn-primary">Create a batch<br>in a form</a>
        <a href="{{request.prefix}}/wizard/load/batchlist/?currentstep=55" class="btn btn-primary">Wizard to upload batchlist<br>from a spreadsheet</a>
        </div>
        <br>
        """
    )
    rows = (
        GridFieldText("id", title=_("ID"), formatter="detail", model=BatchList, extra='"role":"qm/batchlist"',),
        GridFieldHierarchicalText(
            "manufacturing_order",
            title=_("Заказ"),
            field_name="manufacturing_order",
            key=False,
            formatter="detail",
            extra='"role":"input/operationTOCHECK"',
            model=ManufacturingOrder,
        ),
        GridFieldHierarchicalText(
            "manufacturing_order__item",
            title=_("Товарная позиция"),
            field_name="manufacturing_order__item",
            key=False,
            formatter="detail",
            extra='"role":"technology/itemy"',
            model=ItemT,
        ),
        GridFieldInteger(
            "serie_no_start", title=_("Начальный s/n")
        ),
        GridFieldInteger(
            "manufacturing_order__quantity", title=_("Кол. s/n")
        ),
    )