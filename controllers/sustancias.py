# -*- coding: utf-8 -*-
from gluon.tools import Crud

@auth.requires_login()
def sustanciapeligrosa_manage():
    if(auth.has_permission('gestor','t_sustanciapeligrosa') or \
    auth.has_permission('director','t_sustanciapeligrosa')):
        table = SQLFORM.smartgrid(db.t_sustanciapeligrosa,onupdate=auth.archive)
    else:
        rows = db(db.t_sustanciapeligrosa).select(db.t_sustanciapeligrosa.f_nombre,
                                                  db.t_sustanciapeligrosa.f_cas,
                                                  db.t_sustanciapeligrosa.f_pureza,
                                                  db.t_sustanciapeligrosa.f_estado,
                                                  db.t_sustanciapeligrosa.f_control,
                                                  db.t_sustanciapeligrosa.f_peligrosidad)
        table = SQLTABLE(rows, headers='fieldname:capitalize',orderby=db.t_sustanciapeligrosa.f_pureza, _width="100%")
    return locals()

@auth.requires_login()
def inventario_manage():
    if(auth.has_permission('tecnico','t_inventario')):

        rows = db(
            (db.t_espaciofisico.f_tecnico == auth.user.id)&
            (db.t_espaciofisico.id == db.t_inventario.f_espaciofisico)
        ).select(db.t_inventario.f_sustancia,
                 db.t_inventario.f_cantidadusointerno,
                 db.t_inventario.f_cantidadonacion,
                 db.t_inventario.f_total,
                 )
        table = SQLTABLE(rows, headers='fieldname:capitalize', _width="100%")
    else:
        table = SQLFORM.smartgrid(db.t_inventario,onupdate=auth.archive)
    return locals()

@auth.requires_login()
def view_bitacora():
    sust = request.args[0]
    name = str(db(db.t_materiales.id == sust).select(db.t_materiales.f_nombre))[22:]
    #for row in db((db.t_bitacora.f_sustancia == name)&
    #            (db.t_bitacora.espaciofisico == db.t_inventario.espaciofisico)).select(db.t_inventario.ALL,db.t_bitacora.cantidad):

    rows = db(db.t_bitacora.f_sustancia == sust).select(db.t_bitacora.f_fecha,
    db.t_bitacora.f_proceso,db.t_bitacora.f_ingreso,db.t_bitacora.f_consumo,db.t_bitacora.f_cantidad)
    table = SQLTABLE(rows, headers='fieldname:capitalize', _width="100%")
    return locals()
