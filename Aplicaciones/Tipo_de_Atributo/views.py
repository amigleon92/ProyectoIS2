from django.shortcuts import render
from .models import Tipo_de_Atributo
from Aplicaciones.Usuario.models import Usuario
from Aplicaciones.Rol.models import Rol
from Aplicaciones.Proyecto.models import Proyecto
from Aplicaciones.Fase.views import FaseView
from Aplicaciones.Tipo_de_Item.models import Tipo_de_Item
# Create your views here.

class TipoDeAtributoView(FaseView):
    template_name = 'Tipo_de_Atributo/TipoDeAtributo.html'
    def post(self, request, *args, **kwargs):
        diccionario={}
        tipo_de_item_actual= Tipo_de_Item.objects.get(id=request.POST['tipo_de_item'])
        usuario_logueado= Usuario.objects.get(id= request.POST['login'])
        proyecto_actual= Proyecto.objects.get(id= request.POST['proyecto'])
        diccionario['logueado']= usuario_logueado
        diccionario['proyecto']= proyecto_actual
        diccionario['tipo_de_item']=tipo_de_item_actual
        diccionario['lista_tipo_de_atributos']= Tipo_de_Atributo.objects.filter(tipo_de_item= tipo_de_item_actual, activo=True)
        return render(request, self.template_name, diccionario)

#crea tipo de atributo
class CrearTipoDeAtributo(TipoDeAtributoView):
    template_name = 'Tipo_de_Atributo/CrearTipoDeAtributo.html'
    def post(self, request, *args, **kwargs):
        diccionario={}
        tipo_de_item_actual= Tipo_de_Item.objects.get(id=request.POST['tipo_de_item'])
        usuario_logueado= Usuario.objects.get(id= request.POST['login'])
        proyecto_actual= Proyecto.objects.get(id= request.POST['proyecto'])
        diccionario['logueado']= usuario_logueado
        diccionario['proyecto']= proyecto_actual
        diccionario['tipo_de_item']=tipo_de_item_actual
        diccionario[self.context_object_name]= Tipo_de_Atributo.objects.filter(activo= True)
        if len(Rol.objects.filter(usuario=usuario_logueado, proyecto=proyecto_actual,crear_tipodeatributo=True, activo=True)):
            del diccionario[self.context_object_name]
            return render(request, self.template_name, diccionario)
        else:
            diccionario['lista_tipo_de_atributos']= Tipo_de_Atributo.objects.filter(tipo_de_item= tipo_de_item_actual, activo=True)
            diccionario['error']= 'No puedes realizar esta accion'
            return render(request, super(CrearTipoDeAtributo, self).template_name, diccionario)



#crear tipo de atributo confirmacion
class CrearTipoDeAtributoConfirm(CrearTipoDeAtributo):
    template_name = 'Tipo_de_Atributo/CrearTipoDeAtributoConfirm.html'
    def post(self, request, *args, **kwargs):
        diccionario= {}
        tipo_de_item_actual= Tipo_de_Item.objects.get(id=request.POST['tipo_de_item'])
        usuario_logueado= Usuario.objects.get(id= request.POST['login'])
        proyecto_actual= Proyecto.objects.get(id= request.POST['proyecto'])
        diccionario['logueado']= usuario_logueado
        diccionario['proyecto']= proyecto_actual
        diccionario['tipo_de_item']=tipo_de_item_actual
        new_nombre= request.POST['nombre_tipo_de_atributo']
        existe= Tipo_de_Atributo.objects.filter(nombre= new_nombre)
        if existe:
            diccionario['error']= 'Nombre de Tipo de Atributo ya existe'
            return render(request, super(CrearTipoDeAtributoConfirm, self).template_name, diccionario)
        else:
            nuevo_tipodeatributo= Tipo_de_Atributo()
            nuevo_tipodeatributo.nombre= new_nombre
            nuevo_tipodeatributo.tipo= request.POST['tipo_tipo_de_atributo']
            nuevo_tipodeatributo.tipo_de_item=tipo_de_item_actual
            nuevo_tipodeatributo.save()
            return render(request, self.template_name, diccionario)


#Eliminar Item
class EliminarTipoDeAtributo(TipoDeAtributoView):
    template_name = 'Tipo_de_Atributo/EliminarTipoDeAtributo.html'
    def post(self, request, *args, **kwargs):
        diccionario={}
        tipo_de_item_actual= Tipo_de_Item.objects.get(id=request.POST['tipo_de_item'])
        usuario_logueado= Usuario.objects.get(id= request.POST['login'])
        proyecto_actual= Proyecto.objects.get(id= request.POST['proyecto'])
        tipo_de_atributo_actual=Tipo_de_Atributo.objects.get(id=request.POST['tipo_de_atributo'])
        diccionario['logueado']= usuario_logueado
        diccionario['tipo_de_atributo']= tipo_de_atributo_actual
        diccionario['proyecto']= proyecto_actual
        diccionario['tipo_de_item']=tipo_de_item_actual
        if len(Rol.objects.filter(usuario=usuario_logueado, proyecto=proyecto_actual, eliminar_tipodeatributo=True, activo=True)):
            tipo_de_atributo_actual.activo= False
            tipo_de_atributo_actual.save()
            return render(request, self.template_name, diccionario)
        else:
            diccionario['lista_tipo_de_atributos']= Tipo_de_Atributo.objects.filter(tipo_de_item= tipo_de_item_actual, activo=True)
            diccionario['error']= 'No puedes realizar esta accion'
            return render(request, super(EliminarTipoDeAtributo,self).template_name, diccionario)

