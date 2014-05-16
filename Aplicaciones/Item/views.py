from django.shortcuts import render
from .models import Item
from Aplicaciones.Usuario.models import Usuario
from Aplicaciones.Rol.models import Rol
from Aplicaciones.Proyecto.models import Proyecto
from Aplicaciones.Fase.models import Fase
from Aplicaciones.Fase.views import FaseView
from Aplicaciones.Tipo_de_Item.models import Tipo_de_Item
from Aplicaciones.Atributo.models import Atributo
from Aplicaciones.Tipo_de_Atributo.models import Tipo_de_Atributo


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
        if fase_actual.estado=='I':
            diccionario['lista_items']= Item.objects.filter(fase= fase_actual, activo=True)
            return render(request, self.template_name, diccionario)
        elif fase_actual.estado=='F':
            diccionario['error']= 'No puede ingresar a la fase - Fase Finalizada'
        else:
            diccionario['error']= 'Debe inicializar fase'
        diccionario['lista_fases']= Fase.objects.filter(proyecto=proyecto_actual)
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
        diccionario['lista_tipo_de_item']= Tipo_de_Item.objects.filter(proyecto= proyecto_actual, activo=True)
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
        diccionario= {}
        fase_actual= Fase.objects.get(id=request.POST['fase_item'])
        usuario_logueado= Usuario.objects.get(id= request.POST['login'])
        proyecto_actual= Proyecto.objects.get(id= request.POST['proyecto'])
        diccionario['logueado']= usuario_logueado
        diccionario['fase']= fase_actual
        diccionario['proyecto']= proyecto_actual
        new_nombre= request.POST['nombre_item']
        existe= Item.objects.filter(nombre= new_nombre, fase=fase_actual)
        if existe:
            diccionario['error']= 'Nombre de Item ya fue utilizado'
            diccionario['lista_tipo_de_item']= Tipo_de_Item.objects.filter(proyecto= proyecto_actual, activo=True)
            return render(request, super(CrearItemConfirm, self).template_name, diccionario)
        else:
            nuevo_item= Item()
            nuevo_item.nombre= new_nombre
            nuevo_item.costo=request.POST['costo_item']
            nuevo_item.prioridad=request.POST['prioridad_item']
            nuevo_item.descripcion= request.POST['descripcion_item']
            nuevo_item.fase=Fase.objects.get(id=request.POST['fase_item'])
            tipodeitem= Tipo_de_Item.objects.get(id=request.POST['tipo_item'], activo=True)
            tipodeitem.cantidad_de_item=tipodeitem.cantidad_de_item+1
            nuevo_item.tipodeItemAsociado= tipodeitem.nombre
            nuevo_item.tipo_de_item=tipodeitem
            nuevo_item.save()
            tipodeitem.save()
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
        tipodeitem= Tipo_de_Item.objects.get(nombre=item_actual.tipodeItemAsociado)
        tipodeitem.cantidad_de_item=tipodeitem.cantidad_de_item-1
        diccionario['logueado']= usuario_logueado
        diccionario['item']= item_actual
        diccionario['proyecto']= proyecto_actual
        diccionario['fase']= fase_actual

        if len(Rol.objects.filter(usuario=usuario_logueado, proyecto=proyecto_actual,eliminar_item=True, activo=True)):
            item_actual.activo= False
            tipodeitem.save()
            item_actual.save()
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


#Generacion de Informe del Item
class InformeItem(ItemView):
    template_name = 'Item/InformeItem.html'
    def post(self, request, *args, **kwargs):
        diccionario={}
        usuario_logueado= Usuario.objects.get(id= request.POST['login'])
        proyecto_actual= Proyecto.objects.get(id= request.POST['proyecto'])
        item_actual=Item.objects.get(id=request.POST['item'])
        fase_actual=Fase.objects.get(id=request.POST['fase'])
        diccionario['fase']=fase_actual
        diccionario['item']=item_actual
        diccionario['logueado']= usuario_logueado
        diccionario['proyecto']= proyecto_actual
        tipo_de_item_actual=Tipo_de_Item.objects.get(nombre=item_actual.tipodeItemAsociado)
        diccionario['lista_de_atributos']= Atributo.objects.filter(item=item_actual, activo= True)
        return render(request, self.template_name, diccionario)

class AprobarItem(ItemView):
    template_name = 'Item/AprobarItem.html'
    def post(self, request, *args, **kwargs):
        diccionario= {}
        fase_actual= Fase.objects.get(id=request.POST['fase'])
        usuario_logueado= Usuario.objects.get(id= request.POST['login'])
        proyecto_actual= Proyecto.objects.get(id= request.POST['proyecto'])
        item_actual=Item.objects.get(id=request.POST['item'])
        diccionario['logueado']= usuario_logueado
        diccionario['fase']= fase_actual
        diccionario['proyecto']= proyecto_actual
        existe_atributo_nulo= False
        lista_de_atributos= Atributo.objects.filter(item=item_actual, activo=True)
        for atributo_actual in lista_de_atributos:
                if atributo_actual.tipo_de_atributo_tipo == 'N' and not atributo_actual.tipo_numerico:
                    existe_atributo_nulo=True
                    break
                elif atributo_actual.tipo_de_atributo_tipo == 'T' and not atributo_actual.tipo_texto:
                    existe_atributo_nulo=True
                    break
                elif atributo_actual.tipo_de_atributo_tipo == 'B' and not atributo_actual.tipo_boolean:
                    existe_atributo_nulo=True
                    break
                elif atributo_actual.tipo_de_atributo_tipo == 'F' and not atributo_actual.tipo_fecha:
                    existe_atributo_nulo=True
                    break

        if item_actual.estado == 'D' and len(lista_de_atributos):
            if existe_atributo_nulo:
                diccionario['lista_items']= Item.objects.filter(fase= fase_actual, activo=True)
                diccionario['error']= 'Existe atributos sin completar.'
                return render(request, super(AprobarItem, self).template_name, diccionario)
            item_actual.estado='A'
            item_actual.version= item_actual.version + 1
            item_actual.save()
            diccionario['item']= item_actual
            return render(request, self.template_name, diccionario)
        elif not len(lista_de_atributos):
            diccionario['lista_items']= Item.objects.filter(fase= fase_actual, activo=True)
            diccionario['error']= 'Item sin atributos.'
            return render(request, super(AprobarItem, self).template_name, diccionario)
        elif item_actual.estado== 'A':
            diccionario['lista_items']= Item.objects.filter(fase= fase_actual, activo=True)
            diccionario['error']= 'Item ya esta Aprobado.'
            return render(request, super(AprobarItem, self).template_name, diccionario)
        elif item_actual.estado== 'B':
            diccionario['lista_items']= Item.objects.filter(fase= fase_actual, activo=True)
            diccionario['error']= 'Item Bloqueado. No puede realizar accion.'
            return render(request, super(AprobarItem, self).template_name, diccionario)