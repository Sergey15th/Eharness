from django.views.generic import View, DetailView
from django.http import HttpResponse, request
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import mm
from django.utils.translation import gettext_lazy as _
from io import BytesIO
from barcode import Code128
from barcode.writer import ImageWriter
from django.shortcuts import get_object_or_404
from django.template import Template
from freppledb.common.report import (
    GridReport,
    GridFieldLastModified,
    GridFieldText,

)
from freppledb.labels.models import (
    LabelTemplate,
)
class CreatedLabelList(GridReport):
    title = _("Созданные этикетки")
    basequeryset = LabelTemplate.objects.all()
    model = LabelTemplate
    frozenColumns = 0
    editable = True
    help_url = "help/label.html"
    message_when_empty = Template(
        """
        <h3>Создайте этикетки</h3>
        <br>
        Различные этикетки для готовой продукции, упаковки и т.п.<br>
        После создания этикеток их возможно напечатать.<br>
        <br><br>
        <div role="group" class="btn-group.btn-group-justified">
        <a href="{{request.prefix}}/data/qm/label/add/" class="btn btn-primary">Create a single label<br>in a form</a>
        <a href="{{request.prefix}}/wizard/load/production/?currentstep=25" class="btn btn-primary">Wizard to upload labels<br>from a spreadsheet</a>
        </div>
        <br>
        """
    )
    rows = (
        GridFieldText(
            "id",
            title=_("id"),
            key=True,
            formatter="detail",
            extra='"role":"qm/label"',
        ),
        GridFieldText(
            "name",
            title=_("name"),
        ),
        GridFieldText(
            "template",
            title=_("IM"),
            formatter="imagenew",
            key=False,
        ),
        GridFieldText("source", title=_("source"), initially_hidden=True),
        GridFieldLastModified("lastmodified"),
    )

