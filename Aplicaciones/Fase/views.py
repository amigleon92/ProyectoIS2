from django.shortcuts import render
from .models import Fase
from Aplicaciones.Usuario.models import Usuario
from Aplicaciones.Proyecto.models import Proyecto
from Aplicaciones.Proyecto.views import ProyectoView

# Create your views here.

#Lista de Fases correspondientes al Proyecto dentro
class FaseView(ProyectoView):
    template_name = 'Fase/Fase.html'
    def post(self, request, *args, **kwargs):
        diccionario={}
        usuario_logueado= Usuario.objects.get(id= request.POST['login'])
        proyecto_actual= Proyecto.objects.get(id= request.POST['proyecto'])
        diccionario['logueado']= usuario_logueado
        diccionario['proyecto']= proyecto_actual
        if not proyecto_actual.estado=='N':
            diccionario['lista_fases']= Fase.objects.filter(proyecto= proyecto_actual)
            return render(request, self.template_name, diccionario)
        else:
            diccionario['lista_proyectos']= Proyecto.objects.filter(activo= True)
            diccionario['error']= 'Debe inicializar proyecto'
            return render(request, super(FaseView, self).template_name, diccionario)

#Editar los campos de los detalles de las fases
class EditarFase(FaseView):
    template_name = 'Fase/EditarFase.html'
    def post(self, request, *args, **kwargs):
        diccionario={}
        usuario_logueado= Usuario.objects.get(id= request.POST['login'])
        proyecto_actual= Proyecto.objects.get(id= request.POST['proyecto'])
        diccionario['logueado']= usuario_logueado
        diccionario['proyecto']= proyecto_actual
        if self.tienePermiso(usuario_logueado) and usuario_logueado== proyecto_actual.lider:
            fase= Fase.objects.get(id= request.POST['fase'])
            diccionario['fase']= fase
            return render(request, self.template_name, diccionario)
        diccionario['lista_fases']= Fase.objects.filter(proyecto= proyecto_actual)
        diccionario['error']= 'No puedes realizar esta accion'
        return render(request, super(EditarFase, self).template_name, diccionario)
    def tienePermiso(self, usuario):
        permisos= usuario.permiso.all()
        for i in permisos:
            if i.modificar_fase: return True
        return False

class EditarFaseConfirm(EditarFase):
    template_name = 'Fase/EditarFaseConfirm.html'
    def post(self, request, *args, **kwargs):
        diccionario={}
        usuario_logueado= Usuario.objects.get(id= request.POST['login'])
        proyecto_actual= Proyecto.objects.get(id= request.POST['proyecto'])
        diccionario['logueado']= usuario_logueado
        diccionario['proyecto']= proyecto_actual
        modificar_fase= Fase.objects.get(id=request.POST['fase'])
        modificar_fase.nombre= request.POST['nombre_fase']
        modificar_fase.descripcion= request.POST['descripcion_fase']
        modificar_fase.fechaInicio= request.POST['fechaInicio_fase']
        modificar_fase.fechaFin=request.POST['fechaFin_fase']
        modificar_fase.estado=request.POST['estado']
        modificar_fase.save()
        return render(request, self.template_name, diccionario)

#Muestra un informe de la fase.
class InformeFase(FaseView):
    template_name = 'Fase/InformeFase.html'
    def post(self, request, *args, **kwargs):
        diccionario={}
        usuario_logueado= Usuario.objects.get(id= request.POST['login'])
        proyecto_actual= Proyecto.objects.get(id= request.POST['proyecto'])
        diccionario['logueado']= usuario_logueado
        diccionario['proyecto']= proyecto_actual
        mostrar_fase= Fase.objects.get(id= request.POST['fase'])
        if not mostrar_fase.estado== 'N':
            diccionario['fase']= mostrar_fase
            return render(request, self.template_name, diccionario)
        else:
            diccionario['lista_fases']= Fase.objects.filter(proyecto= proyecto_actual)
            diccionario['error']= 'No se puede mostrar - Fase No Iniciada'
            return render(request, super(InformeFase, self).template_name, diccionario)

class CerrarFase(FaseView):
    template_name = 'Fase/CerrarFase.html'
    def post(self, request, *args, **kwargs):
        diccionario={}
        usuario_logueado= Usuario.objects.get(id= request.POST['login'])
        proyecto_actual= Proyecto.objects.get(id= request.POST['proyecto'])
        diccionario['logueado']= usuario_logueado
        diccionario['proyecto']= proyecto_actual
        diccionario['lista_fases']= Fase.objects.filter(proyecto= proyecto_actual)
        if self.tienePermiso(usuario_logueado) and usuario_logueado==proyecto_actual.lider:
            fase_actual= Fase.objects.get(id= request.POST['fase'])
            if fase_actual.estado=='I':
                for i in diccionario['lista_fases']:
                    if i.numeroSecuencia < fase_actual.numeroSecuencia and not i.estado=='F':
                        diccionario['error']= 'No se puede cerra la fase - Fase Anterior No Finalizadda'
                        return render(request, super(CerrarFase, self).template_name, diccionario)
                fase_actual.estado='F'
                fase_actual.save()
                return render(request, self.template_name, diccionario)
            else:
                diccionario['error']= 'No se puede cerrar - Fase No Iniciada'
        else:
            diccionario['error']= 'No puedes realizar esta accion'
        return render(request, super(CerrarFase, self).template_name, diccionario)
    def tienePermiso(self, usuario):
        permisos= usuario.permiso.all()
        for i in permisos:
            if i.cerrar_fase: return True
        return False

#Finalizar el proyecto una vez terminadas las fases
class FinalizarProyecto(FaseView):
    template_name = 'Fase/FinalizarProyecto.html'
    def post(self, request, *args, **kwargs):
        diccionario={}
        usuario_logueado= Usuario.objects.get(id= request.POST['login'])
        proyecto_actual= Proyecto.objects.get(id= request.POST['proyecto'])
        diccionario['logueado']= usuario_logueado
        diccionario['proyecto']= proyecto_actual
        if self.tienePermiso(usuario_logueado) and usuario_logueado==proyecto_actual.lider:
            ultima_fase= Fase.objects.get(numeroSecuencia= proyecto_actual.numeroFase, proyecto= proyecto_actual)       #comporbamos si se termino la ultima fase
            if not ultima_fase.estado=='F':
                diccionario['error']= 'Para finalizar, todas las fases deberian de estar cerradas'
                diccionario['lista_fases']= Fase.objects.filter(proyecto= proyecto_actual)
                return render(request, super(FinalizarProyecto, self).template_name, diccionario)
            else:
                proyecto_actual.estado= 'F'
                proyecto_actual.save()
                diccionario['lista_proyectos']= Proyecto.objects.filter(activo= True)
                return render(request, ProyectoView.template_name, diccionario)
        else:
            diccionario['lista_fases']= Fase.objects.filter(proyecto= proyecto_actual)
            diccionario['error']= 'No puedes realizar esta accion'
            return render(request, super(FinalizarProyecto, self).template_name, diccionario)
    def tienePermiso(self, usuario):
        permisos= usuario.permiso.all()
        for i in permisos:
            if i.finalizar_proyecto: return True
        return False