# coding=utf-8
from django.shortcuts import render
from .models import Fase
from Aplicaciones.Usuario.models import Usuario
from Aplicaciones.Proyecto.models import Proyecto
from Aplicaciones.Rol.models import Rol
from Aplicaciones.Proyecto.views import ProyectoView
from Aplicaciones.Item.models import Item
from Aplicaciones.Relacion.models import Relacion
from Aplicaciones.Linea_Base.models import LineaBase
from Aplicaciones.Solicitud_de_Cambios.models import Solicitud_de_Cambios, Voto
import os


# Create your views here.

#Lista de Fases correspondientes al Proyecto dentro
class FaseView(ProyectoView):
    template_name = 'Fase/Fase.html'
    context_object_name = 'lista_fases'
    def post(self, request, *args, **kwargs):
        diccionario={}
        usuario_logueado= Usuario.objects.get(id= request.POST['login'])
        proyecto_actual= Proyecto.objects.get(id= request.POST['proyecto'])
        diccionario['logueado']= usuario_logueado
        diccionario['proyecto']= proyecto_actual
        if not proyecto_actual.estado=='N':
            diccionario['lista_fases']= Fase.objects.filter(proyecto= proyecto_actual)
            return render(request, self.template_name, diccionario)
        else:
            diccionario['lista_proyectos']= Proyecto.objects.filter(activo= True)
            diccionario['error']= 'Debe inicializar proyecto'
            return render(request, super(FaseView, self).template_name, diccionario)

#Editar los campos de los detalles de las fases
class EditarFase(FaseView):
    template_name = 'Fase/EditarFase.html'
    def post(self, request, *args, **kwargs):
        diccionario={}
        usuario_logueado= Usuario.objects.get(id= request.POST['login'])
        proyecto_actual= Proyecto.objects.get(id= request.POST['proyecto'])
        diccionario['logueado']= usuario_logueado
        diccionario['proyecto']= proyecto_actual
        if len(Rol.objects.filter(nombre= 'Lider del Proyecto', usuario= usuario_logueado, proyecto= proyecto_actual)):
            fase_actual= Fase.objects.get(id= request.POST['fase'])
            if fase_actual.estado=='N':
                if fase_actual.numeroSecuencia==1:
                    diccionario['fase']= fase_actual
                    return render(request, self.template_name, diccionario)
                else:
                    fase_anterior= Fase.objects.get(proyecto= proyecto_actual, numeroSecuencia= fase_actual.numeroSecuencia-1)
                    if fase_anterior.estado == 'N':
                        diccionario['error']= 'Error - Fase Anterior No Inicializada'
                    else:
                        diccionario['fase']= fase_actual
                        return render(request, self.template_name, diccionario)
            else:
                diccionario['error']= 'La fase ya fue inicializada'
        else:
            diccionario['error']= 'No puedes realizar esta accion'
        diccionario['lista_fases']= Fase.objects.filter(proyecto= proyecto_actual)
        return render(request, super(EditarFase, self).template_name, diccionario)

class EditarFaseConfirm(EditarFase):
    template_name = 'Fase/EditarFaseConfirm.html'
    def post(self, request, *args, **kwargs):
        diccionario={}
        usuario_logueado= Usuario.objects.get(id= request.POST['login'])
        proyecto_actual= Proyecto.objects.get(id= request.POST['proyecto'])
        diccionario['logueado']= usuario_logueado
        diccionario['proyecto']= proyecto_actual
        modificar_fase= Fase.objects.get(id=request.POST['fase'])
        modificar_fase.nombre= request.POST['nombre_fase']
        modificar_fase.descripcion= request.POST['descripcion_fase']
        modificar_fase.fechaInicio= request.POST['fechaInicio_fase']
        modificar_fase.fechaFin=request.POST['fechaFin_fase']
        if modificar_fase.fechaInicio > modificar_fase.fechaFin:
            diccionario['fase']= modificar_fase
            diccionario['error']= 'ERROR - Fecha Inicio supera a Fecha Fin'
            return render(request, super(EditarFaseConfirm, self).template_name, diccionario)
        if modificar_fase.fechaInicio < str(proyecto_actual.fechaInicio) or modificar_fase.fechaFin > str(proyecto_actual.fechaFin):
            diccionario['fase']= modificar_fase
            diccionario['error']= 'ERROR - Alguna fecha esta fuera de los limites del proyecto'
            return render(request, super(EditarFaseConfirm, self).template_name, diccionario)
        modificar_fase.estado= 'I'
        modificar_fase.save()
        return render(request, self.template_name, diccionario)

#Muestra un informe de la fase.
class InformeFase(FaseView):
    template_name = 'Fase/InformeFase.html'
    def post(self, request, *args, **kwargs):
        diccionario={}
        usuario_logueado= Usuario.objects.get(id= request.POST['login'])
        proyecto_actual= Proyecto.objects.get(id= request.POST['proyecto'])
        diccionario['logueado']= usuario_logueado
        diccionario['proyecto']= proyecto_actual
        mostrar_fase= Fase.objects.get(id= request.POST['fase'])
        if not mostrar_fase.estado== 'N':
            diccionario['fase']= mostrar_fase
            return render(request, self.template_name, diccionario)
        else:
            diccionario['lista_fases']= Fase.objects.filter(proyecto= proyecto_actual)
            diccionario['error']= 'No se puede mostrar - Fase No Iniciada'
            return render(request, super(InformeFase, self).template_name, diccionario)

class CerrarFase(FaseView):
    template_name = 'Fase/CerrarFase.html'
    def post(self, request, *args, **kwargs):
        diccionario={}
        usuario_logueado= Usuario.objects.get(id= request.POST['login'])
        proyecto_actual= Proyecto.objects.get(id= request.POST['proyecto'])
        diccionario['logueado']= usuario_logueado
        diccionario['proyecto']= proyecto_actual
        diccionario['lista_fases']= Fase.objects.filter(proyecto= proyecto_actual)
        if len(Rol.objects.filter(nombre= 'Lider del Proyecto', usuario= usuario_logueado, proyecto= proyecto_actual)):
            fase_actual= Fase.objects.get(id= request.POST['fase'])
            lista_de_items= Item.objects.filter(fase=fase_actual, activo=True)
            if fase_actual.estado=='I':
                if not len(lista_de_items):
                        diccionario['error']= 'No se puede cerrar la fase sin items.'
                        return render(request, super(CerrarFase, self).template_name, diccionario)
                for item in lista_de_items:
                    if not item.estado == 'B':
                        diccionario['error']= 'No se puede cerrar la fase - Exite items NO BLOQUEADO'
                        return render(request, super(CerrarFase, self).template_name, diccionario)
                for i in diccionario['lista_fases']:
                    if i.numeroSecuencia < fase_actual.numeroSecuencia and not i.estado=='F':
                        diccionario['error']= 'No se puede cerrar la fase - Fase Anterior No Finalizadda'
                        return render(request, super(CerrarFase, self).template_name, diccionario)
                if not fase_actual.numeroSecuencia == proyecto_actual.numeroFase:
                    #comprobacion de sucesor
                    for itemAntecesor in lista_de_items:
                        if len(Relacion.objects.filter(item1=itemAntecesor, tipo='A/S', activo=True)):
                            fase_actual.estado='F'
                            fase_actual.save()
                            return render(request, self.template_name, diccionario)
                    diccionario['error']= 'Se necesita que al menos un item tenga sucesor para no perder consistencia'
                    return render(request, super(CerrarFase, self).template_name, diccionario)
                fase_actual.estado='F'
                fase_actual.save()
                return render(request, self.template_name, diccionario)
            else:
                diccionario['error']= 'No se puede cerrar - Fase No Iniciada'
        else:
            diccionario['error']= 'No puedes realizar esta accion'
        return render(request, super(CerrarFase, self).template_name, diccionario)

#Finalizar el proyecto una vez terminadas las fases
class FinalizarProyecto(FaseView):
    template_name = 'Fase/FinalizarProyecto.html'
    def post(self, request, *args, **kwargs):
        diccionario={}
        usuario_logueado= Usuario.objects.get(id= request.POST['login'])
        proyecto_actual= Proyecto.objects.get(id= request.POST['proyecto'])
        diccionario['logueado']= usuario_logueado
        diccionario['proyecto']= proyecto_actual
        if len(Rol.objects.filter(nombre= 'Lider del Proyecto', usuario= usuario_logueado, proyecto= proyecto_actual)):
            ultima_fase= Fase.objects.get(numeroSecuencia= proyecto_actual.numeroFase, proyecto= proyecto_actual)       #comporbamos si se termino la ultima fase
            if not ultima_fase.estado=='F':
                diccionario['error']= 'Para finalizar, todas las fases deberian de estar cerradas'
                diccionario['lista_fases']= Fase.objects.filter(proyecto= proyecto_actual)
                return render(request, super(FinalizarProyecto, self).template_name, diccionario)
            else:
                proyecto_actual.estado= 'F'
                proyecto_actual.save()
                diccionario['lista_proyectos']= Proyecto.objects.filter(activo= True)
                return render(request, ProyectoView.template_name, diccionario)
        else:
            diccionario['lista_fases']= Fase.objects.filter(proyecto= proyecto_actual)
            diccionario['error']= 'No puedes realizar esta accion'
            return render(request, super(FinalizarProyecto, self).template_name, diccionario)

class AsignarNuevosMiembros(FaseView):
    template_name = 'Fase/AsignarNuevosMiembros.html'
    def post(self, request, *args, **kwargs):
        diccionario={}
        usuario_logueado= Usuario.objects.get(id= request.POST['login'])
        proyecto_actual= Proyecto.objects.get(id= request.POST['proyecto'])
        diccionario['logueado']= usuario_logueado
        diccionario['proyecto']= proyecto_actual
        if len(Rol.objects.filter(nombre= 'Lider del Proyecto', usuario= usuario_logueado, proyecto= proyecto_actual)):
            lista_usuarios= Usuario.objects.filter(estado= True)
            lista_no_miembros= []
            for usuario in lista_usuarios:
                if not usuario in proyecto_actual.miembros.all():
                    lista_no_miembros.append(usuario)
            if not len(lista_no_miembros):
                diccionario['lista_fases']= Fase.objects.filter(proyecto= proyecto_actual)
                diccionario['error']= 'No existen mas usuarios'
                return render(request, super(AsignarNuevosMiembros, self).template_name, diccionario)
            diccionario['lista_no_miembros']= lista_no_miembros
            return render(request, self.template_name, diccionario)
        else:
            diccionario[super(AsignarNuevosMiembros, self).context_object_name]= Fase.objects.filter(proyecto= proyecto_actual)
            diccionario['error']= 'No posee permisos para asignar nuevos miembros al proyecto'
            return render(request, super(AsignarNuevosMiembros, self).template_name, diccionario)

class AsignarNuevosMiembrosConfirm(FaseView):
    template_name = 'Fase/AsignarNuevosMiembrosConfirmar.html'
    def post(self, request, *args, **kwargs):
        diccionario={}
        usuario_logueado= Usuario.objects.get(id= request.POST['login'])
        proyecto_actual= Proyecto.objects.get(id= request.POST['proyecto'])
        diccionario['logueado']= usuario_logueado
        diccionario['proyecto']= proyecto_actual
        usuarios_miembros= request.POST.getlist('miembros[]')
        for usuario in usuarios_miembros:
            usuario= Usuario.objects.get(nick= usuario)
            proyecto_actual.miembros.add(usuario)
        return render(request, self.template_name, diccionario)

class Graficar(FaseView):
    template_name = 'Fase/Graficar.html'
    def post(self, request, *args, **kwargs):
        diccionario={}
        usuario_logueado= Usuario.objects.get(id=request.POST['login'])
        proyecto_actual= Proyecto.objects.get(id=request.POST['proyecto'])
        diccionario['logueado']=usuario_logueado
        diccionario['proyecto']=proyecto_actual
        fases_proyecto= Fase.objects.filter(proyecto=proyecto_actual)
        items_proyecto=[]
        for fase in fases_proyecto:
            if not fase.estado=='N':
                items=Item.objects.filter(fase=fase, activo=True)
                if len(items):
                    items_proyecto.append(items)
                else:
                    diccionario['error']= 'Fase Iniciada sin Items.'
                    diccionario['lista_fases']= Fase.objects.filter(proyecto= proyecto_actual)
                    return render(request, super(Graficar, self).template_name, diccionario)

        contador=0
        grafico_fichero=open('grafico_proyecto.dot','w')
        grafico_fichero.write('digraph G {\n')
        grafico_fichero.write('     // Informacion de Proyecto\n')
        grafico_fichero.write('     subgraph cluster'+str(contador)+' {\n')
        grafico_fichero.write('         label = "Estados de Item";\n')
        grafico_fichero.write('         color=black;\n')
        grafico_fichero.write('         Bloqueado[style=filled, width="1", color=blue, fontsize=10];\n')
        grafico_fichero.write('         Desaprobado[style=filled, width="1", color=yellow,fontsize=8];\n')
        grafico_fichero.write('         Aprobado[style=filled, width="1", color=green,fontsize=10];\n')
        grafico_fichero.write('         Revisión[style=filled, width="1", color=red,fontsize=10];\n')
        grafico_fichero.write('     }\n')
        grafico_fichero.write('     // Fases\n     rankdir=LR;//orientacion\n     ranksep=1.0;//separacion\n')
        for fase in fases_proyecto:
           contador=contador+1
           grafico_fichero.write('     subgraph cluster'+str(contador)+' {\n')
           if fase.estado =='F':
                    grafico_fichero.write('         label = "Fase Nro '+str(fase.numero)+' - '+fase.nombre+' (Finalizada) ";\n')
                    grafico_fichero.write('         style=filled;\n')
                    grafico_fichero.write('         color=lightgray;\n')
           elif fase.estado=='I':
                    grafico_fichero.write('         label = "Fase Nro '+str(fase.numero)+' - '+fase.nombre+' (Iniciada) ";\n')
                    grafico_fichero.write('         style=bold;\n')
                    grafico_fichero.write('         color=blue;\n')
           lineas_bases= LineaBase.objects.filter(fase=fase, activo=True)
           if len(lineas_bases):
                    grafico_fichero.write('         //Lineas Bases\n')
                    for linea_base in lineas_bases:
                        contador=contador+1
                        itemsLB=Item.objects.filter(lineaBase=linea_base, activo=True)
                        grafico_fichero.write('             subgraph cluster'+str(contador)+' {\n')
                        if linea_base.estado =='C':
                            grafico_fichero.write('                 label = "'+linea_base.nombre+' (Cerrada) ";\n')
                            grafico_fichero.write('                 style=bold;\n')
                            grafico_fichero.write('                 color=black;\n')
                            for item in itemsLB:
                                grafico_fichero.write('                 '+item.nombre+'[style=filled, color=blue];\n')
                        else:
                            grafico_fichero.write('                 label = "'+linea_base.nombre+' (Revision) ";\n')
                            grafico_fichero.write('                 style=dotted;\n')
                            grafico_fichero.write('                 color=black;\n')
                            for item in itemsLB:
                                grafico_fichero.write('                 '+item.nombre+'[style=filled, color=red];\n')
                        grafico_fichero.write('             }\n')
           itemsA=Item.objects.filter(fase=fase, estado='A', activo=True)
           itemsD=Item.objects.filter(fase=fase, estado='D', activo=True)
           if len(itemsA):
                    for itemA in itemsA:
                        grafico_fichero.write('             '+itemA.nombre+'[style=filled, color=green];\n')
           if len(itemsD):
                    for itemD in itemsD:
                        grafico_fichero.write('             '+itemD.nombre+'[style=filled, color=yellow];\n')
           grafico_fichero.write('     }\n')
        for item in items_proyecto:
            relaciones_proyecto= Relacion.objects.filter(item1=item, activo=True)
            if len(relaciones_proyecto):
                for relacion in relaciones_proyecto:
                    if relacion.item2.activo:
                        grafico_fichero.write('     '+relacion.item1.nombre+' -> '+relacion.item2.nombre+';\n')
        grafico_fichero.write('}\n')
        grafico_fichero.close()
        os.system("dot grafico_proyecto.dot -o grafico_proyecto.png -Tpng")
        os.system("mv grafico_proyecto.png static")


        return render(request, self.template_name, diccionario)



# reportes de items
class Reporte_items(FaseView):
    def post(self, request, *args, **kwargs):
        proyecto_actual= Proyecto.objects.get(id=request.POST['proyecto'])
        from django.http import HttpResponse
        import os
        import datetime
        # Obtenemos de platypus las clases Paragraph, para escribir parrafos Image, para insertar imagenes y SimpleDocTemplate para definir el DocTemplate. Ademas importamos Spacer, para incluir espacios .
        from reportlab.platypus import Paragraph
        from reportlab.platypus import SimpleDocTemplate
        from reportlab.platypus import Spacer
        from reportlab.platypus import Table

        # Importamos clase de hoja de estilo de ejemplo.
        from reportlab.lib.styles import getSampleStyleSheet

        # Se importa el tamanho de la hoja y los colores
        from reportlab.lib.pagesizes import A4
        from reportlab.lib import colors


        # Creamos un PageTemplate de ejemplo.
        estiloHoja = getSampleStyleSheet()

        #Inicializamos la lista Platypus Story.
        story = []

        #Definimos como queremos que sea el estilo de la PageTemplate.
        cabecera = estiloHoja['Heading5']

        #No se hara un salto de pagina despues de escribir la cabecera (valor 1 en caso contrario).
        cabecera.pageBreakBefore=0

        # Se quiere que se empiece en la primera pagina a escribir. Si es distinto de 0 deja la primera hoja en blanco.
        cabecera.keepWithNext=0



        # Color de la cabecera.
        cabecera.backColor=colors.white
        cabecera.spaceAfter = 0
        cabecera.spaceBefore = 0

        parrafo = Paragraph('.',cabecera)
        story.append(parrafo)
        parrafo = Paragraph('REPORTE DE ITEMS DEL PROYECTO: '+ proyecto_actual.nombre,cabecera)
        story.append(parrafo)
        parrafo = Paragraph('-'*193,cabecera)
        story.append(parrafo)

        # Incluimos un Flowable, que en este caso es un parrafo.

        cabecera2 = estiloHoja['Heading3']
        cabecera2.pageBreakBefore=0
        cabecera2.keepWithNext=0
        cabecera2.backColor=colors.white

        parrafo = Paragraph('   ',cabecera2)
        # Lo incluimos en el Platypus story.
        story.append(parrafo)

        # Definimos un parrafo. Vamos a crear un texto largo para demostrar como se genera mas de una hoja.
        lista = []
        lista.append(['LISTA DE ITEMS POR FASE','','','','', '', ''])
        lista.append([' ',' ',' ',' ',' ', ' ', ' '])
        lista.append(['FASE','ID ITEM','NOMBRE','TIPO DE ITEM','ITEM PADRE', 'VERSION', 'COSTO'])
        fases = (Fase.objects.filter(proyecto=proyecto_actual)).order_by('numeroSecuencia')
        for fase in fases:
            lista.append([fase.nombre,' ',' ',' ',' ', ' ', ' '])
            items=(Item.objects.filter(fase=fase, activo= True)).order_by('id')
            if len(items):
                for item in items:
                    papa_item=Relacion.objects.filter(item2=item, activo=True)
                    if len(papa_item):
                        lista.append(['',item.id,item.nombre,item.tipodeItemAsociado,papa_item[0].item1.nombre,item.version,item.costo])
                    else:
                        lista.append(['',item.id,item.nombre,item.tipodeItemAsociado,'NO',item.version,item.costo])
            else:
                lista.append(['',' - ',' - ',' - ',' - ',' - ',' - '])
        t=Table( lista, style = [
                       ('GRID',(0,0),(-1,-1),0.5,colors.white),
                       ('BOX',(0,0),(-1,-1),2,colors.white),
                       ('SPAN',(0,0),(-1,0)),
                       ('ROWBACKGROUNDS', (0, 3), (-1, -1), (colors.Color(0.9, 0.9, 0.9),colors.white)),
                       ('BACKGROUND', (0, 2), (-1, 2), colors.rgb2cmyk(r=6,g=62,b=193)),
                       ('BACKGROUND', (0, 1), (-1, 1), colors.white),
                       ('LINEABOVE',(0,0),(-1,0),1.5,colors.black),
                       ('LINEBELOW',(0,0),(-1,0),1.5,colors.black),
                       ('SIZE',(0,0),(-1,0),12),
                       ('ALIGN', (0, 0), (-1, 0), 'CENTER'),
                       ('VALIGN', (0, 0), (-1, 0), 'MIDDLE'),
                       ('TEXTCOLOR', (0, 2), (-1, 2), colors.white),
                       ]
              )
        # Y lo incluimos en el story.
        story.append(t)

        # Dejamos espacio.
        story.append(Spacer(0,20))

        # Creamos un DocTemplate en una hoja DIN A4, en la que se muestra el texto enmarcado (showBoundary=1) por un recuadro.
        doc=SimpleDocTemplate("Rep_items.pdf",pagesize=A4, rightMargin=1, leftMargin=1, topMargin=0, bottomMargin=0)

        parrafo = Paragraph('-'*193,cabecera)
        story.append(parrafo)
        parrafo = Paragraph('Fin del Informe' + ' '*100 + '('+str(datetime.date.today()) + ')' ,cabecera)
        story.append(parrafo)

        # Construimos el Platypus story.
        doc.build(story)

        image_data = open("Rep_items.pdf", "rb").read()
        return HttpResponse(image_data, mimetype="application/pdf")


# reportes de Solicitud de cambio
class Reporte_SC(FaseView):
    def post(self, request, *args, **kwargs):
        from django.http import HttpResponse
        import datetime
        # Obtenemos de platypus las clases Paragraph, para escribir parrafos Image, para insertar imagenes y SimpleDocTemplate para definir el DocTemplate. Ademas importamos Spacer, para incluir espacios .
        from reportlab.platypus import Paragraph
        from reportlab.platypus import SimpleDocTemplate
        from reportlab.platypus import Spacer
        from reportlab.platypus import Table
        # Importamos clase de hoja de estilo de ejemplo.
        from reportlab.lib.styles import getSampleStyleSheet

        # Se importa el tamanho de la hoja y los colores
        from reportlab.lib.pagesizes import A4
        from reportlab.lib import colors
        diccionario={}
        usuario_logueado= Usuario.objects.get(id=request.POST['login'])
        proyecto_actual= Proyecto.objects.get(id=request.POST['proyecto'])
        diccionario['logueado']=usuario_logueado
        diccionario['proyecto']=proyecto_actual
        if not proyecto_actual.lider == usuario_logueado:
            diccionario['error']= 'No puedes realizar esta accion'
            diccionario['lista_fases']= Fase.objects.filter(proyecto= proyecto_actual)
            return render(request, super(Reporte_SC, self).template_name, diccionario)

        # Creamos un PageTemplate de ejemplo.
        estiloHoja = getSampleStyleSheet()

        #Inicializamos la lista Platypus Story.
        story = []

        #Definimos como queremos que sea el estilo de la PageTemplate.
        cabecera = estiloHoja['Heading5']

        #No se hara un salto de pagina despues de escribir la cabecera (valor 1 en caso contrario).
        cabecera.pageBreakBefore=0

        # Se quiere que se empiece en la primera pagina a escribir. Si es distinto de 0 deja la primera hoja en blanco.
        cabecera.keepWithNext=0

        # Color de la cabecera.
        cabecera.backColor=colors.white
        cabecera.spaceAfter = 0
        cabecera.spaceBefore = 0

        parrafo = Paragraph('.',cabecera)
        story.append(parrafo)
        parrafo = Paragraph('REPORTE DE SOLICITUDES DE CAMBIO DEL PROYECTO: '+ proyecto_actual.nombre,cabecera)
        story.append(parrafo)
        parrafo = Paragraph('-'*193,cabecera)
        story.append(parrafo)

        # Incluimos un Flowable, que en este caso es un parrafo.
        cabecera2 = estiloHoja['Heading3']
        cabecera2.pageBreakBefore=0
        cabecera2.keepWithNext=0
        cabecera2.backColor=colors.white

        parrafo = Paragraph('   ',cabecera2)
        # Lo incluimos en el Platypus story.
        story.append(parrafo)

        # Definimos un parrafo. Vamos a crear un texto largo para demostrar como se genera mas de una hoja.
        lista = []
        lista.append(['LISTA DE SOLICITUDES DE CAMBIO','','','','', '', ''])
        lista.append([' ',' ',' ',' ',' ', ' ', ' '])
        lista.append(['ID','LINEA BASE','DETALLES','ESTADO','USUARIO', 'COSTO','VOTO LIDER'])
        solicitudes= (Solicitud_de_Cambios.objects.filter(proyecto=proyecto_actual)).order_by('id')
        for solicitud in solicitudes:
            voto=Voto.objects.filter(usuario=proyecto_actual.lider, solicitud_de_cambios=solicitud)
            if len(voto):
                if voto[0].voto=='Pe':
                    if solicitud.estado=='A':
                        lista.append([solicitud.id,solicitud.item_sc_aprobado.lineaBase.nombre,solicitud.descripcion,solicitud.estado,solicitud.usuario.nombre,solicitud.costo_del_impacto,'Pendiente'])
                    else:
                        lista.append([solicitud.id,solicitud.item_sc_desaprobado.lineaBase.nombre,solicitud.descripcion,solicitud.estado,solicitud.usuario.nombre,solicitud.costo_del_impacto,'Pendiente'])
                else:
                    if solicitud.estado=='A':
                        lista.append([solicitud.id,solicitud.item_sc_aprobado.lineaBase.nombre,solicitud.descripcion,solicitud.estado,solicitud.usuario.nombre,solicitud.costo_del_impacto,'Realizado'])
                    else:
                        lista.append([solicitud.id,solicitud.item_sc_desaprobado.lineaBase.nombre,solicitud.descripcion,solicitud.estado,solicitud.usuario.nombre,solicitud.costo_del_impacto,'Realizado'])
            else:
                if solicitud.estado=='A':
                    lista.append([solicitud.id,solicitud.item_sc_aprobado.lineaBase.nombre,solicitud.descripcion,solicitud.estado,solicitud.usuario.nombre,solicitud.costo_del_impacto,'Lider NO es Miembro'])
                else:
                    lista.append([solicitud.id,solicitud.item_sc_desaprobado.lineaBase.nombre,solicitud.descripcion,solicitud.estado,solicitud.usuario.nombre,solicitud.costo_del_impacto,'Lider NO es Miembro'])
        t=Table( lista, style = [
                       ('GRID',(0,0),(-1,-1),0.5,colors.white),
                       ('BOX',(0,0),(-1,-1),2,colors.white),
                       ('SPAN',(0,0),(-1,0)),
                       ('ROWBACKGROUNDS', (0, 3), (-1, -1), (colors.Color(0.9, 0.9, 0.9),colors.white)),
                       ('BACKGROUND', (0, 2), (-1, 2), colors.rgb2cmyk(r=6,g=62,b=193)),
                       ('BACKGROUND', (0, 1), (-1, 1), colors.white),
                       ('LINEABOVE',(0,0),(-1,0),1.5,colors.black),
                       ('LINEBELOW',(0,0),(-1,0),1.5,colors.black),
                       ('SIZE',(0,0),(-1,0),12),
                       ('ALIGN', (0, 0), (-1, 0), 'CENTER'),
                       ('VALIGN', (0, 0), (-1, 0), 'MIDDLE'),
                       ('TEXTCOLOR', (0, 2), (-1, 2), colors.white),
                       ]
              )
        # Y lo incluimos en el story.
        story.append(t)

        # Dejamos espacio.
        story.append(Spacer(0,20))

        # Creamos un DocTemplate en una hoja DIN A4, en la que se muestra el texto enmarcado (showBoundary=1) por un recuadro.
        doc=SimpleDocTemplate("Rep_Solc_Camb.pdf",pagesize=A4, rightMargin=1, leftMargin=1, topMargin=0, bottomMargin=0)

        parrafo = Paragraph('-'*193,cabecera)
        story.append(parrafo)
        parrafo = Paragraph('Fin del Informe' + ' '*100 + '('+str(datetime.date.today()) + ')' ,cabecera)
        story.append(parrafo)

        # Construimos el Platypus story.
        doc.build(story)

        image_data = open("Rep_Solc_Camb.pdf", "rb").read()
        return HttpResponse(image_data, mimetype="application/pdf")
