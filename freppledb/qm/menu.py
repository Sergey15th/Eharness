
# Use the function "_" for all strings that need translation.
from django.utils.translation import gettext as _

# This is the menu instance used for all frePPLe screens
from freppledb.menu import menu

import freppledb.technology.views
from freppledb.technology.models import (
   ConnectionList, SolderingScheme, ProductLabel, MobileHanger, TraceScheme
)
from freppledb.qm.views.batchlist import BatchList
import freppledb.technology.views.solderingscheme

# Add a new group and a new item
menu.addGroup("quality", label=_("Качество"), index=20)
menu.addItem(
    "quality",
    "batchlist",
    url="/data/qm/batchlist/",
    report=freppledb.qm.views.batchlist.BatchListList,
    index=11,
    model=BatchList,
)