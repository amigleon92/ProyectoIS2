from django.shortcuts import render
from .models import Solicitud_de_Cambios
from .models import Voto
from Aplicaciones.Usuario.models import Usuario
from Aplicaciones.Rol.models import Rol
from Aplicaciones.Proyecto.models import Proyecto
from Aplicaciones.Item.models import Item
from Aplicaciones.Item.views import ItemView
from Aplicaciones.Fase.models import Fase
from Aplicaciones.Proyecto.views import ProyectoView


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
    def ContarVotos(self, solicitud_actual):
        if not len(Voto.objects.filter(solicitud_de_cambios=solicitud_actual, voto='Pe')):
            si=0
            no=0
            votos_de_solicitud=Voto.objects.filter(solicitud_de_cambios=solicitud_actual)
            for voto_solicitud in votos_de_solicitud:
                if voto_solicitud.voto == 'Si': si=si+1
                elif voto_solicitud.voto == 'No': no=no+1
            if si>no:
                solicitud_actual.estado='A'
            else:
                solicitud_actual.estado='D'
            solicitud_actual.save()

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
                return render(request, super(VotarFase, self).template_name, diccionario)
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
        voto_miembro=Voto.objects.get(usuario=usuario_logueado, solicitud_de_cambios=solicitud_actual, activo=True)
        diccionario['logueado']= usuario_logueado
        diccionario['proyecto']= proyecto_actual
        diccionario['fase']=fase_actual
        voto_miembro.voto=voto_actual
        voto_miembro.save()
        solicitud_actual.cantidad_de_votos=solicitud_actual.cantidad_de_votos+1
        solicitud_actual.save()
        self.ContarVotos(solicitud_actual)
        return render(request, self.template_name, diccionario)

class SolicitudesDeProyectoView(ProyectoView):
    template_name = 'Solicitud_de_Cambios/SolicitudesDeProyecto.html'
    def post(self, request, *args, **kwargs):
        diccionario={}
        usuario_logueado= Usuario.objects.get(id= request.POST['login'])
        diccionario['logueado']= usuario_logueado
        lista_solicitudes=[]
        for miembro in Rol.objects.filter(nombre='Miembro del Comite', usuario=usuario_logueado):
              if len(Solicitud_de_Cambios.objects.filter(proyecto=miembro.proyecto, estado='V', activo=True)):
                   for solicitud in Solicitud_de_Cambios.objects.filter(proyecto=miembro.proyecto,estado='V', activo=True):
                       voto_actual=Voto.objects.filter(usuario=usuario_logueado, solicitud_de_cambios=solicitud)
                       if voto_actual[0].voto == 'Pe':
                            lista_solicitudes.append(solicitud)
        diccionario['lista_solicitudes']=lista_solicitudes
        return render(request, self.template_name, diccionario)

class VotarProyecto(SolicitudesDeProyectoView):
    template_name = 'Solicitud_de_Cambios/VotarProyecto.html'
    def post(self, request, *args, **kwargs):
        diccionario={}
        usuario_logueado= Usuario.objects.get(id= request.POST['login'])
        solicitud_actual=Solicitud_de_Cambios.objects.get(id=request.POST['solicitud'])
        diccionario['solicitud']=solicitud_actual
        diccionario['logueado']= usuario_logueado
        voto_miembro=Voto.objects.filter(usuario=usuario_logueado, solicitud_de_cambios=solicitud_actual, activo=True)
        diccionario['voto_miembro']=voto_miembro
        return render(request, self.template_name, diccionario)

class VotarProyectoConfirm(VotarProyecto):
    template_name = 'Solicitud_de_Cambios/VotarProyectoConfirm.html'
    def post(self, request, *args, **kwargs):
        diccionario={}
        usuario_logueado= Usuario.objects.get(id= request.POST['login'])
        solicitud_actual=Solicitud_de_Cambios.objects.get(id=request.POST['solicitud'])
        voto_actual=request.POST['voto']
        voto_miembro=Voto.objects.get(usuario=usuario_logueado, solicitud_de_cambios=solicitud_actual, activo=True)
        diccionario['logueado']= usuario_logueado
        voto_miembro.voto=voto_actual
        voto_miembro.save()
        solicitud_actual.cantidad_de_votos=solicitud_actual.cantidad_de_votos+1
        solicitud_actual.save()
        contar= SolicitudesDeFaseview()
        contar.ContarVotos(solicitud_actual)
        return render(request, self.template_name, diccionario)
