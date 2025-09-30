from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from .services import code_scanned_signal
from .models import *
from django.middleware.csrf import get_token
from django.conf import settings
from django.contrib.admin.utils import unquote
from django.db.models.functions import Cast
from django.db.models import Q, IntegerField
from django.db.models.expressions import RawSQL
from django.template import Template
from django.utils.translation import gettext_lazy as _
from django.utils.encoding import force_str
from django.utils.text import format_lazy
from django.contrib.auth import login
from django.shortcuts import render, redirect
from freppledb.technology.views import CutListList
from urllib.parse import unquote
import re

from freppledb.boot import getAttributeFields
from freppledb.technology.models import *
from freppledb.input.models import (
    Item, Operation
)
from freppledb.common.report import (
    GridReport,
    GridFieldLastModified,
    GridFieldDateTime,
    GridFieldText,
    GridFieldHierarchicalText,
    GridFieldNumber,
    GridFieldInteger,
    GridFieldCurrency,
    GridFieldChoice,
    GridFieldDuration,
    GridFieldBool,
)

import logging

logger = logging.getLogger(__name__)

@csrf_exempt
def CodeScanned(request):
    if request.method == 'POST':
        barcode = request.POST.get('barcode')
        code_scan_event = CodeScanEvent()
        code_scan_event.session_id = get_token(request)
        logger.info('CSRF_Token=' + code_scan_event.session_id)
        code_scan_event.scan_data = barcode
        # Проверяем что за код
        for codetype in CodesTypes.objects.all():
            match = re.fullmatch(codetype.pattern, barcode)
            if match:
                # Ищем пользователя по коду
                # user = User.objects.get(employee__barcode=barcode)  # Пример для модели Employee
                try:
                    w_id = request.COOKIES['workstation_id']
                except Exception as e:
                    w_id = None
                    pass
                try:
                    item_id = request.COOKIES['item_id']
                except Exception as e:
                    item_id = None
                    pass
                if codetype.type =='UserPassCard': # Если отсканировали карту-пропуск пользователя
                    try:
                        user_logged = UserCodes.objects.get(code=barcode)
                        login(request, user_logged.user)
                        return JsonResponse({'status': 'success', 'action':'user_login', 'reload':True, 'redirect':False, 'redirect_url': '/'})
                    except Exception as e:
                        logger.error('User with passcard ' + barcode + ' not found!')
                    pass            
                elif codetype.type =='WorkPlace': # Если отсканировали Рабочее место
                    try:
                        workstation = Workstation.objects.get(qr=barcode)
                        return JsonResponse({'status': 'success', 'action':'workstation_set', 'data':workstation.short_name, 'reload':True, 'redirect':False, 'redirect_url': '/'})
                    except Exception as e:
                        logger.error('Workstation ' + barcode + ' not found!')
                elif codetype.type =='Item_barcode': # Если отсканировали Номенклатуру по штрих-коду
                    try:
                        nom = ItemT.objects.get(barcode=barcode)

                        if w_id =='РМ1': # Рабочее место нарезки и зачистки
                            prev_page = unquote(request.META.get('HTTP_REFERER'))
                            if not '/cutlist/?operation=' in prev_page or ('/cutlist/?operation=' in prev_page and nom.name not in prev_page):
                                # Если текущая страница - не карта резки, или карта резки, но с другой номенклатурой
                                # RETURN REDIRECT CALL TO CUTLIST PAGE
                                return JsonResponse({'status': 'success', 'action':'item_cutlist_open', 'data':nom.name, 'reload':False, 'redirect':True, 'redirect_url': '/data/technology/cutlist/?operation='+ nom.name + ' - Нарезка и зачистка'}) #http://127.0.0.1:8000/data/technology/cutlist/
                            else:
                                # Текущая страница - карта резки, переключаемся на комплектовочную карту
                                # RETURN REDIRECT CALL TO OPERATION MATERIALS PAGE
                                return JsonResponse({'status': 'success', 'action':'item_cutlist_open', 'data':nom.name, 'reload':False, 'redirect':True, 'redirect_url': '/data/input/operationmaterial/?operation='+ nom.name + ' - Нарезка и зачистка'}) #http://127.0.0.1:8000/data/technology/operationmatherial/
                        elif w_id =='РМ2': # Рабочее место пайки
                            prev_page = unquote(request.META.get('HTTP_REFERER'))
                            soldering_scheme_id = SolderingScheme.objects.get(item=nom)
                            if ('/technology/solderingscheme/detail/' in prev_page and ('detail/' + str(soldering_scheme_id.id)) in prev_page) or ('/technology/solderinglist/' in prev_page and nom.name not in prev_page):
                                # Если текущая страница - схема пайки с текущей номенклатурой, или карта пайки, но с другой номенклатурой
                                # Переключаемся на карту пайки
                                return JsonResponse({'status': 'success', 'action':'item_solderinglist_open', 'data':nom.name, 'reload':False, 'redirect':True, 'redirect_url': '/data/technology/solderinglist/?operation='+ nom.name + ' - Нарезка и зачистка'}) #http://127.0.0.1:8000/data/technology/solderinglist/
                            elif ('/data/technology/solderinglist/?operation=' in prev_page and nom.name in prev_page) or '/data/input/operationmaterial/?operation=' in prev_page and nom.name not in prev_page:
                                # Текущая страница - карта пайки с текущей номенклатурой, или комплектовочная карта, но с другой номенклатурой
                                # Преключаемся на комплектовочную карту
                                return JsonResponse({'status': 'success', 'action':'item_operationmaterial_open', 'data':nom.name, 'reload':False, 'redirect':True, 'redirect_url': '/data/input/operationmaterial/?operation='+ nom.name + ' - Пайка'}) #http://127.0.0.1:8000/data/technology/operationmatherial/
                            elif ('/data/input/operationmaterial/' in prev_page and nom.name in prev_page) or ('/data/technology/solderingscheme/detail/' in prev_page and ('detail/' + str(soldering_scheme_id.id)) not in prev_page):
                                # Текущая страница - комплектовочная карта с текущей номенклатурой, или схема пайки, но с другой номенклатурой,  переключаемся на схему пайки
                                # RETURN REDIRECT CALL TO OPERATION MATERIALS PAGE
                                return JsonResponse({'status': 'success', 'action':'item_cutlist_open', 'data':nom.name, 'reload':False, 'redirect':True, 'redirect_url': '/data/technology/solderingscheme/detail/'+ str(soldering_scheme_id.id) + '/'}) #http://127.0.0.1:8000/data/technology/operationmatherial/
                            else:
                                # Переключаемся на карту пайки
                                return JsonResponse({'status': 'success', 'action':'item_solderlist_open', 'data':nom.name, 'reload':False, 'redirect':True, 'redirect_url': '/data/technology/solderinglist/?operation='+ nom.name + ' - Нарезка и зачистка'}) #http://127.0.0.1:8000/data/technology/solderinglist/
                        elif w_id =='РМ3': # Рабочее место печати этикеток
                            pass
                        elif w_id =='РМ4': # Рабочее место монтажа разъёмов
                            pass
                            pass
                        elif w_id =='РМ5': # Испытательный стенд
                            pass
                        elif w_id in ('РМ6.1', 'РМ6.2', 'РМ6.3', 'РМ6.4',): # Сборочные плазы
                            pass
                    except Exception as e:
                        if isinstance(e,KeyError):
                            logger.info('Ошибка ! Рабочее место не определено')
                        else:
                            logger.info('Item with barcode:' + barcode + ' not found!')
                elif codetype.type =='Item_mQR': # Если отсканировали Номенклатуру по mQR коду
                    try:
                        nom = ItemT.objects.get(qr=barcode)
                        if w_id =='РМ1': # Рабочее место нарезки и зачистки
                            return JsonResponse({'status': 'success', 'action':'cutlist_open', 'data':nom.name, 'reload':False, 'redirect':True, 'redirect_url': '/data/technology/cutlist/?operation='+ nom.name + ' - Нарезка и зачистка'}) #http://127.0.0.1:8000/data/technology/cutlist/
                    except Exception as e:
                        logger.info('Item with barcode:' + barcode + ' not found!')
                elif codetype.type =='SalesOrder': # Если отсканировали Заказ на производство по штрих-коду
                    try:
                        if w_id =='РМ1': # Рабочее место нарезки и зачистки
                            return JsonResponse({'status': 'success', 'action':'demamd_open', 'data':barcode, 'reload':False, 'redirect':True, 'redirect_url': '/data/input/demand/?barcode='+ barcode})
                    except Exception as e:
                        logger.info('Item with barcode:' + barcode + ' not found!')
                elif codetype.type == 'MobileHanger':
                    if barcode[2:5] == '000': # Отсканирован код не крючка, а мобильного вешала
                        if w_id =='РМ1': #Отсканировали мобильное вешало на рабочем месте зачистки и нарезки
                            if item_id is not None: #Если предварительно была отсканирована Номенклатура
                                try:
                                    CurrentMobileHanger = MobileHanger.objects.get(number=int(barcode[1]))
                                    LastScannedItem = ItemT.objects.get(name=item_id)
                                    CurrentMobileHanger.current_item = LastScannedItem
                                    CurrentMobileHanger.save()
                                    return JsonResponse({'status': 'success', 'action':'mobile_hanger_set', 'data':CurrentMobileHanger.current_item.short_name, 'reload':True, 'redirect':False, 'redirect_url': '/'})
                                except Exception as e: # Мобильное вешало не зарегистрировано
                                    try:
                                        CurrentMobileHanger = MobileHanger(number=int(barcode[1]))
                                        LastScannedItem = ItemT.objects.get(name=item_id)
                                        CurrentMobileHanger.current_item = LastScannedItem
                                        CurrentMobileHanger.save()
                                        return JsonResponse({'status': 'success', 'action':'mobile_hanger_set', 'data':CurrentMobileHanger.current_item.short_name, 'reload':True, 'redirect':False, 'redirect_url': '/'})
                                    except Exception as e: # Что-то пошло не так
                                        pass
                    else: # Отсканирован крючок на мобильном вешале
                        if w_id in ('РМ6.1', 'РМ6.2', 'РМ6.3'): #Отсканировали на сборочном плазе
                            try:
                                item_mv_id =  MobileHanger.objects.get(number=barcode[1]).current_item.name # Какая Номенклатура привязана к данному мобильному вешалу
                            except Exception as e:
                                logger.info('Не удалось найти информацию о вешале ' + barcode[1])
                            if item_mv_id:
                            #LastScannedItem = ItemT.objects.get(name=item_id)
                                wire_no = ConnectionList.objects.get(operation=item_mv_id + ' - Нарезка и зачистка', hanged_no=barcode[2:4]).wire_no
                                TraceSchemeItem = TraceScheme.objects.get(item__name=item_mv_id, wire_no=wire_no)
                                return JsonResponse({'status': 'success', 'action':'trace_scheme_open', 'data':wire_no, 'reload':False, 'redirect':True, 'redirect_url': '/data/technology/tracescheme/detail/'+ str(TraceSchemeItem.id) + '/'})
        if request.user.is_authenticated:
            code_scan_event.user = request.user._wrapped if hasattr(request.user,'_wrapped') else request.user # Текущий пользователь
        else: code_scan_event.user = None
        code_scan_event.save()
        code_scanned_signal.send(sender=CodeScanEvent, instance=code_scan_event, request=request)
        
        if code_scan_event.user is not None:
            # User is authenticated
            #login(request, user)
            return JsonResponse({'status': 'success', 'username': code_scan_event.user.username})
        else:
            return JsonResponse({'status': 'error', 'message': 'User not found'}, status=404)
    return JsonResponse({'status': 'error'}, status=400)

class CodeScanEventList(GridReport):
    title = _("События сканирования кодов")
    basequeryset = CodeScanEvent.objects.all()
    model = CodeScanEvent
    frozenColumns = 0
    editable = False
    help_url = "help/codescanevent.html"
    message_when_empty = Template(
        """
        <h3>Здесь отображаются события сканирования QR кодов или RFID меток</h3>
        <br>
        <br>
        """
    )
    rows = (
        GridFieldDateTime("created_at", title=_("Отсканировано"), extra = ('"formatoptions":{"srcformat":"Y-m-d H:i:s","newformat":"%s H:i:s"}' % settings.DATE_FORMAT)),
        GridFieldText("scan_data", title=_("Данные")),
        GridFieldText(
            "user",
            title=_("user"),
            field_name="user__username",
            editable=False,
            align="center",
            width=80,
        ),
        GridFieldText("session_id", title=_("CSRF")),
        GridFieldText("source", title=_("source")),
        GridFieldLastModified("lastmodified"),
    )

class CodesTypesList(GridReport):
    title = _("Типы кодов")
    basequeryset = CodesTypes.objects.all()
    model = CodesTypes
    frozenColumns = 0
    editable = True
    help_url = "help/codestypes.html"
    message_when_empty = Template(
        """
        <h3>Здесь отображаются типы QR кодов или RFID меток</h3>
        <br>
        <br>
        """
    )
    rows = (
        GridFieldText("type", title=_("Тип кода")),
        GridFieldText("pattern", title=_("Паттерн")),
        GridFieldText("source", title=_("source")),
        GridFieldLastModified("lastmodified"),
    )

class UserCodesList(GridReport):
    title = _("Коды RFID пользователей")
    basequeryset = UserCodes.objects.all()
    model = UserCodes
    frozenColumns = 0
    editable = True
    help_url = "help/usercodes.html"
    message_when_empty = Template(
        """
        <h3>Здесь отображаются коды RFID меток пользователей</h3>
        <br>
        <br>
        """
    )
    rows = (
        GridFieldText(
            "user",
            title=_("user"),
            field_name="user__username",
            editable=False,
            align="center",
            width=80,
        ),
        GridFieldText("code", title=_("Код RFID карты")),
        GridFieldText("source", title=_("source")),
        GridFieldLastModified("lastmodified"),
    )

class WorkstationsList(GridReport):
    title = _("Рабочие места")
    basequeryset = Workstation.objects.all()
    model = Workstation
    frozenColumns = 0
    editable = True
    help_url = "help/workstations.html"
    message_when_empty = Template(
        """
        <h3>Здесь отображаются рабочие станцместаи</h3>
        <br>
        <br>
        """
    )
    rows = (
        GridFieldText("name", title=_("Наименование"), key=True, formatter="detail", extra='"role":"codescan/workstation"',),
        GridFieldText("short_name", title=_("РМ")),
        GridFieldHierarchicalText(
            "image",
            title=_("Изображение"),
            field_name="image",
            key=False,
            formatter="imagenew",
        ),
        GridFieldText("description", title=_("Описание")),
        GridFieldText("qr", title=_("QR Код")),
        GridFieldText("source", title=_("source")),
        GridFieldLastModified("lastmodified"),
    )
