
# Use the function "_" for all strings that need translation.
from django.utils.translation import gettext as _

# This is the menu instance used for all frePPLe screens
from freppledb.menu import menu

import freppledb.technology.views
from freppledb.labels.models import (
   LabelTemplate, CreatedLabel
)
from freppledb.labels.views.labeltemplatelist import LabelTemplateList
from freppledb.labels.views.createdlabellist import CreatedLabelList

# Add a new group and a new item
menu.addGroup("labels", label=_("Этикетки"), index=25)
menu.addItem(
    "labels",
    "labellist",
    url="/data/labels/labeltemplate/",
    report=LabelTemplateList,
    index=11,
    model=LabelTemplate,
)

menu.addItem(
    "labels",
    "createdlabellist",
    url="/data/labels/createdlabel/",
    report=CreatedLabelList,
    index=12,
    model=CreatedLabel,
)
