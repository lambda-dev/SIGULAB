# -*- coding: utf-8 -*-
from gluon.tools import Crud
from plugin_notemptymarker import mark_not_empty
import json

@auth.requires(not auth.has_membership('Usuario Normal'))
@auth.requires_login()
def validar_bitacora(form):

    espF = request.vars['esp']
    sust = request.vars['sust']
    total = float(str(db((db.t_inventario.f_sustancia == sust)&(db.t_inventario.f_espaciofisico == espF)).select(db.t_inventario.f_total))[22:-2])
    anterior = db((db.v_bitacora.f_fechaingreso <= form.vars.f_fechaingreso)&(db.v_bitacora.f_sustancia == sust)&(db.v_bitacora.f_espaciofisico ==espF)).select(db.v_bitacora.ALL).first()

    if anterior is None:
        disponible = 0
    else:
        disponible = anterior.f_cantidad

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

            anterior = db((db.v_bitacora.f_fechaingreso <= form.vars.f_fechaingreso)&(db.v_bitacora.f_sustancia == sust)&(db.v_bitacora.f_espaciofisico ==espF)).select(db.v_bitacora.ALL).first()
            anterior = db((db.v_bitacora.f_orden > anterior.f_orden)&(db.v_bitacora.f_sustancia == sust)&(db.v_bitacora.f_espaciofisico ==espF)).select(db.v_bitacora.ALL).first()

            if anterior is None:
                disponible = 0
            else:
                disponible = anterior.f_cantidad

            if form.vars.f_proceso in ['Suministro del Almacen','Compra','Prestamo','Donacion','Ingreso Inicial','Traslado Donación -> Uso Interno']:
                form.vars.f_ingreso = form.vars.f_cantidad
                form.vars.f_cantidad = disponible + form.vars.f_ingreso
            else:
                if form.vars.f_cantidad > disponible:
                    form.errors.f_cantidad = T('No puede consumir más de la cantidad disponible (%s)' ,disponible)
                else:
                    form.vars.f_consumo = form.vars.f_cantidad
                    form.vars.f_cantidad = disponible - form.vars.f_consumo

            # anterior_ = anterior.f_orden
            # anterior = db((db.v_bitacora.f_fechaingreso <= form.vars.f_fechaingreso)&(db.v_bitacora.f_sustancia == sust)&(db.v_bitacora.f_espaciofisico ==espF)&(db.v_bitacora.f_orden > anterior_)).select(db.v_bitacora.ALL).first()
            # if anterior is None:
            #     disponible = 0
            # else:
            #     disponible = anterior.f_cantidad
            # actual = db(db.t_bitacora.id == request.args[3])
            # proceso = str(actual.select(db.t_bitacora.f_proceso))[22:-2]
            # actual.select().first().update_record(f_fecha = request.now)
            #
            # if proceso in ['Suministro del Almacen','Compra','Prestamo','Donacion','Ingreso Inicial','Traslado Donación -> Uso Interno']:
            #     form.vars.f_ingreso = form.vars.f_cantidad
            #     form.vars.f_cantidad = disponible + form.vars.f_ingreso
            #
            # # elif proceso in ['Traslado Uso Interno -> Donación','Traslado Donación -> Uso Interno']:
            # #     pass
            # # elif proceso == 'Ingreso Inicial':
            # #     act = db((db.t_bitacora.f_espaciofisico == espF)&(db.t_bitacora.f_sustancia == sust)&(db.t_bitacora.f_proceso == 'Ingreso Inicial')).select(db.t_bitacora.ALL).first()
            # #     act_= db(db.v_bitacora.id == act.id).select(db.v_bitacora.ALL).first()
            # #     disponible = db((db.v_bitacora.f_orden > act_.f_orden)&(db.v_bitacora.f_sustancia == sust)&(db.v_bitacora.f_espaciofisico == espF)).select(db.v_bitacora.ALL).first().f_cantidad
            # #     act.update_record(f_cantidad = disponible)
            # else:
            #     form.vars.f_consumo = form.vars.f_cantidad
            #     form.vars.f_cantidad = disponible - form.vars.f_consumo

        else:
            if form.vars.f_proceso in ['Suministro del Almacen','Compra','Prestamo','Donacion','Ingreso Inicial','Traslado Donación -> Uso Interno']:
                form.vars.f_ingreso = form.vars.f_cantidad
                form.vars.f_cantidad = disponible + form.vars.f_ingreso
            else:
                if form.vars.f_cantidad > disponible:
                    form.errors.f_cantidad = T('No puede consumir más de la cantidad disponible (%s)' ,disponible)
                else:
                    form.vars.f_consumo = form.vars.f_cantidad
                    form.vars.f_cantidad = disponible - form.vars.f_consumo


###################################################
@auth.requires(not auth.has_membership('Usuario Normal'))
@auth.requires_login()
def delete_sustancias():
    db(db.t_sustancias.id == request.vars['d']).delete()
    redirect(URL('sustancias','sustanciapeligrosa_manage'))



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

    table = SQLFORM.smartgrid(db.t_facturas,csv=False,deletable=False,paginate=10)
    return locals()


###################################################
@auth.requires(not auth.has_membership('Usuario Normal'))
@auth.requires_login()
def insert_bitacora(form):

    proceso = db(db.t_bitacora.id == form.vars.id).select(db.t_bitacora.ALL).first().f_proceso

    espF = request.vars['esp']
    sust = request.vars['sust']
    num = db(db.v_bitacora.id == form.vars.id).select(db.v_bitacora.ALL).first().f_orden
    row = db(db.t_bitacora.id == form.vars.id).select(db.t_bitacora.ALL).first()
    actual = db(db.t_bitacora.id == form.vars.id).select(db.t_bitacora.ALL).first()
    actual_ = db(db.v_bitacora.id == form.vars.id).select(db.v_bitacora.ALL).first()
    ultimo = db((db.v_bitacora.f_sustancia == sust)&(db.v_bitacora.f_espaciofisico == espF)).select(db.v_bitacora.ALL).first().f_orden
    ultimo_ = db((db.v_bitacora.f_sustancia == sust)&(db.v_bitacora.f_espaciofisico == espF)).select(db.v_bitacora.ALL).first()
    siguiente_ = db((db.v_bitacora.f_espaciofisico == espF)&(db.v_bitacora.f_sustancia == sust)&(db.v_bitacora.f_orden < actual_.f_orden)).select(db.v_bitacora.ALL).last()
    anterior = db((db.v_bitacora.f_fechaingreso <= form.vars.f_fechaingreso)&(db.v_bitacora.f_sustancia == sust)&(db.v_bitacora.f_espaciofisico ==espF)).select(db.v_bitacora.ALL).first()

    if anterior is None:
        disponible = 0
    else:
        disponible = anterior.f_cantidad

    if siguiente_ is not None:
        n_actual = actual_.f_orden
        siguiente = db(db.t_bitacora.id == siguiente_.id).select(db.t_bitacora.ALL).first()

        while n_actual >= ultimo:

            value = actual.f_cantidad

            if siguiente.f_consumo == 0:
                siguiente.update_record(f_cantidad = value + siguiente.f_ingreso)
            else:
                siguiente.update_record(f_cantidad = value - siguiente.f_consumo)

            actual = siguiente
            actual_ = siguiente_
            siguiente_ = db((db.v_bitacora.f_espaciofisico == espF)&(db.v_bitacora.f_sustancia == sust)&(db.v_bitacora.f_orden < actual_.f_orden)).select(db.v_bitacora.ALL).last()

            if siguiente_ is None:
                break
            else:
                n_actual = siguiente_.f_orden
                siguiente = db(db.t_bitacora.id == siguiente_.id).select(db.t_bitacora.ALL).first()

    bit  = db((db.t_inventario.f_espaciofisico == espF)&(db.t_inventario.f_sustancia == sust)).select(db.t_inventario.ALL).first()

    x = db(db.t_bitacora.id == form.vars.id).select(db.t_bitacora.ALL).first()
    if proceso in ['Suministro del Almacen','Compra','Prestamo','Donacion','Traslado Donación -> Uso Interno','Ingreso Inicial']:
        bit.update_record(f_cantidadusointerno = ultimo_.f_cantidad - bit.f_cantidadonacion)
    else:
        bit.update_record(f_cantidadusointerno = ultimo_.f_cantidad - bit.f_cantidadonacion)
    bit.update_record(f_total = bit.f_cantidadonacion + bit.f_cantidadusointerno)

    if proceso == 'Compra':
        redirect(URL('sustancias','select_facturas',vars=dict(sust=sust,esp=espF)))


###################################################
@auth.requires(not auth.has_membership('Usuario Normal'))
@auth.requires_login()
def insert_inventario(form):
    espF = request.vars['esp']
    espFS = str(db(db.t_espaciofisico.id == espF).select(db.t_espaciofisico.f_espacio))[27:-2]
    estado = db((db.t_sustancias.id == form.vars.f_sustancia)&(db.t_estado.id == db.t_sustancias.f_estado)).select(db.t_estado.ALL).first().f_estado
    if estado == 'Sólido':
        unidad = 'g'
    elif estado == 'Líquido':
        unidad = 'mL'
    else:
        unidad = 'cm3'
    db.t_bitacora.insert(f_fechaingreso=request.now,
                                    f_sustancia=form.vars.f_sustancia,
                                    f_proceso="Ingreso Inicial",
                                    f_ingreso=form.vars.f_cantidadusointerno,
                                    f_consumo=0,
                                    f_unidad = unidad,
                                    f_cantidad=form.vars.f_cantidadusointerno + form.vars.f_cantidadonacion,
                                    f_espaciofisico = espF)


###################################################
@auth.requires(not auth.has_membership('Usuario Normal'))
@auth.requires_login()
def sustanciapeligrosa_manage():

    if not 'view' in request.args:
        db.t_sustancias.f_peligrosidad.represent = lambda v,r: v[0]

    if 'edit' in request.args or 'new' in request.args:
        mark_not_empty(db.t_sustancias)

    if(auth.has_membership('Gestor de SMyDP') or \
    auth.has_membership('WebMaster')):
        table = SQLFORM.smartgrid(db.t_sustancias,onupdate=auth.archive,links_in_grid=False,csv=False,user_signature=True,paginate=10)
    else:
        table = SQLFORM.smartgrid(db.t_sustancias,editable=False,deletable=False,csv=False,links_in_grid=False,create=False,paginate=10)
    return locals()


###################################################
@auth.requires(not auth.has_membership('Usuario Normal'))
@auth.requires_login()
def select_inventario():
    espacios=False
    labs=False
    secciones=False

    if (auth.has_membership('Gestor de SMyDP') or auth.has_membership('Director') or auth.has_membership('WebMaster')):
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

    secciones = db((db.t_laboratorio.id == request.vars['lab'])&(db.t_seccion.f_laboratorio == db.t_laboratorio.id)&(db.t_seccion.id == db.t_inventario.f_seccion)).select(db.t_seccion.ALL,distinct=db.t_seccion.id)
    lab = str(db(db.t_laboratorio.id == request.vars['lab']).select(db.t_laboratorio.f_nombre))[24:-2]
    query = db.v_laboratorio.f_laboratorio == str(request.vars['lab'])
    table = SQLFORM.smartgrid(db.v_laboratorio,constraints=dict(v_laboratorio=query),csv=False,editable=False,deletable=False,create=False,paginate=10)
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
        table = SQLFORM.smartgrid(db.v_seccion,constraints=dict(v_seccion=query),csv=False,editable=False,deletable=False,create=False,paginate=10)
        seccion = False
        sustancia = str(db(db.t_sustancias.id == request.vars['sust']).select(db.t_sustancias.f_nombre))[23:]
        espacios = False
        return locals()
    else:
        espacios = db((db.t_espaciofisico.f_seccion == request.vars['secc'])).select(db.t_espaciofisico.ALL,orderby=[db.t_espaciofisico.f_seccion,db.t_espaciofisico.f_espacio])

    sustancia = False
    secc = request.vars['secc']
    seccion = str(db(db.t_seccion.id == secc).select(db.t_seccion.f_seccion))[21:-2]
    lab = str(db(db.t_seccion.id == secc).select(db.t_seccion.f_laboratorio))[25:-2]
    query = (db.v_seccion.f_laboratorio == lab)&(db.v_seccion.f_seccion == secc)
    lab = str(db( db.t_laboratorio.id == lab ).select(db.t_laboratorio.f_nombre))[24:-2]
    table = SQLFORM.smartgrid(db.v_seccion,constraints=dict(v_seccion=query),csv=False,editable=False,deletable=False,create=False,paginate=10)
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
    js = dict()

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

        form = SQLFORM.factory(Field('tipo','string',requires=IS_IN_SET(['Traslado de Donación a Uso Interno','Traslado de Uso Intero a Donación']),
        label=T('Tipo de Transacción *')),
        Field('cantidad','float',requires= IS_NULL_OR(IS_FLOAT_IN_RANGE(0,donac,
        error_message='Por favor introduzca una cantidad menor o igual a su cantidad de donacion disponible (%s %s)' % (donac, unid) ) ) if request.post_vars.tipo == 'Traslado de Donación a Uso Interno' else IS_NULL_OR(IS_FLOAT_IN_RANGE(0,usoint,
        error_message='Por favor introduzca una cantidad menor o igual a su cantidad de uso interno disponible (%s %s)' % (usoint, unid) ) ),
        default=0, label=T('Cantidad A Trasladar *')))

        if form.process().accepted:

            upd = db(db.t_inventario.id == request.args[3]).select().first()

            if form.vars.tipo == 'Traslado de Donación a Uso Interno':
                upd.update_record(f_cantidadonacion = upd.f_cantidadonacion - form.vars.cantidad)
                upd.update_record(f_cantidadusointerno = upd.f_cantidadusointerno + form.vars.cantidad)

                db.t_bitacora.insert(f_fechaingreso = request.now,
                                    f_sustancia = row.select(db.t_inventario.ALL).first().f_sustancia,
                                    f_proceso = "Traslado Donación -> Uso Interno",
                                    f_ingreso = form.vars.cantidad,
                                    f_unidad = row.select(db.t_inventario.ALL).first().f_unidad,
                                    f_cantidad = upd.f_total,
                                    f_espaciofisico = request.vars['esp'],
                                    )

            else:
                upd.update_record(f_cantidadonacion = upd.f_cantidadonacion + form.vars.cantidad)
                upd.update_record(f_cantidadusointerno = upd.f_cantidadusointerno - form.vars.cantidad)

                db.t_bitacora.insert(f_fechaingreso = request.now,
                                    f_sustancia = row.select(db.t_inventario.ALL).first().f_sustancia,
                                    f_proceso = "Traslado Uso Interno -> Donación",
                                    f_consumo = form.vars.cantidad,
                                    f_unidad = row.select(db.t_inventario.ALL).first().f_unidad,
                                    f_cantidad = upd.f_total,
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
            datas = db((db.t_inventario.f_seccion == request.vars['secc'])&(db.t_espaciofisico.id == db.t_inventario.f_espaciofisico)).select(db.t_espaciofisico.f_espacio, db.t_espaciofisico.f_direccion)
            for data in datas:
                js[data.f_direccion]=data.f_espacio
            js = XML(json.dumps(js))
        else:
            query = (db.t_inventario.f_seccion == request.vars['secc'])
        table = SQLFORM.smartgrid(db.t_inventario,constraints=dict(t_inventario=query),onupdate=auth.archive,editable=auth.has_membership('WebMaster'),
        orderby=[db.t_inventario.f_espaciofisico,db.t_inventario.f_sustancia],create=False,csv=False,deletable=False,links_in_grid=False,paginate=10)

        return locals()

    table = SQLFORM.smartgrid(db.t_inventario,constraints=dict(t_inventario=query),create=(not auth.has_membership('Técnico') and not auth.has_membership('Usuario Normal')),links_in_grid=False,csv=False,deletable=False,oncreate=insert_inventario,
    onvalidation=validar_inventario,editable=auth.has_membership('WebMaster'),paginate=10)
    return locals()


###################################################
@auth.requires(not auth.has_membership('Usuario Normal'))
@auth.requires_login()
def view_bitacora():
    sust = request.vars['sust']
    espF = request.vars['esp']
    name = str(db(db.t_sustancias.id == sust).select(db.t_sustancias.f_nombre))[22:]
    espacio = str(db(db.t_espaciofisico.id == espF).select(db.t_espaciofisico.f_espacio))[27:]
    total = str(db((db.t_inventario.f_sustancia == sust)&(db.t_inventario.f_espaciofisico == espF)).select(db.t_inventario.f_total))[22:]
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
        db.t_bitacora.f_fecha.readable = auth.has_membership('Gestor de SMyDP') or auth.has_membership('WebMaster')

    if 'edit' in request.args:
        row = db(db.t_bitacora.id == request.args[3]).select().first()
        db.t_bitacora.f_consumo.readable = False
        db.t_bitacora.f_consumo.writable = False
        db.t_bitacora.f_ingreso.readable = False
        db.t_bitacora.f_ingreso.writable = False
        db.t_bitacora.f_cantidad.writable = True
        db.t_bitacora.f_proceso.writable = True
        db.t_bitacora.f_unidad.readable = True
        # db.t_bitacora.f_unidad.writable = False
        if not row.f_proceso in ['Suministro del Almacen','Compra','Prestamo','Donacion','Practica de Laboratorio','Tesis','Proyecto de Investigacion','Servicio de Laboratorio']:
            #db.t_bitacora.f_cantidad.writable = False
            pass
        mark_not_empty(db.t_bitacora)
        row = db(db.t_bitacora.id == request.args[3]).select().first()
        if row.f_ingreso == 0:
            row.update_record(f_cantidad = row.f_consumo)
        else:
            row.update_record(f_cantidad = row.f_ingreso)

    table = SQLFORM.smartgrid(db.t_bitacora,constraints=dict(t_bitacora=query),oncreate=insert_bitacora,
    orderby=[~db.t_bitacora.f_fechaingreso,~db.t_bitacora.f_fecha],csv=False,links_in_grid=False,deletable=False,
    user_signature=True,onvalidation=validar_bitacora,paginate=10,onupdate=insert_bitacora,editable=auth.has_membership('WebMaster'))

    return locals()


###################################################
def insert_bitacora_(_id,proceso,ingreso,consumo,sust,espf):
    espF = espf
    sust = sust
    num = db(db.v_bitacora.id == _id).select(db.v_bitacora.ALL).first().f_orden
    row = db(db.t_bitacora.id == _id).select(db.t_bitacora.ALL).first()
    actual = db(db.t_bitacora.id == _id).select(db.t_bitacora.ALL).first()
    actual_ = db(db.v_bitacora.id == _id).select(db.v_bitacora.ALL).first()
    ultimo = db((db.v_bitacora.f_sustancia == sust)&(db.v_bitacora.f_espaciofisico == espF)).select(db.v_bitacora.ALL).first().f_orden
    siguiente_ = db((db.v_bitacora.f_espaciofisico == espF)&(db.v_bitacora.f_sustancia == sust)&(db.v_bitacora.f_orden < actual_.f_orden)).select(db.v_bitacora.ALL).last()

    if siguiente_ is not None:
        n_actual = actual_.f_orden
        siguiente = db(db.t_bitacora.id == siguiente_.id).select(db.t_bitacora.ALL).first()

        while n_actual >= ultimo:

            value = actual.f_cantidad

            if siguiente.f_consumo == 0:
                siguiente.update_record(f_cantidad = value + siguiente.f_ingreso)
            else:
                siguiente.update_record(f_cantidad = value - siguiente.f_consumo)

            actual = siguiente
            actual_ = siguiente_
            siguiente_ = db((db.v_bitacora.f_espaciofisico == espF)&(db.v_bitacora.f_sustancia == sust)&(db.v_bitacora.f_orden < actual_.f_orden)).select(db.v_bitacora.ALL).last()

            if siguiente_ is None:
                break
            else:
                n_actual = siguiente_.f_orden
                siguiente = db(db.t_bitacora.id == siguiente_.id).select(db.t_bitacora.ALL).first()

    bit  = db((db.t_inventario.f_espaciofisico == espF)&(db.t_inventario.f_sustancia == sust)).select(db.t_inventario.ALL).first()

    if proceso in ['Suministro del Almacen','Compra','Prestamo','Donacion']:
        bit.update_record(f_cantidadusointerno = bit.f_cantidadusointerno + ingreso)
    else:
        bit.update_record(f_cantidadusointerno = bit.f_cantidadusointerno - consumo)

    bit.update_record(f_total = bit.f_cantidadonacion + bit.f_cantidadusointerno)

    if proceso == 'Compra':
        redirect(URL('sustancias','select_facturas',vars=dict(sust=sust,esp=espF)))

def validar_bitacora_(unidad,fechaingreso,sust,espf,cantidad,proceso,descripcion):

    espF = espf
    sust = sust
    total = float(str(db((db.t_inventario.f_sustancia == sust)&(db.t_inventario.f_espaciofisico == espF)).select(db.t_inventario.f_total))[22:-2])
    anterior = db((db.v_bitacora.f_fechaingreso <= fechaingreso)&(db.v_bitacora.f_sustancia == sust)&(db.v_bitacora.f_espaciofisico ==espF)).select(db.v_bitacora.ALL).first()

    if anterior is None:
        disponible = 0
    else:
        disponible = anterior.f_cantidad

    if unidad == 'Kg':
        cantidad = cantidad*1000
        unidad = 'g'
    elif unidad == 'L':
        cantidad = cantidad*1000
        if db( db.t_inventario.f_sustancia == sust ).select(db.t_inventario.ALL).first().f_unidad == 'mL':
            unidad = 'mL'
        else:
            unidad = 'cm'+chr(0x00B3)

    if unidad == 'cm3':
        unidad = 'cm'+chr(0x00B3)

    if cantidad == 0:
        cantidad = T('Introduzca un ingreso o consumo')
    else:

        if 'edit' in request.args:
            anterior_ = anterior.f_orden
            anterior = db((db.v_bitacora.f_fechaingreso <= fechaingreso)&(db.v_bitacora.f_sustancia == sust)&(db.v_bitacora.f_espaciofisico ==espF)&(db.v_bitacora.f_orden > anterior_)).select(db.v_bitacora.ALL).first()
            disponible = anterior.f_cantidad
            actual = db(db.t_bitacora.id == request.args[3])
            proceso = str(actual.select(db.t_bitacora.f_proceso))[22:-2]
            actual.select().first().update_record(f_fecha = request.now)

            if proceso in ['Suministro del Almacen','Compra','Prestamo','Donacion']:
                ingreso = cantidad
                cantidad = disponible + ingreso
                consumo = 0
            else:
                consumo = cantidad
                cantidad = disponible - consumo
                ingreso = 0

        else:
            if proceso in ['Suministro del Almacen','Compra','Prestamo','Donacion']:
                ingreso = cantidad
                f_cantidad = disponible + ingreso
                consumo = 0
            else:
                if cantidad > disponible:
                    cantidad = T('No puede consumir más de la cantidad disponible (%s)' ,disponible)
                else:
                    consumo = cantidad
                    cantidad = disponible - consumo
                    ingreso = 0

    _id = db((db.t_bitacora.f_sustancia==sust)&(db.t_bitacora.f_proceso == proceso)&(db.t_bitacora.f_espaciofisico == espF)&(db.t_bitacora.f_descripcion == descripcion)&(db.t_bitacora.f_fechaingreso == fechaingreso)).select(db.t_bitacora.ALL).first().id
    insert_bitacora_(_id,proceso,ingreso,consumo,sust,espf)
