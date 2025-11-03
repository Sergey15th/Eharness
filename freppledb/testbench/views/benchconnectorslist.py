from django.template import Template
from django.utils.translation import gettext_lazy as _

from freppledb.technology.models import (
    ItemT
)
from freppledb.testbench.models import (
    BenchConnectors
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


class BenchConnectorsList(GridReport):
    title = _("Разъёмы стенда")
    basequeryset = BenchConnectors.objects.all()
    model = BenchConnectors
    frozenColumns = 0
    editable = True
    help_url = "help/BenchConnectors.html"
    message_when_empty = Template(
        """
        <h3>Создайте разъёмы стенда</h3>
        <br>
        Здесь перечислены все разъёмы, которые находятся в испытательном стенде.<br>
        Если в испытательный стенд добавляется (встраивается) новый разъём,
        то он должен быть описан здесь<br>
        <br><br>
        <div role="group" class="btn-group.btn-group-justified">
        <a href="{{request.prefix}}/data/testbench/benchconnectors/add/" class="btn btn-primary">Create a single connector<br>in a form</a>
        <a href="{{request.prefix}}/wizard/load/benchconnectors/?currentstep=111" class="btn btn-primary">Wizard to upload bench connectors<br>from a spreadsheet</a>
        </div>
        <br>
        """
    )
    rows = (
        GridFieldHierarchicalText("id", title=_("ID"), key=True, formatter="detail", extra='"role":"testbench/benchconnectors"', model=BenchConnectors, ),
        GridFieldText("connector_name", title=_("Наименование разъёма")),
        GridFieldText("connector_designation", title=_("Обозначение на стенде"), ),
        GridFieldText("connector", title=_("Разъём"), field_name="connector", formatter="detail", extra='"role":"technology/itemt"', ),
        GridFieldNumber("connector_pins_no", title=_("Количество контактов"), ),

        GridFieldText("source", title=_("source"), initially_hidden=True),
        GridFieldLastModified("lastmodified"),
    )
