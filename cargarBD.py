from Aplicaciones.Usuario.models import Usuario
from Aplicaciones.Rol.models import Rol
from Aplicaciones.Proyecto.models import Proyecto
from Aplicaciones.Fase.models import Fase

#Usuarios
	#1
administrador= Usuario(
    nick= 'admin',
    nombre= 'admin',
    apellido= 'admin',
    password= 'admin',
    cedula= 0,
    email= 'admin@admin',
)
administrador.save()

		#Rol de Administrador del Sistema
admin= Rol(nombre='Administrador del Sistema',
	   usuario= administrador, 
)
admin.save()
	#2
u_base=Usuario(
    nick= 'usuario',
    nombre= 'usuario',
    apellido= 'usuario',
    password= 'usuario',
    cedula= 2,
    email= 'usuario@usuario',
)
u_base.save()

#Proyecto
	#1
primer_proyecto= Proyecto(
	nombre= 'Primer Proyecto',
	descripcion= 'Este es el primer proyecto',
	presupuesto= 2000000,
	estado= 'I',
	costoTemporal= 300000,
	costoMonetario= 25000000,
	fechaInicio= '2014-04-29',
	fechaFin= '2015-08-10',
	numeroFase= 3, 
	lider= administrador,
)
primer_proyecto.save()
primer_proyecto.miembros.add(administrador)
primer_proyecto.miembros.add(u_base)
primer_proyecto.save()

#Creamos el Rol Asociado al Lider de este proyecto
lider= Rol(nombre= 'Lider del Proyecto',
	   usuario= administrador,
	   proyecto= primer_proyecto,
)
lider.save()

#Fases
	#1
fase1= Fase(
	nombre= 'Fase Inicial',
	numeroSecuencia= 1,
	descripcion= 'Primera fase',
	estado= 'F',
	fechaInicio= '2014-04-29',
	fechaFin= '2014-08-15',
	proyecto= primer_proyecto,
)
fase1.save()

	#2
fase2= Fase(
	nombre= 'Fase Desarrollo',
	numeroSecuencia= 2,
	descripcion= 'Segunda fase',
	estado= 'I',
	fechaInicio= '2014-08-15',
	fechaFin= '2015-01-10',
	proyecto= primer_proyecto,
)
fase2.save()

	#3
fase3= Fase(
	nombre= 'Fase Final',
	numeroSecuencia= 3,
	descripcion= 'Tercera fase',
	estado= 'I',
	fechaInicio= '2015-01-10',
	fechaFin= '2015-08-10',
	proyecto= primer_proyecto,
)
fase3.save()

#Rol para realizar las distintas operaciones...
rol_operaciones= Rol(
	nombre= 'Administrador del Proyecto',
	usuario= u_base,
	proyecto= primer_proyecto,
	crear_item= True,
	eliminar_item= True,
	editar_item= True,
	consultar_items= True,
	aprobar_item= True,
	agregar_atributo= True,
	eliminar_atributo= True,
	completar_atributos= True,
	consultar_atributos= True,
	crear_tipodeitem= True,
	modificar_tipodeitem= True,
	eliminar_tipodeitem= True,
	crear_tipodeatributo= True,
	eliminar_tipodeatributo= True,
	crear_lineabase= True,
)
rol_operaciones.save()
