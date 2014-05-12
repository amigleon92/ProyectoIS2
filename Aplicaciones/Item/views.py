from django.shortcuts import render
from .models import Item
from Aplicaciones.Usuario.models import Usuario
from Aplicaciones.Rol.models import Rol
from Aplicaciones.Proyecto.models import Proyecto
from Aplicaciones.Fase.models import Fase
from Aplicaciones.Fase.views import FaseView
# Create your views here.
#Lista de Fases correspondientes al Proyecto dentro
class ItemView(FaseView):
    template_name = 'Item/Item.html'
    def post(self, request, *args, **kwargs):
        diccionario={}
        usuario_logueado= Usuario.objects.get(id= request.POST['login'])
        proyecto_actual= Proyecto.objects.get(id= request.POST['proyecto'])
        fase_actual= Fase.objects.get(id=request.POST['fase'])
        diccionario['logueado']= usuario_logueado
        diccionario['proyecto']= proyecto_actual
        diccionario['fase']=fase_actual
        if not fase_actual.estado=='N':
            diccionario['lista_items']= Item.objects.filter(fase= fase_actual, activo=True)
            return render(request, self.template_name, diccionario)
        else:
            diccionario['lista_fases']= Fase.objects.filter(activo= True)
            diccionario['error']= 'Debe inicializar fase'
            return render(request, super(ItemView, self).template_name, diccionario)






#Crear Item
class CrearItem(ItemView):
    template_name = 'Item/CrearItem.html'
    def post(self, request, *args, **kwargs):
        diccionario={}
        fase_actual= Fase.objects.get(id=request.POST['fase'])
        usuario_logueado= Usuario.objects.get(id= request.POST['login'])
        proyecto_actual= Proyecto.objects.get(id= request.POST['proyecto'])
        diccionario['logueado']= usuario_logueado
        diccionario['fase']= fase_actual
        diccionario['proyecto']= proyecto_actual
        diccionario[self.context_object_name]= Item.objects.filter(activo= True)
        if len(Rol.objects.filter(usuario=usuario_logueado, proyecto=proyecto_actual,crear_item=True, activo=True)):

            del diccionario[self.context_object_name]
            return render(request, self.template_name, diccionario)
        else:
            diccionario['lista_items']= Item.objects.filter(fase= fase_actual, activo=True)
            diccionario['error']= 'No puedes realizar esta accion'
            return render(request, super(CrearItem, self).template_name, diccionario)




#crear item confirmacion
class CrearItemConfirm(CrearItem):
    template_name = 'Item/CrearItemConfirm.html'
    def post(self, request, *args, **kwargs):
        print('hola 1')
        diccionario= {}
        fase_actual= Fase.objects.get(id=request.POST['fase_item'])
        usuario_logueado= Usuario.objects.get(id= request.POST['login'])
        proyecto_actual= Proyecto.objects.get(id= request.POST['proyecto'])
        diccionario['logueado']= usuario_logueado
        diccionario['fase']= fase_actual
        diccionario['proyecto']= proyecto_actual
        new_nombre= request.POST['nombre_item']
        existe= Item.objects.filter(nombre= new_nombre)
        if existe:
           #diccionario['lista_usuarios']= Usuario.objects.filter(estado= True)
            diccionario['error']= 'Nombre de Item ya existe'
            return render(request, super(CrearItemConfirm, self).template_name, diccionario)
        else:
            print('hola 2')
            nuevo_item= Item()
            nuevo_item.nombre= new_nombre
            nuevo_item.costo=request.POST['costo_item']
            nuevo_item.prioridad=request.POST['prioridad_item']
            nuevo_item.descripcion= request.POST['descripcion_item']
            nuevo_item.fase=Fase.objects.get(id=request.POST['fase_item'])
            print('hola 3')
            nuevo_item.save()
            print('hola 4')
            return render(request, self.template_name, diccionario)



#Eliminar Item
class EliminarItem(ItemView):
    template_name = 'Item/EliminarItem.html'
    def post(self, request, *args, **kwargs):
        diccionario={}
        fase_actual= Fase.objects.get(id=request.POST['fase'])
        usuario_logueado= Usuario.objects.get(id= request.POST['login'])
        proyecto_actual= Proyecto.objects.get(id= request.POST['proyecto'])
        item_actual=Item.objects.get(id=request.POST['item'])
        diccionario['logueado']= usuario_logueado
        diccionario['item']= item_actual
        diccionario['proyecto']= proyecto_actual
        diccionario['fase']= fase_actual
        #diccionario[self.context_object_name]= Proyecto.objects.filter(activo= True)

        if len(Rol.objects.filter(usuario=usuario_logueado, proyecto=proyecto_actual,eliminar_item=True, activo=True)):
            item_actual.activo= False
            item_actual.save()
            #del diccionario[self.context_object_name]  #No hace falta enviar la lista de proyectos
            return render(request, self.template_name, diccionario)
        else:
            diccionario['lista_items']= Item.objects.filter(fase= fase_actual, activo=True)
            diccionario['error']= 'No puedes realizar esta accion'
            return render(request, super(EliminarItem,self).template_name, diccionario)




#editar Item
class EditarItem(ItemView):
    template_name = 'Item/EditarItem.html'
    def post(self, request, *args, **kwargs):
        diccionario={}
        fase_actual= Fase.objects.get(id=request.POST['fase'])
        usuario_logueado= Usuario.objects.get(id= request.POST['login'])
        proyecto_actual= Proyecto.objects.get(id= request.POST['proyecto'])
        item_actual=Item.objects.get(id=request.POST['item'])
        diccionario['item']=item_actual
        diccionario['logueado']= usuario_logueado
        diccionario['fase']= fase_actual
        diccionario['proyecto']= proyecto_actual
        diccionario[self.context_object_name]= Item.objects.filter(activo= True)
        if len(Rol.objects.filter(usuario=usuario_logueado, proyecto=proyecto_actual,editar_item=True, activo=True)):
            del diccionario[self.context_object_name]
            return render(request, self.template_name, diccionario)
        else:
            diccionario['lista_items']= Item.objects.filter(fase= fase_actual, activo=True)
            diccionario['error']= 'No puedes realizar esta accion'
            return render(request, super(EditarItem, self).template_name, diccionario)




#editar item confirmacion
class EditarItemConfirm(CrearItem):
    template_name = 'Item/EditarItemConfirm.html'
    def post(self, request, *args, **kwargs):
        diccionario= {}
        fase_actual= Fase.objects.get(id=request.POST['fase_item'])
        usuario_logueado= Usuario.objects.get(id= request.POST['login'])
        proyecto_actual= Proyecto.objects.get(id= request.POST['proyecto'])
        item_actual=Item.objects.get(id=request.POST['item'])

        diccionario['logueado']= usuario_logueado
        diccionario['fase']= fase_actual
        diccionario['proyecto']= proyecto_actual
        new_nombre= request.POST['nombre_item']
        item_actual.nombre= new_nombre
        item_actual.costo=request.POST['costo_item']
        item_actual.prioridad=request.POST['prioridad_item']
        item_actual.descripcion= request.POST['descripcion_item']
        item_actual.fase=Fase.objects.get(id=request.POST['fase_item'])
        item_actual.version=item_actual.version + 1
        item_actual.save()
        diccionario['item']= item_actual
        return render(request, self.template_name, diccionario)


