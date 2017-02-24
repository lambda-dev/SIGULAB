# -*- coding: utf-8 -*-
import time
from plugin_notemptymarker import mark_not_empty
# try something like
@auth.requires(not auth.has_membership('Usuario Normal'))
@auth.requires_login()
def index():
	return dict()

@auth.requires(not auth.has_membership('Usuario Normal'))
@auth.requires_login()


def validar_pedido(form):
	#esp=form.vars.f_espacio_fisico
	esp=request.vars['esp']
	sust=form.vars.f_sustancia
	aux=db((db.t_inventario.f_sustancia==sust) & (db.t_inventario.f_espaciofisico==esp)).count()
	if aux==0:
		form.errors.f_sustancia=T('El inventario del espacio debe contener la sustancia solicitada')

def validar_respuesta(form):
	esp=request.vars['esp']
	sust=request.vars['sust']
	tipo=request.vars['t']
	aux=db((db.t_inventario.f_sustancia==sust) & (db.t_inventario.f_espaciofisico==esp)).select()
	for i in aux:
		if tipo=="Donación":
			if i.f_cantidadonacion<(form.vars.f_cantidad):
				form.errors.f_cantidad=T('No posee sustancia suficiente para esta solicitud')
		if tipo=="Préstamo":
			if i.f_total<(form.vars.f_cantidad):
				form.errors.f_cantidad=T('No posee sustancia suficiente para esta solicitud')


def select_solicitud():
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

#Lista para hacer una solicitud solicitudes luego de acceder a un espacio fisico
def view_a():
	query=(db.t_solicitud.f_espacio_fisico==request.vars['esp'])&(db.t_solicitud.f_fecha_tope>=request.now)&(db.t_solicitud.f_cantidad>db.t_solicitud.f_cantidad_devuelta)
	query1=(db.t_solicitud.f_espacio_fisico==request.vars['esp'])&((db.t_solicitud.f_fecha_tope<request.now)|(db.t_solicitud.f_cantidad<=db.t_solicitud.f_cantidad_devuelta))
	respuesta= lambda row: A('Respuestas', _href=URL(c='solicitud', f='view_e', vars=dict(id=row.id, t=row.f_Tipo)))
	links=[respuesta]
	db.t_solicitud.f_fecha_solicitud.readable=False
	db.t_solicitud.f_espacio_fisico.readable=False
	db.t_solicitud.f_responsable.readable=False

	if ('new' in request.args):
		db.t_solicitud.f_cantidad_devuelta.readable=False
		db.t_solicitud.f_cantidad_devuelta.writable=False
		db.t_solicitud.f_cantidad_devuelta.default=0
		db.t_solicitud.f_fecha_solicitud.default=request.now
		db.t_solicitud.f_fecha_solicitud.writable=False
		db.t_solicitud.f_fecha_solicitud.readable=False
		db.t_solicitud.f_espacio_fisico.default=request.vars['esp']
		db.t_solicitud.f_espacio_fisico.writable=False
		db.t_solicitud.f_espacio_fisico.readable=False
		#db.t_solicitud.f_fecha_solicitud.readable=False

	if ('view' in request.args):
		db.t_solicitud.f_fecha_solicitud.readable=True
		db.t_solicitud.f_espacio_fisico.readable=False
		db.t_solicitud.f_responsable.readable=True

	if ('edit' in request.args):
		db.t_solicitud.f_espacio_fisico.readable=True
		db.t_solicitud.f_fecha_solicitud.readable=True
		db.t_solicitud.f_sustancia.writable=False
		db.t_solicitud.f_fecha_solicitud.writable=False
		db.t_solicitud.f_espacio_fisico.writable=False
		db.t_solicitud.f_cantidad_devuelta.writable=False
		db.t_solicitud.f_Tipo.writable=False

	table=SQLFORM.smartgrid(db.t_solicitud, constraints=dict(t_solicitud=query), links=links, csv=False, deletable=False, onvalidation=validar_pedido)
	table1=SQLFORM.smartgrid(db.t_solicitud, constraints=dict(t_solicitud=query1), csv=False, deletable=False, create=False)
	return locals()

@auth.requires(not auth.has_membership('Usuario Normal'))
@auth.requires_login()

#Vista para escoger el espacio que recibe la solicitud
def view_d():
    espacios=False
    labs=False
    secciones=False
    espacios= db(db.t_espaciofisico).select(db.t_espaciofisico.ALL)
    return locals()

#Lista de solicitudes recibidas
def view_b():
	esp=request.vars['esp']
	db.v_solicitud.f_espaciofisico.readable=False
	db.v_solicitud.f_id.readable=False
	query=db.v_solicitud.f_espaciofisico==esp
	db.t_solicitud.f_cantidad_devuelta.readable=False
	db.t_solicitud.f_responsable.readable=False
	aceptar= lambda row: A('Aceptar', _href=URL(c='solicitud',f='view_c', vars=dict(id=row.f_id, esp=request.vars['esp'], sust=row.f_sustancia, c=row.f_cantidad, e=row.f_espacio_fisico, t=row.f_Tipo)))
	links=[aceptar]
	#if ('view' in request.args):
	#	db.t_solicitud.f_responsable.readable=True

	table=SQLFORM.smartgrid(db.v_solicitud,constraints=dict(v_solicitud=query), links=links,create=False,editable=False,deletable=False,links_in_grid=True, csv=False)
	return locals()

#Respuesta a una solicitud, vista desde el que responde
def view_c():
	esp=request.vars['esp']
	i=request.vars['id']
	query=(db.t_solicitud_respuesta.f_espacio_fisico_d==esp)&(db.t_solicitud_respuesta.f_solicitud==i)
	db.t_solicitud_respuesta.f_fecha_entregado.readable=False
	db.t_solicitud_respuesta.f_fecha_recibido.readable=False
	db.t_solicitud_respuesta.f_fecha_devolucion.readable=False
	db.t_solicitud_respuesta.f_cantidad_devuelta.readable=False
	db.t_solicitud_respuesta.f_espacio_fisico_d.readable=False
	db.t_solicitud_respuesta.f_solicitud.readable=False
	db.t_solicitud_respuesta.f_entregado.readable=False
	if request.vars['t']=='Préstamo':
		db.t_solicitud_respuesta.f_fecha_devolucion.readable=True
	if ('new' in request.args):
		db.t_solicitud_respuesta.f_sustancia.default=request.vars['sust']
		db.t_solicitud_respuesta.f_sustancia.writable=False	
		db.t_solicitud_respuesta.f_cantidad.default=request.vars['c']
		db.t_solicitud_respuesta.f_fecha_aceptado.default=request.now
		db.t_solicitud_respuesta.f_fecha_aceptado.readable=False
		db.t_solicitud_respuesta.f_fecha_aceptado.writable=False
		db.t_solicitud_respuesta.f_fecha_entregado.default=None
		db.t_solicitud_respuesta.f_fecha_entregado.readable=False
		db.t_solicitud_respuesta.f_fecha_entregado.writable=False
		db.t_solicitud_respuesta.f_fecha_recibido.default=None
		db.t_solicitud_respuesta.f_fecha_recibido.readable=False
		db.t_solicitud_respuesta.f_fecha_recibido.writable=False
		db.t_solicitud_respuesta.f_tipo.default=request.vars['t']
		db.t_solicitud_respuesta.f_tipo.writable=False
		db.t_solicitud_respuesta.f_tipo.readable=False
		db.t_solicitud_respuesta.f_cantidad_devuelta.default=0
		db.t_solicitud_respuesta.f_cantidad_devuelta.readable=False
		db.t_solicitud_respuesta.f_cantidad_devuelta.writable=False
		db.t_solicitud_respuesta.f_espacio_fisico_s.default=request.vars['e']
		db.t_solicitud_respuesta.f_espacio_fisico_s.readable=False
		db.t_solicitud_respuesta.f_espacio_fisico_s.writable=False
		db.t_solicitud_respuesta.f_espacio_fisico_d.default=esp
		db.t_solicitud_respuesta.f_espacio_fisico_d.readable=False
		db.t_solicitud_respuesta.f_espacio_fisico_d.writable=False
		db.t_solicitud_respuesta.f_solicitud.default=i
		db.t_solicitud_respuesta.f_solicitud.readable=False
		db.t_solicitud_respuesta.f_solicitud.writable=False
		db.t_solicitud_respuesta.f_entregado.default=0
		db.t_solicitud_respuesta.f_entregado.readable=False
		db.t_solicitud_respuesta.f_entregado.writable=False

		if request.vars['t']=='Donación':
			db.t_solicitud_respuesta.f_fecha_devolucion.default=None
			db.t_solicitud_respuesta.f_fecha_devolucion.readable=False
			db.t_solicitud_respuesta.f_fecha_devolucion.writable=False

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
		db.t_solicitud_respuesta.f_fecha_entregado.writable=False
		db.t_solicitud_respuesta.f_fecha_recibido.writable=False
		db.t_solicitud_respuesta.f_tipo.writable=False
		db.t_solicitud_respuesta.f_cantidad_devuelta.writable=False
		db.t_solicitud_respuesta.f_espacio_fisico_d.writable=False
		db.t_solicitud_respuesta.f_espacio_fisico_s.writable=False
		db.t_solicitud_respuesta.f_solicitud.writable=False
		db.t_solicitud_respuesta.f_entregado.writable=False
		db.t_solicitud_respuesta.f_fecha_devolucion.writable=False
		if request.vars['t']=='Préstamo':
			db.t_solicitud_respuesta.f_fecha_devolucion.writable=True



	entregado=lambda row: A('Entregado', _href=URL(c='solicitud', f='add_bit_2', vars=request.vars, args=[row.id]))
	links=[entregado]
	#table=SQLFORM.smartgrid(db.t_solicitud_respuesta, constraints=dict(t_solicitud_respuesta=query), links=links, csv=False,onvalidation=validar_respuesta)
	if db(query).count()==1:
		table=SQLFORM.smartgrid(db.t_solicitud_respuesta, constraints=dict(t_solicitud_respuesta=query), links=links, csv=False,onvalidation=validar_respuesta, create=False)
	else:
		table=SQLFORM.smartgrid(db.t_solicitud_respuesta, constraints=dict(t_solicitud_respuesta=query), links=links, csv=False,onvalidation=validar_respuesta)
	return locals()

def view_e():
	db.t_solicitud_respuesta.f_fecha_entregado.readable=False
	db.t_solicitud_respuesta.f_fecha_recibido.readable=False
	db.t_solicitud_respuesta.f_cantidad_devuelta.readable=False
	db.t_solicitud_respuesta.f_solicitud.readable=False
	db.t_solicitud_respuesta.f_entregado.readable=False
	db.t_solicitud_respuesta.f_espacio_fisico_s.readable=False
	db.t_solicitud_respuesta.f_tipo.readable=False
	db.t_solicitud_respuesta.f_fecha_devolucion.readable=False
	if request.vars	['t']=='Préstamo':
		db.t_solicitud_respuesta.f_fecha_devolucion.readable=True

	query=db.t_solicitud_respuesta.f_solicitud==request.vars['id']
	recibido= lambda row: A('Recibido', _href=URL(c='solicitud', f='add_bit_1'))
	links=[recibido]
	table=SQLFORM.smartgrid(db.t_solicitud_respuesta, constraints=dict(t_solicitud_respuesta=query), links=links, csv=False, create=False, editable=False)
	return locals()

def view_f():
	#Revisar, probablemente la segunda condicion no esté haciendo nada
	espacios=db((db.t_espaciofisico.f_seccion==request.vars['secc'])&(db.t_espaciofisico.f_seccion==db.t_inventario.f_seccion)).select(db.t_espaciofisico.ALL, distinct=db.t_espaciofisico.id)
	return locals()

def view_g():
	seccion=db(db.t_seccion.f_laboratorio==request.vars['lab']).select(db.t_seccion.ALL)
	return locals()

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

def view_i():
	#Revisar, probablemente la segunda condicion no esté haciendo nada
	espacios=db((db.t_espaciofisico.f_seccion==request.vars['secc'])&(db.t_espaciofisico.f_seccion==db.t_inventario.f_seccion)).select(db.t_espaciofisico.ALL, distinct=db.t_espaciofisico.id)
	return locals()

def view_j():
	seccion=db(db.t_seccion.f_laboratorio==request.vars['lab']).select(db.t_seccion.ALL)
	return locals()

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

def view_l():
	#Revisar, probablemente la segunda condicion no esté haciendo nada
	espacios=db((db.t_espaciofisico.f_seccion==request.vars['secc'])&(db.t_espaciofisico.f_seccion==db.t_inventario.f_seccion)).select(db.t_espaciofisico.ALL, distinct=db.t_espaciofisico.id)
	return locals()

def view_m():
	seccion=db(db.t_seccion.f_laboratorio==request.vars['lab']).select(db.t_seccion.ALL)
	return locals()

def view_n():
	db.t_solicitud_respuesta.f_fecha_entregado.readable=False
	db.t_solicitud_respuesta.f_fecha_recibido.readable=False
	db.t_solicitud_respuesta.f_tipo.readable=False
	db.t_solicitud_respuesta.f_espacio_fisico_d.readable=False
	db.t_solicitud_respuesta.f_solicitud.readable=False
	db.t_solicitud_respuesta.f_entregado.readable=False
	pagos= lambda row: A('Pagos', _href=URL(c='solicitud',f='view_t', vars=dict(id=row.id)))
	links=[pagos]
	query=(db.t_solicitud_respuesta.f_entregado==1)&(db.t_solicitud_respuesta.f_espacio_fisico_d==request.vars['esp'])&(db.t_solicitud_respuesta.f_tipo=='Préstamo')
	table=SQLFORM.smartgrid(db.t_solicitud_respuesta,constraints=dict(t_solicitud_respuesta=query), links=links, create=False, csv=False, editable=False)
	return locals()

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

def view_p():
	#Revisar, probablemente la segunda condicion no esté haciendo nada
	espacios=db((db.t_espaciofisico.f_seccion==request.vars['secc'])&(db.t_espaciofisico.f_seccion==db.t_inventario.f_seccion)).select(db.t_espaciofisico.ALL, distinct=db.t_espaciofisico.id)
	return locals()

def view_q():
	seccion=db(db.t_seccion.f_laboratorio==request.vars['lab']).select(db.t_seccion.ALL)
	return locals()

def view_r():
	db.t_solicitud_respuesta.f_fecha_aceptado.readable=False
	db.t_solicitud_respuesta.f_fecha_recibido.readable=False
	db.t_solicitud_respuesta.f_fecha_entregado.readable=False
	db.t_solicitud_respuesta.f_espacio_fisico_s.readable=False
	db.t_solicitud_respuesta.f_solicitud.readable=False
	db.t_solicitud_respuesta.f_entregado.readable=False
	pagos= lambda row: A('Pagar', _href=URL(c='solicitud',f='view_s', vars=dict(id=row.id, sust=row.f_sustancia, cant=row.f_cantidad)))
	links=[pagos]
	query=(db.t_solicitud_respuesta.f_entregado==1)&(db.t_solicitud_respuesta.f_espacio_fisico_s==request.vars['esp'])&(db.t_solicitud_respuesta.f_tipo=='Préstamo')
	table=SQLFORM.smartgrid(db.t_solicitud_respuesta,constraints=dict(t_solicitud_respuesta=query), links=links, csv=False, editable=False, deletable=False, create=False )
	return locals()

def view_s():
	db.t_solicitud_prestamo.f_solicitud.readable=False
	db.t_solicitud_prestamo.f_fecha_recibido.readable=False
	db.t_solicitud_prestamo.f_recibido.readable=False
	i=request.vars['id']
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
	table=SQLFORM.smartgrid(db.t_solicitud_prestamo, constraints=dict(t_solicitud_prestamo=query), editable=False, deletable=False, csv=False)
	return locals()

def view_t():
	db.t_solicitud_prestamo.f_fecha_recibido.readable=False
	db.t_solicitud_prestamo.f_solicitud.readable=False
	db.t_solicitud_prestamo.f_recibido.readable=False
	i=request.vars['id']
	query=db.t_solicitud_prestamo.f_solicitud==i
	recibido= lambda row: A('Recibido', _href=URL(c='solicitud', f='add_bit_3'))
	links=[recibido]
	table=SQLFORM.smartgrid(db.t_solicitud_prestamo, constraints=dict(t_solicitud_prestamo=query), links=links, csv=False, deletable=False, editable=False, create=False)
	return locals()


def add_bit_1():
	return dict()

def add_bit_2():
	#Agregar transaccion a la bitácora
	procesoID = request.args[0]
	proceso=db(db.t_solicitud_respuesta.id==procesoID).select().first()
	proceso.update_record(f_entregado=1)
	#proceso.update_record(f_respuesta=time.strftime("%x %X"))
	redirect(URL(c='solicitud',f='view_c', vars=request.vars))
	return dict()

def add_bit_3():
	return dict()
