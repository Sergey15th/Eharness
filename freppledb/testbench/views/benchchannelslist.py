from django.template import Template
from django.utils.translation import gettext_lazy as _

from freppledb.technology.models import (
    ItemT
)
from freppledb.testbench.models import (
    BenchChannels
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


class BenchChannelsList(GridReport):
    title = _("Подключения стенда")
    basequeryset = BenchChannels.objects.all()
    model = BenchChannels
    frozenColumns = 0
    editable = True
    help_url = "help/BenchChannels.html"
    message_when_empty = Template(
        """
        <h3>Создайте подключения стенда</h3>
        <br>
        Здесь перечислены все подключения, тестовых разъёмов испытательного стенда.<br>
        Если в испытательный стенд добавляется (встраивается) новый разъём,
        то его подключения должны быть описаны здесь<br>
        <br><br>
        <div role="group" class="btn-group.btn-group-justified">
        <a href="{{request.prefix}}/data/testbench/benchchannels/add/" class="btn btn-primary">Create a single channel connection<br>in a form</a>
        <a href="{{request.prefix}}/wizard/load/benchchannels/?currentstep=222" class="btn btn-primary">Wizard to upload bench channels<br>from a spreadsheet</a>
        </div>
        <br>
        """
    )
    rows = (
        GridFieldHierarchicalText("id", title=_("ID"), key=True, formatter="detail", extra='"role":"testbench/benchchannels"', model=BenchChannels, ),
        GridFieldText("bench_connector", title=_("Разъём стенда"), align = "center"),
        GridFieldNumber("bench_pin_no", title=_("Контакт разъёма"), ),
        GridFieldNumber("channel", title=_("Канал ТЖ-04"), ),

        GridFieldText("source", title=_("source"), initially_hidden=True),
        GridFieldLastModified("lastmodified"),
    )
