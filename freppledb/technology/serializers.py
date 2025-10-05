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

class ConnectionListFilter(FilterSet):
    class Meta:
        model = models.ConnectionList
        fields = dict(
            {   "id": ["exact", "in", "gt", "gte", "lt", "lte"],
                "hanged_no": ["exact", "in", "contains"],
                "SP_pos": ["exact", "in", "contains"],
                "item": ["exact", "in"],
                "wire_no": ["exact", "in", "contains"],
                "quantity": ["exact", "in", "gt", "gte", "lt", "lte"],
                "from_tip": ["exact", "in"],
                "start_strip": ["exact", "in", "gt", "gte", "lt", "lte"],
                "start_tinning": ["exact"],
                "from_seal": ["exact", "in"],
                "length": ["exact", "in", "gt", "gte", "lt", "lte"],
                "to_seal": ["exact", "in"],
                "end_tinning": ["exact"],
                "end_strip": ["exact", "in", "gt", "gte", "lt", "lte"],
                "to_tip": ["exact", "in"],
                "allowance": ["exact", "in", "gt", "gte", "lt", "lte"],
                "soldering": ["exact"],
                "source": ["exact", "in"],
                "lastmodified": ["exact", "in", "gt", "gte", "lt", "lte"],
            },
            **getAttributeAPIFilterDefinition(models.ConnectionList),
        )
        filter_fields = fields.keys()

class ConnectionListSerializer(BulkSerializerMixin, ModelSerializer):
    class Meta:
        model = models.ConnectionList
        fields = (
            "id",
            "hanged_no",
            "SP_pos",
            "operation",
            "item",
            "wire_no",
            "quantity",
            "from_tip",
            "start_strip",
            "start_tinning",
            "from_seal",
            "length",
            "to_seal",
            "end_tinning",
            "end_strip",
            "to_tip",
            "allowance",
            "soldering",
            "source",
            "lastmodified",
        ) + getAttributeAPIFields(models.ConnectionList)
        read_only_fields = (
            "lastmodified",
        ) + getAttributeAPIReadOnlyFields(models.ConnectionList)
        list_serializer_class = BulkListSerializer
        update_lookup_field = "id"
        partial = True

class ConnectionListAPI(frePPleListCreateAPIView):
    def get_queryset(self):
        return models.ConnectionList.objects.using(self.request.database).all()
    serializer_class = ConnectionListSerializer
    filter_class = ConnectionListFilter

class ConnectionListdetailAPI(frePPleRetrieveUpdateDestroyAPIView):
    def get_queryset(self):
        return models.ConnectionList.objects.using(self.request.database).all()
    serializer_class = ConnectionListSerializer

class CutListFilter(FilterSet):
    class Meta:
        model = models.ConnectionList
        fields = dict(
            {   "id": ["exact", "in", "gt", "gte", "lt", "lte"],
                "hanged_no": ["exact", "in", "contains"],
                "SP_pos": ["exact", "in", "contains"],
                "item": ["exact", "in"],
                "wire_no": ["exact", "in", "contains"],
                "quantity": ["exact", "in", "gt", "gte", "lt", "lte"],
                "from_tip": ["exact", "in"],
                "start_strip": ["exact", "in", "gt", "gte", "lt", "lte"],
                "start_tinning": ["exact"],
                "from_seal": ["exact", "in"],
                "length": ["exact", "in", "gt", "gte", "lt", "lte"],
                "to_seal": ["exact", "in"],
                "end_tinning": ["exact"],
                "end_strip": ["exact", "in", "gt", "gte", "lt", "lte"],
                "to_tip": ["exact", "in"],
                "allowance": ["exact", "in", "gt", "gte", "lt", "lte"],
                "soldering": ["exact"],
                "source": ["exact", "in"],
                "lastmodified": ["exact", "in", "gt", "gte", "lt", "lte"],
            },
            **getAttributeAPIFilterDefinition(models.ConnectionList),
        )
        filter_fields = fields.keys()

class CutListSerializer(BulkSerializerMixin, ModelSerializer):
    class Meta:
        model = models.ConnectionList
        fields = (
            "id",
            "hanged_no",
            "SP_pos",
            "operation",
            "item",
            "wire_no",
            "quantity",
            "from_tip",
            "start_strip",
            "start_tinning",
            "from_seal",
            "length",
            "to_seal",
            "end_tinning",
            "end_strip",
            "to_tip",
            "allowance",
            "soldering",
            "source",
            "lastmodified",
        ) + getAttributeAPIFields(models.ConnectionList)
        read_only_fields = (
            "lastmodified",
        ) + getAttributeAPIReadOnlyFields(models.ConnectionList)
        list_serializer_class = BulkListSerializer
        update_lookup_field = "id"
        partial = True

class CutListAPI(frePPleListCreateAPIView):
    def get_queryset(self):
        return models.ConnectionList.objects.using(self.request.database).all()
    def filter_queryset(self, queryset):
        filtered = super().filter_queryset(queryset)
        return filtered
    serializer_class = CutListSerializer
    filter_class = CutListFilter

class CutListdetailAPI(frePPleRetrieveUpdateDestroyAPIView):
    def get_queryset(self):
        return models.ConnectionList.objects.using(self.request.database).all()
    serializer_class = CutListSerializer

class ItemTFilter(FilterSet):
    class Meta:
        model = models.ItemT
        fields = dict(
            {
                "name": ["exact", "in", "contains"],
                "owner": ["exact", "in"],
                "description": ["exact", "in", "contains"],
                "category": ["exact", "in", "contains"],
                "subcategory": ["exact", "in", "contains"],
                "cost": ["exact", "in", "gt", "gte", "lt", "lte"],
                "volume": ["exact", "in", "gt", "gte", "lt", "lte"],
                "weight": ["exact", "in", "gt", "gte", "lt", "lte"],
                "uom": ["exact", "in", "contains"],
                "periodofcover": ["exact", "in", "gt", "gte", "lt", "lte"],
                "type": ["exact", "in"],
                "source": ["exact", "in"],
                "lastmodified": ["exact", "in", "gt", "gte", "lt", "lte"],
            },
            **getAttributeAPIFilterDefinition(models.ItemT),
        )
        filter_fields = fields.keys()

class ItemTSerializer(BulkSerializerMixin, ModelSerializer):
    class Meta:
        model = models.ItemT
        fields = (
            "name",
            "owner",
            "qr",
            "description",
            "category",
            "subcategory",
            "cost",
            "volume",
            "short_name",
            "weight",
            "periodofcover",
            "uom",
            "type",
            "source",
            "lastmodified",
        ) + getAttributeAPIFields(models.ItemT)
        read_only_fields = (
            "lastmodified",
            "periodofcover",
            "image",
            "image_height",
            "image_width",
        ) + getAttributeAPIReadOnlyFields(models.ItemT)
        list_serializer_class = BulkListSerializer
        update_lookup_field = "name"
        partial = True

class ItemTAPI(frePPleListCreateAPIView):
    def get_queryset(self):
        return models.ItemT.objects.using(self.request.database).all()

    serializer_class = ItemTSerializer
    filter_class = ItemTFilter

class ItemTdetailAPI(frePPleRetrieveUpdateDestroyAPIView):
    def get_queryset(self):
        return models.ItemT.objects.using(self.request.database).all()
    serializer_class = ItemTSerializer

class SolderingListFilter(FilterSet):
    class Meta:
        model = models.ConnectionList
        fields = dict(
            {   "id": ["exact", "in", "gt", "gte", "lt", "lte"],
                "hanged_no": ["exact", "in", "contains"],
                "SP_pos": ["exact", "in", "contains"],
                "item": ["exact", "in"],
                "wire_no": ["exact", "in", "contains"],
                "quantity": ["exact", "in", "gt", "gte", "lt", "lte"],
                "start_strip": ["exact", "in", "gt", "gte", "lt", "lte"],
                "start_tinning": ["exact"],
                "length": ["exact", "in", "gt", "gte", "lt", "lte"],
                "end_tinning": ["exact"],
                "end_strip": ["exact", "in", "gt", "gte", "lt", "lte"],
                "allowance": ["exact", "in", "gt", "gte", "lt", "lte"],
                "soldering": ["exact"],
                "source": ["exact", "in"],
                "lastmodified": ["exact", "in", "gt", "gte", "lt", "lte"],
            },
            **getAttributeAPIFilterDefinition(models.ConnectionList),
        )
        filter_fields = fields.keys()

class SolderingListSerializer(BulkSerializerMixin, ModelSerializer):
    class Meta:
        model = models.ConnectionList
        fields = (
            "id",
            "hanged_no",
            "SP_pos",
            "operation",
            "item",
            "wire_no",
            "quantity",
            "start_strip",
            "start_tinning",
            "length",
            "end_tinning",
            "end_strip",
            "allowance",
            "soldering",
            "source",
            "lastmodified",
        ) + getAttributeAPIFields(models.ConnectionList)
        read_only_fields = (
            "lastmodified",
        ) + getAttributeAPIReadOnlyFields(models.ConnectionList)
        list_serializer_class = BulkListSerializer
        update_lookup_field = "id"
        partial = True

class SolderingListAPI(frePPleListCreateAPIView):
    def get_queryset(self):
        return models.ConnectionList.objects.using(self.request.database).all()
    serializer_class = SolderingListSerializer
    filter_class = SolderingListFilter

class SolderingListdetailAPI(frePPleRetrieveUpdateDestroyAPIView):
    def get_queryset(self):
        return models.ConnectionList.objects.using(self.request.database).all()
    serializer_class = SolderingListSerializer

class SolderingSchemeFilter(FilterSet):
    class Meta:
        model = models.SolderingScheme
        fields = dict(
            {   "id": ["exact", "in", "gt", "gte", "lt", "lte"],
                "item": ["exact", "in"],
                "source": ["exact", "in"],
                "lastmodified": ["exact", "in", "gt", "gte", "lt", "lte"],
            },
            **getAttributeAPIFilterDefinition(models.SolderingScheme),
        )
        filter_fields = fields.keys()

class SolderingSchemeSerializer(BulkSerializerMixin, ModelSerializer):
    class Meta:
        model = models.SolderingScheme
        fields = (
            "id",
            "item",
            "image",
        ) + getAttributeAPIFields(models.SolderingScheme)
        read_only_fields = (
            "source",
            "lastmodified",
        ) + getAttributeAPIReadOnlyFields(models.SolderingScheme)
        list_serializer_class = BulkListSerializer
        update_lookup_field = "id"
        partial = True

class SolderingSchemeAPI(frePPleListCreateAPIView):
    def get_queryset(self):
        return models.SolderingScheme.objects.using(self.request.database).all()
    serializer_class = SolderingSchemeSerializer
    filter_class = SolderingSchemeFilter

class SolderingSchemedetailAPI(frePPleRetrieveUpdateDestroyAPIView):
    def get_queryset(self):
        return models.SolderingScheme.objects.using(self.request.database).all()
    serializer_class = SolderingSchemeSerializer

class ProductLabelFilter(FilterSet):
    class Meta:
        model = models.ProductLabel
        fields = dict(
            {   "id": ["exact", "in"],
                "name": ["exact", "in"],
                "item": ["exact", "in"],
                "label_template": ["exact", "in"],
                "lastmodified": ["exact", "in", "gt", "gte", "lt", "lte"],
            },
            **getAttributeAPIFilterDefinition(models.ProductLabel),
        )
        filter_fields = fields.keys()

class ProductLabelSerializer(BulkSerializerMixin, ModelSerializer):
    class Meta:
        model = models.ProductLabel
        fields = (
            "id",
            "name",
            "item",
            "label_template",
        ) + getAttributeAPIFields(models.ProductLabel)
        read_only_fields = (
            "source",
            "lastmodified",
        ) + getAttributeAPIReadOnlyFields(models.ProductLabel)
        list_serializer_class = BulkListSerializer
        update_lookup_field = "name"
        partial = True

class ProductLabelAPI(frePPleListCreateAPIView):
    def get_queryset(self):
        return models.ProductLabel.objects.using(self.request.database).all()
    serializer_class = ProductLabelSerializer
    filter_class = ProductLabelFilter

class ProductLabeldetailAPI(frePPleRetrieveUpdateDestroyAPIView):
    def get_queryset(self):
        return models.ProductLabel.objects.using(self.request.database).all()
    serializer_class = ProductLabelSerializer

class MobileHangerFilter(FilterSet):
    class Meta:
        model = models.MobileHanger
        fields = dict(
            {   "number": ["exact", "in", "gt", "gte", "lt", "lte"],
                "current_item": ["exact", "in"],
                "source": ["exact", "in"],
                "lastmodified": ["exact", "in", "gt", "gte", "lt", "lte"],
            },
            **getAttributeAPIFilterDefinition(models.MobileHanger),
        )
        filter_fields = fields.keys()

class MobileHangerSerializer(BulkSerializerMixin, ModelSerializer):
    class Meta:
        model = models.MobileHanger
        fields = (
            "number",
            "current_item",
            "source",
            "lastmodified",#
        ) + getAttributeAPIFields(models.MobileHanger)
        read_only_fields = (
            "lastmodified",
        ) + getAttributeAPIReadOnlyFields(models.MobileHanger)
        list_serializer_class = BulkListSerializer
        update_lookup_field = "number"
        partial = True

class MobileHangerAPI(frePPleListCreateAPIView):
    def get_queryset(self):
        return models.MobileHanger.objects.using(self.request.database).all()
    serializer_class = MobileHangerSerializer
    filter_class = MobileHangerFilter

class MobileHangerdetailAPI(frePPleRetrieveUpdateDestroyAPIView):
    def get_queryset(self):
        return models.MobileHanger.objects.using(self.request.database).all()
    serializer_class = MobileHangerSerializer

class TraceSchemeFilter(FilterSet):
    class Meta:
        model = models.TraceScheme
        fields = dict(
            {   "id": ["exact", "in"],
                "item": ["exact", "in"],
                "wire_no": ["exact", "in"],
                "image_height": ["exact", "in"],
                "image_width": ["exact", "in"],
                "source": ["exact", "in"],
                "lastmodified": ["exact", "in", "gt", "gte", "lt", "lte"],
            },
            **getAttributeAPIFilterDefinition(models.TraceScheme),
        )
        filter_fields = fields.keys()

class TraceSchemeSerializer(BulkSerializerMixin, ModelSerializer):
    class Meta:
        model = models.TraceScheme
        fields = (
            "id",
            "item",
            "wire_no",
            "image",
            "image_height",
            "image_width",
            "source",
            "lastmodified",#
        ) + getAttributeAPIFields(models.TraceScheme)
        read_only_fields = (
            "lastmodified",
        ) + getAttributeAPIReadOnlyFields(models.TraceScheme)
        list_serializer_class = BulkListSerializer
        update_lookup_field = "id"
        partial = True

class TraceSchemeAPI(frePPleListCreateAPIView):
    def get_queryset(self):
        return models.TraceScheme.objects.using(self.request.database).all()
    serializer_class = TraceSchemeSerializer
    filter_class = TraceSchemeFilter

class TraceSchemedetailAPI(frePPleRetrieveUpdateDestroyAPIView):
    def get_queryset(self):
        return models.TraceScheme.objects.using(self.request.database).all()
    serializer_class = TraceSchemeSerializer
