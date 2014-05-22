from django.shortcuts import render
from .models import LineaBase
from Aplicaciones.Usuario.models import Usuario
from Aplicaciones.Rol.models import Rol
from Aplicaciones.Proyecto.models import Proyecto
from Aplicaciones.Fase.models import Fase
from Aplicaciones.Item.models import Item
from Aplicaciones.Item.views import ItemView
from Aplicaciones.Relacion.models import Relacion

# Create your views here.
#Lista de Lineas Bases correspondientes a la Fase
class LineaBaseView(ItemView):
    template_name = 'Linea_Base/LineaBase.html'
    def post(self, request, *args, **kwargs):
        diccionario={}
        usuario_logueado= Usuario.objects.get(id= request.POST['login'])
        proyecto_actual= Proyecto.objects.get(id= request.POST['proyecto'])
        fase_actual= Fase.objects.get(id=request.POST['fase'])
        diccionario['logueado']= usuario_logueado
        diccionario['proyecto']= proyecto_actual
        diccionario['fase']=fase_actual
        diccionario['lista_linea_base']= LineaBase.objects.filter(fase=fase_actual, activo=True)
        #diccionario['lista_items']= Item.objects.filter(fase= fase_actual, activo=True)
        return render(request, self.template_name, diccionario)

#Crear linea base
class CrearLineaBase(LineaBaseView):
    template_name = 'Linea_Base/CrearLineaBase.html'
    def post(self, request, *args, **kwargs):
        diccionario={}
        fase_actual= Fase.objects.get(id=request.POST['fase'])
        usuario_logueado= Usuario.objects.get(id= request.POST['login'])
        proyecto_actual= Proyecto.objects.get(id= request.POST['proyecto'])
        diccionario['logueado']= usuario_logueado
        diccionario['fase']= fase_actual
        diccionario['proyecto']= proyecto_actual
        diccionario['lista_de_items']= Item.objects.filter(fase= fase_actual, activo=True, estado='A')
        diccionario[self.context_object_name]= Item.objects.filter(activo= True)
        print('estoy aqui')
        if len(Rol.objects.filter(usuario=usuario_logueado, proyecto=proyecto_actual,crear_lineabase=True, activo=True)):

            del diccionario[self.context_object_name]
            return render(request, self.template_name, diccionario)
        else:
            diccionario['lista_linea_base']= LineaBase.objects.filter(fase= fase_actual, activo=True)
            diccionario['error']= 'No puedes realizar esta accion'
            return render(request, super(CrearLineaBase, self).template_name, diccionario)




#crear linea base confirmacion
class CrearLineaBaseConfirm(CrearLineaBase):
    template_name = 'Linea_Base/CrearLineaBaseConfirm.html'
    def post(self, request, *args, **kwargs):
        diccionario= {}
        fase_actual= Fase.objects.get(id=request.POST['fase'])
        usuario_logueado= Usuario.objects.get(id= request.POST['login'])
        proyecto_actual= Proyecto.objects.get(id= request.POST['proyecto'])
        diccionario['logueado']= usuario_logueado
        diccionario['fase']= fase_actual
        diccionario['proyecto']= proyecto_actual
        new_nombre= request.POST['nombre_linea_base']
        existe= LineaBase.objects.filter(nombre= new_nombre, fase=fase_actual, activo= True)
        if existe:
            diccionario['error']= 'Nombre de Linea base ya existe'
            diccionario['lista_de_items']= Item.objects.filter(fase= fase_actual, activo=True, estado='A')
            return render(request, super(CrearLineaBaseConfirm, self).template_name, diccionario)
        else:
            items_en_linea_base=request.POST.getlist('items_en_linea_base[]')
            #comprobar si sus padres estan en LB
            for item_hijo in items_en_linea_base:
                relacion_padre_de_item_hijo=Relacion.objects.filter(item2=item_hijo, tipo='P/H', activo=True)
                if len(relacion_padre_de_item_hijo) and not relacion_padre_de_item_hijo[0].item1.estado =='B':
                    diccionario['error']= 'Padre/s de item/s debe/n de estar en Linea Base.'
                    diccionario['lista_de_items']= Item.objects.filter(fase= fase_actual, activo=True, estado='A')
                    return render(request, super(CrearLineaBaseConfirm, self).template_name, diccionario)
            nueva_lienea_base=LineaBase()
            nueva_lienea_base.nombre= new_nombre
            nueva_lienea_base.fase=fase_actual
            nueva_lienea_base.estado='C'
            nueva_lienea_base.save()
            for item in items_en_linea_base:
                item_actual= Item.objects.get(id=item)
                item_actual.lineaBase=nueva_lienea_base
                item_actual.estado='B'
                item_actual.save()
            return render(request, self.template_name, diccionario)

#mostrar items de linea base
class MostrarItems(LineaBaseView):
     template_name =  'Linea_Base/MostrarItems.html'
     def post(self, request, *args, **kwargs):
         diccionario={}
         linea_base_actual=LineaBase.objects.get(id=request.POST['linea_base'])
         fase_actual= Fase.objects.get(id=request.POST['fase'])
         usuario_logueado= Usuario.objects.get(id= request.POST['login'])
         proyecto_actual= Proyecto.objects.get(id= request.POST['proyecto'])
         diccionario['lista_de_items']= Item.objects.filter(lineaBase= linea_base_actual, activo= True)
         diccionario['fase']= fase_actual
         diccionario['logueado']= usuario_logueado
         diccionario['proyecto']= proyecto_actual
         diccionario['linea_base']=linea_base_actual
         return render(request, self.template_name, diccionario)
