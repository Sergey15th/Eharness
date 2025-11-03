from django.urls import re_path
from django.urls import path
from django.views.generic.base import TemplateView

from freppledb import mode

# Automatically add these URLs when the application is installed
autodiscover = True

if mode == "WSGI":
    from . import views
    from freppledb.testbench.views import *
    from . import serializers

    urlpatterns = [
        # Таблица соединений
        re_path(r"^data/testbench/benchconnectors/$", views.BenchConnectorsList.as_view(), name="testbench_benchconnectors_changelist", ),

        # REST API framework
        re_path(r"^api/testbench/benchconnectors/$", serializers.BenchConnectorsListAPI.as_view()),
   ]
'''
'''