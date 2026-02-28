
from django.utils.translation import gettext_lazy as _
from django.contrib import admin
from freppledb.common.adminforms import MultiDBModelAdmin
from freppledb.admin import data_site
from freppledb.boot import getAttributes
from freppledb.labels.models import LabelTemplate

@admin.register(LabelTemplate, site=data_site)
class LabelTemplate_admin(MultiDBModelAdmin):
    model = LabelTemplate
    save_on_top = True
    search_fields = ("name", )
    fieldsets = (
        (None, {"fields": ("name", "template", )}),
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