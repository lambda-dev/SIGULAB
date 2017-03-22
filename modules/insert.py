# -*- coding: utf-8 -*-
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

    db.t_bitacora.insert(f_fechaingreso=fechaingreso,
                                    f_sustancia=sust,
                                    f_proceso=proceso,
                                    f_ingreso=ingreso,
                                    f_consumo=consumo,
                                    f_cantidad=cantidad,
                                    f_espaciofisico = espF,
                                    f_descripcion=descripcion,
                                    f_unidad=unidad)

    _id = db((db.t_bitacora.f_sustancia==sust)&(db.t_bitacora.f_proceso == proceso)&(db.t_bitacora.f_espaciofisico == espF)&(db.t_bitacora.f_descripcion == descripcion)&(db.t_bitacora.f_fechaingreso == fechaingreso)).select(db.t_bitacora.ALL).first().id
    insert_bitacora_(_id,proceso,ingreso,consumo,sust,espf)
