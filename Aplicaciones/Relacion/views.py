from django.shortcuts import render
from .models import Relacion
from Aplicaciones.Item.views import ItemView
from Aplicaciones.Usuario.models import Usuario
from Aplicaciones.Proyecto.models import Proyecto
from Aplicaciones.Fase.models import Fase
from Aplicaciones.Item.models import Item
from Aplicaciones.Rol.models import Rol

# Create your views here.
#Lista de Relaciones correspondientes a la Fase
class RelacionView(ItemView):
    template_name = 'Relacion/Relacion.html'
    def post(self, request, *args, **kwargs):
        diccionario={}
        usuario_logueado= Usuario.objects.get(id= request.POST['login'])
        proyecto_actual= Proyecto.objects.get(id= request.POST['proyecto'])
        fase_actual= Fase.objects.get(id=request.POST['fase'])
        diccionario['fase']=fase_actual
        item_actual=Item.objects.get(id=request.POST['item'])
        diccionario['item']=item_actual
        diccionario['logueado']= usuario_logueado
        diccionario['proyecto']= proyecto_actual
        diccionario['lista_relaciones']= Relacion.objects.filter(item1=item_actual, activo=True)
        return render(request, self.template_name, diccionario)



#Establecer Relacion antecesor sucesor
class EstablecerRelacionAS(RelacionView):
    template_name = 'Relacion/EstablecerRelacionAS.html'
    def post(self, request, *args, **kwargs):
        diccionario={}
        usuario_logueado= Usuario.objects.get(id= request.POST['login'])
        proyecto_actual= Proyecto.objects.get(id= request.POST['proyecto'])
        fase_actual= Fase.objects.get(id=request.POST['fase'])
        diccionario['fase']=fase_actual
        item_actual=Item.objects.get(id=request.POST['item'])
        diccionario['item']=item_actual
        diccionario['logueado']= usuario_logueado
        diccionario['proyecto']= proyecto_actual
        lista_items=[]
        lista_fases= Fase.objects.filter(proyecto=proyecto_actual)
        for fase in lista_fases:
            if fase_actual.numeroSecuencia < fase.numeroSecuencia:
                lista_items_fase=Item.objects.filter(fase=fase)
                for item in lista_items_fase:
                    lista_items.append(item)
        diccionario['lista_items']=lista_items
        #diccionario[self.context_object_name]= Item.objects.filter(activo= True)
        if len(Rol.objects.filter(usuario=usuario_logueado, proyecto=proyecto_actual,establecer_relacion=True, activo=True)):
            if fase_actual.numeroSecuencia == proyecto_actual.numeroFase:
                diccionario['lista_relaciones']= Relacion.objects.filter(item1=item_actual, activo=True)
                diccionario['error']= 'No exite fase sucesora a la actual.'
                return render(request, super(EstablecerRelacionAS, self).template_name, diccionario)
            else:
                return render(request, self.template_name, diccionario)
        else:
            diccionario['lista_relaciones']= Relacion.objects.filter(item1=item_actual, activo=True)
            diccionario['error']= 'No puedes realizar esta accion'
            return render(request, super(EstablecerRelacionAS, self).template_name, diccionario)




#Establecer Relacion antecesor sucesor confirmar
class EstablecerRelacionASConfirm(EstablecerRelacionAS):
    template_name = 'Relacion/EstablecerRelacionASConfirm.html'
    def post(self, request, *args, **kwargs):
        diccionario= {}
        usuario_logueado= Usuario.objects.get(id= request.POST['login'])
        proyecto_actual= Proyecto.objects.get(id= request.POST['proyecto'])
        fase_actual= Fase.objects.get(id=request.POST['fase'])
        diccionario['fase']=fase_actual
        item_actual=Item.objects.get(id=request.POST['item'])
        diccionario['item']=item_actual
        diccionario['logueado']= usuario_logueado
        diccionario['proyecto']= proyecto_actual
        item_actual2=Item.objects.get(id=request.POST['item2'])
        new_nombre= request.POST['nombre_relacion']
        lista_items=[]
        lista_fases= Fase.objects.filter(proyecto=proyecto_actual)
        for fase in lista_fases:
            if fase_actual.numeroSecuencia < fase.numeroSecuencia:
                lista_items_fase=Item.objects.filter(fase=fase)
                for item in lista_items_fase:
                    lista_items.append(item)
        diccionario['lista_items']=lista_items
        existe= Relacion.objects.filter(nombre= new_nombre, item1=item_actual, activo=True)
        lista_relaciones= Relacion.objects.filter(item2=item_actual2, activo=True)
        if existe:
            diccionario['error']= 'Nombre de Relacion ya fue utilizado'
            return render(request, super(EstablecerRelacionASConfirm, self).template_name, diccionario)
        elif not lista_relaciones:
                nueva_relacion= Relacion()
                nueva_relacion.nombre=new_nombre
                nueva_relacion.item1=item_actual
                nueva_relacion.item2=item_actual2
                nueva_relacion.tipo='A/S'
                nueva_relacion.save()
                return render(request, self.template_name, diccionario)
        else:
            diccionario['error']= 'El item selecionado ya posee un ANTECESOR.'
            return render(request, super(EstablecerRelacionASConfirm, self).template_name, diccionario)
