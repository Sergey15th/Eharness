from django.db import models
from freppledb.input.models.operationplan import ManufacturingOrder
from freppledb.codescan.models import QR
from freppledb.common.models import AuditModel
from freppledb.labels.models import CreatedLabel
from django.utils.translation import gettext_lazy as _     
import re
from django.core.exceptions import ValidationError
#from freppledb.technology.models import ItemT

class ControlType(models.TextChoices):
   CONTINUITY = _('прозвонка')
   VISUAL = _('визуальный контроль')
   CLIMATE = _('климатические испытания')

class Batch(AuditModel): # Партия номенклатуры
  # Database fields
  id = models.AutoField(_("identifier"), primary_key=True)
  manufacturing_order = models.OneToOneField(
      ManufacturingOrder,
      verbose_name=_("Заказ в производство"),
      on_delete=models.PROTECT,
      unique=True,
      db_index=False,
      related_name='order_batch',
  )
  serie_no_start = models.DecimalField(_("Начальный s/n"), max_digits=20, decimal_places=0,)
  serials_created = models.BooleanField(_("s/n созданы"), blank=True, default = False, )
  def __str__(self):
     return 'партия-' + str(ManufacturingOrder.batch) + '(' + str(ManufacturingOrder.name) + ')'
  class Meta(AuditModel.Meta):
    db_table = 'qm_batch_list'                 # Name of the database table
    verbose_name = _('Серия номенклатуры')          # A translatable name for the entity
    verbose_name_plural = _('Серии номенклатуры')  # Plural name
    ordering = ['id', 'serie_no_start']

class SerialUsed(AuditModel):
    def _next_serial(self) -> int:
      pass
    #item = models.ForeignKey(ItemT, on_delete=models.CASCADE, related_name='last_serial', null=True, blank=True)
    last_serial = models.IntegerField(blank=False, null=False)
    class Meta:
        verbose_name = "Last used serial"
        verbose_name_plural = "Last used serialss"
        db_table = "qm_last_serials"

# класс product_passport, в котором создаются экземпляры продуктов с серийными номерами по партиям
class ProductPassport(AuditModel):
  id = models.AutoField(_("identifier"), primary_key=True)
  date = models.DateTimeField(auto_now=False)
  @property
  def date_formatted(self):
      """Возвращает отформатированную дату создания"""
      if self.date:
          return self.date.strftime('%d.%m.%Y %H:%M')
      return None
  serial_number = models.IntegerField(_('s/n'), null=False, blank=True)
  @property
  def serial_number_str(self):
      return f"{self.serial_number:05d}"
  @property
  def name(self):
      """Возвращает отформатированное наименоване"""
      return f'{self.id}-{self.manufacturing_order.batch}-{self.serial_number_str}'

  manufacturing_order = models.ForeignKey(
      ManufacturingOrder,
      verbose_name=_("Заказ в производство"),
      on_delete=models.PROTECT,
      unique=False,
      db_index=False,
      related_name='order_passports',
  )
  label = models.ForeignKey( CreatedLabel, verbose_name=_("Этикетка"), on_delete=models.PROTECT, unique=False, db_index=False, null=True, related_name='label_passports', default=None)
  label_path = models.CharField(max_length=300, null=True, blank=True)
  product_qrcode = models.OneToOneField(QR, verbose_name=_("QR код продукта"), on_delete=models.PROTECT, unique=True, db_index=False, related_name='product_passports', )
  status = models.CharField(max_length=50, null=True, blank=True, default='Создан')
  part_name = models.CharField(max_length=200, null=True, blank=True)
  firmware = models.CharField(max_length=200, null=True, blank=True)
  specification = models.CharField(max_length=200, null=True, blank=True)
  sertificate = models.CharField(max_length=200, null=True, blank=True)
  sertificate_validto = models.DateTimeField(null=True, blank=True)
  last_maintenance = models.CharField(max_length=200, null=True, blank=True)
  last_maintenance_date = models.DateTimeField(null=True, blank=True)
  user_manual = models.URLField(null=True, blank=True)
  service_manual = models.URLField(null=True, blank=True)
  url = models.URLField(null=True, blank=True)
  def __str__(self):
    # Fixed: was using self.name twice, changed to show barcode if available
    return f"Паспорт изделия {self.manufacturing_order.item} от {self.date} - {self.product_qrcode.qr}"
  class Meta(AuditModel.Meta):
    db_table = 'qm_pasports'                 # Name of the database table
    verbose_name = _('Паспорт изделия')          # A translatable name for the entity
    verbose_name_plural = _('Паспорта изделий')  # Plural name
    unique_together = [['manufacturing_order', 'serial_number']]

# класс quality_control_types, в котором создаются требования к видам контроля качества номенклатуры
class QualityControlTypes(AuditModel):
  id = models.AutoField(_("identifier"), primary_key=True)
  item = models.ForeignKey("technology.ItemT", verbose_name=_("Объект контроля"), on_delete=models.PROTECT, null=False, blank=False, db_index=False, related_name='qm_control_types', )
  type = models.CharField(max_length=200, null=False, blank=False, choices=ControlType.choices, default=ControlType.CONTINUITY)
  def __str__(self):
    # Fixed: was using self.name twice, changed to show barcode if available
    return f"Контроль качества {self.item.name} - {self.type}"
  class Meta(AuditModel.Meta):
    db_table = 'qm_quality_control_types'                 # Name of the database table
    verbose_name = _('Требование контроля качества')          # A translatable name for the entity
    verbose_name_plural = _('Требования контроля качества')  # Plural name
    unique_together = [['item', 'type']]

# класс quality_control, в котором создаются экземпляры контроля качества
class QualityControl(AuditModel):
  id = models.AutoField(_("identifier"), primary_key=True)
  date = models.DateTimeField(auto_now=True)
  product_passport = models.ForeignKey(ProductPassport, verbose_name=_("Паспорт продукта"), on_delete=models.PROTECT, null=False, blank=False, db_index=False, related_name='quality_control_results', )
  type = models.ForeignKey(QualityControlTypes, verbose_name=_("Вид контроля"), on_delete=models.PROTECT, null=False, blank=False, db_index=False, related_name='type_quality_controls', )
  control_result = models.CharField(max_length=50, null=True, blank=True)
  control_result_log = models.JSONField(default=dict, null=True, blank=True, help_text="Отчёт по результатам контроля")
  def __str__(self):
    # Fixed: was using self.name twice, changed to show barcode if available
    if self.control_result is None:
       return f"Результат контроля качества {self.product_passport.manufacturing_order.item} от {self.date} - #"
    else:
       return f"Результат контроля качества {self.product_passport.manufacturing_order.item} от {self.date} - {self.control_result}"
  class Meta(AuditModel.Meta):
    db_table = 'qm_quality_control'                 # Name of the database table
    verbose_name = _('Контроль качества')          # A translatable name for the entity
    verbose_name_plural = _('Контроль качества')  # Plural name

