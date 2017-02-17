# -*- coding: utf-8 -*-
import time
# try something like
@auth.requires(not auth.has_membership('Usuario Normal'))
@auth.requires_login()
def index():
	return dict()

@auth.requires(not auth.has_membership('Usuario Normal'))
@auth.requires_login()
def entrada():
	datos=db(db.table_solicitud.f_estado=='Pendiente')
	#datos=db(db.table_solicitud)
	fields = [db.table_solicitud.f_sustancia, db.table_solicitud.f_espaciofisico, db.table_solicitud.f_responsable,
				db.table_solicitud.f_solicitador, db.table_solicitud.f_cantidadsolicitada, db.table_solicitud.f_estado, db.table_solicitud.f_respuesta]
	headers={
		'table_solicitud.f_sustancia': 'Sustancia',
		'table_solicitud.f_espaciofisico': 'Espacio Físico',
		'table_solicitud.f_responsable': 'Solicitante',
		'table_solicitud.f_solicitador': 'Solicitador',
		'table_solicitud.f_cantidadsolicitada': 'Cantidad',
		'table_solicitud.f_estado': 'Estado',
		'table_solicitud.f_respuesta': 'Respuesta'
	}
	confirmar_como_donacion= lambda row: A('Confirmar como donación', _href=URL(c='s_entrada',f='donacion', args=[row.id]))
	confirmar_como_prestamo= lambda row: A('Confirmar como préstamo', _href=URL(c='s_entrada',f='prestamo_pendiente', args=[row.id]))
	rechazar= lambda row: A('Rechazar', _href=URL(c='s_entrada',f='rechazar', args=[row.id]))

	links = [confirmar_como_donacion, confirmar_como_prestamo, rechazar]

	form = SQLFORM.grid(query=datos, fields=fields, headers=headers, create=False, deletable=False, editable=False, details=False, csv=False, links=links)

	datos1=db((db.table_solicitud.f_estado =='Donado')|(db.table_solicitud.f_estado =='Prestado')|(db.table_solicitud.f_estado=='Rechazado'))
	form1 = SQLFORM.grid(query=datos1, fields=fields, headers=headers, create=False, deletable=False, editable=False, details=False, csv=False)
	return locals()

@auth.requires(not auth.has_membership('Usuario Normal'))
@auth.requires_login()
def salida():
	datos=db(db.table_solicitud.f_estado=='Pendiente')
	#datos=db(db.table_solicitud)
	fields = [db.table_solicitud.f_sustancia, db.table_solicitud.f_espaciofisico, db.table_solicitud.f_responsable,
				db.table_solicitud.f_solicitador, db.table_solicitud.f_cantidadsolicitada, db.table_solicitud.f_estado]
	headers={
		'table_solicitud.f_sustancia': 'Sustancia',
		'table_solicitud.f_espaciofisico': 'Espacio Físico',
		'table_solicitud.f_responsable': 'Solicitante',
		'table_solicitud.f_solicitador': 'Solicitador',
		'table_solicitud.f_cantidadsolicitada': 'Cantidad',
		'table_solicitud.f_estado': 'Estado'
	}
	cancelar= lambda row: A('Cancelar', _href=URL(c='s_entrada',f='cancelar', args=[row.id]))

	links = [cancelar]

	form = SQLFORM.grid(query=datos, fields=fields, headers=headers, deletable=False, editable=False, details=False, csv=False, links=links)
	datos1=db((db.table_solicitud.f_estado =='Donado')|(db.table_solicitud.f_estado =='Prestado')|(db.table_solicitud.f_estado=='Rechazado')|(db.table_solicitud.f_estado=='Cancelado'))
	form1 = SQLFORM.grid(query=datos1, fields=fields, headers=headers, create=False, deletable=False, editable=False, details=False, csv=False)
	return locals()

@auth.requires(not auth.has_membership('Usuario Normal'))
@auth.requires_login()
def p_por_devolver():
	datos=db(db.table_solicitud.f_estado=='Préstamo/Pendiente')
	#datos=db(db.table_solicitud)
	fields = [db.table_solicitud.f_sustancia, db.table_solicitud.f_espaciofisico, db.table_solicitud.f_responsable,
				db.table_solicitud.f_solicitador, db.table_solicitud.f_cantidadsolicitada, db.table_solicitud.f_estado]
	headers={
		'table_solicitud.f_sustancia': 'Sustancia',
		'table_solicitud.f_espaciofisico': 'Espacio Físico',
		'table_solicitud.f_responsable': 'Solicitante',
		'table_solicitud.f_solicitador': 'Solicitador',
		'table_solicitud.f_cantidadsolicitada': 'Cantidad',
		'table_solicitud.f_estado': 'Estado'
	}

	form = SQLFORM.grid(query=datos, fields=fields, headers=headers, deletable=False, editable=False, details=False, csv=False)

	datos1=db((db.table_solicitud.f_estado =='Préstamo/Devuelto'))
	form1 = SQLFORM.grid(query=datos1, fields=fields, headers=headers, create=False, deletable=False, editable=False, details=False, csv=False)
	return locals()

@auth.requires(not auth.has_membership('Usuario Normal'))
@auth.requires_login()
def p_por_recibir():
	datos=db(db.table_solicitud.f_estado=='Préstamo/Pendiente')
	#datos=db(db.table_solicitud)
	fields = [db.table_solicitud.f_sustancia, db.table_solicitud.f_espaciofisico, db.table_solicitud.f_responsable,
				db.table_solicitud.f_solicitador, db.table_solicitud.f_cantidadsolicitada, db.table_solicitud.f_estado]
	headers={
		'table_solicitud.f_sustancia': 'Sustancia',
		'table_solicitud.f_espaciofisico': 'Espacio Físico',
		'table_solicitud.f_responsable': 'Solicitante',
		'table_solicitud.f_solicitador': 'Solicitador',
		'table_solicitud.f_cantidadsolicitada': 'Cantidad',
		'table_solicitud.f_estado': 'Estado'
	}
	devuelto= lambda row: A('Confirmar devolución', _href=URL(c='s_entrada',f='prestamo_devuelto', args=[row.id]))

	links = [devuelto]

	form = SQLFORM.grid(query=datos, fields=fields, headers=headers, deletable=False, editable=False, details=False, csv=False, links=links)
	datos1=db((db.table_solicitud.f_estado =='Préstamo/Devuelto'))
	form1 = SQLFORM.grid(query=datos1, fields=fields, headers=headers, create=False, deletable=False, editable=False, details=False, csv=False)
	return locals()

@auth.requires(not auth.has_membership('Usuario Normal'))
@auth.requires_login()
def donacion():
	procesoID = request.args[0]
	proceso=db(db.table_solicitud.id==procesoID).select().first()
	proceso.update_record(f_estado='Donado')
	proceso.update_record(f_respuesta=time.strftime("%x %X"))
	redirect(URL(c='s_entrada',f='entrada'))
	return dict()

@auth.requires(not auth.has_membership('Usuario Normal'))
@auth.requires_login()
def prestamo_pendiente():
	procesoID = request.args[0]
	proceso=db(db.table_solicitud.id==procesoID).select().first()
	proceso.update_record(f_estado='Préstamo/Pendiente')
	redirect(URL(c='s_entrada',f='entrada'))
	return dict()

@auth.requires(not auth.has_membership('Usuario Normal'))
@auth.requires_login()
def prestamo_devuelto():
	procesoID = request.args[0]
	proceso=db(db.table_solicitud.id==procesoID).select().first()
	proceso.update_record(f_estado='Préstamo/Devuelto')
	redirect(URL(c='s_entrada',f='p_por_recibir'))
	return dict()

@auth.requires(not auth.has_membership('Usuario Normal'))
@auth.requires_login()
def rechazar():
	procesoID = request.args[0]
	proceso=db(db.table_solicitud.id==procesoID).select().first()
	proceso.update_record(f_estado='Rechazado')
	redirect(URL(c='s_entrada',f='entrada'))
	return dict()

@auth.requires(not auth.has_membership('Usuario Normal'))
@auth.requires_login()
def cancelar():
	procesoID = request.args[0]
	proceso=db(db.table_solicitud.id==procesoID).select().first()
	proceso.update_record(f_estado='Cancelado')
	redirect(URL(c='s_entrada',f='salida'))
	return dict()
