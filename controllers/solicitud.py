# -*- coding: utf-8 -*-
import time
from plugin_notemptymarker import mark_not_empty
import json
# try something like
@auth.requires(not auth.has_membership('Usuario Normal'))
@auth.requires_login()
def index():
	return dict()

@auth.requires(not auth.has_membership('Usuario Normal'))
@auth.requires_login()
def validar_pedido(form):
	if ('edit' in request.args):
		return
	#esp=form.vars.f_espacio_fisico
	esp=request.vars['esp']
	sust=form.vars.f_sustancia
	aux=db((db.t_inventario.f_sustancia==sust) & (db.t_inventario.f_espaciofisico==esp)).count()
	if aux==0:
		form.errors.f_sustancia=T('El inventario del espacio debe contener la sustancia solicitada')
	#if form.vars.f_cantidad <= 0:
	#	form.errors.f_cantidad=T('La cantidad solicitada debe ser un valor positivo')
	#if (form.vars.f_fecha_tope < (request.now.date()))|(form.vars.f_fecha_tope==''):
	#	form.errors.f_fecha_tope=T('La fecha tope de la solicitud debe ser mayor o igual a la fecha actual')
	#if form.vars.f_responsable=='':
	#	form.errors.f_responsable=T('Debe introducir un responsable para la solicitud')
@auth.requires(not auth.has_membership('Usuario Normal'))
@auth.requires_login()
def validar_respuesta(form):
	esp=request.vars['esp']
	sust=request.vars['sust']
	tipo=request.vars['t']
	aux=db((db.t_inventario.f_sustancia==sust) & (db.t_inventario.f_espaciofisico==esp)).select()
	for i in aux:
		if tipo=="Donación":
			if i.f_cantidadonacion<(form.vars.f_cantidad):
				form.errors.f_cantidad=T('No posee suficiente sustancia disponible para donar para realizar esta donación.')
		if tipo=="Préstamo":
			if i.f_cantidadusointerno<(form.vars.f_cantidad):
				form.errors.f_cantidad=T('No posee suficiente sustancia de uso interno para realizar este préstamo.')

	aux=db(db.t_solicitud.id==request.vars['id']).select().first()
	if int(aux.f_cantidad)<int(form.vars.f_cantidad):
		form.errors.f_cantidad=T('La cantidad debe ser menor o igual a la cantidad solicitada.')
@auth.requires(not auth.has_membership('Usuario Normal'))
@auth.requires_login()
def validar_prestamo(form):
	esp=request.vars['esp']
	sust=request.vars['sust']
	#tipo=request.vars['t']
	aux=db((db.t_inventario.f_sustancia==sust) & (db.t_inventario.f_espaciofisico==esp)).select()
	for i in aux:
		if i.f_cantidadusointerno<(form.vars.f_cantidad):
			form.errors.f_cantidad=T('No posee suficiente sustancia de uso interno para realizar este pago.')
	aux=db(db.t_solicitud_respuesta.id==request.vars['id']).select().first()
	if int(aux.f_cantidad-aux.f_cantidad_devuelta)<int(form.vars.f_cantidad):
		form.errors.f_cantidad=T('La cantidad a devolver debe ser menor o igual a la cantidad que se debe.')
	solicitud_respuesta_asociada=db(db.t_solicitud_respuesta.id==request.vars['id']).select().first()
	if (solicitud_respuesta_asociada.f_cantidad_devuelta_prestamo+form.vars.f_cantidad)>solicitud_respuesta_asociada.f_cantidad:
		form.errors.f_cantidad=T('La cantidad a devolver debe ser menor o igual a la cantidad que se debe.')
	

@auth.requires(not auth.has_membership('Usuario Normal'))
@auth.requires_login()
def select_solicitud():
    espacios=False
    labs=False
    secciones=False
    funcion=request.vars['f']

    if (auth.has_membership('Gestor de Sustancias') or auth.has_membership('Director') or auth.has_membership('WebMaster')):
        espacios = db(db.t_inventario.f_espaciofisico == db.t_espaciofisico.id).select(db.t_espaciofisico.ALL,groupby=db.t_espaciofisico.id,orderby=[db.t_espaciofisico.f_seccion,db.t_espaciofisico.f_espacio])
        secciones = db(db.t_inventario.f_seccion == db.t_seccion.id).select(db.t_seccion.ALL,distinct=db.t_seccion.id)
        labs = db(db.t_inventario.f_laboratorio == db.t_laboratorio.id).select(db.t_laboratorio.ALL,distinct=db.t_laboratorio.id)
    elif (auth.has_membership('Jefe de Laboratorio') ):
        espacios = db( (db.t_laboratorio.f_jefe == auth.user.id)&(db.t_seccion.f_laboratorio == db.t_laboratorio.id)&(db.t_espaciofisico.f_seccion == db.t_seccion.id)&(db.t_espaciofisico.id == db.t_inventario.f_espaciofisico) ).select(db.t_espaciofisico.ALL,distinct=db.t_espaciofisico.id)#,orderby=db.t_espaciofisico.f_seccion)
        secciones = db((db.t_laboratorio.f_jefe == auth.user.id)&(db.t_seccion.f_laboratorio == db.t_laboratorio.id)&(db.t_seccion.id == db.t_inventario.f_seccion) ).select(db.t_seccion.ALL,distinct=db.t_seccion.id)
        labs = db(db.t_laboratorio.f_jefe == auth.user.id).select(db.t_laboratorio.ALL)
    elif (auth.has_membership('Jefe de Sección') ):
        espacios = db((db.t_espaciofisico.f_seccion == db.t_seccion.id)&(db.t_seccion.f_jefe == auth.user.id)).select(db.t_espaciofisico.ALL,orderby=[db.t_espaciofisico.f_seccion,db.t_espaciofisico.f_espacio])
        secciones = db(db.t_seccion.f_jefe == auth.user.id ).select(db.t_seccion.ALL)
    else:
        espacios = db((db.t_tecs_esp.f_tecnico == auth.user.id)&(db.t_espaciofisico.id == db.t_tecs_esp.f_espaciofisico)).select(db.t_espaciofisico.ALL,orderby=[db.t_espaciofisico.f_seccion,db.t_espaciofisico.f_espacio])
    return locals()

def aprobar():
	if (auth.has_membership('Usuario Normal')) | (auth.has_membership('Técnico')):
		session.flash=T('No posees privilegios suficientes para realizar esta operación.')
		redirect(URL(c='solicitud',f='tipo_solicitud', vars=request.vars))
	i=request.args[0]
	aux=db(db.t_solicitud.id==i).select().first()
	aux.update_record(f_aprobado=1)
	redirect(URL(c='solicitud',f='tipo_solicitud', vars=request.vars))
	return dict()


#Lista para hacer una solicitud solicitudes luego de acceder a un espacio fisico
@auth.requires(not auth.has_membership('Usuario Normal'))
@auth.requires_login()
def tipo_solicitud():
	f=request.vars['f']	#Función asociada
	seccion = str(db((db.t_espaciofisico.id == request.vars['esp'])&(db.t_seccion.id == db.t_espaciofisico.f_seccion)).select(db.t_seccion.f_seccion))[21:-2]
	labs = str( db((db.t_seccion.f_seccion == seccion)&(db.t_laboratorio.id == db.t_seccion.f_laboratorio) ).select(db.t_laboratorio.f_nombre) )[24:-2]
	espFisico = str( db(db.t_espaciofisico.id == request.vars['esp']).select(db.t_espaciofisico.f_espacio) )[27:-2]
	esp=request.vars['esp']
	x = 0
	js = dict()
	aux=db(db.t_solicitud.f_espacio_fisico==request.vars['esp']).select(db.t_solicitud.f_aprobado,orderby=[~db.t_solicitud.id])
	for r in aux:
		js[x]=r.f_aprobado
		x = x+1
	aux = XML(json.dumps(js))
	if ('new' in request.args):
		db.t_solicitud.f_cantidad_devuelta.readable=False
		db.t_solicitud.f_cantidad_devuelta.default=0
		db.t_solicitud.f_fecha_solicitud.default=request.now
		db.t_solicitud.f_espacio_fisico.default=request.vars['esp']
		mark_not_empty(db.t_solicitud)
		db.t_solicitud.f_Tipo.comment='Los campos marcados con (*) son obligatorios'
	if ('view' in request.args):
		db.t_solicitud.f_fecha_solicitud.readable=True
		db.t_solicitud.f_responsable.readable=True
	if ('edit' in request.args):
		db.t_solicitud.f_sustancia.writable=False
		db.t_solicitud.f_Tipo.writable=False
	if f=='1': #Mis solicitudes, antigua view_a
		db.t_solicitud.f_cantidad_respuestas.readable=True
		if ('new' in request.args):
			db.t_solicitud.f_cantidad_respuestas.readable=False
		respuesta= lambda row: A('Respuestas', _href=URL(c='solicitud', f='view_e', vars=dict(id=row.id, t=row.f_Tipo, esp=request.vars['esp'], s=row.f_sustancia)))
		aprobar= lambda row: A('Aprobar', _href=URL(c='solicitud', f='aprobar', vars=request.vars, args=[row.id]))
		links=[aprobar,respuesta]
		query=(db.t_solicitud.f_espacio_fisico==request.vars['esp'])
		table=SQLFORM.smartgrid(db.t_solicitud, constraints=dict(t_solicitud=query), links=links, csv=False, deletable=False, editable=False, onvalidation=validar_pedido, orderby=[~db.t_solicitud.id], onupdate=None)
		return locals()	
	elif f=='2':#Solicitudes recibidas, antigua view_b
		db.v_solicitud.f_espaciofisico.readable=False
		query=(db.v_solicitud.f_espacio_fisico!=esp) & (db.v_solicitud.f_espaciofisico==esp) & (db.v_solicitud.f_aprobado==1) & (db.v_solicitud.f_satisfecho!=1)
		aceptar= lambda row: A('Aceptar', _href=URL(c='solicitud',f='view_c', vars=dict(id=row.f_id, esp=request.vars['esp'], sust=row.f_sustancia, c=row.f_cantidad, e=row.f_espacio_fisico, t=row.f_Tipo)))
		links=[aceptar]
		table=SQLFORM.smartgrid(db.v_solicitud,constraints=dict(v_solicitud=query), links=links,create=False,editable=False,deletable=False,details=False,links_in_grid=True, csv=False, orderby=[~db.v_solicitud.f_id])
	elif f=='3':#Préstamos, antigua view_n
		db.t_solicitud_respuesta.f_fecha_entregado.readable=False
		db.t_solicitud_respuesta.f_fecha_recibido.readable=False
		db.t_solicitud_respuesta.f_tipo.readable=False
		db.t_solicitud_respuesta.f_espacio_fisico_d.readable=False
		db.t_solicitud_respuesta.f_solicitud.readable=False
		db.t_solicitud_respuesta.f_entregado.readable=False
		db.t_solicitud_respuesta.f_cantidad_devuelta.readable=True
		db.t_solicitud_respuesta.f_estado.readable=False
		pagos= lambda row: A('Pagos', _href=URL(c='solicitud',f='view_t', vars=dict(id=row.id, esp=request.vars['esp'], s=row.f_sustancia)))
		links=[pagos]
		query=(db.t_solicitud_respuesta.f_entregado==1)&(db.t_solicitud_respuesta.f_espacio_fisico_d==request.vars['esp'])&(db.t_solicitud_respuesta.f_tipo=='Préstamo')
		table=SQLFORM.smartgrid(db.t_solicitud_respuesta,constraints=dict(t_solicitud_respuesta=query), links=links, create=False, csv=False, editable=False, orderby=[~db.t_solicitud_respuesta.id], deletable=False, details=False)#
	elif f=='4':#Deudas, antigua view_r
		db.t_solicitud_respuesta.f_fecha_aceptado.readable=False
		db.t_solicitud_respuesta.f_fecha_recibido.readable=False
		db.t_solicitud_respuesta.f_fecha_entregado.readable=False
		db.t_solicitud_respuesta.f_espacio_fisico_s.readable=False
		db.t_solicitud_respuesta.f_solicitud.readable=False
		db.t_solicitud_respuesta.f_entregado.readable=False
		db.t_solicitud_respuesta.f_estado.readable=False
		pagos= lambda row: A('Pagar', _href=URL(c='solicitud',f='view_s', vars=dict(id=row.id, sust=row.f_sustancia, cant=row.f_cantidad, esp=row.f_espacio_fisico_s, esp1=row.f_espacio_fisico_d)))
		links=[pagos]
		query=(db.t_solicitud_respuesta.f_entregado==1)&(db.t_solicitud_respuesta.f_espacio_fisico_s==request.vars['esp'])&(db.t_solicitud_respuesta.f_tipo=='Préstamo')
		table=SQLFORM.smartgrid(db.t_solicitud_respuesta,constraints=dict(t_solicitud_respuesta=query), links=links, csv=False, editable=False, deletable=False, create=False, orderby=[~db.t_solicitud_respuesta.id] )
	return locals()

#Vista para escoger el espacio que recibe la solicitud
@auth.requires(not auth.has_membership('Usuario Normal'))
@auth.requires_login()
def view_d():
    espacios=False
    labs=False
    secciones=False
    espacios= db(db.t_espaciofisico).select(db.t_espaciofisico.ALL)
    return locals()

#Lista de solicitudes recibidas, sustituida, no necesaria
@auth.requires(not auth.has_membership('Usuario Normal'))
@auth.requires_login()

#Respuesta a una solicitud, vista desde el que responde
@auth.requires(not auth.has_membership('Usuario Normal'))
@auth.requires_login()
def view_c():
	esp=request.vars['esp']
	i=request.vars['id']
	sust=str(db(db.t_sustancias.id==request.vars['sust']).select(db.t_sustancias.f_nombre))[21:-2]
	cantidad_total=str(db(db.t_solicitud.id==request.vars['id']).select(db.t_solicitud.f_cantidad))[22:-2]
	tipo=str(db(db.t_solicitud.id==request.vars['id']).select(db.t_solicitud.f_Tipo))[18:-2]
	x = 0
	js = dict()
	aux=db((db.t_solicitud_respuesta.f_espacio_fisico_d==esp)&(db.t_solicitud_respuesta.f_solicitud==i)).select(db.t_solicitud_respuesta.f_entregado,orderby=[~db.t_solicitud_respuesta.id])
	for r in aux:
		js[x]=r.f_entregado
		x = x+1
	aux = XML(json.dumps(js))
	query=(db.t_solicitud_respuesta.f_espacio_fisico_d==esp)&(db.t_solicitud_respuesta.f_solicitud==i)
	db.t_solicitud_respuesta.f_sustancia.readable=False
	db.t_solicitud_respuesta.f_tipo.readable=False
	db.t_solicitud_respuesta.f_cantidad_devuelta_prestamo.readable=False
	if request.vars['t']=='Préstamo':
		db.t_solicitud_respuesta.f_fecha_devolucion.readable=True
	if ('new' in request.args):
		db.t_solicitud_respuesta.f_sustancia.default=request.vars['sust']
		db.t_solicitud_respuesta.f_sustancia.writable=False	
		db.t_solicitud_respuesta.f_sustancia.readable=False	
		db.t_solicitud_respuesta.f_cantidad.default=request.vars['c']
		db.t_solicitud_respuesta.f_fecha_aceptado.default=request.now
		db.t_solicitud_respuesta.f_fecha_aceptado.readable=False
		db.t_solicitud_respuesta.f_fecha_entregado.default=None
		db.t_solicitud_respuesta.f_fecha_recibido.default=None
		db.t_solicitud_respuesta.f_tipo.default=request.vars['t']
		db.t_solicitud_respuesta.f_tipo.readable=False
		db.t_solicitud_respuesta.f_tipo.writable=False
		db.t_solicitud_respuesta.f_estado.readable=False
		db.t_solicitud_respuesta.f_cantidad_devuelta_prestamo.readable=False
		db.t_solicitud_respuesta.f_cantidad_devuelta.default=0
		db.t_solicitud_respuesta.f_espacio_fisico_s.default=request.vars['e']
		db.t_solicitud_respuesta.f_espacio_fisico_d.default=esp
		db.t_solicitud_respuesta.f_solicitud.default=i
		db.t_solicitud_respuesta.f_entregado.default=0
		db.t_solicitud_respuesta.f_recibido.default=0
		mark_not_empty(db.t_solicitud_respuesta)
		if request.vars['t']=="Donación":
			db.t_solicitud_respuesta.f_cantidad.comment='Unidades en: g - mL - cm3. Los campos marcados con (*) son obligatorios'
		if request.vars['t']=="Préstamo":
			db.t_solicitud_respuesta.f_cantidad.comment='Unidades en: g - mL - cm3.'
			db.t_solicitud_respuesta.f_fecha_devolucion.comment='Los campos marcados con (*) son obligatorios'
		if request.vars['t']=='Donación':
			db.t_solicitud_respuesta.f_fecha_devolucion.default=None
		if request.vars['t']=='Préstamo':
			db.t_solicitud_respuesta.f_fecha_devolucion.readable=True
			db.t_solicitud_respuesta.f_fecha_devolucion.readable=True
			db.t_solicitud_respuesta.f_fecha_devolucion.writable=True
	if ('view' in request.args):
		db.t_solicitud_respuesta.f_fecha_entregado.readable=True
		db.t_solicitud_respuesta.f_fecha_recibido.readable=True
		db.t_solicitud_respuesta.f_fecha_devolucion.readable=False
		if request.vars['t']=='Préstamo':
			db.t_solicitud_respuesta.f_fecha_devolucion.readable=True
	if 'edit' in request.args:
		db.t_solicitud_respuesta.f_sustancia.writable=False
		db.t_solicitud_respuesta.f_fecha_aceptado.writable=False
		db.t_solicitud_respuesta.f_tipo.writable=False
		db.t_solicitud_respuesta.f_fecha_devolucion.writable=False
		if request.vars['t']=='Préstamo':
			db.t_solicitud_respuesta.f_fecha_devolucion.writable=True
	entregado=lambda row: A('Entregado', _href=URL(c='solicitud', f='add_bit_2', vars=request.vars, args=[row.id, row.f_solicitud, row.f_cantidad, row.f_sustancia, row.f_espacio_fisico_d, row.f_espacio_fisico_s]))
	links=[entregado]
	if (auth.has_membership('Usuario Normal')) | (auth.has_membership('Técnico')):
		table=SQLFORM.smartgrid(db.t_solicitud_respuesta, constraints=dict(t_solicitud_respuesta=query), links=links, csv=False,onvalidation=validar_respuesta, details=False, orderby=[~db.t_solicitud_respuesta.id], editable=False, create=False, oncreate=act_cant_respuestas, deletable=False)
	else:
		table=SQLFORM.smartgrid(db.t_solicitud_respuesta, constraints=dict(t_solicitud_respuesta=query), links=links, csv=False,onvalidation=validar_respuesta, details=False, orderby=[~db.t_solicitud_respuesta.id], editable=False, oncreate=act_cant_respuestas, deletable=False)
	return locals()
@auth.requires(not auth.has_membership('Usuario Normal'))
@auth.requires_login()
def view_e():
	esp=request.vars['esp']
	i=request.vars['id']
	x = 0
	js = dict()
	js1=dict()
	aux=db((db.t_solicitud_respuesta.f_espacio_fisico_s==esp)&(db.t_solicitud_respuesta.f_solicitud==i)).select(db.t_solicitud_respuesta.f_recibido,orderby=[~db.t_solicitud_respuesta.id])
	for r in aux:
		js[x]=r.f_recibido
		x = x+1
	x=0
	aux = XML(json.dumps(js))
	aux1=db((db.t_solicitud_respuesta.f_espacio_fisico_s==esp)&(db.t_solicitud_respuesta.f_solicitud==i)).select(db.t_solicitud_respuesta.f_entregado,orderby=[~db.t_solicitud_respuesta.id])
	for r in aux1:
		js1[x]=r.f_entregado
		x = x+1
	aux1= XML(json.dumps(js1))

	sust=str(db(db.t_sustancias.id==request.vars['s']).select(db.t_sustancias.f_nombre))[21:-2]
	cantidad_total=str(db(db.t_solicitud.id==request.vars['id']).select(db.t_solicitud.f_cantidad))[22:-2]
	cantidad_recolectada=str(db(db.t_solicitud.id==request.vars['id']).select(db.t_solicitud.f_cantidad_devuelta))[32:-2]
	tipo=1
	db.t_solicitud_respuesta.f_sustancia.readable=False
	db.t_solicitud_respuesta.f_cantidad_devuelta_prestamo.readable=False
	db.t_solicitud_respuesta.f_fecha_entregado.readable=False
	db.t_solicitud_respuesta.f_fecha_recibido.readable=False
	db.t_solicitud_respuesta.f_cantidad_devuelta.readable=False
	db.t_solicitud_respuesta.f_solicitud.readable=False
	db.t_solicitud_respuesta.f_entregado.readable=False
	db.t_solicitud_respuesta.f_espacio_fisico_s.readable=False
	db.t_solicitud_respuesta.f_espacio_fisico_d.readable=True
	db.t_solicitud_respuesta.f_tipo.readable=False
	db.t_solicitud_respuesta.f_fecha_devolucion.readable=False
	if request.vars	['t']=='Préstamo':
		db.t_solicitud_respuesta.f_fecha_devolucion.readable=True

	query=(db.t_solicitud_respuesta.f_solicitud==request.vars['id'])
	#query1=(db.t_solicitud_respuesta.f_solicitud==request.vars['id'])&(db.t_solicitud_respuesta.f_recibido==1)
	recibido= lambda row: A('Recibido', _href=URL(c='solicitud', f='add_bit_1', vars=request.vars, args=[row.id, row.f_solicitud, row.f_cantidad, row.f_sustancia, row.f_espacio_fisico_s, row.f_espacio_fisico_d, row.f_solicitud]))
	links=[recibido]
	table=SQLFORM.smartgrid(db.t_solicitud_respuesta, constraints=dict(t_solicitud_respuesta=query), links=links, csv=False, create=False, editable=False, details=False, orderby=[~db.t_solicitud_respuesta.id], deletable=False)
	#table1=SQLFORM.smartgrid(db.t_solicitud_respuesta, constraints=dict(t_solicitud_respuesta=query1), csv=False, create=False, editable=False, links_in_grid=False, deletable=False, details=False)
	return locals()
@auth.requires(not auth.has_membership('Usuario Normal'))
@auth.requires_login()
def view_f():
	#Revisar, probablemente la segunda condicion no esté haciendo nada
	espacios=db((db.t_espaciofisico.f_seccion==request.vars['secc'])&(db.t_espaciofisico.f_seccion==db.t_inventario.f_seccion)).select(db.t_espaciofisico.ALL, distinct=db.t_espaciofisico.id)
	return locals()
@auth.requires(not auth.has_membership('Usuario Normal'))
@auth.requires_login()
def view_g():
	seccion=db(db.t_seccion.f_laboratorio==request.vars['lab']).select(db.t_seccion.ALL)
	return locals()
@auth.requires(not auth.has_membership('Usuario Normal'))
@auth.requires_login()
def view_h():
    espacios=False
    labs=False
    secciones=False

    if (auth.has_membership('Gestor de Sustancias') or auth.has_membership('Director') or auth.has_membership('WebMaster')):
        espacios = db(db.t_inventario.f_espaciofisico == db.t_espaciofisico.id).select(db.t_espaciofisico.ALL,groupby=db.t_espaciofisico.id,orderby=[db.t_espaciofisico.f_seccion,db.t_espaciofisico.f_espacio])
        secciones = db(db.t_inventario.f_seccion == db.t_seccion.id).select(db.t_seccion.ALL,distinct=db.t_seccion.id)
        labs = db(db.t_inventario.f_laboratorio == db.t_laboratorio.id).select(db.t_laboratorio.ALL,distinct=db.t_laboratorio.id)
    elif (auth.has_membership('Jefe de Laboratorio') ):
        espacios = db( (db.t_laboratorio.f_jefe == auth.user.id)&(db.t_seccion.f_laboratorio == db.t_laboratorio.id)&(db.t_espaciofisico.f_seccion == db.t_seccion.id)&(db.t_espaciofisico.id == db.t_inventario.f_espaciofisico) ).select(db.t_espaciofisico.ALL,distinct=db.t_espaciofisico.id)#,orderby=db.t_espaciofisico.f_seccion)
        secciones = db((db.t_laboratorio.f_jefe == auth.user.id)&(db.t_seccion.f_laboratorio == db.t_laboratorio.id)&(db.t_seccion.id == db.t_inventario.f_seccion) ).select(db.t_seccion.ALL,distinct=db.t_seccion.id)
        labs = db(db.t_laboratorio.f_jefe == auth.user.id).select(db.t_laboratorio.ALL)
    elif (auth.has_membership('Jefe de Sección') ):
        espacios = db((db.t_espaciofisico.f_seccion == db.t_seccion.id)&(db.t_seccion.f_jefe == auth.user.id)).select(db.t_espaciofisico.ALL,orderby=[db.t_espaciofisico.f_seccion,db.t_espaciofisico.f_espacio])
        secciones = db(db.t_seccion.f_jefe == auth.user.id ).select(db.t_seccion.ALL)
    else:
        espacios = db((db.t_tecs_esp.f_tecnico == auth.user.id)&(db.t_espaciofisico.id == db.t_tecs_esp.f_espaciofisico)).select(db.t_espaciofisico.ALL,orderby=[db.t_espaciofisico.f_seccion,db.t_espaciofisico.f_espacio])
    return locals()
@auth.requires(not auth.has_membership('Usuario Normal'))
@auth.requires_login()
def view_i():
	#Revisar, probablemente la segunda condicion no esté haciendo nada
	espacios=db((db.t_espaciofisico.f_seccion==request.vars['secc'])&(db.t_espaciofisico.f_seccion==db.t_inventario.f_seccion)).select(db.t_espaciofisico.ALL, distinct=db.t_espaciofisico.id)
	return locals()
@auth.requires(not auth.has_membership('Usuario Normal'))
@auth.requires_login()
def view_j():
	seccion=db(db.t_seccion.f_laboratorio==request.vars['lab']).select(db.t_seccion.ALL)
	return locals()
@auth.requires(not auth.has_membership('Usuario Normal'))
@auth.requires_login()
def view_k():
    espacios=False
    labs=False
    secciones=False

    if (auth.has_membership('Gestor de Sustancias') or auth.has_membership('Director') or auth.has_membership('WebMaster')):
        espacios = db(db.t_inventario.f_espaciofisico == db.t_espaciofisico.id).select(db.t_espaciofisico.ALL,groupby=db.t_espaciofisico.id,orderby=[db.t_espaciofisico.f_seccion,db.t_espaciofisico.f_espacio])
        secciones = db(db.t_inventario.f_seccion == db.t_seccion.id).select(db.t_seccion.ALL,distinct=db.t_seccion.id)
        labs = db(db.t_inventario.f_laboratorio == db.t_laboratorio.id).select(db.t_laboratorio.ALL,distinct=db.t_laboratorio.id)
    elif (auth.has_membership('Jefe de Laboratorio') ):
        espacios = db( (db.t_laboratorio.f_jefe == auth.user.id)&(db.t_seccion.f_laboratorio == db.t_laboratorio.id)&(db.t_espaciofisico.f_seccion == db.t_seccion.id)&(db.t_espaciofisico.id == db.t_inventario.f_espaciofisico) ).select(db.t_espaciofisico.ALL,distinct=db.t_espaciofisico.id)#,orderby=db.t_espaciofisico.f_seccion)
        secciones = db((db.t_laboratorio.f_jefe == auth.user.id)&(db.t_seccion.f_laboratorio == db.t_laboratorio.id)&(db.t_seccion.id == db.t_inventario.f_seccion) ).select(db.t_seccion.ALL,distinct=db.t_seccion.id)
        labs = db(db.t_laboratorio.f_jefe == auth.user.id).select(db.t_laboratorio.ALL)
    elif (auth.has_membership('Jefe de Sección') ):
        espacios = db((db.t_espaciofisico.f_seccion == db.t_seccion.id)&(db.t_seccion.f_jefe == auth.user.id)).select(db.t_espaciofisico.ALL,orderby=[db.t_espaciofisico.f_seccion,db.t_espaciofisico.f_espacio])
        secciones = db(db.t_seccion.f_jefe == auth.user.id ).select(db.t_seccion.ALL)
    else:
        espacios = db((db.t_tecs_esp.f_tecnico == auth.user.id)&(db.t_espaciofisico.id == db.t_tecs_esp.f_espaciofisico)).select(db.t_espaciofisico.ALL,orderby=[db.t_espaciofisico.f_seccion,db.t_espaciofisico.f_espacio])
    return locals()
@auth.requires(not auth.has_membership('Usuario Normal'))
@auth.requires_login()
def view_l():
	#Revisar, probablemente la segunda condicion no esté haciendo nada
	espacios=db((db.t_espaciofisico.f_seccion==request.vars['secc'])&(db.t_espaciofisico.f_seccion==db.t_inventario.f_seccion)).select(db.t_espaciofisico.ALL, distinct=db.t_espaciofisico.id)
	return locals()
@auth.requires(not auth.has_membership('Usuario Normal'))
@auth.requires_login()
def view_m():
	seccion=db(db.t_seccion.f_laboratorio==request.vars['lab']).select(db.t_seccion.ALL)
	return locals()
@auth.requires(not auth.has_membership('Usuario Normal'))
@auth.requires_login()
def view_o():
    espacios=False
    labs=False
    secciones=False

    if (auth.has_membership('Gestor de Sustancias') or auth.has_membership('Director') or auth.has_membership('WebMaster')):
        espacios = db(db.t_inventario.f_espaciofisico == db.t_espaciofisico.id).select(db.t_espaciofisico.ALL,groupby=db.t_espaciofisico.id,orderby=[db.t_espaciofisico.f_seccion,db.t_espaciofisico.f_espacio])
        secciones = db(db.t_inventario.f_seccion == db.t_seccion.id).select(db.t_seccion.ALL,distinct=db.t_seccion.id)
        labs = db(db.t_inventario.f_laboratorio == db.t_laboratorio.id).select(db.t_laboratorio.ALL,distinct=db.t_laboratorio.id)
    elif (auth.has_membership('Jefe de Laboratorio') ):
        espacios = db( (db.t_laboratorio.f_jefe == auth.user.id)&(db.t_seccion.f_laboratorio == db.t_laboratorio.id)&(db.t_espaciofisico.f_seccion == db.t_seccion.id)&(db.t_espaciofisico.id == db.t_inventario.f_espaciofisico) ).select(db.t_espaciofisico.ALL,distinct=db.t_espaciofisico.id)#,orderby=db.t_espaciofisico.f_seccion)
        secciones = db((db.t_laboratorio.f_jefe == auth.user.id)&(db.t_seccion.f_laboratorio == db.t_laboratorio.id)&(db.t_seccion.id == db.t_inventario.f_seccion) ).select(db.t_seccion.ALL,distinct=db.t_seccion.id)
        labs = db(db.t_laboratorio.f_jefe == auth.user.id).select(db.t_laboratorio.ALL)
    elif (auth.has_membership('Jefe de Sección') ):
        espacios = db((db.t_espaciofisico.f_seccion == db.t_seccion.id)&(db.t_seccion.f_jefe == auth.user.id)).select(db.t_espaciofisico.ALL,orderby=[db.t_espaciofisico.f_seccion,db.t_espaciofisico.f_espacio])
        secciones = db(db.t_seccion.f_jefe == auth.user.id ).select(db.t_seccion.ALL)
    else:
        espacios = db((db.t_tecs_esp.f_tecnico == auth.user.id)&(db.t_espaciofisico.id == db.t_tecs_esp.f_espaciofisico)).select(db.t_espaciofisico.ALL,orderby=[db.t_espaciofisico.f_seccion,db.t_espaciofisico.f_espacio])
    return locals()
@auth.requires(not auth.has_membership('Usuario Normal'))
@auth.requires_login()
def view_p():
	#Revisar, probablemente la segunda condicion no esté haciendo nada
	espacios=db((db.t_espaciofisico.f_seccion==request.vars['secc'])&(db.t_espaciofisico.f_seccion==db.t_inventario.f_seccion)).select(db.t_espaciofisico.ALL, distinct=db.t_espaciofisico.id)
	return locals()
@auth.requires(not auth.has_membership('Usuario Normal'))
@auth.requires_login()
def view_q():
	seccion=db(db.t_seccion.f_laboratorio==request.vars['lab']).select(db.t_seccion.ALL)
	return locals()
@auth.requires(not auth.has_membership('Usuario Normal'))
@auth.requires_login()
def insert_deuda(form):
	espF = request.vars['esp']
	aux=db(db.t_espaciofisico.id==request.vars['esp1']).select().first()
    #espFS = str(db(db.t_espaciofisico.id == espF).select(db.t_espaciofisico.f_espacio))[27:-2]
	upd=db((db.t_inventario.f_sustancia==request.vars['sust'])&(db.t_inventario.f_espaciofisico==espF)).select().first()
	db.t_bitacora.insert(f_fechaingreso=request.now,
                                    f_sustancia=request.vars['sust'],
                                    f_proceso="Retorno de Préstamo",
                                    f_ingreso=0,
                                    f_consumo=form.vars.f_cantidad,
                                    f_cantidad=upd.f_cantidadusointerno-form.vars.f_cantidad,
                                    f_espaciofisico = espF,
                                    f_descripcion="Pago de deuda con el espacio físico: "+str(aux.f_direccion)+" - "+str(aux.f_espacio))

	a=db((db.t_bitacora.f_sustancia==request.vars['sust'])&(db.t_bitacora.f_espaciofisico==espF)).select().last()

	upd.update_record(f_cantidadusointerno=a.f_cantidad)
	upd.update_record(f_total = upd.f_cantidadusointerno+upd.f_cantidadonacion)
	solicitud_respuesta_asociada=db(db.t_solicitud_respuesta.id==request.vars['id']).select().first()
	solicitud_respuesta_asociada.update_record(f_cantidad_devuelta_prestamo=solicitud_respuesta_asociada.f_cantidad_devuelta_prestamo+form.vars.f_cantidad)
	#Actualizacion de cantidad devuelta
	#proceso=db(db.t_solicitud_respuesta.id==request.vars['id']).select().first()
	#proceso.update_record(f_cantidad_devuelta=proceso.f_cantidad_devuelta+form.vars.f_cantidad)
def act_cant_respuestas(form):
	i=request.vars['id']
	aux=db(db.t_solicitud.id==i).select().first()
	aux.update_record(f_cantidad_respuestas=aux.f_cantidad_respuestas+1)
@auth.requires(not auth.has_membership('Usuario Normal'))
@auth.requires_login()
def view_s():
	db.t_solicitud_prestamo.f_solicitud.readable=False
	db.t_solicitud_prestamo.f_fecha_recibido.readable=False
	db.t_solicitud_prestamo.f_recibido.readable=False
	db.t_solicitud_prestamo.f_sustancia.readable=False
	i=request.vars['id']
	sust=str(db(db.t_sustancias.id==request.vars['sust']).select(db.t_sustancias.f_nombre))[21:-2]
	cantidad_total=str(db(db.t_solicitud_respuesta.id==request.vars['id']).select(db.t_solicitud_respuesta.f_cantidad))[33:-2]
	cantidad_recolectada=str(db(db.t_solicitud_respuesta.id==request.vars['id']).select(db.t_solicitud_respuesta.f_cantidad_devuelta_prestamo))[51:-2]
	query=db.t_solicitud_prestamo.f_solicitud==i
	if ('new' in request.args):
		db.t_solicitud_prestamo.f_sustancia.default=request.vars['sust']
		db.t_solicitud_prestamo.f_sustancia.writable=False
		db.t_solicitud_prestamo.f_solicitud.default=request.vars['id']
		db.t_solicitud_prestamo.f_solicitud.readable=False
		db.t_solicitud_prestamo.f_solicitud.writable=False
		db.t_solicitud_prestamo.f_fecha_aceptado.default=request.now
		db.t_solicitud_prestamo.f_fecha_aceptado.readable=False
		db.t_solicitud_prestamo.f_fecha_aceptado.writable=False
		db.t_solicitud_prestamo.f_fecha_recibido.default=None
		db.t_solicitud_prestamo.f_fecha_recibido.readable=False
		db.t_solicitud_prestamo.f_fecha_recibido.writable=False
		db.t_solicitud_prestamo.f_cantidad.default=request.vars['cant']
		db.t_solicitud_prestamo.f_recibido.default=0
		db.t_solicitud_prestamo.f_recibido.writable=False
		db.t_solicitud_prestamo.f_recibido.readable=False
		mark_not_empty(db.t_solicitud_prestamo)
		db.t_solicitud_prestamo.f_cantidad.comment='Unidades en: g - mL - cm3. Los campos marcados con (*) son obligatorios'
	table=SQLFORM.smartgrid(db.t_solicitud_prestamo, constraints=dict(t_solicitud_prestamo=query), editable=False, deletable=False, csv=False, oncreate=insert_deuda, onvalidation=validar_prestamo, orderby=[~db.t_solicitud_prestamo.id], details=False)
	return locals()
@auth.requires(not auth.has_membership('Usuario Normal'))
@auth.requires_login()
def view_t():
	db.t_solicitud_prestamo.f_fecha_recibido.readable=False
	db.t_solicitud_prestamo.f_solicitud.readable=False
	db.t_solicitud_prestamo.f_recibido.readable=False
	db.t_solicitud_prestamo.f_sustancia.readable=False
	i=request.vars['id']
	x = 0
	js = dict()
	aux=db(db.t_solicitud_prestamo.f_solicitud==i).select(db.t_solicitud_prestamo.f_recibido,orderby=[~db.t_solicitud_prestamo.id])
	for r in aux:
		js[x]=r.f_recibido
		x = x+1
	aux = XML(json.dumps(js))
	sust=str(db(db.t_sustancias.id==request.vars['s']).select(db.t_sustancias.f_nombre))[21:-2]
	cantidad_total=str(db(db.t_solicitud_respuesta.id==request.vars['id']).select(db.t_solicitud_respuesta.f_cantidad))[33:-2]
	cantidad_recolectada=str(db(db.t_solicitud_respuesta.id==request.vars['id']).select(db.t_solicitud_respuesta.f_cantidad_devuelta))[42:-2]
	query=(db.t_solicitud_prestamo.f_solicitud==i)
	query1=(db.t_solicitud_prestamo.f_solicitud==i)&(db.t_solicitud_prestamo.f_recibido==1)
	recibido= lambda row: A('Recibido', _href=URL(c='solicitud', f='add_bit_3',vars=request.vars, args=[row.id, row.f_solicitud, row.f_cantidad, row.f_sustancia]))
	links=[recibido]
	table=SQLFORM.smartgrid(db.t_solicitud_prestamo, constraints=dict(t_solicitud_prestamo=query), links=links, csv=False, deletable=False, editable=False, create=False,orderby=[~db.t_solicitud_prestamo.id]	)
	#table1=SQLFORM.smartgrid(db.t_solicitud_prestamo, constraints=dict(t_solicitud_prestamo=query1), csv=False, deletable=False, editable=False, create=False)
	return locals()

@auth.requires(not auth.has_membership('Usuario Normal'))
@auth.requires_login()
#Recibido, agrega en ambas bitácoras, verifica antes de agregar en ambas bitácoras, errores posibles:
#	se recibe solo parte de la misma, el restante
#	cambia a estado recibido
def add_bit_1():
	id_solicitud=request.args[0]
	id_solicitud_asociada=request.args[1]
	cantidad=float(request.args[2])
	sustancia=int(request.args[3])
	e_solicitante=request.args[4]
	e_donante=request.args[5]
	solicitud_asociada=db(db.t_solicitud.id==id_solicitud_asociada).select().first()
	solicitud_respuesta_asociada=db(db.t_solicitud_respuesta.id==id_solicitud).select().first()
	reajuste=False
	resto=0
	if solicitud_asociada.f_cantidad<=solicitud_asociada.f_cantidad_devuelta:
		session.flash=T('Solicitud satisfecha, no puedes aceptar más respuestas.')
		redirect(URL(c='solicitud',f='view_e', vars=request.vars))
	inventario_e_donante=db((db.t_inventario.f_sustancia==sustancia)&(db.t_inventario.f_espaciofisico==e_donante)).select().first()
	inventario_e_solicitante=db((db.t_inventario.f_sustancia==sustancia)&(db.t_inventario.f_espaciofisico==e_solicitante)).select().first()
	i_e_donante=db(db.t_espaciofisico.id==e_donante).select().first()
	i_e_solicitante=db(db.t_espaciofisico.id==e_solicitante).select().first()
	if solicitud_asociada.f_cantidad<(solicitud_asociada.f_cantidad_devuelta+cantidad):
		reajuste=True
		cantidad=solicitud_asociada.f_cantidad-solicitud_asociada.f_cantidad_devuelta
		resto=solicitud_respuesta_asociada.f_cantidad-cantidad
		solicitud_respuesta_asociada.update_record(f_cantidad=cantidad)
		session.flash=T('Reajuste de cantidad realizado, ver descripcion de transaccion en bitácora para más detallles.')
	if request.vars['t']=="Donación":
		if inventario_e_donante.f_cantidadonacion<cantidad:
			session.flash=T('Actualmente, el espacio físico donante no posee suficiente cantidad para donar la sustancia.')
			redirect(URL(c='solicitud',f='view_e', vars=request.vars))
		descripcion="Donación a espacio físico: "+str(i_e_solicitante.f_direccion)+" - "+str(i_e_solicitante.f_espacio)
		if reajuste:
			descripcion="Donación a espacio físico: "+str(i_e_solicitante.f_direccion)+" - "+str(i_e_solicitante.f_espacio)+ ". Existe un excedente de "+str(resto)+" que debe ser devuelto a su unidad."
		db.t_bitacora.insert(f_fechaingreso = request.now,
                            f_sustancia = sustancia,
                            f_proceso = "Donación",
                            f_consumo = cantidad,
                            f_cantidad = 0,
                            f_espaciofisico = int(e_donante),
                            f_descripcion= descripcion)
		inventario_e_donante.update_record(f_cantidadonacion=inventario_e_donante.f_cantidadonacion-cantidad)
		inventario_e_donante.update_record(f_total=inventario_e_donante.f_cantidadonacion+inventario_e_donante.f_cantidadusointerno)
	elif request.vars['t']=="Préstamo":
		if inventario_e_donante.f_cantidadusointerno<cantidad:
			session.flash=T('Actualmente, el espacio físico dispuesto a prestar no posee suficiente cantidad para realizar la solicitud.')
			redirect(URL(c='solicitud',f='view_e', vars=request.vars))
		descripcion="Préstamo a espacio físico: "+str(i_e_solicitante.f_direccion)+" - "+str(i_e_solicitante.f_espacio)
		if reajuste:
			descripcion="Préstamo a espacio físico: "+str(i_e_solicitante.f_direccion)+" - "+str(i_e_solicitante.f_espacio)+ ". Existe un excedente de "+str(resto)+" que debe ser devuelto a su unidad."
		db.t_bitacora.insert(f_fechaingreso = request.now,
                            f_sustancia = sustancia,
                            f_proceso = "Préstamo",
                            f_consumo = cantidad,
                            f_cantidad = 0,
                            f_espaciofisico = int(e_donante),
                            f_descripcion= descripcion)
		inventario_e_donante.update_record(f_cantidadusointerno =inventario_e_donante.f_cantidadusointerno-cantidad)
		inventario_e_donante.update_record(f_total=inventario_e_donante.f_cantidadonacion+inventario_e_donante.f_cantidadusointerno)
	solicitud_respuesta_asociada.update_record(f_recibido=1)
	solicitud_respuesta_asociada.update_record(f_estado='Recibido')
	solicitud_asociada.update_record(f_cantidad_devuelta=solicitud_asociada.f_cantidad_devuelta+cantidad)
	if solicitud_asociada.f_cantidad_devuelta==solicitud_asociada.f_cantidad:
		solicitud_asociada.update_record(f_satisfecho=1)
	descripcion=str(request.vars['t'])+" del espacio físico: "+str(i_e_donante.f_direccion)+" - "+str(i_e_donante.f_espacio)
	if reajuste:
		descripcion=str(request.vars['t'])+" del espacio físico: "+str(i_e_donante.f_direccion)+" - "+str(i_e_donante.f_espacio)+" . Existe un excedente de "+str(resto)+" que debe devolver."
	db.t_bitacora.insert(f_fechaingreso=request.now,
                                    f_sustancia=sustancia,
                                    f_proceso=str(request.vars['t']),
                                    f_ingreso=cantidad,
                                    f_cantidad=0,
                                    f_espaciofisico = int(e_solicitante),
                                    f_descripcion= descripcion)
	inventario_e_solicitante.update_record(f_cantidadusointerno =inventario_e_solicitante.f_cantidadusointerno+cantidad)

	redirect(URL(c='solicitud',f='view_e', vars=request.vars))
	return dict()
@auth.requires(not auth.has_membership('Usuario Normal'))
@auth.requires_login()
#Entregado, cmabia ciertas fechas, no agrega nada a la bitácora, verifica que tienen cantidad suficiente
def add_bit_2():
	procesoID = request.args[0]
	proceso=db(db.t_solicitud_respuesta.id==procesoID).select().first()
	proceso.update_record(f_entregado=1)
	proceso.update_record(f_estado='Por Recibir')
	redirect(URL(c='solicitud',f='view_c', vars=request.vars))
	return dict()
@auth.requires(not auth.has_membership('Usuario Normal'))
@auth.requires_login()
def add_bit_3():
	#Agregar transaccion a la bitácora
	procesoID = request.args[0]
	solicitudAsociada=request.args[1]
	proceso1=db(db.t_solicitud_respuesta.id==solicitudAsociada).select().first()
	if proceso1.f_cantidad<(proceso1.f_cantidad_devuelta+float(request.args[2])):
		redirect(URL(c='solicitud',f='view_error2', vars=request.vars))

	proceso=db(db.t_solicitud_prestamo.id==procesoID).select().first()
	proceso.update_record(f_recibido=1)

	proceso=db(db.t_solicitud_respuesta.id==solicitudAsociada).select().first()
	proceso.update_record(f_cantidad_devuelta=proceso.f_cantidad_devuelta+float(request.args[2]))
	aux=db(db.t_espaciofisico.id==proceso.f_espacio_fisico_s).select().first()

	upd=db((db.t_inventario.f_sustancia==request.args[3])&(db.t_inventario.f_espaciofisico==int(proceso.f_espacio_fisico_d))).select().first()
	#a=db((db.t_bitacora.f_sustancia==request.args[3])&(db.t_bitacora.f_espaciofisico==request.args[4])).select().first()

	db.t_bitacora.insert(f_fechaingreso=request.now,
                                    f_sustancia=int(request.args[3]),
                                    f_proceso="Retorno de deuda",
                                    f_ingreso=float(request.args[2]),
                                    f_consumo=0,
                                    f_cantidad=upd.f_cantidadusointerno+float(request.args[2]),
                                    f_espaciofisico = proceso.f_espacio_fisico_d,
                                    f_descripcion="Retorno de deuda del espacio físico: "+str(aux.f_direccion)+" - "+str(aux.f_espacio))

	a=db((db.t_bitacora.f_sustancia==request.args[3])&(db.t_bitacora.f_espaciofisico==int(proceso.f_espacio_fisico_d))).select().last()

	upd.update_record(f_cantidadusointerno=a.f_cantidad)
	upd.update_record(f_total = upd.f_cantidadusointerno+upd.f_cantidadonacion)

	redirect(URL(c='solicitud',f='view_t', vars=request.vars))
	return dict()

#Problemas por resolver:
#	Refactorizar código