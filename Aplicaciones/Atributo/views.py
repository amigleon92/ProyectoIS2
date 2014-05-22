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
        diccionario['lista_atributos']= Atributo.objects.filter(item= item_actual, activo=True)
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
            #diccionario['lista_atributos']= Atributo.objects.filter(item= item_actual, activo=True)
            return render(request, self.template_name, diccionario)
        else:
            diccionario['lista_tipo_de_atributos']= Tipo_de_Atributo.objects.filter(tipo_de_item= item_actual.tipo_de_item, activo=True)
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
            if not fase_actual.estado == 'F':
                    return render(request, self.template_name, diccionario)
            else:
               diccionario['lista_atributos']= Atributo.objects.filter(item= item_actual, activo=True)
               diccionario['error']= 'Fase finalizada. No puedes realizar esta accion'
               return render(request, super(CompletarAtributo, self).template_name, diccionario)
        else:
            diccionario['lista_atributos']= Atributo.objects.filter(item= item_actual, activo=True)
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

        #Guardamos la version anterior
        version_anterior= Item(
            nombre= item_actual.nombre,
            prioridad= item_actual.prioridad,
            descripcion= item_actual.descripcion,
            version= item_actual.version,
            estado= item_actual.estado,
            tipodeItemAsociado= item_actual.tipodeItemAsociado,
            tipo_de_item= item_actual.tipo_de_item,
            fase= item_actual.fase,
            lineaBase= item_actual.lineaBase,
            costo= item_actual.costo,
            activo= False,
            identificador= item_actual.identificador,
            version_descripcion= item_actual.version_descripcion,
        )
        version_anterior.save()
        #modificar los atributos para que apunten a una nueva version
        lista_atributos= Atributo.objects.filter(item= item_actual, activo= True)
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
                item= version_anterior,
            )
            nuevo_atributo.save()
        item_actual.version+=1 #Atributo Eliminado NuevaVersion
        item_actual.version_descripcion='Atributo '+ atributo_actual.nombre + ' completado'
        item_actual.save()

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
        return render(request, self.template_name, diccionario)

