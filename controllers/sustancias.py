# -*- coding: utf-8 -*-
from gluon.tools import Crud

def validar_bitacora(form):
    espF = request.vars['esp']
    sust = request.vars['sust']
    total = float(str(db((db.t_inventario.f_sustancia == sust)&(db.t_inventario.f_espaciofisico == espF)).select(db.t_inventario.f_cantidadusointerno))[34:])
    if form.vars.f_consumo > total:
        form.errors.f_consumo = T('No puede consumir más de la cantidad disponible')

    if form.vars.f_consumo != 0 and form.vars.f_ingreso !=0:
        form.errors.f_consumo = T('No puede ingresar y consumir a la vez')
        form.errors.f_ingreso = T('No puede ingresar y consumir a la vez')

    if form.vars.f_consumo == 0 and form.vars.f_ingreso == 0:
        form.errors.f_consumo = T('Introduzca un ingreso o consumo')
        form.errors.f_ingreso = T('Introduzca un ingreso o consumo')


def insert_bitacora(form):
    espF = request.vars['esp']
    sust = request.vars['sust']
    new  = float(str(db((db.t_bitacora.f_sustancia == sust)&(db.t_bitacora.f_espaciofisico == espF)).select(db.t_bitacora.f_cantidad).last())[20:-2])
    row = db((db.t_inventario.f_espaciofisico == espF)&(db.t_inventario.f_sustancia == sust)).select().first()
    row.update_record(f_cantidadusointerno=new)
    row.update_record(f_total = row.f_cantidadusointerno+row.f_cantidadonacion)

@auth.requires_login()
def sustanciapeligrosa_manage():
    if(auth.has_permission('gestor','t_sustancias') or \
    auth.has_permission('director','t_sustancias')):
        table = SQLFORM.smartgrid(db.t_sustancias,onupdate=auth.archive,details=False,links_in_grid=False,csv=False,user_signature=True)
    else:
        table = SQLFORM.smartgrid(db.t_sustancias,editable=False,deletable=False,csv=False,links_in_grid=False,create=False)
    return locals()

@auth.requires_login()
def select_inventario():
    espacios=False
    labs=False
    secciones=False

    #si hay espacios fisicos
    if (auth.has_membership('Jefe de Laboratorio') ):
        espacios = db((db.t_laboratorio.f_jefe == auth.user.id)&(db.t_laboratorio.f_nombre == db.t_inventario.f_laboratorio)&(db.t_espaciofisico.id == db.t_inventario.f_espaciofisico)).select(db.t_espaciofisico.ALL,distinct=db.t_espaciofisico.id)
    elif (auth.has_membership('Jefe de Sección') ):
        espacios = db((db.t_espaciofisico.f_seccion == db.t_seccion.id)&(db.t_seccion.f_jefe == auth.user.id)).select(db.t_espaciofisico.f_espacio,db.t_espaciofisico.id)
    else:
        espacios = db(db.t_espaciofisico.f_tecnico == auth.user.id).select(db.t_espaciofisico.f_espacio, db.t_espaciofisico.id)

    #si tiene secciones
    if auth.has_membership('Jefe de Laboratorio'):
        secciones = db((db.t_laboratorio.f_jefe == auth.user.id)&(db.t_inventario.f_laboratorio == db.t_laboratorio.f_nombre)&(db.t_seccion.id == db.t_inventario.f_seccion)).select(db.t_seccion.ALL,distinct=db.t_seccion.id)
    elif auth.has_membership('Jefe de Sección'):
        secciones = db(db.t_seccion.f_jefe == auth.user.id ).select(db.t_seccion.ALL)

    #si tiene labs
    if auth.has_membership('Jefe de Laboratorio'):
        labs = db( (db.t_laboratorio.f_jefe == auth.user.id) ).select(db.t_laboratorio.ALL)
    return locals()



@auth.requires_login()
def inventario_manage():
    #cheqeuar que no agreguen lo mismo
    espF = request.vars['esp']
    query = db.t_inventario.f_espaciofisico == espF
    db.t_inventario.f_espaciofisico.default = espF
    if (request.vars['lab']):
        lab = str(db(db.t_laboratorio.id == request.vars['lab']).select(db.t_laboratorio.f_nombre))[24:-2]
        query = db.t_inventario.f_laboratorio == lab
        db.t_inventario.f_espaciofisico.readable = True
        db.t_inventario.f_seccion.readable = True
        table = SQLFORM.smartgrid(db.t_inventario,constraints=dict(t_inventario=query),editable=False,
        orderby=[db.t_inventario.f_espaciofisico,db.t_inventario.f_sustancia],create=False,csv=False,deletable=False,links_in_grid=False)

    if (request.vars['secc']):
        db.t_inventario.f_espaciofisico.readable = True
        query = (db.t_inventario.f_seccion == request.vars['secc'])
        table = SQLFORM.smartgrid(db.t_inventario,constraints=dict(t_inventario=query),onupdate=auth.archive,editable=False,
        orderby=[db.t_inventario.f_espaciofisico,db.t_inventario.f_sustancia],create=False,csv=False,deletable=False,links_in_grid=False)
        return locals()

    #if(auth.has_membership('tecnico','t_inventario')):
    table = SQLFORM.smartgrid(db.t_inventario,constraints=dict(t_inventario=query),create=False,links_in_grid=False,csv=False,editable=False,deletable=False)
    #else:
    #    table = SQLFORM.smartgrid(db.t_inventario,constraints=dict(t_inventario=query),onupdate=auth.archive)
    return locals()

@auth.requires_login()
def view_bitacora():
    sust = request.vars['sust']
    espF = request.vars['esp']
    name = str(db(db.t_sustancias.id == sust).select(db.t_sustancias.f_nombre))[22:]
    total = str(db((db.t_inventario.f_sustancia == sust)&(db.t_inventario.f_espaciofisico == espF)).select(db.t_inventario.f_cantidadusointerno))[34:]
    db.t_bitacora.f_sustancia.default = sust
    db.t_bitacora.f_espaciofisico.default = espF
    db.t_bitacora.f_espaciofisico.readable = False
    query = (db.t_bitacora.f_sustancia == sust)
    table = SQLFORM.smartgrid(db.t_bitacora,constraints=dict(t_bitacora=query),oncreate=insert_bitacora,
    orderby=~db.t_bitacora.f_fechaingreso,csv=False,links_in_grid=False,deletable=False,
    user_signature=True,onvalidation=validar_bitacora)
    return locals()