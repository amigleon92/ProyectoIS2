from django.shortcuts import render
from .models import Tipo_de_Item
from Aplicaciones.Usuario.models import Usuario
from Aplicaciones.Rol.models import Rol
from Aplicaciones.Proyecto.models import Proyecto
from Aplicaciones.Fase.views import FaseView
# Create your views here.

class TipoDeItemView(FaseView):
    template_name = 'Tipo_De_Item/TipoDeItem.html'
    def post(self, request, *args, **kwargs):
        diccionario={}
        usuario_logueado= Usuario.objects.get(id= request.POST['login'])
        proyecto_actual= Proyecto.objects.get(id= request.POST['proyecto'])
        diccionario['logueado']= usuario_logueado
        diccionario['proyecto']= proyecto_actual
        diccionario['lista_tipo_de_items']= Tipo_de_Item.objects.filter(proyecto= proyecto_actual, activo=True)
        return render(request, self.template_name, diccionario)



#crear tipo de item
class CrearTipoDeItem(TipoDeItemView):
    template_name = 'Tipo_De_Item/CrearTipoDeItem.html'
    def post(self, request, *args, **kwargs):
        diccionario={}
        usuario_logueado= Usuario.objects.get(id= request.POST['login'])
        proyecto_actual= Proyecto.objects.get(id= request.POST['proyecto'])
        diccionario['logueado']= usuario_logueado
        diccionario['proyecto']= proyecto_actual
        diccionario[self.context_object_name]= Tipo_de_Item.objects.filter(activo= True)
        if len(Rol.objects.filter(usuario=usuario_logueado, proyecto=proyecto_actual,crear_tipodeitem=True, activo=True)):

            del diccionario[self.context_object_name]
            return render(request, self.template_name, diccionario)
        else:
            diccionario['lista_tipo_de_items']= Tipo_de_Item.objects.filter(proyecto= proyecto_actual, activo=True)
            diccionario['error']= 'No puedes realizar esta accion'
            return render(request, super(CrearTipoDeItem, self).template_name, diccionario)



#crear tipo de atributo confirmacion
class CrearTipoDeItemConfirm(CrearTipoDeItem):
    template_name = 'Tipo_De_Item/CrearTipoDeItemConfirm.html'
    def post(self, request, *args, **kwargs):
        diccionario= {}
        usuario_logueado= Usuario.objects.get(id= request.POST['login'])
        proyecto_actual= Proyecto.objects.get(id= request.POST['proyecto'])
        diccionario['logueado']= usuario_logueado
        diccionario['proyecto']= proyecto_actual
        new_nombre= request.POST['nombre_tipo_de_item']
        existe= Tipo_de_Item.objects.filter(nombre= new_nombre)
        if existe:
            diccionario['error']= 'Nombre de Tipo de Item ya existe'
            return render(request, super(CrearTipoDeItemConfirm, self).template_name, diccionario)
        else:
            nuevo_tipodeitem= Tipo_de_Item()
            nuevo_tipodeitem.nombre= new_nombre
            nuevo_tipodeitem.descripcion= request.POST['descripcion_tipo_de_item']
            nuevo_tipodeitem.proyecto=proyecto_actual
            nuevo_tipodeitem.save()
            return render(request, self.template_name, diccionario)

class EliminarTipoDeItem(TipoDeItemView):
    template_name = 'Tipo_De_Item/EliminarTipoDeItem.html'
    def post(self, request, *args, **kwargs):
        diccionario={}
        usuario_logueado= Usuario.objects.get(id= request.POST['login'])
        proyecto_actual= Proyecto.objects.get(id= request.POST['proyecto'])
        tipo_de_item_actual=Tipo_de_Item.objects.get(id=request.POST['tipo_de_item'])
        diccionario['logueado']= usuario_logueado
        diccionario['tipo_de_item']= tipo_de_item_actual
        diccionario['proyecto']= proyecto_actual
        if len(Rol.objects.filter(usuario=usuario_logueado, proyecto=proyecto_actual,eliminar_tipodeitem=True, activo=True)):
            if tipo_de_item_actual.cantidad_de_item == 0:
                tipo_de_item_actual.activo= False
                tipo_de_item_actual.save()
                return render(request, self.template_name, diccionario)
            else:
                diccionario['lista_tipo_de_items']= Tipo_de_Item.objects.filter(proyecto= proyecto_actual, activo=True)
                diccionario['error']= 'Tipo de Item asociado a item, no puede realizar esta accion'
                return render(request, super(EliminarTipoDeItem, self).template_name, diccionario)
        else:
            diccionario['lista_tipo_de_items']= Tipo_de_Item.objects.filter(proyecto= proyecto_actual, activo=True)
            diccionario['error']= 'No puedes realizar esta accion'
            return render(request, super(EliminarTipoDeItem,self).template_name, diccionario)



#editar tipo de Item
class EditarTipoDeItem(TipoDeItemView):
    template_name = 'Tipo_De_Item/EditarTipoDeItem.html'
    def post(self, request, *args, **kwargs):
        diccionario={}
        usuario_logueado= Usuario.objects.get(id= request.POST['login'])
        proyecto_actual= Proyecto.objects.get(id= request.POST['proyecto'])
        tipo_de_item_actual=Tipo_de_Item.objects.get(id=request.POST['tipo_de_item'])
        diccionario['tipo_de_item']=tipo_de_item_actual
        diccionario['logueado']= usuario_logueado
        diccionario['proyecto']= proyecto_actual
        diccionario[self.context_object_name]= Tipo_de_Item.objects.filter(activo= True)
        if len(Rol.objects.filter(usuario=usuario_logueado, proyecto=proyecto_actual,modificar_tipodeitem=True, activo=True)):
            if tipo_de_item_actual.cantidad_de_item == 0:
                del diccionario[self.context_object_name]
                return render(request, self.template_name, diccionario)
            else:
                diccionario['lista_tipo_de_items']= Tipo_de_Item.objects.filter(proyecto= proyecto_actual, activo=True)
                diccionario['error']= 'Tipo de Item asociado a item, no puede realizar esta accion'
                return render(request, super(EditarTipoDeItem, self).template_name, diccionario)
        else:
            diccionario['lista_tipo_de_items']= Tipo_de_Item.objects.filter(proyecto= proyecto_actual, activo=True)
            diccionario['error']= 'No puedes realizar esta accion'
            return render(request, super(EditarTipoDeItem, self).template_name, diccionario)




#editar item confirmacion
class EditarTipoDeItemConfirm(EditarTipoDeItem):
    template_name =  'Tipo_De_Item/EditarTipoDeItemConfirm.html'
    def post(self, request, *args, **kwargs):
        diccionario= {}
        usuario_logueado= Usuario.objects.get(id= request.POST['login'])
        proyecto_actual= Proyecto.objects.get(id= request.POST['proyecto'])
        tipo_de_item_actual=Tipo_de_Item.objects.get(id=request.POST['tipo_de_item'])
        diccionario['logueado']= usuario_logueado
        diccionario['proyecto']= proyecto_actual
        new_nombre= request.POST['nombre_tipo_de_item']
        tipo_de_item_actual.nombre= new_nombre
        tipo_de_item_actual.descripcion=request.POST['descripcion_tipo_de_item']
        tipo_de_item_actual.save()
        diccionario['tipo_de_item']= tipo_de_item_actual
        return render(request, self.template_name, diccionario)


