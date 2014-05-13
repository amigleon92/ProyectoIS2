from django.conf.urls import patterns, include, url
from .views import AtributoView, AgregarAtributo, AgregarAtributoConfirm, EliminarAtributo

from django.contrib import admin
admin.autodiscover()

urlpatterns= patterns('',
    url(r'^$', AtributoView.as_view(), name="atributo"),
    url(r'^agregarAtributo/$', AgregarAtributo.as_view(), name="agregar_atributo"),
    url(r'^agregarAtributo/confirmar/$', AgregarAtributoConfirm.as_view(), name="agregar_atributo_confirm"),
    url(r'^eliminar/$', EliminarAtributo.as_view(), name="eliminar_atributo"),
)
