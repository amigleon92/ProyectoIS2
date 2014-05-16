from django.shortcuts import render
from .models import Fase
from Aplicaciones.Usuario.models import Usuario
from Aplicaciones.Proyecto.models import Proyecto
from Aplicaciones.Rol.models import Rol
from Aplicaciones.Proyecto.views import ProyectoView
from Aplicaciones.Item.models import Item

# Create your views here.

#Lista de Fases correspondientes al Proyecto dentro
class FaseView(ProyectoView):
    template_name = 'Fase/Fase.html'
    context_object_name = 'lista_fases'
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
        if len(Rol.objects.filter(nombre= 'Lider del Proyecto', usuario= usuario_logueado, proyecto= proyecto_actual)):
            fase_actual= Fase.objects.get(id= request.POST['fase'])
            if fase_actual.estado=='N':
                diccionario['fase']= fase_actual
                return render(request, self.template_name, diccionario)
            else:
                diccionario['error']= 'La fase ya fue inicializada'
        else:
            diccionario['error']= 'No puedes realizar esta accion'
        diccionario['lista_fases']= Fase.objects.filter(proyecto= proyecto_actual)
        return render(request, super(EditarFase, self).template_name, diccionario)

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
        modificar_fase.estado= 'I'
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
        if len(Rol.objects.filter(nombre= 'Lider del Proyecto', usuario= usuario_logueado, proyecto= proyecto_actual)):
            fase_actual= Fase.objects.get(id= request.POST['fase'])
            lista_de_items= Item.objects.filter(fase=fase_actual, activo=True)
            if fase_actual.estado=='I':
                for i in diccionario['lista_fases']:
                    if i.numeroSecuencia < fase_actual.numeroSecuencia and not i.estado=='F':
                        diccionario['error']= 'No se puede cerrar la fase - Fase Anterior No Finalizadda'
                        return render(request, super(CerrarFase, self).template_name, diccionario)
                for item in lista_de_items:
                    if not item.estado == 'B':
                        diccionario['error']= 'No se puede cerrar la fase - Exite items NO BLOQUEADO'
                        return render(request, super(CerrarFase, self).template_name, diccionario)
                fase_actual.estado='F'
                fase_actual.save()
                return render(request, self.template_name, diccionario)
            else:
                diccionario['error']= 'No se puede cerrar - Fase No Iniciada'
        else:
            diccionario['error']= 'No puedes realizar esta accion'
        return render(request, super(CerrarFase, self).template_name, diccionario)

#Finalizar el proyecto una vez terminadas las fases
class FinalizarProyecto(FaseView):
    template_name = 'Fase/FinalizarProyecto.html'
    def post(self, request, *args, **kwargs):
        diccionario={}
        usuario_logueado= Usuario.objects.get(id= request.POST['login'])
        proyecto_actual= Proyecto.objects.get(id= request.POST['proyecto'])
        diccionario['logueado']= usuario_logueado
        diccionario['proyecto']= proyecto_actual
        if len(Rol.objects.filter(nombre= 'Lider del Proyecto', usuario= usuario_logueado, proyecto= proyecto_actual)):
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

class AsignarNuevosMiembros(FaseView):
    template_name = 'Fase/AsignarNuevosMiembros.html'
    def post(self, request, *args, **kwargs):
        diccionario={}
        usuario_logueado= Usuario.objects.get(id= request.POST['login'])
        proyecto_actual= Proyecto.objects.get(id= request.POST['proyecto'])
        diccionario['logueado']= usuario_logueado
        diccionario['proyecto']= proyecto_actual
        if len(Rol.objects.filter(nombre= 'Lider del Proyecto', usuario= usuario_logueado, proyecto= proyecto_actual)):
            lista_usuarios= Usuario.objects.filter(estado= True)
            lista_no_miembros= []
            for usuario in lista_usuarios:
                if not usuario in proyecto_actual.miembros.all():
                    lista_no_miembros.append(usuario)
            if not len(lista_no_miembros):
                diccionario['lista_fases']= Fase.objects.filter(proyecto= proyecto_actual)
                diccionario['error']= 'No existen mas usuarios'
                return render(request, super(AsignarNuevosMiembros, self).template_name, diccionario)
            diccionario['lista_no_miembros']= lista_no_miembros
            return render(request, self.template_name, diccionario)
        else:
            diccionario[super(AsignarNuevosMiembros, self).context_object_name]= Fase.objects.filter(proyecto= proyecto_actual)
            diccionario['error']= 'No posee permisos para asignar nuevos miembros al proyecto'
            return render(request, super(AsignarNuevosMiembros, self).template_name, diccionario)

class AsignarNuevosMiembrosConfirm(FaseView):
    template_name = 'Fase/AsignarNuevosMiembrosConfirmar.html'
    def post(self, request, *args, **kwargs):
        diccionario={}
        usuario_logueado= Usuario.objects.get(id= request.POST['login'])
        proyecto_actual= Proyecto.objects.get(id= request.POST['proyecto'])
        diccionario['logueado']= usuario_logueado
        diccionario['proyecto']= proyecto_actual
        usuarios_miembros= request.POST.getlist('miembros[]')
        for usuario in usuarios_miembros:
            usuario= Usuario.objects.get(nick= usuario)
            proyecto_actual.miembros.add(usuario)
        return render(request, self.template_name, diccionario)
