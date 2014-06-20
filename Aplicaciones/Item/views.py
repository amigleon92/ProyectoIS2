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
from Aplicaciones.Solicitud_de_Cambios.models import Solicitud_de_Cambios, Voto


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
            diccionario['lista_items']= (Item.objects.filter(fase= fase_actual, activo=True)).order_by('nombre')
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
    def impacto(self, item_padre, costo):
        if not item_padre.activo: return costo          #Para items inactivos que tienen varios hijos...
        lista_relaciones_padre = Relacion.objects.filter(item1=item_padre, activo=True)
        for relacion_padre in lista_relaciones_padre:
            if len(Relacion.objects.filter(item1=relacion_padre.item2, activo=True)):
                costo=self.impacto(relacion_padre.item2, costo)
            if relacion_padre.item2.activo: costo=costo+relacion_padre.item2.costo        #Sumar solo si corresponde
        return costo

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
            diccionario['lista_items']= (Item.objects.filter(fase= fase_actual, activo=True)).order_by('nombre')
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
        relacion_donde_item_es_padre=Relacion.objects.filter(item1=item_actual, tipo='P/H', activo=True)
        if not item_actual.estado=='D':
            diccionario['lista_items']=(Item.objects.filter(fase= fase_actual, activo=True)).order_by('nombre')
            diccionario['error']= 'Item esta Aprobado, Bloqueado o en Revision. No puedes realizar esta accion'
            return render(request, super(EliminarItem,self).template_name, diccionario)
            #verificamos si el item es padre
        elif len(relacion_donde_item_es_padre):
            diccionario['lista_items']=(Item.objects.filter(fase= fase_actual, activo=True)).order_by('nombre')
            diccionario['error']= 'Este es un item Padre! no puedes dejar huerfanos.'
            return render(request, super(EliminarItem,self).template_name, diccionario)
            #verificamos si el item tiene relacion A/S
        elif len(Relacion.objects.filter(item1=item_actual, tipo='A/S', activo=True)) or len(Relacion.objects.filter(item2=item_actual, tipo='A/S', activo=True)):
            diccionario['lista_items']=(Item.objects.filter(fase= fase_actual, activo=True)).order_by('nombre')
            diccionario['error']= 'Item tiene Antecesor o Sucesor. La accion podria generar inconsistencia'
            return render(request, super(EliminarItem,self).template_name, diccionario)
        if len(Rol.objects.filter(usuario=usuario_logueado, proyecto=proyecto_actual,eliminar_item=True, activo=True)):
            #eliminamos la relacion donde el item es hijo
            relacion_donde_item_es_hijo=Relacion.objects.filter(item2=item_actual, tipo='P/H', activo=True)
            if len(relacion_donde_item_es_hijo):
                relacion_donde_item_es_hijo[0].activo=False
                relacion_donde_item_es_hijo[0].save()
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
            diccionario['lista_items']= (Item.objects.filter(fase= fase_actual, activo=True)).order_by('nombre')
            diccionario['error']= 'No puedes realizar esta accion'
            return render(request, super(EliminarItem, self).template_name, diccionario)




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
            if item_actual.estado == 'A':
                diccionario['lista_items']= (Item.objects.filter(fase= fase_actual, activo=True)).order_by('nombre')
                diccionario['error']= 'Item Aprobado. No puedes realizar esta accion'
                return render(request, super(EditarItem, self).template_name, diccionario)
            elif item_actual.estado == 'R':
                diccionario['lista_items']= (Item.objects.filter(fase= fase_actual, activo=True)).order_by('nombre')
                diccionario['error']= 'Item en Revision. No puedes realizar esta accion'
                return render(request, super(EditarItem, self).template_name, diccionario)
            elif item_actual.estado == 'B':
                #Si se definio ya los miembros del Comite.
                if len(Rol.objects.filter(nombre= 'Miembro del Comite', proyecto=proyecto_actual)):
                    diccionario['aviso']= 'Los cambios que realizara entraran en una Solicitud de Cambios'
                    return render(request, self.template_name, diccionario)
                else:
                    diccionario['lista_items']= (Item.objects.filter(fase= fase_actual, activo=True)).order_by('nombre')
                    diccionario['error']= 'Aun no se definio un Comite de Cambios - No puede realizar esta accion'
                    return render(request, super(EditarItem, self).template_name, diccionario)
            else:
                #El item es desaprobado
                return render(request, self.template_name, diccionario)
        else:
            diccionario['lista_items']= (Item.objects.filter(fase= fase_actual, activo=True)).order_by('nombre')
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
        if item_actual.estado=='D':
            #Guardamos la version anterior
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
        else:
            #Versiones de la solicitud
            version_desaprobada= item_actual
            version_desaprobada.estado= 'R'
            version_desaprobada.save()
            version_aprobada= self.crear_copia(item_actual)
            version_aprobada.nombre= request.POST['nombre_item']
            version_aprobada.costo=request.POST['costo_item']
            version_aprobada.prioridad=request.POST['prioridad_item']
            version_aprobada.descripcion= request.POST['descripcion_item']
            version_aprobada.fase=Fase.objects.get(id=request.POST['fase_item'])
            version_aprobada.version=item_actual.version + 1
            version_aprobada.version_descripcion= 'Item modificado'
            version_aprobada.activo= False
            version_aprobada.save()
            #Generamos la Solicitud de Cambios
            nueva_solicitud= Solicitud_de_Cambios(
                descripcion= 'Editar Item ' + version_desaprobada.nombre,
                costo_del_impacto= self.impacto(item_actual,0)+item_actual.costo,
                proyecto= proyecto_actual,
                fase= fase_actual,
                item_sc_aprobado= version_aprobada,
                item_sc_desaprobado= version_desaprobada,
                usuario= usuario_logueado
            )
            if version_aprobada.nombre != version_desaprobada.nombre:
                nueva_solicitud.descripcion += ' .Nombre modificado -> ' + version_aprobada.nombre
            if version_aprobada.prioridad != version_desaprobada.prioridad:
                nueva_solicitud.descripcion += ' .Prioridad modificada -> ' + version_aprobada.prioridad
            if version_aprobada.descripcion != version_desaprobada.descripcion:
                nueva_solicitud.descripcion += ' .Descripcion modificada -> ' + version_aprobada.descripcion
            if version_aprobada.costo != version_desaprobada.costo:
                nueva_solicitud.descripcion += ' .Costo modificado -> ' + version_aprobada.costo
            nueva_solicitud.save()
            #Generamos los votos
            for miembro in Rol.objects.filter(nombre= 'Miembro del Comite', proyecto= proyecto_actual, activo= True):
                nuevo_voto= Voto(
                    usuario= miembro.usuario,
                    solicitud_de_cambios= nueva_solicitud,
                )
                nuevo_voto.save()
            #Rompemos la Linea Base
            item_actual.lineaBase.estado= 'A'
            item_actual.lineaBase.save()
            #Todos los demas items de la linea base
            for i in Item.objects.filter(activo= True, lineaBase= item_actual.lineaBase):
                i.estado= 'R'
                i.save()
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
        relacion_donde_es_hijo= Relacion.objects.filter(item2=item_actual, tipo='P/H', activo=True)
        diccionario['logueado']= usuario_logueado
        diccionario['fase']= fase_actual
        diccionario['proyecto']= proyecto_actual
        existe_atributo_nulo= False
        if item_actual.estado == 'D':
            #verificamos si su padre esta aprobado
            if not (len(Relacion.objects.filter(item1=item_actual, activo=True)) or len(Relacion.objects.filter(item2=item_actual, activo=True))):
                diccionario['lista_items']= (Item.objects.filter(fase= fase_actual, activo=True)).order_by('nombre')
                diccionario['error']= 'El item no posee ningun tipo de relacion.'
                return render(request, super(AprobarItem, self).template_name, diccionario)
            elif len(relacion_donde_es_hijo) and relacion_donde_es_hijo[0].item1.estado == 'D':
                diccionario['lista_items']= (Item.objects.filter(fase= fase_actual, activo=True)).order_by('nombre')
                diccionario['error']= 'El padre del Item debe de estar aprobado.'
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
        elif item_actual.estado== 'A':
            diccionario['lista_items']= (Item.objects.filter(fase= fase_actual, activo=True)).order_by('nombre')
            diccionario['error']= 'Item ya esta Aprobado.'
            return render(request, super(AprobarItem, self).template_name, diccionario)
        elif item_actual.estado== 'B':
            diccionario['lista_items']= (Item.objects.filter(fase= fase_actual, activo=True)).order_by('nombre')
            diccionario['error']= 'Item Bloqueado. No puede realizar accion.'
            return render(request, super(AprobarItem, self).template_name, diccionario)
        elif item_actual.estado== 'R':
            diccionario['lista_items']= (Item.objects.filter(fase= fase_actual, activo=True)).order_by('nombre')
            diccionario['error']= 'Item en Revision. No puede realizar accion.'
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
            diccionario['lista_items']= (Item.objects.filter(fase= fase_actual, activo=True)).order_by('nombre')
            diccionario['error']= 'No posee permisos para realizar esta accion'
            return render(request, super(ReversionarItem, self).template_name, diccionario)
        else:
            if item_actual.estado=='B':
                diccionario['lista_items']= (Item.objects.filter(fase= fase_actual, activo=True)).order_by('nombre')
                diccionario['error']= 'Item Bloqueado. No puedes realizar esta accion'
                return render(request, super(ReversionarItem, self).template_name, diccionario)
            elif item_actual.estado=='R':
                diccionario['lista_items']= (Item.objects.filter(fase= fase_actual, activo=True)).order_by('nombre')
                diccionario['error']= 'Item en Revision. No puedes realizar esta accion'
                return render(request, super(ReversionarItem, self).template_name, diccionario)
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
            diccionario['lista_items']= (Item.objects.filter(fase= fase_actual, activo=True)).order_by('nombre')
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
        #Las relaciones actuales quedaran obsoletas
        lista_relaciones= Relacion.objects.filter(item1= item_ultima_version, activo= True)
        for i in lista_relaciones: i.activo= False
        lista_relaciones= Relacion.objects.filter(item2= item_ultima_version, activo= True)
        for i in lista_relaciones: i.activo= False
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
        nueva_version.version_descripcion= 'Item revivido ' + 'Version ' + str(item_actual.version)
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
            diccionario['lista_items']= (Item.objects.filter(fase= fase_actual, activo=True)).order_by('nombre')
            diccionario['error']= 'No posee permisos para realizar esta accion'
            return render(request, super(RevertirItem, self).template_name, diccionario)

        item_actual= Item.objects.get(id= request.POST['item'])
        if item_actual.version== 1:
            diccionario['lista_items']= (Item.objects.filter(fase= fase_actual, activo=True)).order_by('nombre')
            diccionario['error']= 'Esta es la primera version del item - Nada que revertir'
            return render(request, super(RevertirItem, self).template_name, diccionario)
        if item_actual.estado=='B':
                diccionario['lista_items']= (Item.objects.filter(fase= fase_actual, activo=True)).order_by('nombre')
                diccionario['error']= 'Item Bloqueado. No puedes realizar esta accion'
                return render(request, super(RevertirItem, self).template_name, diccionario)
        elif item_actual.estado=='R':
                diccionario['lista_items']= (Item.objects.filter(fase= fase_actual, activo=True)).order_by('nombre')
                diccionario['error']= 'Item en Revision. No puedes realizar esta accion'
                return render(request, super(RevertirItem, self).template_name, diccionario)
        item_version_anterior= Item.objects.get(identificador= item_actual.identificador, version= item_actual.version-1)
        #Las relaciones actuales quedaran obsoletas
        lista_relaciones= Relacion.objects.filter(item1= item_actual, activo= True)
        for i in lista_relaciones: i.activo= False
        lista_relaciones= Relacion.objects.filter(item2= item_actual, activo= True)
        for i in lista_relaciones: i.activo= False
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