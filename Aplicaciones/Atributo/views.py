from django.shortcuts import render
from .models import Atributo
from Aplicaciones.Usuario.models import Usuario
from Aplicaciones.Rol.models import Rol
from Aplicaciones.Proyecto.models import Proyecto
from Aplicaciones.Tipo_de_Item.models import Tipo_de_Item
from Aplicaciones.Tipo_de_Item.views import TipoDeItemView
from Aplicaciones.Tipo_de_Atributo.models import Tipo_de_Atributo
# Create your views here.

class AtributoView(TipoDeItemView):
    template_name = 'Atributo/Atributo.html'
    def post(self, request, *args, **kwargs):
        diccionario={}
        usuario_logueado= Usuario.objects.get(id= request.POST['login'])
        proyecto_actual= Proyecto.objects.get(id= request.POST['proyecto'])
        tipo_de_item_actual= Tipo_de_Item.objects.get(id= request.POST['tipo_de_item'])
        diccionario['logueado']= usuario_logueado
        diccionario['proyecto']= proyecto_actual
        diccionario['tipo_de_item']=tipo_de_item_actual
        diccionario['lista_atributos']= Atributo.objects.filter(tipodeitem= tipo_de_item_actual, activo=True)

        return render(request, self.template_name, diccionario)


# Agregar atributo
class AgregarAtributo(AtributoView):
    template_name = 'Atributo/AgregarAtributo.html'
    def post(self, request, *args, **kwargs):
        diccionario={}
        usuario_logueado= Usuario.objects.get(id= request.POST['login'])
        proyecto_actual= Proyecto.objects.get(id= request.POST['proyecto'])
        tipo_de_item_actual= Tipo_de_Item.objects.get(id= request.POST['tipo_de_item'])
        diccionario['logueado']= usuario_logueado
        diccionario['proyecto']= proyecto_actual
        diccionario['tipo_de_item']=tipo_de_item_actual
        diccionario['lista_tipo_de_atributos']= Tipo_de_Atributo.objects.filter(proyecto= proyecto_actual, activo=True)
        diccionario[self.context_object_name]= Atributo.objects.filter(activo= True)
        if len(Rol.objects.filter(usuario=usuario_logueado, proyecto=proyecto_actual,agregar_atributo=True, activo=True)):


            print(diccionario['lista_tipo_de_atributos'])
            return render(request, self.template_name, diccionario)
        else:
            diccionario['lista_atributos']= Atributo.objects.filter(tipodeitem= tipo_de_item_actual, activo=True)
            diccionario['error']= 'No puedes realizar esta accion'
            return render(request, super(AgregarAtributo, self).template_name, diccionario,)



#crear tipo de atributo confirmacion
class AgregarAtributoConfirm(AgregarAtributo):
    template_name = 'Atributo/AgregarAtributoConfirm.html'
    def post(self, request, *args, **kwargs):
        diccionario= {}
        usuario_logueado= Usuario.objects.get(id= request.POST['login'])
        proyecto_actual= Proyecto.objects.get(id= request.POST['proyecto'])
        tipo_de_item_actual= Tipo_de_Item.objects.get(id= request.POST['tipo_de_item'])
        diccionario['logueado']= usuario_logueado
        diccionario['proyecto']= proyecto_actual
        diccionario['tipo_de_item']=tipo_de_item_actual
        new_nombre= request.POST['nombre_atributo']
        tipo_de_atributo= Tipo_de_Atributo.objects.filter(id=request.POST['tipo_de_atributo'])
        existe= Atributo.objects.filter(nombre= new_nombre)
        if existe:
           #diccionario['lista_usuarios']= Usuario.objects.filter(estado= True)
            diccionario['error']= 'Nombre del atributo ya existe'
            return render(request, super(AgregarAtributoConfirm, self).template_name, diccionario)
        else:
            nuevo_atributo= Atributo()
            nuevo_atributo.nombre= new_nombre
            nuevo_atributo.descripcion= request.POST['descripcion_atributo']
            nuevo_atributo.tipo=tipo_de_item_actual.nombre
            nuevo_atributo.tipodeitem=tipo_de_item_actual
            nuevo_atributo.save()
            print('hola 4 rena')
            return render(request, self.template_name, diccionario)


#eliminar atributo
class EliminarAtributo(AtributoView):
    template_name = 'Atributo/EliminarAtributo.html'
    def post(self, request, *args, **kwargs):
        diccionario={}
        usuario_logueado= Usuario.objects.get(id= request.POST['login'])
        proyecto_actual= Proyecto.objects.get(id= request.POST['proyecto'])
        tipo_de_item_actual=Tipo_de_Atributo.objects.get(id= request.POST['tipo_de_item'])
        atributo_actual=Atributo.objects.get(id=request.POST['atributo'])
        diccionario['logueado']= usuario_logueado
        diccionario['atributo']= atributo_actual
        diccionario['tipo_de_item']=tipo_de_item_actual
        diccionario['proyecto']= proyecto_actual

        if len(Rol.objects.filter(usuario=usuario_logueado, proyecto=proyecto_actual,eliminar_atributo=True, activo=True)):
            atributo_actual.activo= False
            atributo_actual.save()
            return render(request, self.template_name, diccionario)
        else:
            diccionario['lista_atributos']= Atributo.objects.filter(tipodeitem= tipo_de_item_actual, activo=True)
            diccionario['error']= 'No puedes realizar esta accion'
            return render(request, super(EliminarAtributo,self).template_name, diccionario)
