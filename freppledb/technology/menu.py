
# Use the function "_" for all strings that need translation.
from django.utils.translation import gettext as _

# This is the menu instance used for all frePPLe screens
from freppledb.menu import menu

import freppledb.technology.views
from freppledb.technology.models import (
   ConnectionList, SolderingScheme, ProductLabel, MobileHanger, TraceScheme
)
import freppledb.technology.views.cutlist
import freppledb.technology.views.solderingscheme

# Add a new group and a new item
menu.addGroup("technology", label=_("Технология"), index=10)
menu.addItem("technology", "google", url="http://google.com", label=_('link to my company'), index=1)

menu.addItem(
    "technology",
    "connectionlist",
    url="/data/technology/connectionlist/",
    report=freppledb.technology.views.cutlist.ConnectionListList,
    index=11,
    model=ConnectionList,
)
menu.addItem(
    "technology",
    "cutlist",
    url="/data/technology/cutlist/",
    report=freppledb.technology.views.cutlist.CutListList,
    index=12,
    model=ConnectionList,
)
menu.addItem(
    "technology",
    "crimplist",
    url="/data/technology/crimplist/",
    report=freppledb.technology.views.cutlist.CrimpListList,
    index=13,
    model=ConnectionList,
)
menu.addItem(
    "technology",
    "solderinglist",
    url="/data/technology/solderinglist/",
    report=freppledb.technology.views.cutlist.SolderingList,
    index=14,
    model=ConnectionList,
)
menu.addItem(
    "technology",
    "solderingscheme",
    url="/data/technology/solderingscheme/",
    report=freppledb.technology.views.solderingscheme.SolderingSchemeList,
    index=15,
    model=SolderingScheme,
)
menu.addItem(
    "technology",
    "productlabel",
    url="/data/technology/productlabel/",
    report=freppledb.technology.views.label.ProductLabelList,
    index=16,
    model=ProductLabel,
)
menu.addItem(
    "technology",
    "tracescheme",
    url="/data/technology/tracescheme/",
    report=freppledb.technology.views.tracescheme.TraceSchemeList,
    index=17,
    model=TraceScheme,
)
menu.addItem(
    "admin",
    "hangers",
    url="/data/technology/mobilehanger/",
    report=freppledb.technology.views.hangers.MobileHangerList,
    index=3500,
    model=MobileHanger,
    #permission="auth.change_workstations",
    admin=False,
)
