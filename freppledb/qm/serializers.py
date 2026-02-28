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
        model = models.Batch
        fields = dict(
            {   "id": ["exact", "in", "gt", "gte", "lt", "lte"],
                "manufacturing_order": ["exact", "in"],
                "serie_no_start": ["exact", "in", "gt", "gte", "lt", "lte"],
                "source": ["exact", "in"],
                "lastmodified": ["exact", "in", "gt", "gte", "lt", "lte"],
            },
            **getAttributeAPIFilterDefinition(models.Batch),
        )
        filter_fields = fields.keys()

class BatchListSerializer(BulkSerializerMixin, ModelSerializer):
    class Meta:
        model = models.Batch
        fields = (
            "id",
            "manufacturing_order",
            "serie_no_start",
            "source",
            "lastmodified",
        ) + getAttributeAPIFields(models.Batch)
        read_only_fields = (
            "lastmodified",
        ) + getAttributeAPIReadOnlyFields(models.Batch)
        list_serializer_class = BulkListSerializer
        update_lookup_field = "id"
        partial = True

class BatchListAPI(frePPleListCreateAPIView):
    def get_queryset(self):
        return models.Batch.objects.using(self.request.database).all()
    serializer_class = BatchListSerializer
    filter_class = BatchListFilter

class BatchListdetailAPI(frePPleRetrieveUpdateDestroyAPIView):
    def get_queryset(self):
        return models.Batch.objects.using(self.request.database).all()
    serializer_class = BatchListSerializer

class ProductPassportListFilter(FilterSet):
    class Meta:
        model = models.ProductPassport
        fields = dict(
            {   "id": ["exact", "in", "gt", "gte", "lt", "lte"],
                "manufacturing_order": ["exact", "in"],
                "serial_number": ["exact", "in", "gt", "gte", "lt", "lte"],
                "date": ["exact", "in", "gt", "gte", "lt", "lte"],
                "status": ["exact", "in"],
                "part_name": ["exact", "in"],
                "source": ["exact", "in"],
                "lastmodified": ["exact", "in", "gt", "gte", "lt", "lte"],
            },
            **getAttributeAPIFilterDefinition(models.ProductPassport),
        )
        filter_fields = fields.keys()

class ProductPassportListSerializer(BulkSerializerMixin, ModelSerializer):
    class Meta:
        model = models.ProductPassport
        fields = (
            "id",
            "date",
            "serial_number",
            "manufacturing_order",
            "product_qrcode",
            "ststus",
            "part_name",
            "firmware",
            "specification",
            "sertificate",
            "sertificate_validto",
            "last_maintenance",
            "last_maintenance_date",
            "user_manual",
            "service_manual",
            "url",
            "source",
            "lastmodified",
        ) + getAttributeAPIFields(models.ProductPassport)
        read_only_fields = (
            "source",
            "lastmodified",
        ) + getAttributeAPIReadOnlyFields(models.ProductPassport)
        list_serializer_class = BulkListSerializer
        update_lookup_field = "id"
        partial = True

class ProductPassportListAPI(frePPleListCreateAPIView):
    def get_queryset(self):
        return models.ProductPassport.objects.using(self.request.database).all()
    serializer_class = ProductPassportListSerializer
    filter_class = ProductPassportListFilter

class ProductPassportListdetailAPI(frePPleRetrieveUpdateDestroyAPIView):
    def get_queryset(self):
        return models.ProductPassport.objects.using(self.request.database).all()
    serializer_class = ProductPassportListSerializer

class QualityControlListFilter(FilterSet):
    class Meta:
        model = models.QualityControl
        fields = dict(
            {   "id": ["exact", "in", "gt", "gte", "lt", "lte"],
                "date": ["exact", "in", "gt", "gte", "lt", "lte"],
                "type": ["exact", "in"],
                "product_passport": ["exact", "in"],
                "control_result": ["exact", "in"],
                "source": ["exact", "in"],
                "lastmodified": ["exact", "in", "gt", "gte", "lt", "lte"],
            },
            **getAttributeAPIFilterDefinition(models.QualityControl),
        )
        filter_fields = fields.keys()

class QualityControlListSerializer(BulkSerializerMixin, ModelSerializer):
    class Meta:
        model = models.QualityControl
        fields = (
            "id",
            "date",
            "type",
            "product_passport",
            "control_result",
            "control_result_log",
            "source",
            "lastmodified",
        ) + getAttributeAPIFields(models.QualityControl)
        read_only_fields = (
            "source",
            "lastmodified",
        ) + getAttributeAPIReadOnlyFields(models.QualityControl)
        list_serializer_class = BulkListSerializer
        update_lookup_field = "id"
        partial = True

class QualityControlListAPI(frePPleListCreateAPIView):
    def get_queryset(self):
        return models.QualityControl.objects.using(self.request.database).all()
    serializer_class = QualityControlListSerializer
    filter_class = QualityControlListFilter

class QualityControlListdetailAPI(frePPleRetrieveUpdateDestroyAPIView):
    def get_queryset(self):
        return models.QualityControl.objects.using(self.request.database).all()
    serializer_class = QualityControlListSerializer

class QualityControlTypesListFilter(FilterSet):
    class Meta:
        model = models.QualityControlTypes
        fields = dict(
            {   "id": ["exact", "in", "gt", "gte", "lt", "lte"],
                "item": ["exact", "in"],
                "type": ["exact", "in"],
                "source": ["exact", "in"],
                "lastmodified": ["exact", "in", "gt", "gte", "lt", "lte"],
            },
            **getAttributeAPIFilterDefinition(models.QualityControlTypes),
        )
        filter_fields = fields.keys()

class QualityControlTypesListSerializer(BulkSerializerMixin, ModelSerializer):
    class Meta:
        model = models.QualityControlTypes
        fields = (
            "id",
            "item",
            "type",
            "source",
            "lastmodified",
        ) + getAttributeAPIFields(models.QualityControlTypes)
        read_only_fields = (
            "source",
            "lastmodified",
        ) + getAttributeAPIReadOnlyFields(models.QualityControlTypes)
        list_serializer_class = BulkListSerializer
        update_lookup_field = "id"
        partial = True

class QualityControlTypesListAPI(frePPleListCreateAPIView):
    def get_queryset(self):
        return models.QualityControlTypes.objects.using(self.request.database).all()
    serializer_class = QualityControlTypesListSerializer
    filter_class = QualityControlTypesListFilter

class QualityControlTypesListdetailAPI(frePPleRetrieveUpdateDestroyAPIView):
    def get_queryset(self):
        return models.QualityControlTypes.objects.using(self.request.database).all()
    serializer_class = QualityControlTypesListSerializer
