from django.conf import settings
from django.template import Template
from django.utils.translation import gettext_lazy as _
from django.views.generic import DetailView
from freppledb.technology.models import (
    ItemT, TraceScheme, ConnectionList
)
from freppledb.input.models.operation import Operation
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


class TraceSchemeList(GridReport):
    title = _("Схемы трассировки")
    basequeryset = TraceScheme.objects.all()
    model = TraceScheme
    frozenColumns = 0
    editable = True
    help_url = "help/TraceScheme.html"
    message_when_empty = Template( # TODO: СДЕЛАТЬ WIZARD ДЛЯ ЗАГРУЗКИ CUTLIST, ПОД ШАГОМ №11
        """
        <h3>Создайте схемы трассировки</h3>
        <br>
        Схема трассировки представляет собой схему прокладки конкретного провода<br>
        <br>
        <br><br>
        <div role="group" class="btn-group.btn-group-justified">
        <a href="{{request.prefix}}/data/technology/tracescheme/add/" class="btn btn-primary">Create a single item<br>in a form</a>
        <a href="{{request.prefix}}/wizard/load/production/?currentstep=16" class="btn btn-primary">Wizard to upload tracescheme<br>from a spreadsheet</a>
        </div>
        <br>
        """
    )
    rows = (
        GridFieldText("id", title=_("ID"), formatter="detail", model=TraceScheme, extra='"role":"technology/tracescheme"',),
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
            title=_("Схема трассировки"),
            formatter="imagenew",
            key=False,
        ),
        GridFieldText("wire_no", title=_("Имя жилы")),
        GridFieldText("source", title=_("source")),
        GridFieldLastModified("lastmodified"),
)

class TraceSchemeDetailView(DetailView):
    model = TraceScheme
    template_name = 'trace_scheme_detail.html'
    context_object_name = 'scheme'
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Получаем основной объект
        scheme = self.get_object()
        # Добавляем дополнительные данные
        #context['related_objects'] = RelatedModel.objects.filter(main_model=scheme)
        OperationItem = Operation.objects.get(name=scheme.item.name + ' - Нарезка и зачистка')
        CutListItem = ConnectionList.objects.get(wire_no=scheme.wire_no, operation=OperationItem)
        context['wire_no'] = CutListItem.wire_no
        context['hanged_no'] = CutListItem.hanged_no
        return context