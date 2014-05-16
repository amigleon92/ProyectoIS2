from django.conf.urls import patterns, include, url
from .views import ItemView, CrearItem, CrearItemConfirm, EliminarItem, EditarItem, EditarItemConfirm
from .views import InformeItem, AprobarItem
from django.contrib import admin
admin.autodiscover()

urlpatterns= patterns('',
    url(r'^$', ItemView.as_view(), name="item"),
    url(r'^crearItem/$', CrearItem.as_view(), name="crear_item"),
    url(r'^crearItem/confirmar/$', CrearItemConfirm.as_view(), name="crear_item_confirmar"),
    url(r'^eliminar/$', EliminarItem.as_view(), name="eliminar_item_"),
    url(r'^editarItem/$', EditarItem.as_view(), name="editar_item"),
    url(r'^editarItem/confirmarEditado/$', EditarItemConfirm.as_view(), name="editar_item_confirmar"),
    url(r'^informe/$', InformeItem.as_view(), name="informe_item_"),
    url(r'^aprobar/$', AprobarItem.as_view(), name="aprobar_item"),

    #Atributo
    url(r'^atributo/', include('Aplicaciones.Atributo.urls')),

    #linea base urls
    url(r'^lineaBase/', include('Aplicaciones.Linea_Base.urls')),


)
