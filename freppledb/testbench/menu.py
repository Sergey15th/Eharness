
# Use the function "_" for all strings that need translation.
from django.utils.translation import gettext as _

# This is the menu instance used for all frePPLe screens
from freppledb.menu import menu

import freppledb.testbench.views
from freppledb.testbench.models import (
   BenchConnectors, BenchChannels
)
import freppledb.testbench.views.benchconnectorslist

# Add a new group and a new item
menu.addGroup("testbench", label=_("Испытательный стенд"), index=30)

menu.addItem(
    "testbench",
    "benchconnectorslist",
    url="/data/testbench/benchconnectors/",
    report=freppledb.testbench.views.benchconnectorslist.BenchConnectorsList,
    index=31,
    model=BenchConnectors,
)
menu.addItem(
    "testbench",
    "benchchannelslist",
    url="/data/testbench/benchchannels/",
    report=freppledb.testbench.views.benchchannelslist.BenchChannelsList,
    index=32,
    model=BenchChannels,
)
menu.addItem(
    "testbench",
    "ARM",
    url="/data/testbench/landing/",
    report=freppledb.testbench.views.RM_mainscreen.RM_Dashboard,
    index=33,
    #model=BenchChannels,
)
