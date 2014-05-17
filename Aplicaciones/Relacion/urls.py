from django.conf.urls import patterns, include, url
from .views import RelacionView, EstablecerRelacionAS, EstablecerRelacionASConfirm, EstablecerRelacionPH, EstablecerRelacionPHConfirm, EliminarRelacion
from django.contrib import admin
admin.autodiscover()

urlpatterns= patterns('',
    url(r'^$', RelacionView.as_view(), name="item"),
    url(r'^establecerRelacionAS/$', EstablecerRelacionAS.as_view(), name="establecerRelacionAS"),
    url(r'^establecerRelacionAS/Confirmar/$', EstablecerRelacionASConfirm.as_view(), name="establecerRelacionASConfirm"),
    url(r'^establecerRelacionPH/$', EstablecerRelacionPH.as_view(), name="establecerRelacionPH"),
    url(r'^establecerRelacionPH/Confirmar/$', EstablecerRelacionPHConfirm.as_view(), name="establecerRelacionPHConfirm"),
    url(r'^eliminarRelacion/$', EliminarRelacion.as_view(), name="eliminarRelacion"),
    )