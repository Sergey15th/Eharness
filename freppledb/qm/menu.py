
# Use the function "_" for all strings that need translation.
from django.utils.translation import gettext as _

# This is the menu instance used for all frePPLe screens
from freppledb.menu import menu

import freppledb.technology.views
from freppledb.qm.models import (
   Label, Batch, ProductPassport, QualityControl, QualityControlTypes
)
from freppledb.qm.views.labellist import LabelList
from freppledb.qm.views.batchlist import BatchList
from freppledb.qm.views.productpassportlist import ProductPassportList
from freppledb.qm.views.qualitycontrollist import QualityControlList
import freppledb.technology.views.solderingscheme

# Add a new group and a new item
menu.addGroup("quality", label=_("Качество"), index=20)
menu.addItem(
    "quality",
    "batchlist",
    url="/data/qm/batch/",
    report=freppledb.qm.views.batchlist.BatchList,
    index=11,
    model=Batch,
)
menu.addItem(
    "quality",
    "labellist",
    url="/data/qm/label/",
    report=freppledb.qm.views.labellist.LabelList,
    index=12,
    model=Label,
)
menu.addItem(
    "quality",
    "productpassportlist",
    url="/data/qm/productpassport/",
    report=freppledb.qm.views.productpassportlist.ProductPassportList,
    index=13,
    model=ProductPassport,
)
menu.addItem(
    "quality",
    "qualitycontrollist",
    url="/data/qm/qualitycontrol/",
    report=freppledb.qm.views.qualitycontrollist.QualityControlList,
    index=14,
    model=QualityControl,
)
menu.addItem(
    "quality",
    "qualitycontroltypeslist",
    url="/data/qm/qualitycontroltypes/",
    report=freppledb.qm.views.qualitycontroltypeslist.QualityControlTypesList,
    index=15,
    model=QualityControlTypes,
)