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
    ProductPassport,
    QualityControl,
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

class QualityControlList(GridReport):
    title = _("Контроль качества")
    basequeryset = QualityControl.objects.all()
    model = QualityControl
    frozenColumns = 0
    editable = True
    help_url = "help/qualitycontrollist.html"
    message_when_empty = Template( # TODO: СДЕЛАТЬ WIZARD ДЛЯ ЗАГРУЗКИ PRODUCTPASSPORTLIST, ПОД ШАГОМ №xx
        """
        <h3>Создайте запись контроля качества</h3>
        <br>
        Запись контроля качества создаётся автоматически при проведении электрических испытаний жгута.
        <br>
        <br><br>
        <div role="group" class="btn-group.btn-group-justified">
        <a href="{{request.prefix}}/data/qm/qualitycontrollist/add/" class="btn btn-primary">Create a qualitycontrol<br>in a form</a>
        <a href="{{request.prefix}}/wizard/load/qualitycontrollist/?currentstep=77" class="btn btn-primary">Wizard to upload qualitycontrollist<br>from a spreadsheet</a>
        </div>
        <br>
        """
    )
    rows = (
        GridFieldText("id", title=_("ID"), formatter="text", model=ProductPassport, extra='"role":"qm/qualitycontrol"',),
        GridFieldDateTime("date", title=_("Дата создания"), extra = ('"formatoptions":{"srcformat":"Y-m-d H:i:s","newformat":"%s H:i:s"}' % settings.DATE_FORMAT), editable=False),
        GridFieldHierarchicalText("product_passport", title=_("Паспорт продукта"), field_name="product_passport", key=False, formatter="text", extra='"role":"qm/productpassport"', model=ProductPassport, ),
        GridFieldText("type", title=_("Вид проверки"), field_name="type__type", editable=False),
        GridFieldText("control_result", title=_("Результат"), field_name="control_result", editable=False),
        GridFieldText("control_result_log", title=_("Данные контроля"), field_name="control_result_log", editable=False),
        GridFieldText("source", title=_("source"), initially_hidden=True),
        GridFieldLastModified("lastmodified"),
    )