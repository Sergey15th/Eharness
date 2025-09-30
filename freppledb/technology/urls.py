from django.urls import re_path
from django.urls import path
from django.views.generic.base import TemplateView

from freppledb import mode

# Automatically add these URLs when the application is installed
autodiscover = True

if mode == "WSGI":
    from . import views
    from freppledb.technology.views import *
    from . import serializers

    urlpatterns = [
        # Таблица соединений
        re_path(r"^data/technology/connectionlist/$", views.ConnectionListList.as_view(), name="technology_connectionlist_changelist", ),
        # Карта резки
        re_path(r"^data/technology/cutlist/$", views.CutListList.as_view(), name="technology_cutlist_changelist", ),

        # Карта обжимки
        re_path(r"^data/technology/crimplist/$", views.CrimpListList.as_view(), name="technology_crimplist_changelist", ),

        # Карта пайки
        re_path(r"^data/technology/solderinglist/$", views.SolderingList.as_view(), name="technology_solderinglist_changelist", ),
        
        # Перечень схем пайки
        re_path(r"^data/technology/solderingscheme/$", views.SolderingSchemeList.as_view(), name="technology_solderingscheme_changelist", ),

        # Перечень схем трассировки
        re_path(r"^data/technology/tracescheme/$", views.TraceSchemeList.as_view(), name="technology_tracescheme_changelist", ),

        # Схема пайки - отображение
        re_path(r"^data/technology/solderingscheme/detail/(?P<pk>(.+))/$", SolderingSchemeDetailView.as_view(), name='scheme-detail'),

        # Схема трассировки - отображение
        re_path(r"^data/technology/tracescheme/detail/(?P<pk>(.+))/$", TraceSchemeDetailView.as_view(), name='trace-scheme-detail'),

        # ОТОБРАЖЕНИЕ ItemT
        re_path(r"^data/technology/itemt/$", views.ItemTList.as_view(), name="input_itemt_changelist", ),

        # ОТОБРАЖЕНИЕ превью этикетки
        re_path(r"^data/technology/print-label/(?P<product_id>(.+))/$", ProductLabelView.as_view(), name='print-label'),
        re_path(r"^data/technology/label-preview/(?P<product_id>(.+))/$", ProductLabelPreviewView.as_view(), name='label-preview'),

        # ОТОБРАЖЕНИЕ списка этикеток
        re_path(r"^data/technology/productlabel/$", views.ProductLabelList.as_view(), name="technology_productlabel_changelist", ),

        # ОТОБРАЖЕНИЕ списка мобильных вешал
        re_path(r"^data/technology/mobilehanger/$", views.MobileHangerList.as_view(), name="technology_mobilehanger_changelist", ),
        # ОТОБРАЖЕНИЕ мобильного вешала
        re_path(r"^data/technology/mobilehanger/(?P<pk>(.+))/$", views.MobileHangerView.as_view(), name="technology_mobilehanger_view", ),

        # REST API framework
        re_path(r"^api/technology/connectionlist/$", serializers.ConnectionListAPI.as_view()),
        re_path(r"^api/technology/cutlist/$", serializers.CutListAPI.as_view()),
        re_path(r"^api/technology/crimplist/$", serializers.ConnectionListAPI.as_view()),
        re_path(r"^api/technology/solderinglist/$", serializers.SolderingListAPI.as_view()),
        re_path(r"^api/technology/productlabel/$", serializers.ProductLabelAPI.as_view(), name='product-label'),
        re_path(r"^api/technology/solderingscheme/$", serializers.SolderingSchemeAPI.as_view()),
        re_path(r"^api/technology/tracescheme/$", serializers.TraceSchemeAPI.as_view()),
        re_path(r"^api/input/item/(?P<pk>(.+))/$", serializers.ItemTdetailAPI.as_view(), ),
        re_path(r"^api/technology/itemt/$", serializers.ItemTAPI.as_view()),

        # ПЕРЕХВАТЫВАЕМ REST API framework ТОВАРНОЙ ПОЗИЦИИ
        re_path(r"^api/input/item/$", serializers.ItemTAPI.as_view()),
        # ПЕРЕХВАТЫВАЕМ ОТОБРАЖЕНИЕ ТОВАРНОЙ ПОЗИЦИИ
        re_path(r"^data/input/item/$", views.ItemTList.as_view(), name="input_itemt_changelist", ),
   ]
'''
'''