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
        # Разъёмы испытательного стенда
        re_path(r"^data/testbench/benchconnectors/$", views.BenchConnectorsList.as_view(), name="testbench_benchconnectors_changelist", ),
        re_path(r"^data/testbench/benchchannels/$", views.BenchChannelsList.as_view(), name="testbench_benchchannels_changelist", ),
        
        re_path(r"^data/testbench/landing/$", views.RM_Dashboard.as_view(), name='testbench_landing'),
        # REST API framework
        re_path(r"^api/testbench/benchconnectors/$", serializers.BenchConnectorsListAPI.as_view()),
        re_path(r"^api/testbench/benchconnectors/(?P<pk>[^/]+)/led/$", serializers.BenchConnectorsLEDControlAPI.as_view()),
        re_path(r"^api/testbench/benchchannels/$", serializers.BenchChannelsListAPI.as_view()),
        re_path(r"^api/testbench/metrics/", serializers.SystemMetricsAPI.as_view(), name='system_metrics'),
   ]
