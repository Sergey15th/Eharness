from django.conf import settings
from django.contrib.admin.utils import unquote
from django.db.models.functions import Cast
from django.db.models import Q, IntegerField
from django.db.models.expressions import RawSQL
from django.template import Template
from django.utils.translation import gettext_lazy as _
from django.utils.encoding import force_str
from django.utils.text import format_lazy
from django.db.models import Case, When, Value, CharField, DecimalField, Count, Min, Max, F
from django.db.models.functions import Concat
from django.contrib.postgres.aggregates import ArrayAgg

from freppledb.boot import getAttributeFields
from freppledb.input.views import (
    ItemList,
)
from freppledb.technology.models import (
    ConnectionList #, SolderingScheme
)
from freppledb.technology.models import (
    ItemT
)
from freppledb.input.models import (
    Item, Operation
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

class ConnectionListList(GridReport):
    title = _("Таблица соединений")
    basequeryset = ConnectionList.objects.all()
    model = ConnectionList
    frozenColumns = 0
    editable = True
    help_url = "help/connectionlist.html"
    message_when_empty = Template( # TODO: СДЕЛАТЬ WIZARD ДЛЯ ЗАГРУЗКИ CUTLIST, ПОД ШАГОМ №11
        """
        <h3>Создайте таблицу соединений</h3>
        <br>
        Таблица соединений является исходной таблицей для карт резки, обжимки и пайки.
        Таблица соединений представляет собой список проводов и гофротруб, которые имеются в жгуте.
        Для каждого провода (гофротрубы) необходимо указать наименование, длину, параметры концов проводов и т.п.<br>
        <br>
        <br><br>
        <div role="group" class="btn-group.btn-group-justified">
        <a href="{{request.prefix}}/data/technology/connectionlist/add/" class="btn btn-primary">Create a single connection<br>in a form</a>
        <a href="{{request.prefix}}/wizard/load/production/?currentstep=11" class="btn btn-primary">Wizard to upload connectionlist<br>from a spreadsheet</a>
        </div>
        <br>
        """
    )
    rows = (
        GridFieldText("id", title=_("ID"), formatter="detail", model=ConnectionList, extra='"role":"technology/connectionlist"',),
        GridFieldText("hanged_no", title=_("№ МВ")),
        GridFieldText("SP_pos", title=_("Поз.")),
        GridFieldHierarchicalText(
            "operation",
            title=_("Операция"),
            field_name="operation__name",
            key=False,
            formatter="detail",
            extra='"role":"input/operation"',
            model=Operation,
        ),
        GridFieldHierarchicalText(
            "item",
            title=_("Провод"),
            field_name="item__short_name",
            key=False,
            formatter="detail",
            extra='"role":"technology/itemt"',
            model=ItemT,
        ),
        GridFieldText("wire_no", title=_("Имя жилы")),
        GridFieldInteger(
            "quantity", title=_("Кол-во")
        ),
        GridFieldHierarchicalText(
            "from_tip",
            title=_("наконечник начала"),
            field_name="from_tip__image",
            key=False,
            formatter="imagenew",
            #extra='"role":"technology/itemt"',
            #model=ItemT,
        ),
        GridFieldHierarchicalText(
            "to_tip",
            title=_("наконечник конца"),
            field_name="to_tip__imagef",
            key=False,
            formatter="imagenew",
            #extra='"role":"technology/itemt"',
            #model=ItemT,
        ),
        GridFieldNumber("start_strip", title=_("Зачистка начало, мм")),
        GridFieldBool("start_tinning", title=_("облудить начало"), formatter='checkbox'),
        GridFieldHierarchicalText(
            "from_seal",
            title=_("уплотнитель начала"),
            field_name="from_seal__image",
            key=False,
            formatter="imagenew",
            #extra='"role":"technology/itemt"',
            #model=ItemT,
        ),
        GridFieldNumber("length", title=_("Длина, мм")),
        GridFieldHierarchicalText(
            "to_seal",
            title=_("уплотнитель конца"),
            field_name="to_seal__imagef",
            key=False,
            formatter="imagenew",
            #extra='"role":"technology/itemt"',
            #model=ItemT,
        ),
        GridFieldBool("end_tinning", title=_("облудить конец"), formatter='checkbox'),
        GridFieldNumber("end_strip", title=_("Зачистка конец, мм")),
        GridFieldNumber("allowance", title=_("Припуск, мм")),
        GridFieldBool("soldering", title=_("пайка"), formatter='checkbox'),
        GridFieldText("source", title=_("source")),
        GridFieldLastModified("lastmodified"),
    )

class CutListList(GridReport):
    @classmethod
    def basequeryset(reportclass, request, *args, **kwargs):
        qset = ConnectionList.objects.select_related('item').annotate(
                # Нормализуем зачистки: всегда меньшая значение first
                normalized_start_strip=Case(
                    When(
                        Q(start_strip__isnull=False, end_strip__isnull=False,
                        start_strip__lte=F('end_strip')),
                        then=F('start_strip')
                    ),
                    When(
                        Q(start_strip__isnull=False, end_strip__isnull=False,
                        end_strip__lte=F('start_strip')),
                        then=F('end_strip')
                    ),
                    When(start_strip__isnull=False, then=F('start_strip')),
                    When(end_strip__isnull=False, then=F('end_strip')),
                    default=Value(0),
                    output_field=DecimalField(max_digits=20, decimal_places=0)
                ),
                normalized_end_strip=Case(
                    When(
                        Q(start_strip__isnull=False, end_strip__isnull=False,
                        start_strip__lte=F('end_strip')),
                        then=F('end_strip')
                    ),
                    When(
                        Q(start_strip__isnull=False, end_strip__isnull=False,
                        end_strip__lte=F('start_strip')),
                        then=F('start_strip')
                    ),
                    When(start_strip__isnull=False, then=F('start_strip')),
                    When(end_strip__isnull=False, then=F('end_strip')),
                    default=Value(0),
                    output_field=DecimalField(max_digits=20, decimal_places=0)
                )
            ).annotate(
                # Создаем ключ для группировки (после всех аннотаций)
                group_key=Concat(
                    'length',
                    Value('|'),
                    'item__short_name',
                    Value('|'),
                    Cast('normalized_start_strip', CharField()),
                    Value('|'),
                    Cast('normalized_end_strip', CharField()),
                    output_field=CharField()
                )
            ).values(
                'length',
                'item__short_name',
                'normalized_start_strip',
                'normalized_end_strip',
                'group_key'
            ).annotate(
                total_quantity=Count('id'),
                wire_count=Count('wire_no', distinct=True),
                min_start_strip=Min('start_strip'),
                max_start_strip=Max('start_strip'),
                min_end_strip=Min('end_strip'),
                max_end_strip=Max('end_strip'),
                ids=ArrayAgg('id', distinct=True)  # Только для PostgreSQL
            ).order_by('length', 'item__short_name')
        return qset
    title = _("Карта резки")
    model = ConnectionList
    frozenColumns = 0
    default_sort = ""
    editable = False
    help_url = "help/cutlist.html"
    message_when_empty = Template( # TODO: СДЕЛАТЬ WIZARD ДЛЯ ЗАГРУЗКИ CUTLIST, ПОД ШАГОМ №11
        """
        <h3>Карты резки создаются с помощью таблицы соединений</h3>
        <br>
        Для операций резки и зацистки проводов, необходимо создать таблицу соединений.
        Таблица соединений представляет собой список проводов и (или) гофротруб, которые
        необходимо нарезать и зачистить, с указанием длин проводов, параметров концов проводов и т.п.<br>
        <br>
        <br><br>
        <div role="group" class="btn-group.btn-group-justified">
        <a href="{{request.prefix}}/data/technology/connectionlist/add/" class="btn btn-primary">Create a single connection<br>in a form</a>
        <a href="{{request.prefix}}/wizard/load/production/?currentstep=11" class="btn btn-primary">Wizard to upload connectionlist<br>from a spreadsheet</a>
        </div>
        <br>
        """
    )
    rows = (
        GridFieldText("id", title=_("ID"), formatter="detail", model=ConnectionList, extra='"role":"technology/connectionlist"',),
        GridFieldText("hanged_no", title=_("№ МВ")),
        GridFieldText("SP_pos", title=_("Поз.")),
        GridFieldHierarchicalText(
            "operation",
            title=_("Операция"),
            field_name="operation__name",
            key=False,
            formatter="detail",
            extra='"role":"input/operation"',
            model=Operation,
        ),
        GridFieldHierarchicalText(
            "item",
            title=_("Провод"),
            field_name="item__short_name",
            key=False,
            formatter="detail",
            extra='"role":"technology/itemt"',
            model=ItemT,
        ),
        GridFieldText("wire_no", title=_("Имя жилы")),
        GridFieldInteger(
            "quantity", title=_("Кол-во")
        ),
        GridFieldHierarchicalText(
            "from_tip",
            title=_("наконечник начала"),
            field_name="from_tip__image",
            key=False,
            formatter="imagenew",
            #extra='"role":"technology/itemt"',
            #model=ItemT,
        ),
        GridFieldHierarchicalText(
            "to_tip",
            title=_("наконечник конца"),
            field_name="to_tip__imagef",
            key=False,
            formatter="imagenew",
            #extra='"role":"technology/itemt"',
            #model=ItemT,
        ),
        GridFieldNumber("start_strip", title=_("Зачистка начало, мм")),
        GridFieldBool("start_tinning", title=_("облудить начало"), formatter='checkbox'),
        GridFieldHierarchicalText(
            "from_seal",
            title=_("уплотнитель начала"),
            field_name="from_seal__image",
            key=False,
            formatter="imagenew",
            #extra='"role":"technology/itemt"',
            #model=ItemT,
        ),
        GridFieldNumber("length", title=_("Длина, мм")),
        GridFieldNumber("total_quantity", title=_("кол-во")),
        #GridFieldNumber("wire_count", title=_("кол-во пр")),
        #GridFieldText("strip_key", title=_("SK")),
        GridFieldText("group_key", title=_("GK")),
        GridFieldHierarchicalText(
            "to_seal",
            title=_("уплотнитель конца"),
            field_name="to_seal__imagef",
            key=False,
            formatter="imagenew",
            #extra='"role":"technology/itemt"',
            #model=ItemT,
        ),
        GridFieldBool("end_tinning", title=_("облудить конец"), formatter='checkbox'),
        GridFieldNumber("end_strip", title=_("Зачистка конец, мм")),
        GridFieldNumber("allowance", title=_("Припуск, мм")),
        GridFieldBool("soldering", title=_("пайка"), formatter='checkbox'),
        GridFieldText("source", title=_("source")),
        GridFieldLastModified("lastmodified"),
    )

class CrimpListList(GridReport):
    title = _("Карта обжимки")
    #basequeryset = CutList.objects.all() #Все провода
    basequeryset = ConnectionList.objects.filter(from_tip__isnull=False) | ConnectionList.objects.filter(to_tip__isnull=False) #Все провода с наконечниками, у которых from_tip или to_tip не null
    model = ConnectionList
    frozenColumns = 0
    editable = False
    help_url = "help/crimplist.html"
    message_when_empty = Template( # TODO: СДЕЛАТЬ WIZARD ДЛЯ ЗАГРУЗКИ CUTLIST, ПОД ШАГОМ №11
        """
        <h3>Карты обжимки создаюся с помощью таблицы соединений</h3>
        <br>
        Для операций обжимки проводов, необходимо создать таблицу соединений.
        Карта обжимки представляет собой список проводов, которые необходимо обжать наконечниками,
        указав "наконечник начала" или "наконечник конца"<br>
        <br>
        <br><br>
        <div role="group" class="btn-group.btn-group-justified">
        <a href="{{request.prefix}}/data/technology/connectionlist/add/" class="btn btn-primary">Create a single connection<br>in a form</a>
        <a href="{{request.prefix}}/wizard/load/production/?currentstep=11" class="btn btn-primary">Wizard to upload connectionlist<br>from a spreadsheet</a>
        </div>
        <br>
        """
    )
    rows = (
        GridFieldText("id", title=_("ID"), formatter="detail", model=ConnectionList, extra='"role":"technology/cutlist"',),
        GridFieldText("hanged_no", title=_("№ МВ")),
        GridFieldText("SP_pos", title=_("Поз.")),
        GridFieldHierarchicalText(
            "operation",
            title=_("Операция"),
            field_name="operation__name",
            key=False,
            formatter="detail",
            extra='"role":"input/operation"',
            model=Operation,
        ),
        GridFieldHierarchicalText(
            "item",
            title=_("Провод"),
            field_name="item__short_name",
            key=False,
            formatter="detail",
            extra='"role":"technology/itemt"',
            model=ItemT,
        ),
        GridFieldText("wire_no", title=_("Имя жилы")),
        GridFieldInteger(
            "quantity", title=_("Кол-во")
        ),
        GridFieldHierarchicalText(
            "from_tip",
            title=_("наконечник начала"),
            field_name="from_tip__image",
            key=False,
            formatter="imagenew",
            #extra='"role":"technology/itemt"',
            #model=ItemT,
        ),
        GridFieldHierarchicalText(
            "to_tip",
            title=_("наконечник конца"),
            field_name="to_tip__imagef",
            key=False,
            formatter="imagenew",
            #extra='"role":"technology/itemt"',
            #model=ItemT,
        ),
        GridFieldNumber("start_strip", title=_("Зачистка начало, мм")),
        GridFieldBool("start_tinning", title=_("облудить начало"), formatter='checkbox'),
        GridFieldHierarchicalText(
            "from_seal",
            title=_("уплотнитель начала"),
            field_name="from_seal__image",
            key=False,
            formatter="imagenew",
            #extra='"role":"technology/itemt"',
            #model=ItemT,
        ),
        GridFieldNumber("length", title=_("Длина, мм")),
        GridFieldHierarchicalText(
            "to_seal",
            title=_("уплотнитель конца"),
            field_name="to_seal__imagef",
            key=False,
            formatter="imagenew",
            #extra='"role":"technology/itemt"',
            #model=ItemT,
        ),
        GridFieldBool("end_tinning", title=_("облудить конец"), formatter='checkbox'),
        GridFieldNumber("end_strip", title=_("Зачистка конец, мм")),
        GridFieldNumber("allowance", title=_("Припуск, мм")),
        GridFieldBool("soldering", title=_("пайка"), formatter='checkbox'),
        GridFieldText("source", title=_("source")),
        GridFieldLastModified("lastmodified"),
    )

class ItemTList(GridReport):
    title = _("Номенклатура")
    basequeryset = ItemT.objects.all()
    model = ItemT
    frozenColumns = 1
    editable = False
    help_url = "help/itemT.html"
    message_when_empty = Template(
        """
        <h3>Define T-items</h3>
        <br>
        A basic piece of master data is the list of items to plan.<br>
        End products, intermediate products and raw materials all need to be defined.<br>
        <br><br>
        <div role="group" class="btn-group.btn-group-justified">
        <a href="{{request.prefix}}/data/input/item/add/" class="btn btn-primary">Create a single item<br>in a form</a>
        <a href="{{request.prefix}}/wizard/load/production/?currentstep=1" class="btn btn-primary">Wizard to upload items<br>from a spreadsheet</a>
        </div>
        <br>
        """
    )
    rows = (
        GridFieldHierarchicalText(
            "name",
            title=_("name"),
            key=True,
            formatter="detail",
            extra='"role":"technology/itemt"',
            model=Item,
        ),
        GridFieldText("description", title=_("description")),
        GridFieldText("category", title=_("category"), initially_hidden=True,),
        GridFieldText("subcategory", title=_("subcategory"), initially_hidden=True),
        GridFieldText(
            "image",
            title=_("IM"),
            formatter="imagenew",
            key=False,
        ),
        GridFieldNumber("image_height", title=_("высота изобр."), initially_hidden=True),
        GridFieldNumber("image_width", title=_("ширина изобр."), initially_hidden=True),
        GridFieldText("short_name", title=_("арт."), initially_hidden=True),
        GridFieldText(
            "owner",
            title=_("owner"),
            field_name="owner__name",
            formatter="detail",
            extra='"role":"technology/itemt"',
        ),
        GridFieldCurrency("cost", title=_("cost")),
        GridFieldNumber("weight", title=_("weight"), initially_hidden=True),
        GridFieldNumber("volume", title=_("volume"), initially_hidden=True),
        GridFieldText("uom", title=_("unit of measure"), initially_hidden=True),
        GridFieldInteger(
            "periodofcover", title=_("period of cover"), initially_hidden=True
        ),
        GridFieldChoice(
            "type", title=_("type"), choices=ItemT.types, initially_hidden=True
        ),
        GridFieldText("source", title=_("source"), initially_hidden=True),
        GridFieldLastModified("lastmodified"),
    )

class SolderingList(GridReport):
    title = _("Карта пайки")
    basequeryset = ConnectionList.objects.filter(soldering=True) | ConnectionList.objects.filter(start_tinning=True) | ConnectionList.objects.filter(end_tinning=True)
    model = ConnectionList
    frozenColumns = 0
    editable = False
    help_url = "help/cutlist.html"
    message_when_empty = Template( # TODO: СДЕЛАТЬ WIZARD ДЛЯ ЗАГРУЗКИ CUTLIST, ПОД ШАГОМ №11
        """
        <h3>Карты пайки создаюся с помощью таблицы соединений</h3>
        <br>
        Для операций пайки проводов, необходимо создать таблицу соединений,
        с указанием операции пайки (столбец "пайка"), или  "облудить начало" "облудить конец".
        Карта пацйки представляет собой список проводов, которые необходимо лудить или паять<br>
        <br>
        <br><br>
        <div role="group" class="btn-group.btn-group-justified">
        <a href="{{request.prefix}}/data/technology/connectionlist/add/" class="btn btn-primary">Create a single connection<br>in a form</a>
        <a href="{{request.prefix}}/wizard/load/production/?currentstep=11" class="btn btn-primary">Wizard to upload connectionlist<br>from a spreadsheet</a>
        </div>
        <br>
        """
    )
    rows = (
        GridFieldText("id", title=_("ID"), formatter="detail", model=ConnectionList, extra='"role":"technology/cutlist"',),
        GridFieldText("hanged_no", title=_("№ МВ")),
        GridFieldText("SP_pos", title=_("Поз.")),
        GridFieldHierarchicalText(
            "operation",
            title=_("Операция"),
            field_name="operation__name",
            key=False,
            formatter="detail",
            extra='"role":"input/operation"',
            model=Operation,
        ),
        GridFieldHierarchicalText(
            "item",
            title=_("Провод"),
            field_name="item__short_name",
            key=False,
            formatter="detail",
            extra='"role":"technology/itemt"',
            model=Item,
        ),
        GridFieldText("wire_no", title=_("Имя жилы")),
        GridFieldInteger(
            "quantity", title=_("Кол-во")
        ),
        GridFieldNumber("start_strip", title=_("Зачистка начало, мм")),
        GridFieldBool("start_tinning", title=_("облудить начало"), formatter='checkbox'),
        GridFieldNumber("length", title=_("Длина, мм")),
        GridFieldBool("end_tinning", title=_("облудить конец"), formatter='checkbox'),
        GridFieldNumber("end_strip", title=_("Зачистка конец, мм")),
        GridFieldBool("soldering", title=_("пайка"), formatter='checkbox'),
        GridFieldText("source", title=_("source")),
        GridFieldLastModified("lastmodified"),
    )
