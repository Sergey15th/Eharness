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

class BatchListFilter(FilterSet):
    class Meta:
        model = models.BatchList
        fields = dict(
            {   "id": ["exact", "in", "gt", "gte", "lt", "lte"],
                "manufacturing_order": ["exact", "in"],
                "serie_no_start": ["exact", "in", "gt", "gte", "lt", "lte"],
                "source": ["exact", "in"],
                "lastmodified": ["exact", "in", "gt", "gte", "lt", "lte"],
            },
            **getAttributeAPIFilterDefinition(models.BatchList),
        )
        filter_fields = fields.keys()

class BatchListSerializer(BulkSerializerMixin, ModelSerializer):
    class Meta:
        model = models.BatchList
        fields = (
            "id",
            "manufacturing_order",
            "serie_no_start",
            "source",
            "lastmodified",
        ) + getAttributeAPIFields(models.BatchList)
        read_only_fields = (
            "lastmodified",
        ) + getAttributeAPIReadOnlyFields(models.BatchList)
        list_serializer_class = BulkListSerializer
        update_lookup_field = "id"
        partial = True

class BatchListAPI(frePPleListCreateAPIView):
    def get_queryset(self):
        return models.BatchList.objects.using(self.request.database).all()
    serializer_class = BatchListSerializer
    filter_class = BatchListFilter

class BatchListdetailAPI(frePPleRetrieveUpdateDestroyAPIView):
    def get_queryset(self):
        return models.BatchList.objects.using(self.request.database).all()
    serializer_class = BatchListSerializer

