__author__ = 'rodrigo'
from django.conf.urls import patterns, include, url
from .views import LineaBaseView, CrearLineaBase, CrearLineaBaseConfirm, MostrarItems
from django.contrib import admin
admin.autodiscover()

urlpatterns= patterns('',
    url(r'^$', LineaBaseView.as_view(), name="linea_base"),
    url(r'^crearLineaBase/$', CrearLineaBase.as_view(), name="crear_linea_base"),
    url(r'^crearLineaBase/confirmar/$', CrearLineaBaseConfirm.as_view(), name="crear_linea_base_confirm"),
    url(r'^mostrarItems/$', MostrarItems.as_view(), name="mostrar_items_de_linea_base"),
    )
