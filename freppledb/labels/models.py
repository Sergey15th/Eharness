from django.db import models
from freppledb.input.models.operationplan import ManufacturingOrder
from freppledb.technology.models import ItemT
from freppledb.common.models import AuditModel
from django.utils.translation import gettext_lazy as _
import re
import cairosvg
import svglue
from django.core.exceptions import ValidationError
from freppledb.labels.services import save_svg_to_file, escape_text
from freppledb.settings import MEDIA_ROOT, MEDIA_URL
import os

class LabelTemplate(AuditModel):
  def fix_svg_qr_codes(self,svg_content):
    # Добавляем xmlns:xlink в корневой тег, если его нет
    if 'xmlns:xlink' not in svg_content:
        svg_content = svg_content.replace('<svg ', '<svg xmlns:xlink="http://www.w3.org/1999/xlink" ')
    
    # Заменяем неправильные префиксы ns0, ns1 и т.д. на xlink
    pattern = r'ns\d+:href="([^"]+)"'
    svg_content = re.sub(pattern, r'xlink:href="\1"', svg_content)
    return svg_content
  
  def generate_svg(self, instance, svg_name):
    """Генерирует SVG шильдик на основе шаблона"""
    # Загружаем шаблон
    template = svglue.load(file=self.template)
    # Заменяем текстовые элементы
    for elem_key in template._tspan_subs: # Перебираем все текстовые template-id
        elem_key_clean = re.sub(r'\d+$', '', elem_key)
        try:
            parts = elem_key_clean.split('.') # Смотрим на структуру ссылки в SVG файле
            current_obj = instance
            for part in parts:
                if part == 'item': # Если обращение к аттрибуту объекта Item, то подменяем его ItemT для возможности доступа к расширенным данным
                    current_obj = ItemT.objects.get(item_ptr_id=getattr(current_obj, part))
                else:
                    current_obj = getattr(current_obj, part)
                if current_obj is None:
                    value = None
            value = current_obj
        except (AttributeError, ValueError):
            value = None
        if value is not None:
            template.set_text(elem_key, escape_text(str(value)))
    for elem_key in template._rect_subs: # Перебираем все прямоугольники template-id
        elem_key_clean = re.sub(r'\d+$', '', elem_key)
        try:
            parts = elem_key_clean.split('.')
            current_obj = instance
            for part in parts:
                if part == 'item': # Если обращение к аттрибуту объекта Item, то подменяем его ItemT для возможности доступа к расширенным данным
                    current_obj = ItemT.objects.get(item_ptr_id=getattr(current_obj, part))
                else:
                    current_obj = getattr(current_obj, part)
                if current_obj is None:
                    value = None
            value = current_obj
        except (AttributeError, ValueError):
            value = None
        if value is not None:
            path = os.path.join(MEDIA_ROOT, str(value)) # Берём файл из MEDIA_ROOT/img/qr/*.png
            template.set_image(elem_key, file=path, mimetype='image/png')
    src = template.__str__()
    # Рендерим финальный SVG
    src=self.fix_svg_qr_codes(src)
    ## Нужно сохранить файл SVG и вернуть ссылку на него
    safe_name = re.sub(r'[^\w\-_.]', '_', svg_name)
    return save_svg_to_file(src, os.path.join(MEDIA_ROOT, 'svg', self.dir, safe_name + '.svg'))
  
  def validate_svg(file):
    SVG_R = r'(?:<\?xml\b[^>]*>[^<]*)?(?:<!--.*?-->[^<]*)*(?:<svg|<!DOCTYPE svg)\b'
    SVG_RE = re.compile(SVG_R, re.DOTALL)
    # an example SVG file:
    try:
       file_contents = file.read().decode('utf-8')  # Use utf-8
       file.seek(0)  # Reset file pointer after reading        
       is_svg = SVG_RE.match(file_contents) is not None
       if not is_svg:
            raise ValidationError("File is not a valid SVG")
    except (UnicodeDecodeError, AttributeError) as e:
       raise ValidationError("Error reading file") from e
  name = models.CharField(_("name"), max_length=300)
  dir = models.CharField(_("directory"), max_length=300, default = '')
  template = models.FileField(upload_to='svg/', validators=[validate_svg])
  def __str__(self):
      # Fixed: was using self.name twice, changed to show barcode if available
      return f"#{self.name} - {self.template}"
  class Meta(AuditModel.Meta):
    db_table = 'lb_labels'                 # Name of the database table
    verbose_name = _('Шаблон этикетки')          # A translatable name for the entity
    verbose_name_plural = _('Шаблоны этикеток')  # Plural name
    #ordering = ['']

class CreatedLabel(AuditModel):
    template = models.ForeignKey(LabelTemplate, on_delete=models.CASCADE)
    file = models.FileField(upload_to='created_labels/')
    name = models.CharField(_("name"), max_length=300)
    dir = models.CharField(_("directory"), max_length=300, default = '')
    def __str__(self):
        # Fixed: was using self.name twice, changed to show barcode if available
        return f"#{self.name} - {self.file}"
    class Meta(AuditModel.Meta):
        db_table = 'lb_createdlabels'                 # Name of the database table
        verbose_name = _('Созданная этикетка')          # A translatable name for the entity
        verbose_name_plural = _('Созданные этикетки')  # Plural name
        #ordering = ['']