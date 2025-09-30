# This is the menu instance used for all frePPLe screens
from freppledb.menu import menu

from freppledb.codescan.views import *
from freppledb.codescan.models import *

# User maintenance
menu.addItem("admin", "code scan", separator=True, index=3000)
menu.addItem(
    "admin",
    "scan events",
    url="/data/codescan/eventlist/",
    report=CodeScanEventList,
    index=3100,
    model=CodeScanEvent,
    admin=False,
)
menu.addItem(
    "admin",
    "user codes",
    url="/data/codescan/usercodes/",
    report=UserCodesList,
    index=3200,
    model=UserCodes,
    #permission="auth.change_group",
    admin=False,
)
menu.addItem(
    "admin",
    "codes types",
    url="/data/codescan/codestypes/",
    report=CodesTypesList,
    index=3300,
    model=CodesTypes,
    #permission="auth.change_group",
    admin=False,
)
menu.addItem(
    "admin",
    "workstations",
    url="/data/codescan/workstation/",
    report=WorkstationsList,
    index=3400,
    model=Workstation,
    #permission="auth.change_workstations",
    admin=False,
)
