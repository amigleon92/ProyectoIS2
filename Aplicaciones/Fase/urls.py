from django.conf.urls import patterns, include, url
from .views import FaseView, EditarFase, EditarFaseConfirm, InformeFase, CerrarFase, FinalizarProyecto
from .views import AsignarNuevosMiembros, AsignarNuevosMiembrosConfirm, Graficar, Reporte_items, Reporte_SC

urlpatterns= patterns('',
    url(r'^$', FaseView.as_view(), name="fase"),
    url(r'^graficar/$', Graficar.as_view(), name="graficar_proyecto"),
    url(r'^reporteItem/$', Reporte_items.as_view(), name="reporte_Item"),
    url(r'^reporteSC/$', Reporte_SC.as_view(), name="reporte_SC"),
    url(r'^editar/$', EditarFase.as_view(), name='editar_fase'),
    url(r'^editar/confirmar/$', EditarFaseConfirm.as_view(), name='editar_fase_confirmar'),
    url(r'^informe/$', InformeFase.as_view(), name='informe_fase'),
    url(r'^cerrar/$', CerrarFase.as_view(), name='cerrar_fase'),
    url(r'^finalizar_proyecto/$', FinalizarProyecto.as_view(), name="finalizar_proyecto"),
    url(r'^asignar_nuevos_miembros/$', AsignarNuevosMiembros.as_view(), name='asignar_nuevos_miembros'),
    url(r'^asignar_nuevos_miembros/confirmar/$', AsignarNuevosMiembrosConfirm.as_view(), name='asignar_nuevos_miembros_confirmar'),

    #Rol
    url(r'^rol/', include('Aplicaciones.Rol.urls')),

    #Item
    url(r'^item/', include('Aplicaciones.Item.urls')),

    #Tipo de Item
    url(r'^tipoDeItem/', include('Aplicaciones.Tipo_de_Item.urls')),

)
