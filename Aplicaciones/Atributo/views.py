from django.shortcuts import render
from .models import Atributo
from Aplicaciones.Usuario.models import Usuario
from Aplicaciones.Rol.models import Rol
from Aplicaciones.Proyecto.models import Proyecto
from Aplicaciones.Tipo_de_Item.models import Tipo_de_Item
from Aplicaciones.Tipo_de_Atributo.models import Tipo_de_Atributo
from Aplicaciones.Item.models import Item
from Aplicaciones.Item.views import ItemView
from Aplicaciones.Fase.models import Fase
from Aplicaciones.Solicitud_de_Cambios.models import Solicitud_de_Cambios, Voto
# Create your views here.

class AtributoView(ItemView):
    template_name = 'Atributo/Atributo.html'
    def post(self, request, *args, **kwargs):
        diccionario={}
        item_actual= Item.objects.get(id=request.POST['item'])
        usuario_logueado= Usuario.objects.get(id= request.POST['login'])
        proyecto_actual= Proyecto.objects.get(id= request.POST['proyecto'])
        fase_actual= Fase.objects.get(id=request.POST['fase'])
        diccionario['logueado']= usuario_logueado
        diccionario['proyecto']= proyecto_actual
        diccionario['item']=item_actual
        diccionario['fase']=fase_actual
        diccionario['lista_atributos']= (Atributo.objects.filter(item= item_actual, activo=True)).order_by('nombre')
        return render(request, self.template_name, diccionario)


# Agregar atributo
class AgregarAtributo(AtributoView):
    template_name = 'Atributo/AgregarAtributo.html'
    def post(self, request, *args, **kwargs):
        diccionario={}
        fase_actual= Fase.objects.get(id=request.POST['fase'])
        usuario_logueado= Usuario.objects.get(id= request.POST['login'])
        proyecto_actual= Proyecto.objects.get(id= request.POST['proyecto'])
        item_actual= Item.objects.get(id=request.POST['item'])
        diccionario['item']=item_actual
        diccionario['fase']=fase_actual
        diccionario['logueado']= usuario_logueado
        diccionario['proyecto']= proyecto_actual
        diccionario['lista_tipo_de_atributos']= Tipo_de_Atributo.objects.filter(tipo_de_item= item_actual.tipo_de_item, activo=True)
        diccionario[self.context_object_name]= Atributo.objects.filter(activo= True)
        if len(Rol.objects.filter(usuario=usuario_logueado, proyecto=proyecto_actual,agregar_atributo=True, activo=True)):
            if not item_actual.estado=='D':
                diccionario['lista_atributos']= (Atributo.objects.filter(item= item_actual, activo=True)).order_by('nombre')
                diccionario['error']= 'Item Aprobado o Bloqueado. No puedes realizar esta accion'
                return render(request, super(AgregarAtributo, self).template_name, diccionario)
            return render(request, self.template_name, diccionario)
        else:
            diccionario['lista_tipo_de_atributos']= Tipo_de_Atributo.objects.filter(tipo_de_item= item_actual.tipo_de_item, activo=True)
            diccionario['lista_atributos']= (Atributo.objects.filter(item= item_actual, activo=True)).order_by('nombre')
            diccionario['error']= 'No puedes realizar esta accion'
            return render(request, super(AgregarAtributo, self).template_name, diccionario,)



#crear tipo de atributo confirmacion
class AgregarAtributoConfirm(AgregarAtributo):
    template_name = 'Atributo/AgregarAtributoConfirm.html'
    def post(self, request, *args, **kwargs):
        diccionario= {}
        fase_actual= Fase.objects.get(id=request.POST['fase'])
        diccionario['fase']=fase_actual
        usuario_logueado= Usuario.objects.get(id= request.POST['login'])
        proyecto_actual= Proyecto.objects.get(id= request.POST['proyecto'])
        item_actual= Item.objects.get(id=request.POST['item'])
        diccionario['item']=item_actual
        diccionario['logueado']= usuario_logueado
        diccionario['proyecto']= proyecto_actual
        diccionario['lista_tipo_de_atributos']= Tipo_de_Atributo.objects.filter(tipo_de_item= item_actual.tipo_de_item, activo=True)
        new_nombre= request.POST['nombre_atributo']
        existe= Atributo.objects.filter(nombre= new_nombre, activo= True, item= item_actual)
        if existe:
            diccionario['error']= 'Nombre del atributo ya existe'
            return render(request, super(AgregarAtributoConfirm, self).template_name, diccionario)
        else:
            #Guardamos la version anterior
            version_anterior= self.crear_copia(item_actual)
            version_anterior.activo= False
            version_anterior.save()
            #Creamos un nuevo atributo
            nuevo_atributo= Atributo()
            nuevo_atributo.nombre= new_nombre
            nuevo_atributo.descripcion= request.POST['descripcion_atributo']
            tipo_de_atributo= Tipo_de_Atributo.objects.get(id=request.POST['tipo_de_atributo'])
            nuevo_atributo.tipo_de_atributo_nombre= tipo_de_atributo.nombre
            nuevo_atributo.tipo_de_atributo_tipo= tipo_de_atributo.tipo
            nuevo_atributo.item = item_actual
            nuevo_atributo.save()
            #Actualizamos la version
            item_actual.version+=1 #Nueva Version con el atributo creado
            item_actual.version_descripcion='Atributo ' + new_nombre + ' agregado'
            item_actual.save()
            return render(request, self.template_name, diccionario)


#eliminar atributo
class EliminarAtributo(AtributoView):
    template_name = 'Atributo/EliminarAtributo.html'
    def post(self, request, *args, **kwargs):
        diccionario={}
        fase_actual= Fase.objects.get(id=request.POST['fase'])
        diccionario['fase']=fase_actual
        item_actual= Item.objects.get(id=request.POST['item'])
        diccionario['item']=item_actual
        usuario_logueado= Usuario.objects.get(id= request.POST['login'])
        proyecto_actual= Proyecto.objects.get(id= request.POST['proyecto'])
        atributo_actual=Atributo.objects.get(id=request.POST['atributo'])
        diccionario['logueado']= usuario_logueado
        diccionario['atributo']= atributo_actual
        diccionario['proyecto']= proyecto_actual

        if len(Rol.objects.filter(usuario=usuario_logueado, proyecto=proyecto_actual,eliminar_atributo=True, activo=True)):
            if not item_actual.estado=='D':
                diccionario['lista_atributos']= (Atributo.objects.filter(item= item_actual, activo=True)).order_by('nombre')
                diccionario['error']= 'Item Aprobado o Bloqueado. No puedes realizar esta accion'
                return render(request, super(EliminarAtributo, self).template_name, diccionario)
            #Guardamos la version anterior
            version_anterior= self.crear_copia(item_actual)
            version_anterior.activo= False
            version_anterior.save()
            #Actualizamos la version
            item_actual.version+=1 #Atributo Eliminado NuevaVersion
            item_actual.version_descripcion= 'Atributo ' + atributo_actual.nombre + ' eliminado'
            item_actual.save()
            #Eliminamos el atributo
            atributo_actual.activo= False
            atributo_actual.save()
            return render(request, self.template_name, diccionario)
        else:
            diccionario['lista_tipo_de_atributos']= Tipo_de_Atributo.objects.filter(tipo_de_item= item_actual.tipo_de_item, activo=True)
            diccionario['lista_atributos']= (Atributo.objects.filter(item= item_actual, activo=True)).order_by('nombre')
            diccionario['error']= 'No puedes realizar esta accion'
            return render(request, super(EliminarAtributo,self).template_name, diccionario)


#Completar atributo
class CompletarAtributo(AtributoView):
    template_name = 'Atributo/CompletarAtributo.html'
    def post(self, request, *args, **kwargs):
        diccionario={}
        fase_actual= Fase.objects.get(id=request.POST['fase'])
        usuario_logueado= Usuario.objects.get(id= request.POST['login'])
        proyecto_actual= Proyecto.objects.get(id= request.POST['proyecto'])
        atributo_actual= Atributo.objects.get(id=request.POST['atributo'])
        item_actual= Item.objects.get(id=request.POST['item'])
        diccionario['fase']= fase_actual
        diccionario['logueado']= usuario_logueado
        diccionario['proyecto']= proyecto_actual
        diccionario['atributo']=atributo_actual
        diccionario['item']=item_actual
        if len(Rol.objects.filter(usuario=usuario_logueado, proyecto=proyecto_actual,completar_atributos=True, activo=True)):
            if item_actual.estado=='A':
                diccionario['lista_atributos']= (Atributo.objects.filter(item= item_actual, activo=True)).order_by('nombre')
                diccionario['error']= 'Item Aprobado. No puedes realizar esta accion'
                return render(request, super(CompletarAtributo, self).template_name, diccionario)
            elif item_actual.estado == 'B':
                #Si se definio ya los miembros del Comite.
                if len(Rol.objects.filter(nombre= 'Miembro del Comite', proyecto=proyecto_actual)):
                    diccionario['aviso']= 'Los cambios que realizara entraran en una Solicitud de Cambios'
                    return render(request, self.template_name, diccionario)
                else:
                    diccionario['lista_items']= (Item.objects.filter(fase= fase_actual, activo=True)).order_by('nombre')
                    diccionario['error']= 'Aun no se definio un Comite de Cambios - No puede realizar esta accion'
                    return render(request, super(CompletarAtributo, self).template_name, diccionario)
            else:
                #El item es desaprobado
                return render(request, self.template_name, diccionario)
        else:
            diccionario['lista_atributos']= (Atributo.objects.filter(item= item_actual, activo=True)).order_by('nombre')
            diccionario['error']= 'No puedes realizar esta accion'
            return render(request, super(CompletarAtributo, self).template_name, diccionario)

#completar atributo confirmar
class CompletarAtributoConfirm(CompletarAtributo):
    template_name = 'Atributo/CompletarAtributoConfirm.html'
    def post(self, request, *args, **kwargs):
        diccionario= {}
        item_actual= Item.objects.get(id=request.POST['item'])
        fase_actual= Fase.objects.get(id=request.POST['fase'])
        usuario_logueado= Usuario.objects.get(id= request.POST['login'])
        proyecto_actual= Proyecto.objects.get(id= request.POST['proyecto'])
        atributo_actual= Atributo.objects.get(id= request.POST['atributo'])
        diccionario['logueado']= usuario_logueado
        diccionario['item']=item_actual
        diccionario['fase']= fase_actual
        diccionario['proyecto']= proyecto_actual
        print item_actual.estado
        if item_actual.estado=='D':
            #Guardamos la version anterior
            version_anterior= self.crear_copia(item_actual)
            version_anterior.activo= False
            version_anterior.save()
            #Actualizamos la version
            item_actual.version+=1 #Atributo Completado NuevaVersion
            item_actual.version_descripcion='Atributo '+ atributo_actual.nombre + ' completado'
            item_actual.save()
            #Completamos Atributo
            if atributo_actual.tipo_de_atributo_tipo == 'N':
                atributo_actual.tipo_numerico= request.POST['tipo_numerico']
            elif atributo_actual.tipo_de_atributo_tipo == 'T':
                atributo_actual.tipo_texto= request.POST['tipo_texto']
            elif atributo_actual.tipo_de_atributo_tipo == 'B':
                if 'tipo_buleano' in request.POST: atributo_actual.tipo_boolean= True
                else: atributo_actual.tipo_boolean= False
            elif atributo_actual.tipo_de_atributo_tipo == 'F':
                atributo_actual.tipo_fecha=request.POST['tipo_fecha']
            atributo_actual.save()
        else:
            #Versiones de la solicitud
            version_desaprobada= item_actual
            version_desaprobada.estado= 'R'
            version_desaprobada.save()
            version_aprobada= self.crear_copia(item_actual)
            version_aprobada.version=item_actual.version + 1
            version_aprobada.version_descripcion= 'Atributo Agregado'
            version_aprobada.activo= False
            version_aprobada.save()
            #Completamos Atributo
            if atributo_actual.tipo_de_atributo_tipo == 'N':
                atributo_actual.tipo_numerico= request.POST['tipo_numerico']
            elif atributo_actual.tipo_de_atributo_tipo == 'T':
                atributo_actual.tipo_texto= request.POST['tipo_texto']
            elif atributo_actual.tipo_de_atributo_tipo == 'B':
                if 'tipo_buleano' in request.POST: atributo_actual.tipo_boolean= True
                else: atributo_actual.tipo_boolean= False
            elif atributo_actual.tipo_de_atributo_tipo == 'F':
                atributo_actual.tipo_fecha=request.POST['tipo_fecha']
            atributo_actual.item= version_desaprobada
            atributo_actual.save()
            #Generamos la Solicitud de Cambios
            nueva_solicitud= Solicitud_de_Cambios(
                descripcion= 'Editar Item ' + version_desaprobada.nombre,
                costo_del_impacto= 1000,
                proyecto= proyecto_actual,
                fase= fase_actual,
                item_sc_aprobado= version_aprobada,
                item_sc_desaprobado= version_desaprobada,
            )
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
        return render(request, self.template_name, diccionario)

