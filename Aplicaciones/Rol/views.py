from django.shortcuts import render
from Aplicaciones.Fase.views import FaseView
from Aplicaciones.Usuario.models import Usuario
from Aplicaciones.Proyecto.models import Proyecto
from Aplicaciones.Fase.models import Fase
from .models import Rol

# Create your views here.
class RolView(FaseView):
    template_name = 'Rol/Rol.html'
    context_object_name = 'lista_roles'
    def post(self, request, *args, **kwargs):
        diccionario={}
        usuario_logueado= Usuario.objects.get(id= request.POST['login'])
        proyecto_actual= Proyecto.objects.get(id= request.POST['proyecto'])
        diccionario['logueado']= usuario_logueado
        diccionario['proyecto']= proyecto_actual
        if len(Rol.objects.filter(nombre= 'Lider del Proyecto', usuario= usuario_logueado, proyecto= proyecto_actual)):
            diccionario[self.context_object_name]= Rol.objects.filter(proyecto= proyecto_actual, activo= True)
            return render(request, self.template_name, diccionario)
        else:
            diccionario[super(RolView, self).context_object_name]= Fase.objects.filter(proyecto= proyecto_actual)
            diccionario['error']= 'No posee permisos para visualizar los roles del proyecto'
            return render(request, super(RolView, self).template_name, diccionario)

class CrearRol(RolView):
    template_name = 'Rol/CrearRol.html'
    def post(self, request, *args, **kwargs):
        diccionario={}
        usuario_logueado= Usuario.objects.get(id= request.POST['login'])
        proyecto_actual= Proyecto.objects.get(id= request.POST['proyecto'])
        diccionario['logueado']= usuario_logueado
        diccionario['proyecto']= proyecto_actual
        return render(request, self.template_name, diccionario)

class CrearRolConfirm(CrearRol):
    template_name = 'Rol/CrearRolConfirm.html'
    def post(self, request, *args, **kwargs):
        diccionario={}
        usuario_logueado= Usuario.objects.get(id= request.POST['login'])
        proyecto_actual= Proyecto.objects.get(id= request.POST['proyecto'])
        diccionario['logueado']= usuario_logueado
        diccionario['proyecto']= proyecto_actual
        nuevo_rol= Rol(
            nombre= request.POST['nombre_rol'],
            usuario= Usuario.objects.get(nick= request.POST['usuario_rol']),
            proyecto= proyecto_actual,
        )
        nuevo_rol.save()
        #Completamos los permisos
        if 'votar_solicitud' in request.POST: nuevo_rol.votar= True
        if 'consultar_solicitud' in request.POST: nuevo_rol.consultar_solicitud= True
        if 'crear_item' in request.POST: nuevo_rol.crear_item= True
        if 'editar_item' in request.POST: nuevo_rol.editar_item= True
        if 'eliminar_item' in request.POST: nuevo_rol.eliminar_item= True
        if 'consultar_item' in request.POST: nuevo_rol.consultar_items= True
        if 'aprobar_item' in request.POST: nuevo_rol.aprobar_item= True
        if 'revivir_item' in request.POST: nuevo_rol.revivir_item= True
        if 'revertir_item' in request.POST: nuevo_rol.revertir_item= True
        if 'establecer_relacion' in request.POST: nuevo_rol.establecer_relacion= True
        if 'eliminar_relacion' in request.POST: nuevo_rol.eliminar_relacion= True
        if 'consultar_relacion' in request.POST: nuevo_rol.consultar_relaciones= True
        if 'agregar_atributo' in request.POST: nuevo_rol.agregar_atributo= True
        if 'eliminar_atributo' in request.POST: nuevo_rol.eliminar_atributo= True
        if 'completar_atributo' in request.POST: nuevo_rol.completar_atributos= True
        if 'consultar_atributo' in request.POST: nuevo_rol.consultar_atributos= True
        if 'crear_tipodeitem' in request.POST: nuevo_rol.crear_tipodeitem= True
        if 'eliminar_tipodeitem' in request.POST: nuevo_rol.eliminar_tipodeotem= True
        if 'modificar_tipodeitem' in request.POST: nuevo_rol.modificar_tipodeitem= True
        if 'crear_lineabase' in request.POST: nuevo_rol.crear_lineabase= True
        nuevo_rol.save()
        return render(request, self.template_name, diccionario)


class EditarRol(RolView):
    template_name = 'Rol/EditarRol.html'
    def post(self, request, *args, **kwargs):
        diccionario={}
        usuario_logueado= Usuario.objects.get(id= request.POST['login'])
        proyecto_actual= Proyecto.objects.get(id= request.POST['proyecto'])
        rol_actual= Rol.objects.get(id= request.POST['rol'])
        diccionario['logueado']= usuario_logueado
        diccionario['proyecto']= proyecto_actual
        diccionario['rol']= rol_actual
        return render(request, self.template_name, diccionario)

class EditarRolConfirmar(EditarRol):
    template_name = 'Rol/EditarRolConfirm.html'
    def post(self, request, *args, **kwargs):
        diccionario={}
        usuario_logueado= Usuario.objects.get(id= request.POST['login'])
        proyecto_actual= Proyecto.objects.get(id= request.POST['proyecto'])
        rol_actual= Rol.objects.get(id= request.POST['rol'])
        diccionario['logueado']= usuario_logueado
        diccionario['proyecto']= proyecto_actual
        rol_actual.nombre= request.POST['nombre_rol']
        #Actualizamos los permisos
        if 'votar_solicitud' in request.POST: rol_actual.votar= True
        else: rol_actual.votar= False
        if 'consultar_solicitud' in request.POST: rol_actual.consultar_solicitud= True
        else: rol_actual.consultar_solicitud= False
        if 'crear_item' in request.POST: rol_actual.crear_item= True
        else: rol_actual.crear_item= False
        if 'editar_item' in request.POST: rol_actual.editar_item= True
        else: rol_actual.editar_item= False
        if 'eliminar_item' in request.POST: rol_actual.eliminar_item= True
        else: rol_actual.eliminar_item= False
        if 'consultar_item' in request.POST: rol_actual.consultar_items= True
        else: rol_actual.consultar_items= False
        if 'aprobar_item' in request.POST: rol_actual.aprobar_item= True
        else: rol_actual.aprobar_item= False
        if 'revivir_item' in request.POST: rol_actual.revivir_item= True
        else: rol_actual.revivir_item= False
        if 'revertir_item' in request.POST: rol_actual.revertir_item= True
        else: rol_actual.revertir_item= False
        if 'establecer_relacion' in request.POST: rol_actual.establecer_relacion= True
        else: rol_actual.establecer_relacion= False
        if 'eliminar_relacion' in request.POST: rol_actual.eliminar_relacion= True
        else: rol_actual.eliminar_relacion= False
        if 'consultar_relacion' in request.POST: rol_actual.consultar_relaciones= True
        else: rol_actual.consultar_relaciones= False
        if 'agregar_atributo' in request.POST: rol_actual.agregar_atributo= True
        else: rol_actual.agregar_atributo= False
        if 'eliminar_atributo' in request.POST: rol_actual.eliminar_atributo= True
        else: rol_actual.eliminar_atributo= False
        if 'completar_atributo' in request.POST: rol_actual.completar_atributos= True
        else: rol_actual.completar_atributos= False
        if 'consultar_atributo' in request.POST: rol_actual.consultar_atributos= True
        else: rol_actual.consultar_atributos= False
        if 'crear_tipodeitem' in request.POST: rol_actual.crear_tipodeitem= True
        else: rol_actual.crear_tipodeitem= False
        if 'eliminar_tipodeitem' in request.POST: rol_actual.eliminar_tipodeotem= True
        else: rol_actual.eliminar_tipodeotem= False
        if 'modificar_tipodeitem' in request.POST: rol_actual.modificar_tipodeitem= True
        else: rol_actual.modificar_tipodeitem= False
        if 'crear_lineabase' in request.POST: rol_actual.crear_lineabase= True
        else: rol_actual.crear_lineabase= False
        rol_actual.save()
        return render(request, self.template_name, diccionario)

class EliminarRol(RolView):
    template_name = 'Rol/EliminarRol.html'
    def post(self, request, *args, **kwargs):
        diccionario={}
        usuario_logueado= Usuario.objects.get(id= request.POST['login'])
        proyecto_actual= Proyecto.objects.get(id= request.POST['proyecto'])
        rol_actual= Rol.objects.get(id= request.POST['rol'])
        diccionario['logueado']= usuario_logueado
        diccionario['proyecto']= proyecto_actual
        rol_actual.activo= False
        rol_actual.save()
        return render(request, self.template_name, diccionario)