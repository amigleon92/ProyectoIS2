from django.conf.urls import patterns, include, url
from .views import TipoDeAtributoView, CrearTipoDeAtributo, CrearTipoDeAtributoConfirm, EliminarTipoDeAtributo

from django.contrib import admin
admin.autodiscover()

urlpatterns= patterns('',
    url(r'^$', TipoDeAtributoView.as_view(), name="tipo_de_atributo"),
    url(r'^crearTipoDeAtributo/$', CrearTipoDeAtributo.as_view(), name="crear_tipo_de_atributo"),
    url(r'^crearTipoDeAtributo/confirmar/$', CrearTipoDeAtributoConfirm.as_view(), name="crear_tipo_de_atributo_confirmar"),
    url(r'^eliminar/$', EliminarTipoDeAtributo.as_view(), name="eliminar_tipo_de_atributo")

)
