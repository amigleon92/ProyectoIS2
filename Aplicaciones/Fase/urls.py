from django.conf.urls import patterns, include, url
from .views import FaseView, EditarFase, EditarFaseConfirm, InformeFase, CerrarFase, FinalizarProyecto

urlpatterns= patterns('',
    url(r'^$', FaseView.as_view(), name="fase"),
    url(r'^editar/$', EditarFase.as_view(), name='editar_fase'),
    url(r'^editar/confirmar/$', EditarFaseConfirm.as_view(), name='editar_fase_confirmar'),
    url(r'^informe/$', InformeFase.as_view(), name='informe_fase'),
    url(r'^cerrar/$', CerrarFase.as_view(), name='cerrar_fase'),
    url(r'^finalizar_proyecto/$', FinalizarProyecto.as_view(), name="finalizar_proyecto"),

    #Rol
    url(r'^rol/', include('Aplicaciones.Rol.urls')),


    #Item
    url(r'^item/', include('Aplicaciones.Item.urls')),

    #Tipo de Item
    url(r'^tipoDeItem/', include('Aplicaciones.Tipo_de_Item.urls')),

    #Tipo de Atributo
    url(r'^tipoDeAtributo/', include('Aplicaciones.Tipo_de_Atributo.urls')),



)
