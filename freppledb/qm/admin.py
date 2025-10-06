
from django.utils.translation import gettext_lazy as _
from django.contrib import admin
from freppledb.common.adminforms import MultiDBModelAdmin
from freppledb.admin import data_site
from freppledb.boot import getAttributes
from freppledb.qm.models import BatchList

@admin.register(BatchList, site=data_site)
class BatcchList_admin(MultiDBModelAdmin):
    model = BatchList
    save_on_top = True  # Добавляет кнопки сохранения вверху
    save_as = True      # Добавляет кнопку "Сохранить как"
    #raw_id_fields = ("manufacturing_order", ) # Показывать поле как текстовое, а не как выпадающий список
    search_fields = ("serie_no_start", ) # По каким полям может поиск на странице просмотра списка
    exclude = ("source",)
    fieldsets = (
        (None, {"fields": ("serie_no_start",  "manufacturing_order")}),
        (
            _("advanced"), # Поля, которые показываются в detail view при нажатии плюсика
            {
                "fields": [ ]
                + [a[0] for a in getAttributes(BatchList) if a[3]],
                "classes": ("collapse",),
            },
        ),
    )
    tabs = [
        {
            "name": "edit",
            "label": _("edit"),
            "view": "admin:qm_batchlist_change",
            "permissions": "qm.change_batchlist",
        },
        {
            "name": "messages",
            "label": _("messages"),
            "view": "admin:qm_batchlist_comment",
        },
    ]    
    