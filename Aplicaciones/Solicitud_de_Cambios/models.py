from django.db import models
from Aplicaciones.Proyecto.models import Proyecto
from Aplicaciones.Fase.models import Fase
from Aplicaciones.Item.models import Item
from Aplicaciones.Usuario.models import Usuario
# Create your models here.


class Solicitud_de_Cambios(models.Model):
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
    cantidad_de_votos=models.IntegerField(default=0)

    activo= models.BooleanField(default= True)
    def __unicode__(self):
        return self.descripcion


#modelo de voto
class Voto(models.Model):
    estados_probables=(
        ('Si', 'Si'),
        ('No', 'No'),
        ('Pe', 'Pendiente')
    )
    usuario= models.ForeignKey(Usuario, related_name='fkusuariovoto')
    solicitud_de_cambios= models.ForeignKey(Solicitud_de_Cambios, related_name= 'fkSC')
    voto= models.CharField(max_length=2, choices= estados_probables, default='Pe')
    activo= models.BooleanField(default= True)
    def __unicode__(self):
        return self.usuario.nombre + ' -> ' + self.voto