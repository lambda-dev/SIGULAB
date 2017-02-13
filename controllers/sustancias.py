# -*- coding: utf-8 -*-
from gluon.tools import Crud

@auth.requires_login()
def validar_bitacora(form):
    espF = request.vars['esp']
    sust = request.vars['sust']
    total = float(str(db((db.t_inventario.f_sustancia == sust)&(db.t_inventario.f_espaciofisico == espF)).select(db.t_inventario.f_cantidadusointerno))[33:-2])

    if form.vars.f_cantidad == 0:
        form.errors.f_cantidad = T('Introduzca un ingreso o consumo')

    if 'edit' in request.args:
        if form.vars.f_proceso in ['Suministro del Almacen','Compra','Prestamo','Donacion']:
            back =  float(str(db((db.t_bitacora.f_fechaingreso == form.vars.f_fechaingreso)&(db.t_bitacora.f_sustancia == sust)&(db.t_bitacora.f_espaciofisico == espF)).select(db.t_bitacora.f_ingreso))[21:])
            form.vars.f_ingreso = form.vars.f_cantidad
            form.vars.f_cantidad = form.vars.f_ingreso + total - back
        else:
            if form.vars.f_cantidad > total:
                form.errors.f_cantidad = T('No puede consumir más de la cantidad disponible')
            else:
                back =  float(str(db((db.t_bitacora.f_fechaingreso == form.vars.f_fechaingreso)&(db.t_bitacora.f_sustancia == sust)&(db.t_bitacora.f_espaciofisico == espF)).select(db.t_bitacora.f_consumo))[21:])
                form.vars.f_consumo = form.vars.f_cantidad
                form.vars.f_cantidad = total - form.vars.f_consumo + back

    else:

        if form.vars.f_proceso in ['Suministro del Almacen','Compra','Prestamo','Donacion']:
            form.vars.f_ingreso = form.vars.f_cantidad
            form.vars.f_cantidad = form.vars.f_ingreso + total
        else:
            if form.vars.f_cantidad > total:
                form.errors.f_cantidad = T('No puede consumir más de la cantidad disponible')
            else:
                form.vars.f_consumo = form.vars.f_cantidad
                form.vars.f_cantidad = total - form.vars.f_consumo

@auth.requires_login()
def update_bitacora(form):
        espF = request.vars['esp']
        sust = request.vars['sust']
        new  = float(str(db((db.t_bitacora.f_sustancia == sust)&(db.t_bitacora.f_espaciofisico == espF)).select(db.t_bitacora.f_cantidad).last())[20:-2])
        row = db((db.t_inventario.f_espaciofisico == espF)&(db.t_inventario.f_sustancia == sust)).select().first()
        row.update_record(f_cantidadusointerno=new)
        row.update_record(f_total = row.f_cantidadusointerno+row.f_cantidadonacion)

@auth.requires_login()
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
    if (auth.has_membership('Gestor de Sustancias') or auth.has_membership('Director') or auth.has_membership('WebMaster')):
        espacios = db(db.t_inventario.f_espaciofisico == db.t_espaciofisico.id).select(db.t_espaciofisico.ALL,groupby=db.t_espaciofisico.id)
        secciones = db(db.t_inventario.f_seccion == db.t_seccion.id).select(db.t_seccion.ALL,distinct=db.t_seccion.id)
        labs = db(db.t_inventario.f_laboratorio == db.t_laboratorio.f_nombre).select(db.t_laboratorio.ALL,distinct=db.t_laboratorio.id)
    elif (auth.has_membership('Jefe de Laboratorio') ):
        espacios = db((db.t_laboratorio.f_jefe == auth.user.id)&(db.t_laboratorio.f_nombre == db.t_inventario.f_laboratorio)&(db.t_espaciofisico.id == db.t_inventario.f_espaciofisico)).select(db.t_espaciofisico.ALL,distinct=db.t_espaciofisico.id)
        secciones = db((db.t_laboratorio.f_jefe == auth.user.id)&(db.t_inventario.f_laboratorio == db.t_laboratorio.f_nombre)&(db.t_seccion.id == db.t_inventario.f_seccion)).select(db.t_seccion.ALL,distinct=db.t_seccion.id)
        labs = db(db.t_laboratorio.f_jefe == auth.user.id).select(db.t_laboratorio.ALL)
    elif (auth.has_membership('Jefe de Sección') ):
        espacios = db((db.t_espaciofisico.f_seccion == db.t_seccion.id)&(db.t_seccion.f_jefe == auth.user.id)).select(db.t_espaciofisico.f_espacio,db.t_espaciofisico.id)
        secciones = db(db.t_seccion.f_jefe == auth.user.id ).select(db.t_seccion.ALL)
    else:
        espacios = db(db.t_espaciofisico.f_tecnico == auth.user.id).select(db.t_espaciofisico.f_espacio, db.t_espaciofisico.id)


    return locals()



@auth.requires_login()
def inventario_lab():

    lab = str(db(db.t_laboratorio.id == request.vars['lab']).select(db.t_laboratorio.f_nombre))[24:-2]
    query = db(db.t_inventario.f_laboratorio == lab)
    #db.t_inventario.f_espaciofisico.readable = True
    #db.t_inventario.f_seccion.readable = True
    table = SQLFORM.grid(query=query,groupby=db.t_inventario.f_sustancia)
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
        orderby=[db.t_inventario.f_espaciofisico,db.t_inventario.f_sustancia],create=False,csv=False,deletable=False,links_in_grid=False,groupby=db.t_inventario.f_sustancia,count=db.t_inventario.f_sustancia)
        return locals()

    table = SQLFORM.smartgrid(db.t_inventario,constraints=dict(t_inventario=query),create=(not auth.has_membership('Técnico') and not auth.has_membership('Usuario Normal')),links_in_grid=False,csv=False,editable=False,deletable=False)
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
    query = (db.t_bitacora.f_sustancia == sust)&(db.t_bitacora.f_espaciofisico == espF)

    if ('new' in request.args):
        db.t_bitacora.f_consumo.readable = False
        db.t_bitacora.f_consumo.writable = False
        db.t_bitacora.f_ingreso.readable = False
        db.t_bitacora.f_ingreso.writable = False
        db.t_bitacora.f_cantidad.writable = True

    if ('view' in request.args):
        db.t_bitacora.f_descripcion.readable = True
        db.t_bitacora.f_cantidad.readable = False

    if 'edit' in request.args:
        db.t_bitacora.f_consumo.readable = False
        db.t_bitacora.f_consumo.writable = False
        db.t_bitacora.f_ingreso.readable = False
        db.t_bitacora.f_ingreso.writable = False
        db.t_bitacora.f_cantidad.writable = True
        row = db(db.t_bitacora.id == request.args[3]).select().first()
        if row.f_ingreso == 0:
            row.update_record(f_cantidad = row.f_consumo)
        else:
            row.update_record(f_cantidad = row.f_ingreso)



    table = SQLFORM.smartgrid(db.t_bitacora,constraints=dict(t_bitacora=query),oncreate=insert_bitacora,
    orderby=~db.t_bitacora.f_fechaingreso,csv=False,links_in_grid=False,deletable=False,
    user_signature=True,onvalidation=validar_bitacora,paginate=10,onupdate=update_bitacora)



    return locals()
