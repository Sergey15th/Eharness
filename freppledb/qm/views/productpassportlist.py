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
    ProductPassport,
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

class ProductPassportList(GridReport):
    def label_gen(self):
        return
    title = _("Паспорт продукта")
    actions = [
    {
        "name": "label_preview",
        "label": "LABEL",
        "function": "label_gen()",
    }]
    basequeryset = ProductPassport.objects.all()
    model = ProductPassport
    frozenColumns = 0
    editable = True
    help_url = "help/productpassport.html"
    message_when_empty = Template( # TODO: СДЕЛАТЬ WIZARD ДЛЯ ЗАГРУЗКИ PRODUCTPASSPORTLIST, ПОД ШАГОМ №xx
        """
        <h3>Создайте паспорт продукта</h3>
        <br>
        Паспорт продукта создаётся автоматически при создании партий номенклатуры.
        При автоматическом создании, паспортам из партии автоматически присваиваются серийные номера<br>
        <br>
        <br><br>
        <div role="group" class="btn-group.btn-group-justified">
        <a href="{{request.prefix}}/data/qm/productpassportlist/add/" class="btn btn-primary">Create a product passport<br>in a form</a>
        <a href="{{request.prefix}}/wizard/load/productpassportlist/?currentstep=66" class="btn btn-primary">Wizard to upload productpassportlist<br>from a spreadsheet</a>
        </div>
        <br>
        """
    )
    rows = (
        GridFieldText("id", title=_("ID"), formatter="detail", model=ProductPassport, extra='"role":"qm/productpassport"',),
        GridFieldDateTime("date", title=_("Дата создания"), extra = ('"formatoptions":{"srcformat":"Y-m-d H:i:s","newformat":"%s H:i:s"}' % settings.DATE_FORMAT), editable=False),
        GridFieldInteger("serial_number", title=_("s/n"), editable=False),
        GridFieldHierarchicalText( "manufacturing_order", title=_("Заказ"), field_name="manufacturing_order", key=False, formatter="text", ),
        GridFieldText( "item", title=_("Продукт"), field_name="manufacturing_order__operation__item", key=False, formatter="text", editable=False ),  
        GridFieldText("label", title=_("этикетка"), field_name="label__file", key=False, formatter="showlink",
                      extra = ('"formatoptions": {"baseLinkUrl":"/data/qm/productpassportlabel/", "showaction ":"255", "target":"_blank"}'), #, "addParam": "?source=grid"
                      editable=False),
        GridFieldText("manufacturing_order__batch", title=_("Партия"), field_name="manufacturing_order__batch", editable=False),
        GridFieldText("product_qrcode", title=_("QR"), field_name="product_qrcode", editable=False),
        GridFieldText("status", title=_("Состояние"), field_name="status", editable=False),
        GridFieldText("part_name", title=_("Чертёж"), field_name="part_name", ),
        GridFieldText("firmware", title=_("Версия ПО"), field_name="firmware", ),
        GridFieldText("specification", title=_("Спецификация"), field_name="specification", ),
        GridFieldText("sertificate", title=_("Сертификат"), field_name="sertificate", ),
        GridFieldDateTime("sertificate_validto", title=_("Действителен до"), extra = ('"formatoptions":{"srcformat":"Y-m-d H:i:s","newformat":"%s H:i:s"}' % settings.DATE_FORMAT)),
        GridFieldText("last_maintenance", title=_("Последнее ТО"), field_name="last_maintenance", ),
        GridFieldDateTime("last_maintenance_date", title=_("Дата последнего ТО"), extra = ('"formatoptions":{"srcformat":"Y-m-d H:i:s","newformat":"%s H:i:s"}' % settings.DATE_FORMAT)),
        GridFieldText("user_manual", title=_("Руководство пользователя"), field_name="user_manual", ),
        GridFieldText("service_manual", title=_("Руководство по обслуживанию"), field_name="service_manual", ),
        GridFieldText("url", title=_("url"), field_name="url", ),
        GridFieldText("source", title=_("source"), initially_hidden=True, editable=False),
        GridFieldLastModified("lastmodified", editable=False),
)
'''
        GridFieldText("labeltemplate", title=_("Шаблон этикетки"), field_name="label_path", key=False, formatter="showlink",
                      extra = ('"formatoptions": {"baseLinkUrl":"/data/qm/productpassportlabel/", "showaction ":"255", "target":"_blank"}'), #, "addParam": "?source=grid"
                      editable=False),
'''