from django.urls import re_path
from .views import *

app_name = 'barcode_scan'
# Automatically add these URLs when the application is installed
autodiscover = True

urlpatterns = [
    re_path(r"^api/barcode-scanned/$", CodeScanned, name='code-scanned'),
    re_path(
        r"^data/codescan/eventlist/$",
        CodeScanEventList.as_view(),
        name="codescan_eventlist",
    ),
    re_path(
        r"^data/codescan/usercodes/$",
        UserCodesList.as_view(),
        name="codescan_usercodeslist",
    ),
    re_path(
        r"^data/codescan/codestypes/$",
        CodesTypesList.as_view(),
        name="codescan_codestypeslist",
    ),
    re_path(
        r"^data/codescan/workstation/$",
        WorkstationsList.as_view(),
        name="codescan_workstationslist",
    ),
]