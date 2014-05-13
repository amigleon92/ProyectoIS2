from django.conf.urls import patterns, include, url
from .views import TipoDeItemView, CrearTipoDeItem, CrearTipoDeItemConfirm, EliminarTipoDeItem, EditarTipoDeItem, EditarTipoDeItemConfirm

from django.contrib import admin
admin.autodiscover()

urlpatterns= patterns('',
    url(r'^$', TipoDeItemView.as_view(), name="tipo_de_item"),
    url(r'^crearTipoDeItem/$', CrearTipoDeItem.as_view(), name="crear_tipo_de_item"),
    url(r'^crearTipoDeItem/confirmar/$', CrearTipoDeItemConfirm.as_view(), name="crear_tipo_de_item_confirm"),
    url(r'^eliminar/$', EliminarTipoDeItem.as_view(), name="eliminar_tipo_de_item"),
    url(r'^editar/$', EditarTipoDeItem.as_view(), name="editar_tipo_de_item"),
    url(r'^editar/confirmar/$', EditarTipoDeItemConfirm.as_view(), name="editar_tipo_de_item_confirm"),
    #Atributo
    url(r'^atributo/', include('Aplicaciones.Atributo.urls')),



)
