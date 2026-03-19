from rest_framework.serializers import SerializerMethodField, PrimaryKeyRelatedField
from rest_framework_bulk.drf3.serializers import BulkListSerializer, BulkSerializerMixin

from freppledb.common.api.views import (
    frePPleListCreateAPIView,
    frePPleRetrieveUpdateDestroyAPIView,
)
from . import models
from freppledb.common.api.serializers import (
    ModelSerializer,
    getAttributeAPIFilterDefinition,
    getAttributeAPIFields,
    getAttributeAPIReadOnlyFields,
)
from freppledb.common.api.filters import FilterSet

import logging

logger = logging.getLogger(__name__)

class LabelTemplateListFilter(FilterSet):
    class Meta:
        model = models.LabelTemplate
        fields = dict(
            {   "id": ["exact", "in"],
                "name": ["exact", "in"],
                #"template": ["in"],
                "lastmodified": ["exact", "in", "gt", "gte", "lt", "lte"],
            },
            **getAttributeAPIFilterDefinition(models.LabelTemplate),
        )
        filter_fields = fields.keys()

class LabelTemplateListSerializer(BulkSerializerMixin, ModelSerializer):
    class Meta:
        model = models.LabelTemplate
        fields = (
            "id",
            "name",
            "template",
        ) + getAttributeAPIFields(models.LabelTemplate)
        read_only_fields = (
            "source",
            "lastmodified",
        ) + getAttributeAPIReadOnlyFields(models.LabelTemplate)
        list_serializer_class = BulkListSerializer
        update_lookup_field = "name"
        partial = True

class LabelTemplateListAPI(frePPleListCreateAPIView):
    def get_queryset(self):
        return models.LabelTemplate.objects.using(self.request.database).all()
    serializer_class = LabelTemplateListSerializer
    filter_class = LabelTemplateListFilter

class LabelTemplateDetailAPI(frePPleRetrieveUpdateDestroyAPIView):
    def get_queryset(self):
        return models.LabelTemplate.objects.using(self.request.database).all()
    serializer_class = LabelTemplateListSerializer

class CreatedLabelListFilter(FilterSet):
    class Meta:
        model = models.CreatedLabel
        fields = dict(
            {   "id": ["exact", "in"],
                "name": ["exact", "in"],
                "dir": ["exact", "in"],
                "template": ["in"],
                "lastmodified": ["exact", "in", "gt", "gte", "lt", "lte"],
            },
            **getAttributeAPIFilterDefinition(models.CreatedLabel),
        )
        filter_fields = fields.keys()

class CreatedLabelListSerializer(BulkSerializerMixin, ModelSerializer):
    class Meta:
        model = models.CreatedLabel
        fields = (
            "id",
            "name",
            "dir",
            "file",
            "template",
        ) + getAttributeAPIFields(models.CreatedLabel)
        read_only_fields = (
            "source",
            "lastmodified",
        ) + getAttributeAPIReadOnlyFields(models.CreatedLabel)
        list_serializer_class = BulkListSerializer
        update_lookup_field = "name"
        partial = True

class CreatedLabelListAPI(frePPleListCreateAPIView):
    def get_queryset(self):
        return models.CreatedLabel.objects.using(self.request.database).all()
    serializer_class = CreatedLabelListSerializer
    filter_class = CreatedLabelListFilter

class CreatedLabelDetailAPI(frePPleRetrieveUpdateDestroyAPIView):
    def get_queryset(self):
        return models.CreatedLabel.objects.using(self.request.database).all()
    serializer_class = CreatedLabelListSerializer
