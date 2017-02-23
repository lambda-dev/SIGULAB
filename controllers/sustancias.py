# -*- coding: utf-8 -*-
from gluon.tools import Crud
from plugin_notemptymarker import mark_not_empty

@auth.requires(not auth.has_membership('Usuario Normal'))
@auth.requires_login()
def validar_bitacora(form):

    espF = request.vars['esp']
    sust = request.vars['sust']
    total = float(str(db((db.t_inventario.f_sustancia == sust)&(db.t_inventario.f_espaciofisico == espF)).select(db.t_inventario.f_cantidadusointerno))[33:-2])

    if form.vars.f_unidad == 'Kg':
        form.vars.f_cantidad = form.vars.f_cantidad*1000
        form.vars.f_unidad = 'g'
    elif form.vars.f_unidad == 'L':
        form.vars.f_cantidad = form.vars.f_cantidad*1000
        if db( db.t_inventario.f_sustancia == sust ).select(db.t_inventario.ALL).first().f_unidad == 'mL':
            form.vars.f_unidad = 'mL'
        else:
            form.vars.f_unidad = 'cm'+chr(0x00B3)

    if form.vars.f_unidad == 'cm3':
        form.vars.f_unidad = 'cm'+chr(0x00B3)

    if form.vars.f_cantidad == 0:
        form.errors.f_cantidad = T('Introduzca un ingreso o consumo')
    else:

        if 'edit' in request.args:
            actual = db(db.t_bitacora.id == request.args[3])
            proceso = str(actual.select(db.t_bitacora.f_proceso))[22:-2]
            actual.select().first().update_record(f_fecha = request.now)

            if proceso in ['Suministro del Almacen','Compra','Prestamo','Donacion']:
                ingreso = float(str(actual.select(db.t_bitacora.f_ingreso))[22:-2])
                delta = form.vars.f_cantidad - ingreso
                form.vars.f_ingreso = form.vars.f_cantidad
                form.vars.f_cantidad = total + delta
            else:
                consumo = float(str(actual.select(db.t_bitacora.f_consumo))[22:-2])
                delta = form.vars.f_cantidad - consumo
                form.vars.f_consumo = form.vars.f_cantidad
                form.vars.f_cantidad = total - delta

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
@auth.requires(not auth.has_membership('Usuario Normal'))
@auth.requires_login()
def validar_inventario(form):
        count = db( (db.t_inventario.f_sustancia == form.vars.f_sustancia)&(db.t_inventario.f_espaciofisico == request.vars['esp'])).count()
        if (count > 0):
            form.errors.f_sustancia = T('Ya existe esta sustancia en el inventario')


###################################################
@auth.requires(not auth.has_membership('Usuario Normal'))
@auth.requires_login()
def view_compras():
    if 'edit' in request.args or 'new' in request.args:
        mark_not_empty(db.t_facturas)

    if 'view' in request.args:
        db.t_facturas.f_sustancia.readable=True

    table = SQLFORM.smartgrid(db.t_facturas,csv=False,deletable=False)
    return locals()


###################################################
@auth.requires(not auth.has_membership('Usuario Normal'))
@auth.requires_login()
def insert_bitacora(form):
    espF = request.vars['esp']
    sust = request.vars['sust']
    new  = float(str(db((db.t_bitacora.f_sustancia == sust)&(db.t_bitacora.f_espaciofisico == espF)).select(db.t_bitacora.f_cantidad).last())[20:-2])
    row = db((db.t_inventario.f_espaciofisico == espF)&(db.t_inventario.f_sustancia == sust)).select().first()
    row.update_record(f_cantidadusointerno=new)
    row.update_record(f_total = row.f_cantidadusointerno+row.f_cantidadonacion)
    if form.vars.f_proceso == 'Compra':
        redirect(URL('sustancias','select_facturas',vars=dict(sust=sust,esp=espF)))


###################################################
@auth.requires(not auth.has_membership('Usuario Normal'))
@auth.requires_login()
def insert_inventario(form):
    espF = request.vars['esp']
    espFS = str(db(db.t_espaciofisico.id == espF).select(db.t_espaciofisico.f_espacio))[27:-2]
    db.t_bitacora.insert(f_fechaingreso=request.now,
                                    f_sustancia=form.vars.f_sustancia,
                                    f_proceso="Ingreso Inicial",
                                    f_ingreso=form.vars.f_cantidadusointerno,
                                    f_consumo=0,
                                    f_cantidad=form.vars.f_cantidadusointerno,
                                    f_espaciofisico = espF)


###################################################
@auth.requires(not auth.has_membership('Usuario Normal'))
@auth.requires_login()
def sustanciapeligrosa_manage():

    if not 'view' in request.args:
        db.t_sustancias.f_peligrosidad.represent = lambda v,r: v[0]

    if 'edit' in request.args or 'new' in request.args:
        mark_not_empty(db.t_sustancias)

    if(auth.has_membership('Gestor de Sustancias') or \
    auth.has_membership('Director') or\
    auth.has_membership('WebMaster')):
        table = SQLFORM.smartgrid(db.t_sustancias,onupdate=auth.archive,links_in_grid=False,csv=False,user_signature=True)
    else:
        table = SQLFORM.smartgrid(db.t_sustancias,editable=False,deletable=False,csv=False,links_in_grid=False,create=False,onvalidation=sustancias_validate)
    return locals()


###################################################
@auth.requires(not auth.has_membership('Usuario Normal'))
@auth.requires_login()
def select_inventario():
    espacios=False
    labs=False
    secciones=False

    if (auth.has_membership('Gestor de Sustancias') or auth.has_membership('Director') or auth.has_membership('WebMaster')):
        espacios = db(db.t_inventario.f_espaciofisico == db.t_espaciofisico.id).select(db.t_espaciofisico.ALL,groupby=db.t_espaciofisico.id,orderby=[db.t_espaciofisico.f_seccion,db.t_espaciofisico.f_espacio])
        secciones = db(db.t_inventario.f_seccion == db.t_seccion.id).select(db.t_seccion.ALL,distinct=db.t_seccion.id)
        labs = db(db.t_inventario.f_laboratorio == db.t_laboratorio.id).select(db.t_laboratorio.ALL,distinct=db.t_laboratorio.id)
    elif (auth.has_membership('Jefe de Laboratorio') ):
        espacios = db( (db.t_laboratorio.f_jefe == auth.user.id)&(db.t_seccion.f_laboratorio == db.t_laboratorio.id)&(db.t_espaciofisico.f_seccion == db.t_seccion.id)&(db.t_espaciofisico.id == db.t_inventario.f_espaciofisico) ).select(db.t_espaciofisico.ALL,distinct=db.t_espaciofisico.id)
        secciones = db((db.t_laboratorio.f_jefe == auth.user.id)&(db.t_seccion.f_laboratorio == db.t_laboratorio.id)&(db.t_seccion.id == db.t_inventario.f_seccion) ).select(db.t_seccion.ALL,distinct=db.t_seccion.id)
        labs = db(db.t_laboratorio.f_jefe == auth.user.id).select(db.t_laboratorio.ALL)
    elif (auth.has_membership('Jefe de Sección') ):
        espacios = db((db.t_espaciofisico.f_seccion == db.t_seccion.id)&(db.t_seccion.f_jefe == auth.user.id)).select(db.t_espaciofisico.ALL,orderby=[db.t_espaciofisico.f_seccion,db.t_espaciofisico.f_espacio])
        secciones = db(db.t_seccion.f_jefe == auth.user.id ).select(db.t_seccion.ALL)
    else:
        espacios = db((db.t_tecs_esp.f_tecnico == auth.user.id)&(db.t_espaciofisico.id == db.t_tecs_esp.f_espaciofisico)).select(db.t_espaciofisico.ALL,orderby=[db.t_espaciofisico.f_seccion,db.t_espaciofisico.f_espacio])

    return locals()


###################################################
@auth.requires(not auth.has_membership('Usuario Normal'))
@auth.requires_login()
def inventario_lab():

    lab = str(db(db.t_laboratorio.id == request.vars['lab']).select(db.t_laboratorio.f_nombre))[24:-2]
    query = db.v_laboratorio.f_laboratorio == str(request.vars['lab'])
    table = SQLFORM.smartgrid(db.v_laboratorio,constraints=dict(v_laboratorio=query),csv=False,editable=False,deletable=False,create=False)
    return locals()


###################################################
@auth.requires(not auth.has_membership('Usuario Normal'))
@auth.requires_login()
def inventario_seccion():

    if request.vars['secc'] == 't':
        db.v_seccion.f_seccion.readable = True
        db.v_seccion.f_sustancia.readable = False
        lab = str(db(db.t_laboratorio.id == request.vars['lab']).select(db.t_laboratorio.f_nombre))[24:-2]
        sust = str(db(db.t_sustancias.id == request.vars['sust']).select(db.t_sustancias.f_nombre))[23:-2]
        query = (db.v_seccion.f_laboratorio == request.vars['lab'])&(db.v_seccion.f_sustancia == sust)
        table = SQLFORM.smartgrid(db.v_seccion,constraints=dict(v_seccion=query),csv=False,editable=False,deletable=False,create=False)
        seccion = False
        sustancia = str(db(db.t_sustancias.id == request.vars['sust']).select(db.t_sustancias.f_nombre))[23:]
        return locals()

    sustancia = False
    secc = request.vars['secc']
    seccion = str(db(db.t_seccion.id == secc).select(db.t_seccion.f_seccion))[21:-2]
    lab = str(db(db.t_seccion.id == secc).select(db.t_seccion.f_laboratorio))[25:-2]
    query = (db.v_seccion.f_laboratorio == lab)&(db.v_seccion.f_seccion == secc)
    lab = str(db( db.t_laboratorio.id == lab ).select(db.t_laboratorio.f_nombre))[24:-2]
    table = SQLFORM.smartgrid(db.v_seccion,constraints=dict(v_seccion=query),csv=False,editable=False,deletable=False,create=False)
    return locals()


###################################################
@auth.requires(not auth.has_membership('Usuario Normal'))
@auth.requires_login()
def select_facturas():
    table = SQLFORM.factory(Field('factura',
                                requires=IS_IN_DB(db,db.t_facturas.id,'%(f_proveedor)s - %(f_numero)s',error_message='Por favor seleccione una factura o introduzca una nueva.'),
                                label=T('Factura Existente')),
                                )
    if table.process().accepted:
        fact = table.vars.factura
        sust = str(db(db.t_sustancias.id == request.vars['sust']).select(db.t_sustancias.f_nombre))[23:-2]
        row = db(db.t_facturas.id == table.vars.factura).select().first()
        if row.f_sustancia == "":
            row.update_record(f_sustancia=[sust])
        else:
            l = row.f_sustancia
            if not sust in l:
                l.append(sust)
                row.update_record(f_sustancia=l)
        redirect(URL('sustancias','view_bitacora',vars=dict(esp=request.vars['esp'],sust=request.vars['sust'] )))
    return locals()




###################################################
@auth.requires(not auth.has_membership('Usuario Normal'))
@auth.requires_login()
def new_facturas():
    table = SQLFORM.factory(Field('f_numero',label=T('Numero de Factura *'),requires=IS_NOT_EMPTY()),
                            Field('f_fecha','date',requires=IS_DATE_IN_RANGE(maximum=request.now.date(),error_message='Debe introducir una fecha menor a la actual.'),label=T('Fecha de Compra *')),
                            Field('f_proveedor','string',label=T('Proveedor *'),requires=IS_NOT_EMPTY())
                                )
    if table.process().accepted:
        fact = table.vars.f_numero
        fecha = table.vars.f_fecha
        proov = table.vars.f_proveedor

        sust = str(db(db.t_sustancias.id == request.vars['sust']).select(db.t_sustancias.f_nombre))[23:-2]
        db.t_facturas.insert(f_numero=fact,f_fecha=fecha,f_proveedor=proov,f_sustancia=[sust])
        redirect(URL('sustancias','view_bitacora',vars=dict(esp=request.vars['esp'],sust=request.vars['sust'] )))
    return locals()




###################################################
@auth.requires(not auth.has_membership('Usuario Normal'))
@auth.requires_login()
def inventario_manage():

    sustancia = False
    labs = False
    seccion = False
    espFisico = False

    espF = request.vars['esp']
    query = db.t_inventario.f_espaciofisico == espF
    db.t_inventario.f_espaciofisico.default = espF

    if 'new' in request.args:
        mark_not_empty(db.t_inventario)
        db.t_inventario.f_cantidadusointerno.comment = "Unidades en: g - mL - cm3"

    if 'edit' in request.args:

        db.t_inventario.f_sustancia.writable = False
        db.t_inventario.f_sustancia.readable = False
        db.t_inventario.f_cantidadusointerno.writable = False
        db.t_inventario.f_cantidadusointerno.readable = False

        row = db((db.t_inventario.id == request.args[3])&(db.t_sustancias.id == db.t_inventario.f_sustancia))
        inv = row.select(db.t_inventario.ALL).first()
        sust = row.select(db.t_sustancias.ALL).first().f_nombre
        usoint = inv.f_cantidadusointerno
        unid = inv.f_unidad
        donac = inv.f_cantidadonacion

        form = SQLFORM.factory(Field('cantidad','float',requires=IS_NULL_OR(IS_FLOAT_IN_RANGE(0,donac,
        error_message='Por favor introduzca una cantidad menor o igual a su cantidad de donacion disponible (%s %s)' % (donac, unid) )),
        default=0, label=T('Cantidad A Trasladar'),comment='Ingrese la cantidad de donación que desea trasladar a uso interno.'))

        if form.process().accepted:
            upd = db(db.t_inventario.id == request.args[3]).select().first()
            upd.update_record(f_cantidadonacion = upd.f_cantidadonacion - form.vars.cantidad)
            upd.update_record(f_cantidadusointerno = upd.f_cantidadusointerno + form.vars.cantidad)

            db.t_bitacora.insert(f_fechaingreso = request.now,
                                f_sustancia = row.select(db.t_inventario.ALL).first().f_sustancia,
                                f_proceso = "Traslado Donación - Uso Interno",
                                f_ingreso = form.vars.cantidad,
                                f_unidad = row.select(db.t_inventario.ALL).first().f_unidad,
                                f_cantidad = upd.f_cantidadusointerno,
                                f_espaciofisico = request.vars['esp'],
                                )

            redirect(URL('inventario_manage',vars=dict(esp=request.vars['esp'])))

    if request.vars['esp']:
        seccion = str(db((db.t_espaciofisico.id == request.vars['esp'])&(db.t_seccion.id == db.t_espaciofisico.f_seccion)).select(db.t_seccion.f_seccion))[21:-2]
        labs = str( db((db.t_seccion.f_seccion == seccion)&(db.t_laboratorio.id == db.t_seccion.f_laboratorio) ).select(db.t_laboratorio.f_nombre) )[24:-2]
        espFisico = str( db(db.t_espaciofisico.id == espF).select(db.t_espaciofisico.f_espacio) )[27:-2]

    if (request.vars['secc']):
        labs = str(db((db.t_seccion.id == request.vars['secc'])&(db.t_laboratorio.id == db.t_seccion.f_laboratorio)).select(db.t_laboratorio.f_nombre))[24:-2]
        seccion = str(db(db.t_seccion.id == request.vars['secc']).select(db.t_seccion.f_seccion))[21:]
        db.t_inventario.f_espaciofisico.readable = True
        if (request.vars['sust']):
            sustancia = str(db(db.t_sustancias.id == request.vars['sust']).select(db.t_sustancias.f_nombre))[23:]
            query = (db.t_inventario.f_seccion == request.vars['secc'])&(db.t_inventario.f_sustancia == request.vars['sust'])
            db.t_inventario.f_espaciofisico.represent = lambda value, row: A(str(db(db.t_espaciofisico.id == value).select(db.t_espaciofisico.f_direccion))[29:-2],_href=URL('sustancias','view_bitacora',vars=dict(sust=row.f_sustancia,esp=row.f_espaciofisico)))
            db.t_inventario.f_sustancia.readable = False
        else:
            query = (db.t_inventario.f_seccion == request.vars['secc'])
        table = SQLFORM.smartgrid(db.t_inventario,constraints=dict(t_inventario=query),onupdate=auth.archive,editable=(not auth.has_membership('Técnico') and not auth.has_membership('Usuario Normal')),
        orderby=[db.t_inventario.f_espaciofisico,db.t_inventario.f_sustancia],create=False,csv=False,deletable=False,links_in_grid=False)
        return locals()

    table = SQLFORM.smartgrid(db.t_inventario,constraints=dict(t_inventario=query),create=(not auth.has_membership('Técnico') and not auth.has_membership('Usuario Normal')),links_in_grid=False,csv=False,deletable=False,oncreate=insert_inventario,
    onvalidation=validar_inventario,editable=(not auth.has_membership('Técnico') and not auth.has_membership('Usuario Normal')))
    return locals()


###################################################
@auth.requires(not auth.has_membership('Usuario Normal'))
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
    unid = db(db.t_inventario.f_sustancia == sust).select(db.t_inventario.f_unidad).first().f_unidad

    if ('new' in request.args):
        db.t_bitacora.f_consumo.readable = False
        db.t_bitacora.f_consumo.writable = False
        db.t_bitacora.f_ingreso.readable = False
        db.t_bitacora.f_ingreso.writable = False
        db.t_bitacora.f_cantidad.writable = True
        if unid == 'g':
            db.t_bitacora.f_unidad.requires=IS_IN_SET(['g','Kg'])
        elif unid == 'mL':
            db.t_bitacora.f_unidad.requires=IS_IN_SET(['mL','L'])
        else:
            db.t_bitacora.f_unidad.requires=IS_IN_SET(['cm3','L'])
        mark_not_empty(db.t_bitacora)

    if ('view' in request.args):
        db.t_bitacora.f_descripcion.readable = True
        db.t_bitacora.f_cantidad.readable = False
        db.t_bitacora.f_fecha.readable = auth.has_membership('Gestor de Sustancias') or auth.has_membership('WebMaster')

    if 'edit' in request.args:
        db.t_bitacora.f_consumo.readable = False
        db.t_bitacora.f_consumo.writable = False
        db.t_bitacora.f_ingreso.readable = False
        db.t_bitacora.f_ingreso.writable = False
        db.t_bitacora.f_cantidad.writable = True
        db.t_bitacora.f_proceso.writable = False
        db.t_bitacora.f_unidad.readable = True
        db.t_bitacora.f_unidad.writable = False
        mark_not_empty(db.t_bitacora)
        row = db(db.t_bitacora.id == request.args[3]).select().first()
        if row.f_ingreso == 0:
            row.update_record(f_cantidad = row.f_consumo)
        else:
            row.update_record(f_cantidad = row.f_ingreso)

    table = SQLFORM.smartgrid(db.t_bitacora,constraints=dict(t_bitacora=query),oncreate=insert_bitacora,
    orderby=[~db.t_bitacora.f_fechaingreso,~db.t_bitacora.f_fecha],csv=False,links_in_grid=False,deletable=False,
    user_signature=True,onvalidation=validar_bitacora,paginate=10,onupdate=insert_bitacora)

    return locals()
