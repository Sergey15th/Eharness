from django.views.generic import View, DetailView
from django.http import HttpResponse, request
from freppledb.labels.models import LabelTemplate
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

class LabelTemplateList(GridReport):
    title = _("Шаблоны этикеток")
    basequeryset = LabelTemplate.objects.all()
    model = LabelTemplate
    frozenColumns = 0
    editable = True
    help_url = "help/labeltemplate.html"
    message_when_empty = Template(
        """
        <h3>Создайте шаблоны этикеток </h3>
        <br>
        Различные этикетки для готовой продукции, упаковки и т.п.<br>
        После создания этикеток их возможно напечатать.<br>
        <br><br>
        <div role="group" class="btn-group.btn-group-justified">
        <a href="{{request.prefix}}/data/labels/labeltemplate/add/" class="btn btn-primary">Create a single label template<br>in a form</a>
        <a href="{{request.prefix}}/wizard/load/production/?currentstep=35" class="btn btn-primary">Wizard to upload labels templates<br>from a spreadsheet</a>
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
            extra='"role":"labels/labeltemplate"',
        ),
        GridFieldText(
            "name",
            title=_("name"),
        ),
        GridFieldText(
            "template",
            title=_("IM"),
            formatter="imagenew2",
            key=False,
        ),
        GridFieldText("source", title=_("source"), initially_hidden=True),
        GridFieldLastModified("lastmodified"),
    )

