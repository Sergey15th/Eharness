from django.contrib import admin
from freppledb.codescan.models import *
from freppledb.common.adminforms import MultiDBModelAdmin
from django.utils.translation import gettext_lazy as _
from freppledb.admin import data_site
from freppledb.boot import getAttributes

@admin.register(CodesTypes, site=data_site)
class CodesTypesAdmin(MultiDBModelAdmin):
    model = CodesTypes
    save_on_top = True  # Добавляет кнопки сохранения вверху
    save_as = True      # Добавляет кнопку "Сохранить как"
    search_fields = ("type",)
    fieldsets = (
        (None, {"fields": ("pattern", "type", )}),
    )
    tabs = [ # При detail view справа сверху табсы
        {
            "name": "edit",
            "label": _("edit"),
            "view": "admin:codes_types_change",
            "permissions": "input.change_codes_types",
        },
        {
            "name": "messages",
            "label": _("messages"),
            "view": "admin:codes_types_comment",
        },
    ]

@admin.register(UserCodes, site=data_site)
class Codes_DBAdmin(MultiDBModelAdmin):
    # Поля, доступные для создания/редактирования
    model = UserCodes
    save_on_top = True  # Добавляет кнопки сохранения вверху
    save_as = True      # Добавляет кнопку "Сохранить как"
    raw_id_fields = ("user", )
    search_fields = ("user", "code")
    fieldsets = (
        (None, {"fields": ("user", "code", )}),
    )
    tabs = [ # При detail view справа сверху табсы
        {
            "name": "edit",
            "label": _("edit"),
            "view": "admin:user_codes_change",
            "permissions": "input.change_user_codes",
        },
        {
            "name": "messages",
            "label": _("messages"),
            "view": "admin:user_codes_comment",
        },
    ]

@admin.register(CodeScanEvent, site=data_site)
class CodeScanEventAdmin(MultiDBModelAdmin):
    # Поля, доступные для создания/редактирования
    model = CodeScanEvent
    save_on_top = True  # Добавляет кнопки сохранения вверху
    save_as = True      # Добавляет кнопку "Сохранить как"
    #raw_id_fields = ()
    search_fields = ("user", "code")
    fieldsets = (
        (None, {"fields": ("created_at", "session_id", "scan_data", )}),
    )
    tabs = [ # При detail view справа сверху табсы
        {
            "name": "edit",
            "label": _("edit"),
            "view": "admin:code_scan_event_change",
            "permissions": "input.change_code_scan_event",
        },
        {
            "name": "messages",
            "label": _("messages"),
            "view": "admin:code_scan_event_comment",
        },
    ]

@admin.register(Workstation, site=data_site)
class WorkstationAdmin(MultiDBModelAdmin):
    model = Workstation
    save_on_top = True  # Добавляет кнопки сохранения вверху
    save_as = True      # Добавляет кнопку "Сохранить как"
    search_fields = ("name",)
    fieldsets = (
        (None, {"fields": ("name", "short_name", "image", "description", "qr", )}),
    )
    tabs = [ # При detail view справа сверху табсы
        {
            "name": "edit",
            "label": _("edit"),
            "view": "admin:codescan_workstation_change",
            "permissions": "codescan.change_workstation",
        },
        {
            "name": "messages",
            "label": _("messages"),
            "view": "admin:codescan_workstation_comment",
        },
    ]

'''
class SessionAdmin(MultiDBModelAdmin, site=data_site):
    list_display = ['session_key', 'expire_date']
    search_fields = ['session_key']
'''