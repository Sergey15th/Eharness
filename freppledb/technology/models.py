from django.db import models
from django.conf import settings
from django.db import models, DEFAULT_DB_ALIAS, connections, transaction
from psycopg2.extras import execute_batch
import logging

# Use the function "_" for all strings that need translation.
from django.utils.translation import gettext_lazy as _

# A subclass of AuditModel will inherit an field "last_modified" and "source".
from freppledb.common.models import HierarchyModel, AuditModel, Parameter
from freppledb.input.models import Item, Operation
from freppledb.codescan.models import QR, barcode

logger = logging.getLogger(__name__)

class ItemT(Item):
  @classmethod
  def rebuildHierarchy(cls, database=DEFAULT_DB_ALIAS):
      # Verify whether we need to rebuild or not.
      # We search for the first record whose lft field is null.
      if len(cls.objects.using(database).filter(lft__isnull=True)[:1]) == 0:
          return

      nodes = {}
      children = {}
      updates = []

      def tagChildren(me, left, level):
          right = left + 1
          # Get all children of this node
          for i in children.get(me, []):
              # Recursive execution of this function for each child of this node
              right = tagChildren(i, right, level + 1)

          # After processing the children of this node now know its left and right values
          updates.append((left, right, level, me))

          # Remove from node list (to mark as processed)
          del nodes[me]

          # Return the right value of this node + 1
          return right + 1

      # Load all nodes in memory
      for i in cls.objects.using(database).values("name", "owner"):
          if i["name"] == i["owner"]:
              logging.error("Data error: '%s' points to itself as owner" % i["name"])
              nodes[i["name"]] = None
          else:
              nodes[i["name"]] = i["owner"]
              if i["owner"]:
                  if not i["owner"] in children:
                      children[i["owner"]] = set()
                  children[i["owner"]].add(i["name"])
      keys = sorted(nodes.items())

      # Loop over nodes without parent
      cnt = 1
      for i, j in keys:
          if j is None:
              cnt = tagChildren(i, cnt, 0)

      if nodes:
          # If the nodes dictionary isn't empty, it is an indication of an
          # invalid hierarchy.
          # There are loops in your hierarchy, ie parent-chains not ending
          # at a top-level node without parent.
          bad = nodes.copy()
          updated = True
          while updated:
              updated = False
              for i in list(bad.keys()):
                  ok = True
                  for j, k in bad.items():
                      if k == i:
                          ok = False
                          break
                  if ok:
                      # If none of the bad keys points to me as a parent, I am unguilty
                      del bad[i]
                      updated = True
          logging.error("Data error: Hierarchy loops among %s" % sorted(bad.keys()))
          for i, j in sorted(bad.items()):
              children[j].remove(i)
              nodes[i] = None

          # Continue loop over nodes without parent
          keys = sorted(nodes.items())
          for i, j in keys:
              if j is None:
                  cnt = tagChildren(i, cnt, 0)

      # Write all results to the database
      #if cls == ItemT:
      with transaction.atomic(using=database):
          cursor = connections[database].cursor()
          execute_batch(
              cursor,
              "update %s set lft=%%s, rght=%%s, lvl=%%s where name = %%s"
              % connections[database].ops.quote_name(Item._meta.db_table),
              updates,
          )
  image = models.ImageField(upload_to='img/', height_field='image_height', width_field='image_width', null=True, blank=True, default=None)
  image_height = models.IntegerField(blank=True, null=True)
  image_width = models.IntegerField(blank=True, null=True)
  imagef = models.ImageField(upload_to='img/', height_field='imagef_height', width_field='imagef_width', null=True, blank=True, default=None)
  imagef_height = models.IntegerField(blank=True, null=True)
  imagef_width = models.IntegerField(blank=True, null=True)
  short_name = models.CharField(_('арт.'), null=True, blank=True)
  erp_code = models.CharField(_('erp code'), null=True, blank=True)
  qr = models.ForeignKey(QR, verbose_name=_("QR код"), on_delete=models.PROTECT, blank=True, null=True, db_index=False, related_name='qr_owners', )
  barcode_number = models.CharField(_('Номер штрих-кода'), null=True, blank=True)
  barcode = models.ForeignKey(barcode, verbose_name=_("Штрих код"), on_delete=models.PROTECT, blank=True, null=True, db_index=False, related_name='barcode_owners', )
  passport_label_template = models.ForeignKey("labels.LabelTemplate", verbose_name=_("Шаблон этикетки паспорта"), on_delete=models.PROTECT, blank=True, null=True, db_index=False, related_name='label_passports', )
  opposite_item = models.ForeignKey("self", verbose_name=_("Ответная часть"), on_delete=models.PROTECT, blank=True, null=True, db_index=False, related_name='opposite_items', )

class ConnectionList(AuditModel):
  # Database fields
  id = models.AutoField(_("identifier"), primary_key=True)
  hanged_no = models.CharField(_('№ на вешале'), null=True, blank=True, max_length=20, help_text= _('Номер крючка на вешале'))
  qr = models.CharField('mQR', null=True, blank=True)
  SP_pos = models.DecimalField(_('Позиция в СП'), decimal_places=0, blank=True, null=True, max_digits=3, default='', help_text= _('№ позиции в спецификации или сборочном чертеже'))
  operation = models.ForeignKey(Operation, verbose_name=_("операция"), on_delete=models.PROTECT, db_index=False, related_name='operation_cutlists',)
  item = models.ForeignKey( ItemT, verbose_name=_("провод"), on_delete=models.PROTECT, db_index=False, related_name='item_cutlists', )
  wire_no = models.CharField(_('имя провода'), null=False, blank=False, max_length=20, help_text= _('Имя жилы или провода'))
  sygnal = models.CharField(_('имя цепи'), null=True, blank=True, max_length=20, help_text= _('Имя цепи'))
  quantity = models.DecimalField(_("количество"), max_digits=20, decimal_places=0, default='',)
  from_tip = models.ForeignKey(ItemT, verbose_name=_("наконечник начала провода"), on_delete=models.PROTECT, blank=True, null=True, db_index=False, related_name='from_tip_in_cutlists', )
  from_connector = models.CharField("от разъёма", null=True, blank=True, max_length=20, help_text=_('от разъёма'))
  from_pin = models.DecimalField(_('от контакта'), max_digits=3, decimal_places=0, blank=True, null=True, help_text=_('от контакта'))
  start_strip = models.DecimalField(_("Зачистка начало, мм"), max_digits=20, decimal_places=0, blank=True, null=True)
  start_tinning = models.BooleanField(_('облудить начало'), blank=True, default=False, help_text = _('лужение начала провода'))
  from_seal = models.ForeignKey( ItemT, verbose_name=_("уплотнитель начала провода"), on_delete=models.PROTECT, db_index=False, blank=True, null=True, related_name='from_seal_in_cutlists', )
  length = models.DecimalField(_("длина"), max_digits=20, decimal_places=0)
  to_seal = models.ForeignKey(ItemT, verbose_name=_('уплотнитель конец провода'), on_delete=models.PROTECT, db_index=False, blank=True, null=True, related_name='to_seal_in_cutlists')
  to_connector = models.CharField("к разъёму", null=True, blank=True, max_length=20, help_text=_('к разъёму'))
  to_pin = models.DecimalField(_('к контакту'), max_digits=3, decimal_places=0, blank=True, null=True, help_text=_('к контакту'))
  end_tinning = models.BooleanField(_('облудить конец'), blank=True, default=False, help_text = _('лужение конец провода'))
  end_strip = models.DecimalField(_('Зачистка конец, мм'), max_digits=20, decimal_places=0, blank=True, null=True)
  to_tip = models.ForeignKey(ItemT, verbose_name=_("наконечник конца провода"), on_delete=models.PROTECT, db_index=False, blank=True, null=True, related_name='to_tip_in_cutlists', )
  allowance = models.DecimalField(_("припуск"), max_digits=5, decimal_places=0, default='0', blank=True, null=True)
  soldering = models.BooleanField(_('пайка проводов'), blank=False, default=False, help_text = _('пайка проводов'))
  class Meta(AuditModel.Meta):
    db_table = 'technology_connection_list'                 # Name of the database table
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
      on_delete=models.PROTECT,
      db_index=False,
      related_name='item_soldering_scheme',
  )
  class Meta(AuditModel.Meta):
    db_table = 'technology_solderingscheme'                 # Name of the database table
    verbose_name = _('Схема пайки')          # A translatable name for the entity
    verbose_name_plural = _('Схемы пайки')  # Plural name
    ordering = ['item']

class MobileHanger(AuditModel):
  id = models.AutoField(_("identifier"), primary_key=True)
  number = models.CharField(_("Номер"), blank=False, null=False)
  current_item = models.ForeignKey(ItemT, on_delete=models.PROTECT, related_name='tied_hangers', null=True, blank=True)
  def __str__(self):
      return f"Вешало №{self.number} - {self.current_item.name}"
  qr = models.ForeignKey(QR, verbose_name=_("QR код"), on_delete=models.PROTECT, blank=True, null=True, db_index=False, related_name='qr_mh_owners', )
  label_path = models.CharField(max_length=300, null=True, blank=True) #Для ссылки в таблице на этикетку
  label_template = models.ForeignKey("labels.LabelTemplate", verbose_name=_("Шаблон этикетки мобильного вешала"), on_delete=models.PROTECT, blank=True, null=True, db_index=False, related_name='label_hangers', )
  label = models.ForeignKey("labels.CreatedLabel", verbose_name=_("Этикетка"), on_delete=models.PROTECT, unique=False, db_index=False, null=True, related_name='label_hangers', default=None)
  class Meta(AuditModel.Meta):
    db_table = 'technology_hangers'                 # Name of the database table
    verbose_name = _('Мобильное вешало') # A translatable name for the entity
    verbose_name_plural = _('Мобильные вешала')  # Plural name
    ordering = ['number']

class TraceScheme(AuditModel):
  item = models.ForeignKey(ItemT, on_delete=models.PROTECT, related_name='trace_schemes', null=True, blank=True)
  wire_no = models.CharField(_('имя провода'), null=False, blank=False, max_length=20, help_text= _('Имя жилы или провода'))
  image = models.ImageField(upload_to='img/', height_field='image_height', width_field='image_width', null=True, blank=True, default=None)
  image_height = models.IntegerField(blank=True, null=True)
  image_width = models.IntegerField(blank=True, null=True)
  class Meta(AuditModel.Meta):
    db_table = 'technology_trace_list'                 # Name of the database table
    verbose_name = _('Схема трассировки')          # A translatable name for the entity
    verbose_name_plural = _('Схемы трассировки')  # Plural name
    ordering = ['item']