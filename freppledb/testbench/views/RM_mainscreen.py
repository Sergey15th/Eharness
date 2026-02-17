from django.views.generic import TemplateView
from django.conf import settings
from django.utils import timezone
from datetime import datetime
import psutil
import platform

class RM_Dashboard(TemplateView):
    """Начальный экран испытательного стенда"""
    template_name = 'RM_mainscreen2.html'
    title = "RM Dashboard"
    @classmethod
    def has_permission(cls, user):
        return user.has_perm("testbench.view_arm")
    def get_system_info(self):
        """Собираем системную информацию"""
        return {
            'os': platform.system(),
            'os_version': platform.version(),
            'python_version': platform.python_version(),
            'hostname': platform.node(),
            'cpu_count': psutil.cpu_count(),
            'memory_total': f"{psutil.virtual_memory().total / (1024**3):.1f} GB",
            'boot_time': datetime.fromtimestamp(psutil.boot_time()).strftime('%Y-%m-%d %H:%M'),
        }
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        system_info = self.get_system_info()
        
        context.update({
            'title_st': 'Испытательный стенд',
            'system_info': system_info,
            'current_time': timezone.now().strftime('%Y-%m-%d %H:%M:%S'),
            'django_version': settings.VERSION,
            'debug_mode': settings.DEBUG,
            
            # Статусы служб (пример)
            'services': [
                {'name': 'Test Controller', 'status': 'running', 'uptime': '15d 4h'},
                {'name': 'Data Logger', 'status': 'running', 'uptime': '15d 4h'},
                {'name': 'Report Generator', 'status': 'idle', 'uptime': '2d 1h'},
                {'name': 'MQTT Broker', 'status': 'running', 'uptime': '7d 12h'},
            ],
            
            # Последние события
            'recent_events': [
                {'time': '10:30', 'message': 'System startup completed', 'type': 'info'},
                {'time': '10:35', 'message': 'Calibration cycle initiated', 'type': 'warning'},
                {'time': '10:40', 'message': 'Test sequence #1245 started', 'type': 'info'},
                {'time': '10:45', 'message': 'Test #1245 completed successfully', 'type': 'success'},
            ],
        })
        
        return context

class TestBenchView(TemplateView):
    template_name = 'RM_mainscreen.html'
    context_object_name = 'testbench'
