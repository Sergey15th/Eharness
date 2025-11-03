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

class BenchConnectorsListFilter(FilterSet):
    class Meta:
        model = models.BenchConnectors
        fields = dict(
            {   "id": ["exact", "in", "gt", "gte", "lt", "lte"],
                "connector_name": ["exact", "in", "contains"],
                "connector_designation": ["exact", "in", "contains"],
                "connector": ["exact", "in"],
                "connector_pins_no": ["exact", "in", "gt", "gte", "lt", "lte"],
                "source": ["exact", "in"],
                "lastmodified": ["exact", "in", "gt", "gte", "lt", "lte"],
            },
            **getAttributeAPIFilterDefinition(models.BenchConnectors),
        )
        filter_fields = fields.keys()

class BenchConnectorsListSerializer(BulkSerializerMixin, ModelSerializer):
    class Meta:
        model = models.BenchConnectors
        fields = (
            "id",
            "connector_name",
            "connector_designation",
            "connector",
            "connector_pins_no",
            "source",
            "lastmodified",
        ) + getAttributeAPIFields(models.BenchConnectors)
        read_only_fields = (
            "lastmodified",
        ) + getAttributeAPIReadOnlyFields(models.BenchConnectors)
        list_serializer_class = BulkListSerializer
        update_lookup_field = "id"
        partial = True

class BenchConnectorsListAPI(frePPleListCreateAPIView):
    def get_queryset(self):
        return models.BenchConnectors.objects.using(self.request.database).all()
    serializer_class = BenchConnectorsListSerializer
    filter_class = BenchConnectorsListFilter

class BenchConnectorsListdetailAPI(frePPleRetrieveUpdateDestroyAPIView):
    def get_queryset(self):
        return models.BenchConnectors.objects.using(self.request.database).all()
    serializer_class = BenchConnectorsListSerializer
