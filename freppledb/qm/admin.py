
from django.utils.translation import gettext_lazy as _
from django.contrib import admin
from freppledb.common.adminforms import MultiDBModelAdmin
from freppledb.admin import data_site
from freppledb.boot import getAttributes
from freppledb.qm.models import Label, Batch, ProductPassport, QualityControl, QualityControlTypes

@admin.register(Label, site=data_site)
class Label_admin(MultiDBModelAdmin):
    model = Label
    save_on_top = True
    search_fields = ("name", )
    fieldsets = (
        (None, {"fields": ("name", "template", )}),
        (
            _("advanced"),
            {
                "fields": []
                + [a[0] for a in getAttributes(Label) if a[3]],
                "classes": ("collapse",),
            },
        ),
    )
    tabs = [
        {
            "name": "edit",
            "label": _("edit"),
            "view": "admin:qm_label_change",
            "permissions": "qm.change_label",
        },
        {
            "name": "messages",
            "label": _("messages"),
            "view": "admin:qm_label_comment",
        },
    ]

@admin.register(Batch, site=data_site)
class Batch_admin(MultiDBModelAdmin):
    model = Batch
    save_on_top = True
    search_fields = ("manufacturing_order__batch", )
    raw_id_fields = ("manufacturing_order",) # Показывать поле как текстовое, а не как выпадающий список
    fieldsets = (
        (None, {"fields": ("manufacturing_order", "serie_no_start")}),
    )
    tabs = [
        {
            "name": "edit",
            "label": _("edit"),
            "view": "admin:qm_batch_change",
            "permissions": "qm.change_batch",
        },
        {
            "name": "messages",
            "label": _("messages"),
            "view": "admin:qm_batch_comment",
        },
    ]

@admin.register(ProductPassport, site=data_site)
class ProductPassport_admin(MultiDBModelAdmin):
    model = ProductPassport
    save_on_top = True
    search_fields = ("serial_number", "date", )
    raw_id_fields = ("manufacturing_order",) # Показывать поле как текстовое, а не как выпадающий список
    fieldsets = (
        (None, {"fields": ("manufacturing_order", "status", "part_name", )}),
    )
    tabs = [
        {
            "name": "edit",
            "label": _("edit"),
            "view": "admin:qm_productpassport_change",
            "permissions": "qm.change_productpassport",
        },
        {
            "name": "messages",
            "label": _("messages"),
            "view": "admin:qm_productpassport_comment",
        },
    ]

@admin.register(QualityControl, site=data_site)
class QualityControl_admin(MultiDBModelAdmin):
    model = QualityControl
    save_on_top = True
    search_fields = ("date", )
    raw_id_fields = ("product_passport",) # Показывать поле как текстовое, а не как выпадающий список
    fieldsets = (
        (None, {"fields": ("product_passport", "type", "control_result", "control_result_log", )}),
    )
    tabs = [
        {
            "name": "edit",
            "label": _("edit"),
            "view": "admin:qm_qualitycontrol_change",
            "permissions": "qm.change_qualitycontrol",
        },
        {
            "name": "messages",
            "label": _("messages"),
            "view": "admin:qm_qualitycontrol_comment",
        },
    ]

@admin.register(QualityControlTypes, site=data_site)
class QualityControlTypes_admin(MultiDBModelAdmin):
    model = QualityControlTypes
    save_on_top = True
    search_fields = ("type", )
    raw_id_fields = ("item",) # Показывать поле как текстовое, а не как выпадающий список
    fieldsets = (
        (None, {"fields": ("item", "type", )}),
    )
    tabs = [
        {
            "name": "edit",
            "label": _("edit"),
            "view": "admin:qm_qualitycontroltypes_change",
            "permissions": "qm.change_qualitycontroltypes",
        },
        {
            "name": "messages",
            "label": _("messages"),
            "view": "admin:qm_qualitycontroltypes_comment",
        },
    ]