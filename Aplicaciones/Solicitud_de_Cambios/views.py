from django.shortcuts import render
from .models import Solicitud_de_Cambios
from .models import Voto
from Aplicaciones.Usuario.models import Usuario
from Aplicaciones.Rol.models import Rol
from Aplicaciones.Proyecto.models import Proyecto
from Aplicaciones.Item.models import Item
from Aplicaciones.Item.views import ItemView
from Aplicaciones.Fase.models import Fase


# Create your views here.
#Lista de Fases correspondientes al Proyecto dentro
class SolicitudesDeFaseview(ItemView):
    template_name = 'Solicitud_de_Cambios/SolicitudesDeFase.html'
    def post(self, request, *args, **kwargs):
        diccionario={}
        usuario_logueado= Usuario.objects.get(id= request.POST['login'])
        proyecto_actual= Proyecto.objects.get(id= request.POST['proyecto'])
        fase_actual= Fase.objects.get(id=request.POST['fase'])
        diccionario['logueado']= usuario_logueado
        diccionario['proyecto']= proyecto_actual
        diccionario['fase']=fase_actual
        diccionario['lista_solicitudes']= Solicitud_de_Cambios.objects.filter(proyecto=proyecto_actual, fase=fase_actual, activo=True)
        return render(request, self.template_name, diccionario)



class VotarFase(SolicitudesDeFaseview):
    template_name = 'Solicitud_de_Cambios/VotarFase.html'
    def post(self, request, *args, **kwargs):
        diccionario={}
        usuario_logueado= Usuario.objects.get(id= request.POST['login'])
        proyecto_actual= Proyecto.objects.get(id= request.POST['proyecto'])
        fase_actual= Fase.objects.get(id=request.POST['fase'])
        solicitud_actual=Solicitud_de_Cambios.objects.get(id=request.POST['solicitud'])
        diccionario['solicitud']=solicitud_actual
        diccionario['logueado']= usuario_logueado
        diccionario['proyecto']= proyecto_actual
        diccionario['fase']=fase_actual
        if len(Rol.objects.filter(nombre='Miembro del Comite', usuario=usuario_logueado, activo=True)):
            voto_miembro=Voto.objects.filter(usuario=usuario_logueado, solicitud_de_cambios=solicitud_actual, activo=True)
            if not voto_miembro[0].voto=='Pe':
                diccionario['lista_solicitudes']= Solicitud_de_Cambios.objects.filter(proyecto=proyecto_actual, fase=fase_actual, activo=True)
                diccionario['error']= 'Usted ya ha votado.'
            return render(request, self.template_name, diccionario)
        else:
            diccionario['lista_solicitudes']= Solicitud_de_Cambios.objects.filter(proyecto=proyecto_actual, fase=fase_actual, activo=True)
            diccionario['error']= 'No puedes realizar esta accion'
            return render(request, super(VotarFase, self).template_name, diccionario)

class VotarFaseConfirm(VotarFase):
    template_name = 'Solicitud_de_Cambios/VotarFaseConfirm.html'
    def post(self, request, *args, **kwargs):
        diccionario={}
        usuario_logueado= Usuario.objects.get(id= request.POST['login'])
        proyecto_actual= Proyecto.objects.get(id= request.POST['proyecto'])
        fase_actual= Fase.objects.get(id=request.POST['fase'])
        solicitud_actual=Solicitud_de_Cambios.objects.get(id=request.POST['solicitud'])
        voto_actual=request.POST['voto']
        voto_miembro=Voto.objects.filter(usuario=usuario_logueado, solicitud_de_cambios=solicitud_actual, activo=True)
        diccionario['logueado']= usuario_logueado
        diccionario['proyecto']= proyecto_actual
        diccionario['fase']=fase_actual
        voto_miembro[0].voto=voto_actual
        voto_miembro[0].save()
        return render(request, self.template_name, diccionario)
