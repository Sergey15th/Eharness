
from django.utils.translation import gettext_lazy as _
from django.contrib import admin

from freppledb.common.adminforms import MultiDBModelAdmin

from freppledb.admin import data_site
from freppledb.boot import getAttributes
from freppledb.technology.models import ConnectionList, ItemT, SolderingScheme, ProductLabel, MobileHanger, TraceScheme
from freppledb.input.admin import Item_admin

@admin.register(ConnectionList, site=data_site)
class ConnectionList_admin(MultiDBModelAdmin):
    model = ConnectionList
    save_on_top = True  # Добавляет кнопки сохранения вверху
    save_as = True      # Добавляет кнопку "Сохранить как"
    raw_id_fields = ("operation", "item", "from_tip", "from_seal", "to_seal", "to_tip") # Показывать поле как текстовое, а не как выпадающий список
    search_fields = ("hanged_no", "description") # По каким полям может поиск на странице просмотра списка
    exclude = ("source",)
    fieldsets = (
        (None, {"fields": ("hanged_no", "operation", "SP_pos", "item", "wire_no", "quantity", "from_tip", "start_strip", "start_tinning", "from_seal", "length", "to_seal", "end_tinning", "end_strip", "to_tip", )}),
        (
            _("advanced"), # Поля, которые показываются в detail view при нажатии плюсика
            {
                "fields": ["allowance", "soldering", ]
                + [a[0] for a in getAttributes(ConnectionList) if a[3]],
                "classes": ("collapse",),
            },
        ),
    )
    tabs = [
        {
            "name": "edit",
            "label": _("edit"),
            "view": "admin:technology_connectionlist_change",
            "permissions": "technology.change_connectionlist",
        },
        {
            "name": "messages",
            "label": _("messages"),
            "view": "admin:technology_connectionlist_comment",
        },
    ]    
    
@admin.register(ItemT, site=data_site)
class ItemT_admin(MultiDBModelAdmin):
    model = ItemT
    save_on_top = True
    raw_id_fields = ("owner",)
    search_fields = ("name", "description")

    fieldsets = (
        (None, {"fields": ("name", "description", "qr", "barcode_number", "cost", "owner", "uom")}),
        (
            _("advanced"),
            {
                "fields": ["category", "subcategory", "type", "volume", "weight", "image", "image_height", "image_width", "short_name",]
                + [a[0] for a in getAttributes(ItemT) if a[3]],
                "classes": ("collapse",),
            },
        ),
    )
    tabs = [
        {
            "name": "edit",
            "label": _("edit"),
            "view": "admin:technology_itemt_change",
            "permissions": "technology.change_itemt",
        },
        {"name": "supplypath", "label": _("supply path"), "view": "supplypath_item"},
        {"name": "whereused", "label": _("where used"), "view": "whereused_item"},
        {
            "name": "inventory",
            "label": _("inventory"),
            "view": "output_buffer_plandetail_by_item",
        },
        {
            "name": "inventorydetail",
            "label": _("inventory detail"),
            "view": "input_operationplanmaterial_plandetail_by_item",
        },
        {
            "name": "messages",
            "label": _("messages"),
            "view": "admin:technology_itemt_comment",
        },
    ]

@admin.register(SolderingScheme, site=data_site)
class SolderingScheme_admin(MultiDBModelAdmin):
    model = SolderingScheme
    save_on_top = True
    search_fields = ("item", )
    raw_id_fields = ("item", )
    fieldsets = (
        (None, {"fields": ("item", "image", )}),
        (
            _("advanced"),
            {
                "fields": ["image_height", "image_width", ]
                + [a[0] for a in getAttributes(SolderingScheme) if a[3]],
                "classes": ("collapse",),
            },
        ),
    )
    tabs = [
        {
            "name": "edit",
            "label": _("edit"),
            "view": "admin:technology_solderingscheme_change",
            "permissions": "technology.change_solderingscheme",
        },
        {
            "name": "messages",
            "label": _("messages"),
            "view": "admin:technology_solderingscheme_comment",
        },
    ]

@admin.register(ProductLabel, site=data_site)
class ProductLabel_admin(MultiDBModelAdmin):
    model = ProductLabel
    save_on_top = True
    search_fields = ("name", "item")
    raw_id_fields = ("item", )
    fieldsets = (
        (None, {"fields": ("name", "item", "label_template", )}),
        (
            _("advanced"),
            {
                "fields": ["barcode", ]
                + [a[0] for a in getAttributes(ProductLabel) if a[3]],
                "classes": ("collapse",),
            },
        ),
    )
    tabs = [
        {
            "name": "edit",
            "label": _("edit"),
            "view": "admin:technology_productlabel_change",
            "permissions": "technology.change_productlabel",
        },
        {
            "name": "messages",
            "label": _("messages"),
            "view": "admin:technology_productlabel_comment",
        },
    ]

@admin.register(MobileHanger, site=data_site)
class MobileHanger_admin(MultiDBModelAdmin):
    model = MobileHanger
    save_on_top = True
    save_as = True
    search_fields = ("number",)
    raw_id_fields = ("current_item", )
    fieldsets = (
        (None, {"fields": ("id", "number", "current_item", )}),
    )
    tabs = [
        {
            "name": "edit",
            "label": _("edit"),
            "view": "admin:technology_mobilehanger_change",
            "permissions": "technology.change_mobilehanger",
        },
        {
            "name": "messages",
            "label": _("messages"),
            "view": "admin:technology_mobilehanger_comment",
        },
    ]

@admin.register(TraceScheme, site=data_site)
class TraceScheme_admin(MultiDBModelAdmin):
    model = TraceScheme
    save_on_top = True
    save_as = True
    search_fields = ("item", "wire_no")
    raw_id_fields = ("item", )
    fieldsets = (
        (None, {"fields": ("item", "wire_no", "image", "image_height", "image_width",)}),
    )
    tabs = [
        {
            "name": "edit",
            "label": _("edit"),
            "view": "admin:technology_tracescheme_change",
            "permissions": "technology.change_tracescheme",
        },
        {
            "name": "messages",
            "label": _("messages"),
            "view": "admin:technology_tracescheme_comment",
        },
    ]
