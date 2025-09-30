from rest_framework.serializers import SerializerMethodField, PrimaryKeyRelatedField
from rest_framework_bulk.drf3.serializers import BulkListSerializer, BulkSerializerMixin
from .models import *
from freppledb.common.api.views import (
    frePPleListCreateAPIView,
    frePPleRetrieveUpdateDestroyAPIView,
)
from freppledb.common.api.serializers import (
    ModelSerializer,
    getAttributeAPIFilterDefinition,
    getAttributeAPIFields,
    getAttributeAPIReadOnlyFields,
)
from freppledb.common.api.filters import FilterSet

import logging

logger = logging.getLogger(__name__)

class CodeScanEventFilter(FilterSet):
    class Meta:
        model = CodeScanEvent
        fields = dict(
            {
                "session_id": ["exact", "in", "contains"],
                "scan_data": ["exact", "in", "contains"],
            },
            **getAttributeAPIFilterDefinition(CodeScanEvent),
        )
        filter_fields = fields.keys()

class UserCodesFilter(FilterSet):
    class Meta:
        model = UserCodes
        fields = dict(
            {
                "user": ["exact", ],
                "code": ["exact", ],
            },
            **getAttributeAPIFilterDefinition(UserCodes),
        )
        filter_fields = fields.keys()

class CodesTypesFilter(FilterSet):
    class Meta:
        model = CodesTypes
        fields = dict(
            {
                "type": ["exact", ],
                "pattern": ["exact", ],
            },
            **getAttributeAPIFilterDefinition(CodesTypes),
        )
        filter_fields = fields.keys()

class CodeScanEventSerializer(BulkSerializerMixin, ModelSerializer):
   class Meta:
        model = CodeScanEvent
        fields = (
            "session_id",
            "scan_data",
        ) + getAttributeAPIFields(CodeScanEvent)
        read_only_fields = (
            "lastmodified",
        ) + getAttributeAPIReadOnlyFields(CodeScanEvent)
        list_serializer_class = BulkListSerializer
        update_lookup_field = "session_id"
        partial = False

class CodeScanEventAPI(frePPleListCreateAPIView):
    def get_queryset(self):
        return CodeScanEvent.objects.using(self.request.database).all()
    serializer_class = CodeScanEventSerializer
    filter_class = CodeScanEventFilter

class CodeScanEventdetailAPI(frePPleRetrieveUpdateDestroyAPIView):
    def get_queryset(self):
        return CodeScanEvent.objects.using(self.request.database).all()
    serializer_class = CodeScanEventSerializer

class UserCodesSerializer(BulkSerializerMixin, ModelSerializer):
   class Meta:
        model = UserCodes
        fields = (
            "user",
            "code",
        ) + getAttributeAPIFields(UserCodes)
        read_only_fields = (
            "lastmodified",
            "source"
        ) + getAttributeAPIReadOnlyFields(UserCodes)
        list_serializer_class = BulkListSerializer
        update_lookup_field = "user"
        partial = False

class UserCodesAPI(frePPleListCreateAPIView):
    def get_queryset(self):
        return UserCodes.objects.using(self.request.database).all()
    serializer_class = UserCodesSerializer
    filter_class = UserCodesFilter

class UserCodesdetailAPI(frePPleRetrieveUpdateDestroyAPIView):
    def get_queryset(self):
        return UserCodes.objects.using(self.request.database).all()
    serializer_class = UserCodesSerializer

class CodesTypesSerializer(BulkSerializerMixin, ModelSerializer):
   class Meta:
        model = CodesTypes
        fields = (
            "id",
            "type",
            "pattern",
        ) + getAttributeAPIFields(CodesTypes)
        read_only_fields = (
            "lastmodified",
            "source"
        ) + getAttributeAPIReadOnlyFields(CodesTypes)
        list_serializer_class = BulkListSerializer
        update_lookup_field = "pattern"
        partial = False

class CodesTypesAPI(frePPleListCreateAPIView):
    def get_queryset(self):
        return CodesTypes.objects.using(self.request.database).all()
    serializer_class = CodesTypesSerializer
    filter_class = CodesTypesFilter

class CodesTypesdetailAPI(frePPleRetrieveUpdateDestroyAPIView):
    def get_queryset(self):
        return CodesTypes.objects.using(self.request.database).all()
    serializer_class = CodesTypesSerializer

class WorkstationSerializer(BulkSerializerMixin, ModelSerializer):
   class Meta:
        model = Workstation
        fields = (
            "name",
            "image",
            "description",
            "qr",
        ) + getAttributeAPIFields(Workstation)
        read_only_fields = (
            "lastmodified",
            "source"
        ) + getAttributeAPIReadOnlyFields(Workstation)
        list_serializer_class = BulkListSerializer
        update_lookup_field = "name"
        partial = False

class WorkstationAPI(frePPleListCreateAPIView):
    def get_queryset(self):
        return Workstation.objects.using(self.request.database).all()
    serializer_class = CodesTypesSerializer
    filter_class = CodesTypesFilter

class WorkstationdetailAPI(frePPleRetrieveUpdateDestroyAPIView):
    def get_queryset(self):
        return Workstation.objects.using(self.request.database).all()
    serializer_class = WorkstationSerializer
