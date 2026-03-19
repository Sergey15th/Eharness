
from django.utils.translation import gettext_lazy as _
from django.contrib import admin
from freppledb.common.adminforms import MultiDBModelAdmin
from freppledb.admin import data_site
from freppledb.boot import getAttributes
from freppledb.labels.models import LabelTemplate, CreatedLabel

@admin.register(LabelTemplate, site=data_site)
class LabelTemplate_admin(MultiDBModelAdmin):
    model = LabelTemplate
    save_on_top = True
    search_fields = ("name", )
    fieldsets = (
        (None, {"fields": ("name", "template", "dir")}),
        (
            _("advanced"),
            {
                "fields": []
                + [a[0] for a in getAttributes(LabelTemplate) if a[3]],
                "classes": ("collapse",),
            },
        ),
    )
    tabs = [
        {
            "name": "edit",
            "label": _("edit"),
            "view": "admin:labels_labeltemplate_change",
            "permissions": "labels.change_labeltemplate",
        },
        {
            "name": "messages",
            "label": _("messages"),
            "view": "admin:labels_labeltemplate_comment",
        },
    ]

@admin.register(CreatedLabel, site=data_site)
class CreatedLabel_admin(MultiDBModelAdmin):
    model = CreatedLabel
    save_on_top = False
    search_fields = ("name", )
    fieldsets = (
        (None, {"fields": ("name", "file", "dir", "template")}),
        (
            _("advanced"),
            {
                "fields": []
                + [a[0] for a in getAttributes(CreatedLabel) if a[3]],
                "classes": ("collapse",),
            },
        ),
    )
    tabs = [
        {
            "name": "edit",
            "label": _("edit"),
            "view": "admin:labels_createdlabel_change",
            "permissions": "labels.change_createdlabel",
        },
        {
            "name": "messages",
            "label": _("messages"),
            "view": "admin:labels_createdlabel_comment",
        },
    ]