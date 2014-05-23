from django.shortcuts import render
from django.views.generic import TemplateView
from .models import Proyecto
from Aplicaciones.Usuario.models import Usuario
from Aplicaciones.Rol.models import Rol
from Aplicaciones.Login.views import LoginView
from Aplicaciones.Fase.models import Fase

# Create your views here.

# Lista de Proyectos
class ProyectoView(TemplateView):
    template_name = 'Proyecto/Proyecto.html'
    context_object_name = 'lista_proyectos'
    def post(self, request, *args, **kwargs):
        diccionario= {}                                                  #Diccionario para ser retornado en HTML
        #Login.html es la unica pagina que envia un 'user' en el diccionario de request.POST
        if 'user' in request.POST:
            existe= Usuario.objects.filter(nick=request.POST['user'])
            if len(existe):
                if existe[0].password == request.POST['pass']:
                    diccionario[self.context_object_name]= Proyecto.objects.filter(activo= True)
                    diccionario['logueado']= existe[0]
                    return render(request, self.template_name, diccionario)
                else: error= 'Password incorrecto'
            else: error= 'Nombre de usuario no existe'
            diccionario['error']= error
            return render(request, LoginView.template_name, diccionario)
        else:
            diccionario[self.context_object_name]= Proyecto.objects.filter(activo= True)
            diccionario['logueado']= Usuario.objects.get(id=request.POST['login'])
            return render(request, self.template_name, diccionario)
    def get(self, request, *args, **kwargs):
        return render(request, LoginView.template_name, {'error':'Acceso Incorrecto'})

#Creacion de Proyectos
class CrearProyecto(ProyectoView):
    template_name = 'Proyecto/CrearProyecto.html'
    def post(self, request, *args, **kwargs):
        diccionario={}
        usuario_logueado= Usuario.objects.get(id= request.POST['login'])
        diccionario['logueado']= usuario_logueado
        diccionario[self.context_object_name]= Proyecto.objects.filter(activo= True)
        if len(Rol.objects.filter(nombre= 'Administrador del Sistema', usuario= usuario_logueado)): #Si el logueado es Admin?
            diccionario['lista_usuarios']= Usuario.objects.filter(estado= True)
            del diccionario[self.context_object_name]
            return render(request, self.template_name, diccionario)
        else:
            diccionario['error']= 'No puedes realizar esta accion'
            return render(request, super(CrearProyecto, self).template_name, diccionario)

class CrearProyectoConfirm(CrearProyecto):
    template_name = 'Proyecto/CrearProyectoConfirm.html'
    def post(self, request, *args, **kwargs):
        diccionario= {}
        usuario_logueado= Usuario.objects.get(id= request.POST['login'])
        diccionario['logueado']= usuario_logueado
        new_nombre= request.POST['nombre_proyecto']
        existe= Proyecto.objects.filter(nombre= new_nombre)
        if existe:
            diccionario['lista_usuarios']= Usuario.objects.filter(estado= True)
            diccionario['error']= 'Nombre de proyecto ya existe'
            return render(request, super(CrearProyectoConfirm, self).template_name, diccionario)
        else:
            #Creamos el proyecto
            nuevo_proyecto= Proyecto()
            nuevo_proyecto.nombre= new_nombre
            nuevo_proyecto.descripcion= request.POST['descripcion_proyecto']
            new_lider= Usuario.objects.get(nick= request.POST['lider_proyecto'])
            nuevo_proyecto.lider= new_lider
            nuevo_proyecto.save()
            #Agregamos al lider a los miembros para que puedda visualizar el proyecto
            nuevo_proyecto.miembros.add(new_lider)
            nuevo_proyecto.save()
            #Creamos el nuevo Rol Lider del Proyecto
            nuevo_rol= Rol(nombre= 'Lider del Proyecto', usuario= new_lider, proyecto= nuevo_proyecto)
            nuevo_rol.save()
            return render(request, self.template_name, diccionario)

#Eliminacion Logica de Proyectos
class EliminarProyecto(ProyectoView):
    template_name = 'Proyecto/EliminarProyecto.html'
    def post(self, request, *args, **kwargs):
        diccionario={}
        usuario_logueado= Usuario.objects.get(id= request.POST['login'])
        proyecto_actual= Proyecto.objects.get(id= request.POST['proyecto'])
        diccionario['logueado']= usuario_logueado
        diccionario[self.context_object_name]= Proyecto.objects.filter(activo= True)
        if len(Rol.objects.filter(nombre= 'Lider del Proyecto', usuario= usuario_logueado, proyecto= proyecto_actual, activo= True)):
            if proyecto_actual.estado=='F':
                proyecto_actual.activo= False
                proyecto_actual.save()
                rol_asociado= Rol.objects.get(nombre= 'Lider del Proyecto', usuario= proyecto_actual.lider, activo= True)
                rol_asociado.activo= False
                rol_asociado.save()
                del diccionario[self.context_object_name]  #No hace falta enviar la lista de proyectos
                return render(request, self.template_name, diccionario)
            else:
                diccionario['error']= 'Proyecto No Finalizado - No se puede eliminar'
        else:
            diccionario['error']= 'No puedes realizar esta accion'
        return render(request, super(EliminarProyecto,self).template_name, diccionario)

#Generacion de Informe del Proyecto
class InformeProyecto(ProyectoView):
    def post(self, request, *args, **kwargs):
        diccionario={}
        usuario_logueado= Usuario.objects.get(id= request.POST['login'])
        proyecto_actual= Proyecto.objects.get(id= request.POST['proyecto'])
        diccionario['logueado']= usuario_logueado
        diccionario[self.context_object_name]= Proyecto.objects.filter(activo= True)
        if not proyecto_actual.estado == 'N':
            diccionario['proyecto']= proyecto_actual
            del diccionario[self.context_object_name]
            return render(request, 'Proyecto/InformeProyecto.html', diccionario)
        diccionario['error']= 'No se puede mostrar proyecto - No Iniciado'
        return render(request, self.template_name, diccionario)

#Iniciando Proyecto
class InicializarProyecto(ProyectoView):
    template_name = 'Proyecto/InicializarProyecto.html'
    def post(self, request, *args, **kwargs):
        diccionario={}
        usuario_logueado= Usuario.objects.get(id= request.POST['login'])
        proyecto_actual= Proyecto.objects.get(id= request.POST['proyecto'])
        diccionario['logueado']= usuario_logueado
        diccionario[self.context_object_name]= Proyecto.objects.filter(activo= True)
        if len(Rol.objects.filter(nombre= 'Lider del Proyecto', usuario= usuario_logueado, proyecto= proyecto_actual)):
            if proyecto_actual.estado == 'N':
                diccionario['lista_usuarios']= Usuario.objects.filter(estado= True)
                diccionario['proyecto']= proyecto_actual
                del diccionario[self.context_object_name]
                return render(request, self.template_name, diccionario)
            else:
                diccionario['error']= 'El proyecto ya esta inicializado'
        else:
            diccionario['error']= 'No puede realizar esta accion'
        return render(request, super(InicializarProyecto, self).template_name, diccionario)

class InicializarProyectoConfirm(InicializarProyecto):
    template_name = 'Proyecto/InicializarProyectoConfirm.html'
    def post(self, request, *args, **kwargs):
        diccionario= {}
        usuario_logueado= Usuario.objects.get(id= request.POST['login'])
        diccionario['logueado']= usuario_logueado
        proyecto_detalles= Proyecto.objects.get(id= request.POST['proyecto'])
        proyecto_detalles.presupuesto= request.POST['presupuesto']
        proyecto_detalles.costoTemporal= request.POST['costoTemporal']
        proyecto_detalles.costoMonetario= request.POST['costoMonetario']
        proyecto_detalles.fechaInicio= request.POST['fechaInicio']
        proyecto_detalles.fechaFin= request.POST['fechaFin']
        proyecto_detalles.numeroFase= request.POST['numeroFase']
        usuarios_miembros= request.POST.getlist('miembros[]')
        for i in usuarios_miembros: proyecto_detalles.miembros.add(Usuario.objects.get(nick= i))
        proyecto_detalles.estado= 'I'
        proyecto_detalles.save()
        proyecto_detalles= Proyecto.objects.get(nombre= proyecto_detalles.nombre)
        for i in range(1, proyecto_detalles.numeroFase+1):
            nueva_fase= Fase()
            nueva_fase.nombre= 'Fase de '+ proyecto_detalles.nombre
            nueva_fase.numeroSecuencia= i
            nueva_fase.numero= i
            nueva_fase.proyecto= proyecto_detalles
            if i==1: nueva_fase.estado='I'
            nueva_fase.save()
        return render(request, self.template_name, diccionario)



#construccion
class ConstruccionView(TemplateView):
    template_name = 'Proyecto/Construccion.html'
    def post(self, request, *args, **kwargs):
        diccionario={}
        return render(request, self.template_name, diccionario)

