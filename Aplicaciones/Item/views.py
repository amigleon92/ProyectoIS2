from django.shortcuts import render
from .models import Item
from Aplicaciones.Usuario.models import Usuario
from Aplicaciones.Rol.models import Rol
from Aplicaciones.Proyecto.models import Proyecto
from Aplicaciones.Fase.models import Fase
from Aplicaciones.Fase.views import FaseView
from Aplicaciones.Tipo_de_Item.models import Tipo_de_Item
from Aplicaciones.Atributo.models import Atributo
from Aplicaciones.Relacion.models import Relacion
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
    def crear_copia(self, item_a_copiar):
        copia= Item(
            nombre= item_a_copiar.nombre,
            prioridad= item_a_copiar.prioridad,
            descripcion= item_a_copiar.descripcion,
            version= item_a_copiar.version,
            version_descripcion= item_a_copiar.version_descripcion,
            estado= item_a_copiar.estado,
            tipodeItemAsociado= item_a_copiar.tipodeItemAsociado,
            tipo_de_item= item_a_copiar.tipo_de_item,
            fase= item_a_copiar.fase,
            lineaBase= item_a_copiar.lineaBase,
            costo= item_a_copiar.costo,
            identificador= item_a_copiar.identificador,
        )
        copia.save()
        #Copiamos los atributos
        lista_atributos= Atributo.objects.filter(item= item_a_copiar, activo= True)
        for atributo in lista_atributos:
            nuevo_atributo= Atributo(
                nombre= atributo.nombre,
                descripcion= atributo.descripcion,
                tipo_de_atributo_nombre= atributo.tipo_de_atributo_nombre,
                tipo_de_atributo_tipo= atributo.tipo_de_atributo_tipo,
                tipo_numerico= atributo.tipo_numerico,
                tipo_texto= atributo.tipo_texto,
                tipo_boolean= atributo.tipo_boolean,
                tipo_fecha= atributo.tipo_fecha,
                item= copia,
            )
            nuevo_atributo.save()
        #Copiamos las relaciones en donde el item es padre o antecesor
        lista_relaciones= Relacion.objects.filter(item1= item_a_copiar, activo= True)
        for relacion in lista_relaciones:
            nueva_relacion= Relacion(
                nombre= relacion.nombre,
                item1= copia,
                item2= relacion.item2,
                tipo= relacion.tipo,
                activo= relacion.activo,
            )
            nueva_relacion.save()
        #Copiamos las relaciones en donde el item es hijo o sucesor
        lista_relaciones= Relacion.objects.filter(item2= item_a_copiar, activo= True)
        for relacion in lista_relaciones:
            nueva_relacion= Relacion(
                nombre= relacion.nombre,
                item1= relacion.item1,
                item2= copia,
                tipo= relacion.tipo,
                activo= relacion.activo,
            )
            nueva_relacion.save()
        return copia





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
            nuevo_item.version_descripcion='Item Creado'
            nuevo_item.save()
            #Identificador para las versiones anteriores
            nuevo_item.identificador= nuevo_item.id
            nuevo_item.save()
            #######################
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
        diccionario['logueado']= usuario_logueado
        diccionario['item']= item_actual
        diccionario['proyecto']= proyecto_actual
        diccionario['fase']= fase_actual

        if not item_actual.estado=='D':
            diccionario['lista_items']= Item.objects.filter(fase= fase_actual, activo=True)
            diccionario['error']= 'Item ya esta Aprobado/Bloqueado'
            return render(request, super(EliminarItem,self).template_name, diccionario)
        if len(Rol.objects.filter(usuario=usuario_logueado, proyecto=proyecto_actual,eliminar_item=True, activo=True)):

            #Guardamos la version anterior
            version_anterior= self.crear_copia(item_actual)
            version_anterior.activo= False
            version_anterior.save()
            #Actualizamos la version existente
            item_actual.version+=1
            item_actual.version_descripcion= 'Item eliminado'
            item_actual.activo= False
            item_actual.save()
            #Actualizamos cantidad de items
            tipodeitem.cantidad_de_item=tipodeitem.cantidad_de_item-1
            tipodeitem.save()
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
        #Guardamos la versrion anterior
        version_anterior= self.crear_copia(item_actual)
        version_anterior.activo= False
        version_anterior.save()
        #Actualizamos la version
        item_actual.nombre= request.POST['nombre_item']
        item_actual.costo=request.POST['costo_item']
        item_actual.prioridad=request.POST['prioridad_item']
        item_actual.descripcion= request.POST['descripcion_item']
        item_actual.fase=Fase.objects.get(id=request.POST['fase_item'])
        item_actual.version=item_actual.version + 1
        item_actual.version_descripcion= 'Item modificado'
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
            #Guardamos la version anterior
            version_anterior= self.crear_copia(item_actual)
            version_anterior.activo= False
            version_anterior.save()
            #Actualizamos
            item_actual.estado='A'
            item_actual.version= item_actual.version + 1
            item_actual.version_descripcion= 'Item Aprobado'
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

class ReversionarItem(ItemView):
    template_name = 'Item/ReversionarItem.html'
    def post(self, request, *args, **kwargs):
        diccionario= {}
        fase_actual= Fase.objects.get(id=request.POST['fase'])
        usuario_logueado= Usuario.objects.get(id= request.POST['login'])
        proyecto_actual= Proyecto.objects.get(id= request.POST['proyecto'])
        item_actual=Item.objects.get(id=request.POST['item'])
        diccionario['logueado']= usuario_logueado
        diccionario['fase']= fase_actual
        diccionario['proyecto']= proyecto_actual
        if not len(Rol.objects.filter(usuario=usuario_logueado, proyecto=proyecto_actual, reversionar_item=True, activo=True)):
            diccionario['lista_items']= Item.objects.filter(fase= fase_actual, activo=True)
            diccionario['error']= 'No posee permisos para realizar esta accion'
            return render(request, super(ReversionarItem, self).template_name, diccionario)
        else:
            diccionario['item']= item_actual
            diccionario['lista_de_items']= (Item.objects.filter(identificador= item_actual.identificador, activo= False )).order_by('version')
            return render(request, self.template_name, diccionario)

class RevivirItem(ItemView):
    template_name = 'Item/RevivirItem.html'
    def post(self, request, *args, **kwargs):
        diccionario= {}
        fase_actual= Fase.objects.get(id=request.POST['fase'])
        usuario_logueado= Usuario.objects.get(id= request.POST['login'])
        proyecto_actual= Proyecto.objects.get(id= request.POST['proyecto'])
        diccionario['logueado']= usuario_logueado
        diccionario['fase']= fase_actual
        diccionario['proyecto']= proyecto_actual
        if not len(Rol.objects.filter(usuario=usuario_logueado, proyecto=proyecto_actual, revivir_item=True, activo=True)):
            diccionario['lista_items']= Item.objects.filter(fase= fase_actual, activo=True)
            diccionario['error']= 'No posee permisos para realizar esta accion'
            return render(request, super(RevivirItem, self).template_name, diccionario)
        else:
            lista_eliminados= Item.objects.filter(activo= False, version_descripcion= 'Item eliminado', fase= fase_actual)
            diccionario['lista_eliminados']= lista_eliminados
            return render(request, self.template_name, diccionario)


class ReversionarItemConfirm(ItemView):
    template_name = 'Item/ReversionarItemConfirmar.html'
    def post(self, request, *args, **kwargs):
        diccionario= {}
        fase_actual= Fase.objects.get(id=request.POST['fase'])
        usuario_logueado= Usuario.objects.get(id= request.POST['login'])
        proyecto_actual= Proyecto.objects.get(id= request.POST['proyecto'])
        item_a_reversionar=Item.objects.get(id=request.POST['item_a_reversionar'])
        item_ultima_version= Item.objects.get(id= request.POST['item_actual'])
        diccionario['logueado']= usuario_logueado
        diccionario['fase']= fase_actual
        diccionario['proyecto']= proyecto_actual

        #Creamos una nueva version
        nueva_version= self.crear_copia(item_a_reversionar)
        nueva_version.version= item_ultima_version.version + 1
        nueva_version.save()
        if nueva_version.version_descripcion== 'Item eliminado_':
            nueva_version.version_descripcion= 'Item eliminado'
            nueva_version.activo= False
            nueva_version.save()
        else:
            nueva_version.version_descripcion= 'Item reversionado - Version ' + str(item_a_reversionar.version)
            nueva_version.save()
        #Actualizamos la version anterior
        item_ultima_version.activo= False
        item_ultima_version.save()
        return render(request, self.template_name, diccionario)

class RevivirItemConfirm(ItemView):
    template_name = 'Item/RevivirItemConfirmar.html'
    def post(self, request, *args, **kwargs):
        diccionario= {}
        fase_actual= Fase.objects.get(id=request.POST['fase'])
        usuario_logueado= Usuario.objects.get(id= request.POST['login'])
        proyecto_actual= Proyecto.objects.get(id= request.POST['proyecto'])
        diccionario['logueado']= usuario_logueado
        diccionario['fase']= fase_actual
        diccionario['proyecto']= proyecto_actual
        item_actual= Item.objects.get(id= request.POST['item'])
        #Creamos una nueva version
        nueva_version= self.crear_copia(item_actual)
        nueva_version.version+=1
        nueva_version.save()
        #Actualizamos la version
        item_actual.version_descripcion= 'Item eliminado_'
        item_actual.save()
        #Actualizamos los tipos de items
        tipodeitem= Tipo_de_Item.objects.get(nombre=item_actual.tipodeItemAsociado)
        tipodeitem.cantidad_de_item +=1
        tipodeitem.save()
        return render(request, self.template_name, diccionario)

class RevertirItem(ItemView):
    template_name = 'Item/RevertirItem.html'
    def post(self, request, *args, **kwargs):
        diccionario={}
        fase_actual= Fase.objects.get(id=request.POST['fase'])
        usuario_logueado= Usuario.objects.get(id= request.POST['login'])
        proyecto_actual= Proyecto.objects.get(id= request.POST['proyecto'])
        diccionario['logueado']= usuario_logueado
        diccionario['fase']= fase_actual
        diccionario['proyecto']= proyecto_actual
        #Permisos pertinentes?
        if not len(Rol.objects.filter(usuario=usuario_logueado, proyecto=proyecto_actual, revertir_item=True, activo=True)):
            diccionario['lista_items']= Item.objects.filter(fase= fase_actual, activo=True)
            diccionario['error']= 'No posee permisos para realizar esta accion'
            return render(request, super(RevertirItem, self).template_name, diccionario)

        item_actual= Item.objects.get(id= request.POST['item'])
        if item_actual.version== 1:
            diccionario['lista_items']= Item.objects.filter(fase= fase_actual, activo=True)
            diccionario['error']= 'Esta es la primera version del item - Nada que revertir'
            return render(request, super(RevertirItem, self).template_name, diccionario)

        item_version_anterior= Item.objects.get(identificador= item_actual.identificador, version= item_actual.version-1)

        #Creamos una nueva version
        nueva_version= self.crear_copia(item_version_anterior)
        nueva_version.version= item_actual.version + 1
        nueva_version.save()
        if nueva_version.version_descripcion== 'Item eliminado_':
            nueva_version.version_descripcion= 'Item eliminado'
            nueva_version.activo= False
            nueva_version.save()
        else:
            nueva_version.version_descripcion= 'Item revertido - Version ' + str(item_version_anterior.version)
            nueva_version.save()
        #Actualizamos la version anterior
        item_actual.activo= False
        item_actual.save()

        return render(request, self.template_name, diccionario)