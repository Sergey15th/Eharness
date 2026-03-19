from django.urls import re_path
from .views import *
from freppledb import mode

app_name = 'labels'
# Automatically add these URLs when the application is installed
autodiscover = True

if mode == "WSGI":
    from . import views
    from freppledb.labels.views import *
    from . import serializers

    urlpatterns = [
        # Шаблоны этикеток
        re_path(r"^data/labels/labeltemplate/$", views.LabelTemplateList.as_view(), name="labels_labeltemplate_changelist", ),
        # Созданные этикетки
        re_path(r"^data/labels/createdlabel/$", views.CreatedLabelList.as_view(), name="labels_createdlabel_changelist", ),

        # REST API framework
        re_path(r"^api/labels/labeltemplate/$", serializers.LabelTemplateListAPI.as_view()),
        re_path(r"^api/labels/createdlabel/$", serializers.CreatedLabelListAPI.as_view()),
   ]