# -*- coding: utf-8 -*-
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
                 (db.t_inventario.f_cantidadusointerno + db.t_inventario.f_cantidadonacion),
                 )
        table = SQLTABLE(rows, headers='fieldname:capitalize', _width="100%")
    else:
        table = SQLFORM.smartgrid(db.t_inventario,onupdate=auth.archive)
    return locals()
