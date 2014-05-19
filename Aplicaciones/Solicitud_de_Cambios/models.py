from django.db import models
from Aplicaciones.Proyecto.models import Proyecto
from Aplicaciones.Fase.models import Fase
from Aplicaciones.Item.models import Item
from Aplicaciones.Usuario.models import Usuario
# Create your models here.


class Solicitud_de_Cambios(models):
    estados_probables= (
        ('D','Desaprobado'),
        ('V','Votacion'),
        ('A','Aprobado'),
    )
    estado= models.CharField ( max_length = 1 ,  choices = estados_probables, default='V')
    costo_del_impacto= models.IntegerField(default=0)
    descripcion= models.CharField(max_length=50, null=False)
    proyecto=models.ForeignKey(Proyecto, related_name='fkProyectoSC')
    fase=models.ForeignKey(Fase, related_name='fkFaseSC')
    item_sc_aprobado=models.ForeignKey(Item, related_name='fkItemSCA')
    item_sc_desaprobado=models.ForeignKey(Item, related_name='fkItemSCD')
    usuario1= models.ForeignKey(Usuario, related_name= 'fkvoto1')
    usuario2= models.ForeignKey(Usuario, related_name= 'fkvoto2')
    usuario3= models.ForeignKey(Usuario, related_name= 'fkvoto3')
    voto1= models.BooleanField(default= False)
    voto2= models.BooleanField(default= False)
    voto3= models.BooleanField(default= False)

    activo= models.BooleanField(default= True)
    def __unicode__(self):
        return self.descripcion