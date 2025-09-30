from django.views.generic import View, DetailView
from django.http import HttpResponse, request
from freppledb.technology.models import ItemT, ProductLabel
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
    GridFieldDateTime,
    GridFieldText,
    GridFieldHierarchicalText,
    GridFieldNumber,
    GridFieldInteger,
    GridFieldCurrency,
    GridFieldChoice,
    GridFieldDuration,
)

class ProductLabelView(View):
    def get(self, request, product_id):
        label = ProductLabel.objects.get(product=product_id)
        
        # Создаем PDF в памяти
        buffer = BytesIO()
        p = canvas.Canvas(buffer, pagesize=(100*mm, 100*mm))  # Размер этикетки
        
        # Дизайн этикетки
        p.setFont("Helvetica-Bold", 10)
        p.drawString(5*mm, 20*mm, label.product.name)
        p.setFont("Helvetica", 8)
        p.drawString(5*mm, 15*mm, f"Арт.: {label.product.code}")
        
        # Генерация штрих-кода (требуется пакет python-barcode)
        barcode_value = label.product.barcode
        barcode = Code128(barcode_value, writer=ImageWriter())
        barcode_path = f"/barcodes/img/barcode_{product_id}.png"
        barcode.write(barcode_path)
        p.drawImage(barcode_path, 5*mm, 5*mm, width=40*mm, height=10*mm)
        
        p.showPage()
        p.save()
        
        buffer.seek(0)
        response = HttpResponse(buffer, content_type='application/pdf')
        response['Content-Disposition'] = f'attachment; filename="label_{label.product.code}.pdf"'
        return response

class ProductLabelPreviewView(DetailView):    
    template_name = 'label_preview.html'
    context_object_name = 'product'

    def get_template_names(self):
        template_type = self.request.GET.get('template', 'standard')
        return [f'labels/preview_{template_type}.html']    
    def get_object(self):
        product_id = self.kwargs.get('product_id')
        return get_object_or_404(ProductLabel, pk=product_id)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        product = self.object
        
        # Добавляем дополнительные данные для предпросмотра
        context.update({
            'barcode_url': product.get_barcode_url(),
            'current_date': timezone.now().strftime("%d.%m.%Y"),
            'price': f"{product.price:.2f} ₽",
            'weight': f"{product.weight} кг" if product.weight else None,
            'manufacturer': product.manufacturer or "",
            'expiry_date': product.expiry_date.strftime("%m.%Y") if product.expiry_date else None
        })
        return context
    
class ProductLabelList(GridReport):
    title = _("Этикетки")
    basequeryset = ProductLabel.objects.all()
    model = ProductLabel
    frozenColumns = 0
    editable = True
    help_url = "help/productlabel.html"
    message_when_empty = Template(
        """
        <h3>Создайте этикетки</h3>
        <br>
        Различные этикетки для готовой продукции, упаковки и т.п.<br>
        После создания этикеток их возможно напечатать.<br>
        <br><br>
        <div role="group" class="btn-group.btn-group-justified">
        <a href="{{request.prefix}}/data/technology/productlabel/add/" class="btn btn-primary">Create a single label<br>in a form</a>
        <a href="{{request.prefix}}/wizard/load/production/?currentstep=15" class="btn btn-primary">Wizard to upload labels<br>from a spreadsheet</a>
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
            extra='"role":"technology/productlabel"',
        ),
        GridFieldText(
            "name",
            title=_("name"),
        ),
        GridFieldHierarchicalText(
            "item",
            title=_("name"),
            key=True,
            formatter="detail",
            extra='"role":"technology/itemt"',
            model=ItemT,
        ),
        GridFieldText("label_template", title=_("label_template")),
        GridFieldText("source", title=_("source"), initially_hidden=True),
        GridFieldLastModified("lastmodified"),
    )

