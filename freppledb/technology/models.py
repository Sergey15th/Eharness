from django.db import models
from django.conf import settings

# Use the function "_" for all strings that need translation.
from django.utils.translation import gettext_lazy as _

# A subclass of AuditModel will inherit an field "last_modified" and "source".
from freppledb.common.models import HierarchyModel, AuditModel, Parameter
from freppledb.input.models import Item, Operation

class ItemT(Item):
   image = models.ImageField(upload_to='img/', height_field='image_height', width_field='image_width', null=True, blank=True, default='img/no_image.png')
   image_height = models.IntegerField(blank=True, null=True)
   image_width = models.IntegerField(blank=True, null=True)
   imagef = models.ImageField(upload_to='img/', height_field='imagef_height', width_field='imagef_width', null=True, blank=True)
   imagef_height = models.IntegerField(blank=True, null=True)
   imagef_width = models.IntegerField(blank=True, null=True)
   short_name = models.CharField(_('арт.'), null=True, blank=True)
   
class ConnectionList(AuditModel):
  # Database fields
  id = models.AutoField(_("identifier"), primary_key=True)
  hanged_no = models.CharField(_('№ на вешале'), null=True,
    blank=True, max_length=20, help_text= _('Номер крючка на вешале'))
  
  qr = models.CharField('mQR', null=True, blank=True)
  #  blank=True, default=('8000'), help_text= _('Микро QR'))

  SP_pos = models.DecimalField(_('Позиция в СП'),
    decimal_places=0,
    blank=True,
    null=True,
    max_digits=3,
    default='',
    help_text= _('№ позиции в спецификации или сборочном чертеже')
    )
  operation = models.ForeignKey(
      Operation,
      verbose_name=_("операция"),
      on_delete=models.CASCADE,
      db_index=False,
      related_name='operation_cutlists',
  )
  item = models.ForeignKey(
      ItemT,
      verbose_name=_("провод"),
      on_delete=models.CASCADE,
      db_index=False,
      related_name='item_cutlists',
  )
  wire_no = models.CharField(_('имя провода'), null=False, blank=False, max_length=20, help_text= _('Имя жилы или провода'))
  quantity = models.DecimalField(_("количество"), max_digits=20, decimal_places=0, default='',)
  from_tip = models.ForeignKey(
      ItemT,
      verbose_name=_("наконечник начала провода"),
      on_delete=models.CASCADE,
      blank=True,
      null=True,
      db_index=False,
      related_name='from_tip_in_cutlists',
  )
  start_strip = models.DecimalField(_("Зачистка начало, мм"), max_digits=20, decimal_places=0, blank=True, null=True)
  start_tinning = models.BooleanField(_('облудить начало'), blank=True, default=False,
    help_text = _('лужение начала провода'))
  from_seal = models.ForeignKey(
      ItemT,
      verbose_name=_("уплотнитель начала провода"),
      on_delete=models.CASCADE,
      db_index=False,
      blank=True,
      null=True,
      related_name='from_seal_in_cutlists',
  )
  length = models.DecimalField(_("длина"), max_digits=20, decimal_places=0)
  to_seal = models.ForeignKey(
      ItemT,
      verbose_name=_('уплотнитель конец провода'),
      on_delete=models.CASCADE,
      db_index=False,
      blank=True,
      null=True,
      related_name='to_seal_in_cutlists',
  )
  end_tinning = models.BooleanField(_('облудить конец'), blank=True, default=False, help_text = _('лужение конец провода'))
  end_strip = models.DecimalField(_('Зачистка конец, мм'), max_digits=20, decimal_places=0, blank=True, null=True)
  to_tip = models.ForeignKey(
      ItemT,
      verbose_name=_("наконечник конца провода"),
      on_delete=models.CASCADE,
      db_index=False,
      blank=True,
      null=True,
      related_name='to_tip_in_cutlists',
  )
  allowance = models.DecimalField(_("припуск"), max_digits=5, decimal_places=0, default='0', blank=True, null=True)
  soldering = models.BooleanField(_('пайка проводов'), blank=False, default=False,
    help_text = _('пайка проводов'))

  class Meta(AuditModel.Meta):
    db_table = 'connection_list'                 # Name of the database table
    verbose_name = _('Таблица соединений')          # A translatable name for the entity
    verbose_name_plural = _('Таблицы соединений')  # Plural name
    ordering = ['SP_pos']

class SolderingScheme(AuditModel):
  # Database fields
  id = models.AutoField(_("identifier"), primary_key=True)
  image = models.ImageField(upload_to='img/', height_field='image_height', width_field='image_width', null=True, blank=True, default='img/no_scheme.png')
  image_height = models.IntegerField(blank=True, null=True)
  image_width = models.IntegerField(blank=True, null=True)
  item = models.ForeignKey(
      ItemT,
      verbose_name=_("Номенклатура"),
      on_delete=models.CASCADE,
      db_index=False,
      related_name='item_soldering_scheme',
  )
  class Meta(AuditModel.Meta):
    db_table = 'solderingscheme'                 # Name of the database table
    verbose_name = _('Схема пайки')          # A translatable name for the entity
    verbose_name_plural = _('Схемы пайки')  # Plural name
    ordering = ['item']

class ProductLabel(AuditModel):
  name = models.CharField(_("name"), max_length=300)
  item = models.ForeignKey(ItemT, on_delete=models.CASCADE, related_name='labels', null=False, blank=False)
  barcode = models.CharField(max_length=50, null=True, blank=True)
  label_template = models.CharField(max_length=100, choices=(
      ('standard', 'Стандартная'),
      ('pro', 'Расширенная')
  ))
  def __str__(self):
      return f"Этикетка {self.name} - {self.item.name}"
  class Meta(AuditModel.Meta):
    db_table = 'label'                 # Name of the database table
    verbose_name = _('Этикетка')          # A translatable name for the entity
    verbose_name_plural = _('Этикетки')  # Plural name
    ordering = ['item']

class MobileHanger(AuditModel):
  #id = models.AutoField(_("identifier"), primary_key=True)
  number = models.CharField(_("Номер"), blank=False, null=False)
  current_item = models.ForeignKey(ItemT, on_delete=models.CASCADE, related_name='tied_hangers', null=True, blank=True)
  def __str__(self):
      return f"Вешало №{self.number} - {self.current_item.name}"
  class Meta(AuditModel.Meta):
    db_table = 'hangers'                 # Name of the database table
    verbose_name = _('Мобильное вешало') # A translatable name for the entity
    verbose_name_plural = _('Мобильные вешала')  # Plural name
    ordering = ['number']

class TraceScheme(AuditModel):
  item = models.ForeignKey(ItemT, on_delete=models.CASCADE, related_name='trace_schemes', null=True, blank=True)
  wire_no = models.CharField(_('имя провода'), null=False, blank=False, max_length=20, help_text= _('Имя жилы или провода'))
  image = models.ImageField(upload_to='img/', height_field='image_height', width_field='image_width', null=True, blank=True, default='img/no_image.png')
  image_height = models.IntegerField(blank=True, null=True)
  image_width = models.IntegerField(blank=True, null=True)
  class Meta(AuditModel.Meta):
    db_table = 'trace_list'                 # Name of the database table
    verbose_name = _('Схема трассировки')          # A translatable name for the entity
    verbose_name_plural = _('Схемы трассировки')  # Plural name
    ordering = ['item']