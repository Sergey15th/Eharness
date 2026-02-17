from rest_framework.serializers import SerializerMethodField, PrimaryKeyRelatedField
from rest_framework_bulk.drf3.serializers import BulkListSerializer, BulkSerializerMixin
import psutil
from django.http import JsonResponse
from django.views import View
import json
import time

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
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from freppledb.mqtt import mqtt_tasks as testbench_tasks

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
            "light_led_mqtt_id",
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

class BenchChannelsListFilter(FilterSet):
    class Meta:
        model = models.BenchChannels
        fields = dict(
            {   "id": ["exact", "in",],
                "bench_connector": ["exact", "in", ],
                "bench_pin_no": ["exact", "in", ],
                "channel": ["exact", "in"],
                "source": ["exact", "in"],
                "lastmodified": ["exact", "in", "gt", "gte", "lt", "lte"],
            },
            **getAttributeAPIFilterDefinition(models.BenchChannels),
        )
        filter_fields = fields.keys()

class BenchChannelsListSerializer(BulkSerializerMixin, ModelSerializer):
    class Meta:
        model = models.BenchChannels
        fields = (
            "id",
            "bench_connector",
            "bench_pin_no",
            "channel",
            "source",
            "lastmodified",
        ) + getAttributeAPIFields(models.BenchChannels)
        read_only_fields = (
            "lastmodified",
        ) + getAttributeAPIReadOnlyFields(models.BenchChannels)
        list_serializer_class = BulkListSerializer
        update_lookup_field = "id"
        partial = True

class BenchChannelsListAPI(frePPleListCreateAPIView):
    def get_queryset(self):
        return models.BenchChannels.objects.using(self.request.database).all()
    serializer_class = BenchChannelsListSerializer
    filter_class = BenchChannelsListFilter

class BenchChannelsListdetailAPI(frePPleRetrieveUpdateDestroyAPIView):
    def get_queryset(self):
        return models.BenchChannels.objects.using(self.request.database).all()
    serializer_class = BenchChannelsListSerializer

class BenchConnectorsLEDControlAPI(APIView):
    """Simple endpoint to trigger LED control for a bench connector.
    POST /api/testbench/benchconnectors/<id>/led/  with JSON {"action":"on"}
    """
    def post(self, request, pk=None, format=None):
        # Determine led id mapping. By default try to read connector_designation field.
        try:
            conn = models.BenchConnectors.objects.using(request.database).get(id=pk)
        except Exception:
            return Response({"detail": "Connector not found"}, status=status.HTTP_404_NOT_FOUND)
        # Resolve LED id: prefer explicit MQTT id field, then designation, then DB id
        led_id = getattr(conn, "light_led_mqtt_id", None)
        action = request.data.get("action", "on")
        logger.info('enqueue Celery task LED_ON: led_id=%s, action=%s', led_id, action)
        # enqueue Celery task

        #TODO: Адрес темы MQTT должен быть настраиваемым, а не жёстко прописанным
        #TODO: Необходимо брать адрес из модели BenchConnectors.light_led_mqtt_id

        try:
            testbench_tasks.publish_mqtt_message.delay("bench-light-d48afca52a04/light/light_bar_section_" + led_id + "/command", '{"state": "TOGGLE"}')


            #TODO: Сделать ожидание результата выполнения задачи и вернуть реальный статус
            #TODO: Читать из MQTT состояние светодиода, а не возвращать заглушку
            
            response = {"status": "scheduled", "led_id": led_id}
            logger.info(response)
            time.sleep(3)

            return Response(response)
        except Exception as e:
            logger.info("detail"+ str(e))
            return Response({"detail": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def get_queryset(self):
        # Provide a queryset for permission checks (DjangoModelPermissions requires this)
        return models.BenchConnectors.objects.using(self.request.database).all()

    # Provide a safe class-level queryset so permission classes like
    # DjangoModelPermissions can be applied before request-specific
    # attributes (like request.database) exist. Use .none() to avoid
    # hitting the DB at import time.
    queryset = models.BenchConnectors.objects.none()

class SystemMetricsAPI(View):
    def get(self, request):
        metrics = {
            'cpu_percent': psutil.cpu_percent(interval=1),
            'memory_percent': psutil.virtual_memory().percent,
            'disk_percent': psutil.disk_usage('/').percent,
            'temperature': self.get_cpu_temperature(),
            'uptime': self.get_uptime(),
            'network_io': self.get_network_io(),
            'timestamp': timezone.now().isoformat(),
        }
        return JsonResponse(metrics)
    
    def get_cpu_temperature(self):
        try:
            import psutil
            temps = psutil.sensors_temperatures()
            if 'coretemp' in temps:
                return temps['coretemp'][0].current
        except:
            pass
        return None
    
    def get_uptime(self):
        import datetime
        uptime_seconds = psutil.boot_time()
        uptime = datetime.datetime.now() - datetime.datetime.fromtimestamp(uptime_seconds)
        return str(uptime)
    
    def get_network_io(self):
        io = psutil.net_io_counters()
        return {
            'bytes_sent': io.bytes_sent,
            'bytes_recv': io.bytes_recv,
        }