from django.utils.translation import gettext_lazy as _
from django.contrib import admin
from freppledb.common.adminforms import MultiDBModelAdmin
from freppledb.admin import data_site
from freppledb.boot import getAttributes
from freppledb.testbench.models import BenchConnectors

@admin.register(BenchConnectors, site=data_site)
class BenchConnectors_admin(MultiDBModelAdmin):
    model = BenchConnectors
    save_on_top = True  # Добавляет кнопки сохранения вверху
    save_as = True      # Добавляет кнопку "Сохранить как"
    raw_id_fields = ("connector",) # Показывать поле как текстовое, а не как выпадающий список
    search_fields = ("connector_designation", "connector_name") # По каким полям может поиск на странице просмотра списка
    exclude = ("source",)
    search_fields = ("connector_name", )
    fieldsets = (
        (None, {"fields": ("connector_name", "connector_designation", "connector", "connector_pins_no", )}),
        (
            _("advanced"),
            {
                "fields": []
                + [a[0] for a in getAttributes(BenchConnectors) if a[3]],
                "classes": ("collapse",),
            },
        ),
    )
    tabs = [
        {
            "name": "edit",
            "label": _("edit"),
            "view": "admin:testbench_benchconnectors_change",
            "permissions": "testbench.change_benchconnectors",
        },
        {
            "name": "messages",
            "label": _("messages"),
            "view": "admin:testbench_benchconnectors_comment",
        },
    ]
