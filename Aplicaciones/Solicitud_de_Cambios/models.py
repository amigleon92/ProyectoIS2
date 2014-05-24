from django.db import models
from Aplicaciones.Proyecto.models import Proyecto
from Aplicaciones.Fase.models import Fase
from Aplicaciones.Item.models import Item
from Aplicaciones.Usuario.models import Usuario
# Create your models here.


class Solicitud_de_Cambios(models.Model):
    """
    Se crea el modelo Solicitud_de_Cambios

    Estan definidos en la tabla los atributos


    - descripcion: Una breve descripcion del cambio a realizar
    - estado: puede encontrarse en 3 estados: Votacion, Desaprobado, Aprobado.
    - costo_del_impacto: calculo del impacto al realizar dicho cambio
    - proyecto: el id proyecto al que pertenece la solicitud
    - fase: el id de la Fase a la que pertenece
    - item_sc_aprobado: id del item ya modificado
    - item_sc_desaprobado: id del item si modificar
    - cantidad_de_votos: cantidad de votos acumulados
    """
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
    """
    Se crea el modelo Voto

    Estan definidos en la tabla los atributos


    - estado: puede encontrarse en 3 estados: SI, NO, Pendiente.
    - usuario: el id usuario al que pertenece el voto
    - solicitud_de_cambios: el id de la solicitud al a que pertenece el voto
    - voto: voto del miembro de comite
    """
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