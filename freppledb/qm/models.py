from django.db import models
from freppledb.input.models.operationplan import ManufacturingOrder
from freppledb.common.models import AuditModel
from django.utils.translation import gettext_lazy as _


class BatchList(AuditModel): # Партия номенклатуры
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
  serie_no_start = models.DecimalField(_("Начальный s/n"), max_digits=20, decimal_places=0,)
  class Meta(AuditModel.Meta):
    db_table = 'batch_list'                 # Name of the database table
    verbose_name = _('Серия номенклатуры')          # A translatable name for the entity
    verbose_name_plural = _('Серии номенклатуры')  # Plural name
    ordering = ['id', 'serie_no_start']

class SerialUsed(AuditModel):
    def _next_serial(self) -> int:
      pass
    #item = models.ForeignKey(ItemT, on_delete=models.CASCADE, related_name='last_serial', null=True, blank=True)
    last_serial = models.IntegerField(max_length=8, blank=False, null=False)
    class Meta:
        verbose_name = "Last used serial"
        verbose_name_plural = "Last used serialss"
        db_table = "last_serials"
