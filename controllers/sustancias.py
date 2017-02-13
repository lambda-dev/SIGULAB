# -*- coding: utf-8 -*-
from gluon.tools import Crud

###################################################
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


###################################################
@auth.requires_login()
def update_bitacora(form):
        espF = request.vars['esp']
        sust = request.vars['sust']
        new  = float(str(db((db.t_bitacora.f_sustancia == sust)&(db.t_bitacora.f_espaciofisico == espF)).select(db.t_bitacora.f_cantidad).last())[20:-2])
        row = db((db.t_inventario.f_espaciofisico == espF)&(db.t_inventario.f_sustancia == sust)).select().first()
        row.update_record(f_cantidadusointerno=new)
        row.update_record(f_total = row.f_cantidadusointerno+row.f_cantidadonacion)


###################################################
@auth.requires_login()
def insert_bitacora(form):
    espF = request.vars['esp']
    sust = request.vars['sust']
    new  = float(str(db((db.t_bitacora.f_sustancia == sust)&(db.t_bitacora.f_espaciofisico == espF)).select(db.t_bitacora.f_cantidad).last())[20:-2])
    row = db((db.t_inventario.f_espaciofisico == espF)&(db.t_inventario.f_sustancia == sust)).select().first()
    row.update_record(f_cantidadusointerno=new)
    row.update_record(f_total = row.f_cantidadusointerno+row.f_cantidadonacion)


###################################################
@auth.requires_login()
def sustanciapeligrosa_manage():
    if(auth.has_permission('gestor','t_sustancias') or \
    auth.has_permission('director','t_sustancias')):
        table = SQLFORM.smartgrid(db.t_sustancias,onupdate=auth.archive,details=False,links_in_grid=False,csv=False,user_signature=True)
    else:
        table = SQLFORM.smartgrid(db.t_sustancias,editable=False,deletable=False,csv=False,links_in_grid=False,create=False)
    return locals()


###################################################
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


###################################################
@auth.requires_login()
def inventario_lab():

    lab = str(db(db.t_laboratorio.id == request.vars['lab']).select(db.t_laboratorio.f_nombre))[24:-2]
    query = db.v_laboratorio.f_laboratorio == lab
    table = SQLFORM.smartgrid(db.v_laboratorio,constraints=dict(v_laboratorio=query),csv=False,editable=False,deletable=False,create=False)
    return locals()


###################################################
@auth.requires_login()
def inventario_seccion():

    if request.vars['secc'] == 't':
        db.v_seccion.f_seccion.readable = True
        db.v_seccion.f_sustancia.readable = False
        lab = str(db(db.t_laboratorio.id == request.vars['lab']).select(db.t_laboratorio.f_nombre))[24:-2]
        query = (db.v_seccion.f_laboratorio == lab)&(db.v_seccion.f_sustancia == request.vars['sust'])
        table = SQLFORM.smartgrid(db.v_seccion,constraints=dict(v_seccion=query),csv=False,editable=False,deletable=False,create=False)
        seccion = False
        sustancia = str(db(db.t_sustancias.id == request.vars['sust']).select(db.t_sustancias.f_nombre))[23:]
        return locals()

    sustancia = False
    secc = request.vars['secc']
    seccion = str(db(db.t_seccion.id == secc).select(db.t_seccion.f_seccion))[21:-2]
    lab = str(db(db.t_seccion.id == secc).select(db.t_seccion.f_laboratorio))[25:-2]
    query = (db.v_seccion.f_laboratorio == lab)&(db.v_seccion.f_seccion == secc)
    table = SQLFORM.smartgrid(db.v_seccion,constraints=dict(v_seccion=query),csv=False,editable=False,deletable=False,create=False)
    return locals()


###################################################
@auth.requires_login()
def inventario_manage():
    #cheqeuar que no agreguen lo mismo
    sustancia = False
    labs = False
    seccion = False

    espF = request.vars['esp']
    query = db.t_inventario.f_espaciofisico == espF
    db.t_inventario.f_espaciofisico.default = espF

    if request.vars['esp']:
        seccion = int(str(db((db.t_espaciofisico.f_seccion == request.vars['esp'])&(db.t_seccion.id == db.t_espaciofisico.f_seccion)).select(db.t_seccion.f_seccion))[21:-2])
        labs = str( db((db.t_seccion.id == seccion) ).select(db.t_seccion.f_laboratorio) )[25:-2]

    if (request.vars['secc']):
        labs = str(db(db.t_seccion.id == request.vars['secc']).select(db.t_seccion.f_laboratorio))[25:]
        seccion = str(db(db.t_seccion.id == request.vars['secc']).select(db.t_seccion.f_seccion))[21:]
        db.t_inventario.f_espaciofisico.readable = True
        if (request.vars['sust']):
            sustancia = str(db(db.t_sustancias.id == request.vars['sust']).select(db.t_sustancias.f_nombre))[23:]
            query = (db.t_inventario.f_seccion == request.vars['secc'])&(db.t_inventario.f_sustancia == request.vars['sust'])
        else:
            query = (db.t_inventario.f_seccion == request.vars['secc'])#&(db.t_inventario.f_sustancia == request.vars['sust'])
        table = SQLFORM.smartgrid(db.t_inventario,constraints=dict(t_inventario=query),onupdate=auth.archive,editable=False,
        orderby=[db.t_inventario.f_espaciofisico,db.t_inventario.f_sustancia],create=False,csv=False,deletable=False,links_in_grid=False)
        return locals()

    table = SQLFORM.smartgrid(db.t_inventario,constraints=dict(t_inventario=query),create=(not auth.has_membership('Técnico') and not auth.has_membership('Usuario Normal')),links_in_grid=False,csv=False,editable=False,deletable=False)
    return locals()


###################################################
@auth.requires_login()
def view_bitacora():
    sust = request.vars['sust']
    espF = request.vars['esp']
    name = str(db(db.t_sustancias.id == sust).select(db.t_sustancias.f_nombre))[22:]
    espacio = str(db(db.t_espaciofisico.id == espF).select(db.t_espaciofisico.f_espacio))[27:]
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
