from django.shortcuts import render
from .models import Relacion
from Aplicaciones.Item.views import ItemView
from Aplicaciones.Usuario.models import Usuario
from Aplicaciones.Proyecto.models import Proyecto
from Aplicaciones.Fase.models import Fase
from Aplicaciones.Item.models import Item

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


