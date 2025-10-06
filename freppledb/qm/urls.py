from django.urls import re_path
from .views import *
from freppledb import mode

app_name = 'qm'
# Automatically add these URLs when the application is installed
autodiscover = True

if mode == "WSGI":
    from . import views
    from freppledb.technology.views import *
    from . import serializers

    urlpatterns = [
        # Партии изделий
        re_path(r"^data/qm/batchlist/$", views.BatchListList.as_view(), name="qm_batchlist_changelist", ),

        # REST API framework
        re_path(r"^api/qm/batchlist/$", serializers.BatchListAPI.as_view()),

   ]