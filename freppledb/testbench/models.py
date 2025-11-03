from django.db import models
from freppledb.common.models import HierarchyModel, AuditModel
from freppledb.technology.models import ItemT
from django.utils.translation import gettext as _

# класс quality_control, в котором создаются экземпляры контроля качества
class BenchConnectors(AuditModel):
    def formfield_for_foreignkey(self, db_field, request, **kwargs): # Фильтруем выбор разъёмов, только из списка opposite_item
            if db_field.name == "connector":
                # Показываем только ItemT из списка opposite_item
                kwargs["queryset"] = ItemT.objects.filter(
                    opposite_item__isnull=False,
                ).distinct()
            return super().formfield_for_foreignkey(db_field, request, using=request.database, **kwargs)
    id = models.AutoField(_("identifier"), primary_key=True)
    connector_name = models.CharField(max_length=50, null=True, blank=True)
    connector_designation = models.CharField(max_length=10, null=False, blank=False, unique=True)
    connector = models.ForeignKey(ItemT, verbose_name=_("Разъём стенда"), on_delete=models.PROTECT, db_index=False, related_name='item_testbench_connectors', blank=False, null=False, )
    connector_pins_no = models.IntegerField(blank=False, null=False)
    class Meta(AuditModel.Meta):
        db_table = 'testbench_connectors'                 # Name of the database table
        verbose_name = _('Разъём стенда')          # A translatable name for the entity
        verbose_name_plural = _('Разъёмы стенда')  # Plural name
