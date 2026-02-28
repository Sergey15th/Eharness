from django.urls import re_path
from .views import *
from freppledb import mode

app_name = 'qm'
# Automatically add these URLs when the application is installed
autodiscover = True

if mode == "WSGI":
    from . import views
    from freppledb.technology.views import *
    from freppledb.qm.views import *
    from . import serializers

    urlpatterns = [
        # Партии изделий
        re_path(r"^data/qm/batch/$", views.BatchList.as_view(), name="qm_batch_changelist", ),
        # Паспорт продукта
        re_path(r"^data/qm/productpassport/$", views.ProductPassportList.as_view(), name="qm_productpassport_changelist", ),
        # Виды контроля качества
        re_path(r"^data/qm/qualitycontroltypes/$", views.QualityControlTypesList.as_view(), name="qm_qualitycontroltypes_changelist", ),
        # Контроль качества
        re_path(r"^data/qm/qualitycontrol/$", views.QualityControlList.as_view(), name="qm_qualitycontrol_changelist", ),
        # Готовые этикетки ProductPassport
        re_path(r"^data/qm/productpassportlabel/$", ProductLabelPreviewView.as_view(), name='preview_product_label'),
        # Печать этикетки ProductPassport
        re_path(r"^data/qm/productpassportlabelprint/$", ProductLabelPrintView.as_view(), name='print_product_label'),
        #path('labels/bulk-print/', views.BulkPrintLabelsView.as_view(), name='bulk_print_labels'),

        # REST API framework
        # Партии изделий
        re_path(r"^api/qm/batch/$", serializers.BatchListAPI.as_view()),
        # Паспорт продукта
        re_path(r"^api/qm/productpassport/$", serializers.ProductPassportListAPI.as_view()),
        # Виды контроля качества
        re_path(r"^api/qm/qualitycontroltypes/$", serializers.QualityControlTypesListAPI.as_view()),
        # Контроль качества
        re_path(r"^api/qm/qualitycontrol/$", serializers.QualityControlListAPI.as_view()),
   ]