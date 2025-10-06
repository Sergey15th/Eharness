from django.db import models
from freppledb.input.models.operationplan import ManufacturingOrder
from freppledb.common.models import AuditModel
from django.utils.translation import gettext_lazy as _


class BatchList(AuditModel):
  # Database fields
  id = models.AutoField(_("identifier"), primary_key=True)
  manufacturing_order = models.ForeignKey(
      ManufacturingOrder,
      verbose_name=_("Заказ в производство"),
      on_delete=models.CASCADE,
      unique=True,
      db_index=False,
      related_name='order_batch',
  )
  serie_no_start = models.DecimalField(_("Начальный s/n"), max_digits=20, decimal_places=0, default='',)
  class Meta(AuditModel.Meta):
    db_table = 'batch_list'                 # Name of the database table
    verbose_name = _('Серия номенклатуры')          # A translatable name for the entity
    verbose_name_plural = _('Серии номенклатуры')  # Plural name
    ordering = ['id', 'serie_no_start']