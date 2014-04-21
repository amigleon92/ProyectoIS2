"""
Django views for ProyectoIS2 project
"""
from django.http import request
from django.views.generic import TemplateView, CreateView, ListView
from ProjectApp.models import Usuarios, Roles, Proyecto, Fase
from django.core.urlresolvers import reverse_lazy
from django.shortcuts import render, render_to_response

#La clase Login es la encargada de la primera vista del proyecto que es un formulario para logueo
class login(TemplateView):
    template_name = 'login.html'
    def get(self, request, *args, **kwargs):
        return render(request,'login.html')

#La clase inicio es el que maneja el Menu Principal
class inicio(TemplateView):
    def existe(self,char):                                              #Funcion que devuelve int y comprueba
        for i in Proyecto.objects.all():                                #si el nick que le pasamos ya existe en la
            if i.nombre==char: return i.codigo                                #lista de proyectos
        return 0
    def post(self, request, *args, **kwargs):                           #En el metodo post en la condicion if
        if 'user' in request.POST:                                      #preguntamos si la pagina desde donde se lo
            buscar_user = request.POST['user']                          #llamo es el login:
            buscar_password = request.POST['pass']                      #Verifica el nombre de usuario y la
            error= ""                                                   #contrasenha ingresadas para verificar
            for i in Usuarios.objects.all():                            #si existe la entrada en la BD Usuarios
                if i.estado:
                    if i.nick == buscar_user:
                        if i.password == buscar_password:
                            listaProyecto= Proyecto.objects.all()
                            return render(request, 'inicio.html', {'lista_proyectos':listaProyecto,'logueado':i})
                        error= "Password incorrecto"
                        return render(request, 'login.html', {'error':error})
            error= "Usuario incorrecto"
            return render(request, 'login.html', {'error': error})
        else:
            if 'nombre_proyecto' in request.POST:
                new_nombre=request.POST['nombre_proyecto']
                existe_proyecto= inicio.existe(self,new_nombre)
                if existe_proyecto:
                    lista= Usuarios.objects.all()
                    return render(request, 'CrearProyecto.html', {'lista_usuarios':lista, 'logueado':Usuarios.objects.get(id=request.POST['login']), 'error': 'Nombre de proyecto ya existe'})
                new_lider= Usuarios.objects.get(nick= request.POST['lider_proyecto'])
                new_descripcion=request.POST['descripcion_proyecto']
                new_proyecto=Proyecto(nombre=new_nombre, descripcion=new_descripcion, lider=new_lider)
                new_proyecto.save()
                new_proyecto.usuarios.add(new_lider)
                new_proyecto.save()
                new_lider.permiso.add(Roles.objects.get(nombre='Lider del Proyecto'))
                new_lider.save()
            if 'presupuesto' in request.POST:
                proyecto_detalles= request.POST['proyecto']
                proyecto_detalles= Proyecto.objects.get(codigo=proyecto_detalles)
                proyecto_detalles.presupuesto= request.POST['presupuesto']
                proyecto_detalles.costoTemporal= request.POST['costoTemporal']
                proyecto_detalles.costoMonetario= request.POST['costoMonetario']
                proyecto_detalles.fechaInicio= request.POST['fechaInicio']
                proyecto_detalles.fechaFin= request.POST['fechaFin']
                proyecto_detalles.numeroFase= request.POST['numeroFase']
                usuarios= request.POST.getlist('miembros[]')
                for i in usuarios:
                    miembro_proyecto= Usuarios.objects.get(nick=i)
                    proyecto_detalles.usuarios.add(miembro_proyecto)
                proyecto_detalles.estado='I'
                proyecto_detalles.save()
            listaProyecto= Proyecto.objects.all()                                                                                                                  #Si no se trata de la pagina de login quien
            return render(request, 'inicio.html', {'lista_proyectos':listaProyecto,'logueado':Usuarios.objects.get(id=request.POST['login'])})                      #lo llamo? Entonces no verifica absolutamente
                                                                                                                                    #nada y muestra la pagina solicitada

#La clase RegistrarUsuario se encarga de crear un nuevo usuario
class RegistrarUsuario(TemplateView):
    def post(self, request, *args, **kwargs):                           #Devuelve la pagina en donde se encuentra el formulario
        usuario_logueado= Usuarios.objects.get(id= request.POST['login'])   #Obtiene el objeto usuario logueado
        permisos= usuario_logueado.permiso.all()                                  #Los permisos del usuario
        tiene_permiso= False
        for i in permisos:
            if i.crear_usuario:
                tiene_permiso=True
                break
        if tiene_permiso:
            return render(request, 'CrearUsuario.html', {'logueado':Usuarios.objects.get(id=request.POST['login'])})
        else:
            lista= Usuarios.objects.all()
            return render(request, 'Usuario.html', {'lista_usuarios': lista,'logueado':Usuarios.objects.get(id=request.POST['login']), 'error':'No puedes realizar esta accion'})

#La clase ListarUsuario se encarga de la vista principal de Administracion de Usuarios
class ListarUsuario(TemplateView):
    def existe(self,char):                                              #Funcion que devuelve int y comprueba
        for i in Usuarios.objects.all():                                #si el nick que le pasamos ya existe en la
            if i.nick==char: return i.id                                #lista de usuarios
        return 0

    def post(self, request, *args, **kwargs):
        if 'user' in request.POST:                                      #La pagina quien lo llama es CrearUsuario.html?
            new_user= request.POST['user']                              #Comprueba absolutamente todos los datos
            new_password= request.POST['pass']
            if new_user and new_password:
                new_nombre= request.POST['nombre']                          #ingresados para averiguar si no se trata de
                new_apellido= request.POST['apellido']                      #un dato vacio el cual genera problemas al
                new_email= request.POST['email']                            #intentar guardar en la BD
                new_cedula= request.POST['cedula']
                if new_cedula=="": new_cedula=0
                existe_otro_usuario= ListarUsuario.existe(self, new_user)                #Si existe otro usuario con el mismo nick
                if existe_otro_usuario: return render(request, 'CrearUsuario.html', {'logueado':Usuarios.objects.get(id=request.POST['login']), 'error':'Nombre de usuario ya existe'})
                nuevo_usuario= Usuarios(nick= new_user, nombre= new_nombre, apellido= new_apellido, email= new_email, cedula= new_cedula, password= new_password) #insert into values
                nuevo_usuario.save()                                    #guardamos en la base de datos
                nuevo_usuario.permiso.add(Roles.objects.get(nombre= 'Sin Permisos'))    #Rol por defecto....
                nuevo_usuario.save()
            else:
                return render(request, 'CrearUsuario.html', {'logueado':Usuarios.objects.get(id=request.POST['login']), 'error':'Complete los campos obligatorios'})             #Si no logra grabar devuelve a la pagina anterior
        lista= Usuarios.objects.all()
        return render(request, 'Usuario.html', {'lista_usuarios':lista, 'logueado':Usuarios.objects.get(id=request.POST['login'])})     #enviamos al html un diccionario que tiene par 'key':lista_de_Usuarios_Existentes

#La clase Cambio Estado se encarga de una pagina de confirmacion de cambios
class CambioEstado(TemplateView):
    def post(self, request, *args, **kwargs):
        usuario_logueado= Usuarios.objects.get(id= request.POST['login'])   #Obtiene el objeto usuario logueado
        permisos= usuario_logueado.permiso.all()                                  #Los permisos del usuario
        tiene_permiso= False
        for i in permisos:
            if i.eliminar_usuario:
                tiene_permiso=True
                break
        if tiene_permiso:
            modif_codigo= request.POST['codigo']
            modificacion= Usuarios.objects.get(id=modif_codigo)
            modificacion.estado= False
            modificacion.save()
            return render(request, 'CambioEstado.html', {'logueado':Usuarios.objects.get(id=request.POST['login'])})
        else:
            lista= Usuarios.objects.all()
            return render(request, 'Usuario.html', {'lista_usuarios': lista,'logueado':Usuarios.objects.get(id=request.POST['login']), 'error':'No puedes realizar esta accion'})

#La clase Editar Usuario se encarga de la Edicion de Usuarios
class EditarUsuario(TemplateView):
    def post(self, request, *args, **kwargs):
        usuario_logueado= Usuarios.objects.get(id= request.POST['login'])   #Obtiene el objeto usuario logueado
        permisos= usuario_logueado.permiso.all()                                  #Los permisos del usuario
        tiene_permiso= False
        for i in permisos:
            if i.modificar_usuario:
                tiene_permiso=True
                break
        if tiene_permiso:                                               #Devuelve un formulario con lo campos
            modif_codigo= request.POST['codigo']                        #completados para modificar
            modificacion= Usuarios.objects.get(id= modif_codigo)
            return render(request, 'EditarUsuario.html', {'usuario':modificacion, 'logueado':Usuarios.objects.get(id=request.POST['login'])})
        else:
            lista= Usuarios.objects.all()
            return render(request, 'Usuario.html', {'lista_usuarios': lista,'logueado':Usuarios.objects.get(id=request.POST['login']), 'error':'No puedes realizar esta accion'})

#La clase EditarUsuarioConfirmar se encarga de una pagina de confirmacion de cambios
class EditarUsuarioConfirmar(TemplateView):
    def existe(self,char):                                              #Funcion que devuelve int y comprueba
        for i in Usuarios.objects.all():                                #si el nick que le pasamos ya existe en la
            if i.nick==char: return i.id                                #lista de usuarios
        return 0
    def post(self, request, *args, **kwargs): #Primero verifica si lo que le envio EditarUsuario.html son datos correctos
        modif_codigo= request.POST['codigo']
        modificacion= Usuarios.objects.get(id= modif_codigo)
        modificacion.nick= request.POST['user']
        modificacion.password= request.POST['pass']
        if modificacion.nick and modificacion.password:
            existe_otro_usuario= EditarUsuarioConfirmar.existe(self, modificacion.nick)
            if existe_otro_usuario and existe_otro_usuario!=modificacion.id:
                return render(request, 'EditarUsuario.html', {'usuario':modificacion,'logueado':Usuarios.objects.get(id=request.POST['login']), 'error':'Nombre de usuario ya existe'})
            modificacion.nombre= request.POST['nombre']
            if request.POST['cedula']=="": modificacion.cedula=0            #Control para que no intente grabar un campo vacio
            else: modificacion.cedula= request.POST['cedula']
            modificacion.apellido= request.POST['apellido']
            modificacion.email= request.POST['email']
            modificacion.save()
            return render(request, 'EditarUsuarioConfirmar.html', {'logueado':Usuarios.objects.get(id=request.POST['login'])})
        else:
            return render(request, 'EditarUsuario.html', {'usuario':modificacion, 'logueado':Usuarios.objects.get(id=request.POST['login']), 'error':'Complete los campos obligatorios'})

        #la clase MostrarUsuario se encarga de mostrar los datos de un usuario especificado
class MostrarUsuario(TemplateView):
    def post(self, request, *args, **kwargs):
        mostrar_codigo= request.POST['codigo']
        mostrar= Usuarios.objects.get(id= mostrar_codigo)
        return render(request, 'MostrarUsuario.html', {'usuario':mostrar, 'logueado':Usuarios.objects.get(id=request.POST['login'])})


#La clase CrearProyecto se encarga de crear un nuevo proyecto
class CrearProyecto(TemplateView):
    def post(self, request, *args, **kwargs):                           #Devuelve la pagina en donde se encuentra el formulario
        usuario_logueado= Usuarios.objects.get(id= request.POST['login'])   #Obtiene el objeto usuario logueado
        permisos= usuario_logueado.permiso.all()                                  #Los permisos del usuario
        tiene_permiso= False
        for i in permisos:
            if i.crear_proyecto:
                tiene_permiso=True
                break
        if tiene_permiso:
                listaUsuario= Usuarios.objects.all()
                return render(request, 'CrearProyecto.html',{'lista_usuarios':listaUsuario, 'logueado':Usuarios.objects.get(id=request.POST['login'])})
        else:
            lista= Proyecto.objects.all()
            return render(request, 'inicio.html', {'lista_proyectos': lista,'logueado':Usuarios.objects.get(id=request.POST['login']), 'error':'No puedes realizar esta accion'})


#La clase inicio es el que maneja el Menu Principal
class MenuProyecto(TemplateView):
    def post(self, request, *args, **kwargs):                           #En el metodo post en la condicion if

            listaFase= Fase.objects.all()                                                                                                                  #Si no se trata de la pagina de login quien
            return render(request, 'MenuProyecto.html', {'lista_fases':listaFase,'logueado':Usuarios.objects.get(id=request.POST['login'])})                      #lo llamo? Entonces no verifica absolutamente
            #return render(request, 'MenuProyecto.html', {'logueado':Usuarios.objects.get(id=request.POST['login'])})

class EliminarProyecto(TemplateView):
    def post(self, request, *args, **kwargs):
        usuario_logueado= Usuarios.objects.get(id= request.POST['login'])   #Obtiene el objeto usuario logueado
        permisos= usuario_logueado.permiso.all()                                  #Los permisos del usuario
        tiene_permiso= False
        for i in permisos:
            if i.eliminar_proyecto:
                tiene_permiso=True
                break
        if tiene_permiso:
            proyecto_actual= request.POST['proyecto']                       #id del proyecto
            proyecto_actual= Proyecto.objects.get(codigo= proyecto_actual)      #proyecto
            if proyecto_actual.estado=='F':
                proyecto_actual.activo=False
                proyecto_actual.save()
                return render(request, 'EliminarProyecto.html', {'logueado':Usuarios.objects.get(id=request.POST['login'])} )
            else:
                lista= Proyecto.objects.all()
                return render(request, 'inicio.html', {'lista_proyectos': lista,'logueado':Usuarios.objects.get(id=request.POST['login']), 'error':'Proyecto No Finalizado - No se puede eliminar'})
        else:
            lista= Proyecto.objects.all()
            return render(request, 'inicio.html', {'lista_proyectos': lista,'logueado':Usuarios.objects.get(id=request.POST['login']), 'error':'No puedes realizar esta accion'})






#Generacion de informe de Proyecto
class InformeProyecto(TemplateView):
    def post(self, request, *args, **kwargs):
        mostrar_proyecto= request.POST['proyecto']
        mostrar_proyecto= Proyecto.objects.get(codigo= mostrar_proyecto)
        if mostrar_proyecto.estado == 'I' or mostrar_proyecto.estado == 'F' :
            return render(request, 'InformeProyecto.html', {'proyecto':mostrar_proyecto, 'logueado':Usuarios.objects.get(id=request.POST['login'])})
        else:
            lista=Proyecto.objects.all()
            return render(request, 'inicio.html', {'lista_proyectos':lista, 'logueado':Usuarios.objects.get(id=request.POST['login']), 'error':'No puede mostrar proyecto NO-INICIADO'})


#Cambia el estado de un proyecto a Inicializado y completa los demas compos requeridos
class InicializarProyecto(TemplateView):
    def post(self, request, *args, **kwargs):
        proyecto= request.POST['proyecto']
        proyecto= Proyecto.objects.get(codigo=proyecto)
        if proyecto.estado == 'N':
            lista=Usuarios.objects.all()
            return render(request, 'InicializarProyecto.html', {'lista_usuarios':lista,'proyecto':proyecto, 'logueado':Usuarios.objects.get(id=request.POST['login'])})
        else:
            lista=Proyecto.objects.all()
            return render(request, 'inicio.html', {'lista_proyectos':lista, 'logueado':Usuarios.objects.get(id=request.POST['login']), 'error':'El Proyecto ya esta Inicializado'})


#Creacion de faces se realiza internamente con la cantidad inidicada en el proyecto, con la primera abierta y las demas no- inicializadas

