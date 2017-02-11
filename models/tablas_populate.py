def Popukatte():

    ################
    #auth_group
    if db(auth_group).isempty():
        db.auth_group.insert(role='Director',description='Director de la Unidad de Laboratorio')
        db.auth_group.insert(role='Administrador Personal',description='Administrador de Personal')
        db.auth_group.insert(role='Gestor de Sustancias',description='Gestor de Sustancias')
        db.auth_group.insert(role='Jefe de Laboratorio',description='Jefe de Laboratorio')
        db.auth_group.insert(role='Jefe de Sección',description='Jefe de Sección')
        db.auth_group.insert(role='Técnico',description='Técnico de Laboratorio')
        db.auth_group.insert(role='Usuario',description='Rol default de registro. No puede acceder a nada.')

    if db(auth_user).isempty():
        db.auth_user.insert(first_name='Super',last_name='Usuario',email='webmaster@sigulab.com',password='0000')
        db.auth_membership.insert(user_id=(db(db.auth_user.email == 'webmaster@sigulab.com').select(db.auth_user.id).first()),\
            group_id=db(db.auth_group.role == "WebMaster").select(db.auth_group.id).first());
    ################
    #auth_group
    if db(auth_permission).isempty():
        db.auth_permission.insert(name='director',table_name='t_sustanciapeligrosa',
                                group_id=db(db.auth_group.role == "Director").select(db.auth_group.id))
        db.auth_permission.insert(name='gestor',table_name='t_sustanciapeligrosa',
                                group_id=db(db.auth_group.role == "Gestor de Sustancias").select(db.auth_group.id))
        db.auth_permission.insert(name='tecnico',table_name='t_inventario',
                                group_id=db(db.auth_group.role == "Técnico").select(db.auth_group.id))

    ################
    #t_materiales
    db.t_materiales.f_nombre.requires = IS_NOT_IN_DB(db,db.t_materiales.f_nombre)

    ################
    #t_estado
    if db(db.t_estado).isempty():
        db.t_estado.insert(f_estado='Sólido')
        db.t_estado.insert(f_estado='Líquido')
        db.t_estado.insert(f_estado='Gaseoso')

    ################
    #t_laboratorio
    db.t_laboratorio.f_jefe.requires = IS_IN_DB(db,db.auth_user.id,'%(first_name)s %(last_name)s')

    ################
    #t_seccion
    db.t_seccion.f_jefe.requires = IS_IN_DB(db,db.auth_user.id,'%(first_name)s %(last_name)s')
    db.t_seccion.f_laboratorio.requires=IS_IN_DB(db,db.t_laboratorio,'%(f_nombre)s',represent=lambda value,row:\
                                    str(db(db.t_laboratorio.id == value).select(db.t_laboratorio.f_nombre)))[23:]

    #################
    #t_espaciofisico
    db.t_espaciofisico.f_seccion.requires = IS_IN_DB(db,db.t_seccion.id,'%(f_laboratorio)s, seccion %(f_seccion)s')
    db.t_espaciofisico.f_tecnico.requires = IS_IN_DB(db,db.auth_user.id,'%(first_name)s %(last_name)s')

    ################
    #t_inventario
    db.t_inventario.cantidadusointerno.default = 0
    db.t_inventario.f_sustancia.requires = IS_IN_DB(db,db.t_materiales.id,'%(f_nombre)s')
    db.t_inventario.f_sustancia.notnull = True
    db.t_inventario.f_espaciofisico.requires =  IS_IN_DB(db,db.t_espaciofisico.id,'%(f_espacio)s')
    db.t_inventario.f_espaciofisico.notnull = True
    db.t_inventario.f_espaciofisico.represent = represent= lambda value,row: str(db(db.t_espaciofisico.id == value).select(db.t_espaciofisico.f_espacio))[27:]
    db.t_inventario.f_sustancia.represent = lambda name,row: A(str(db(db.t_materiales.id==name).select(db.t_materiales.f_nombre))[22:],
                                            _href=URL('sustancias','view_bitacora',vars=dict(sust=row.f_sustancia)))
    #################
    #t_bitacora
    db.t_bitacora.id.readable = False
    db.t_bitacora.f_sustancia.readable=False
    db.t_bitacora.f_sustancia.writable=False
    db.t_bitacora.f_sustancia.requires = IS_IN_DB(db,db.t_materiales.id,'%(f_nombre)s')
    db.t_bitacora.f_sustancia.notnull = True
    db.t_bitacora.f_sustancia = lambda f_sustancia,row: str(db(db.t_materiales.id == f_sustancia).select(db.t_materiales.f_nombre))[22:]
    db.t_bitacora.f_cantidad.writable = False
    db.t_bitacora.f_cantidad.default = 0
    db.t_bitacora.f_fecha.writable = False
    db.t_bitacora.f_fecha.readable = False
    db.t_bitacora.f_fecha.default = request.now
    db.t_bitacora.f_espaciofisico.requires = IS_IN_DB(db,db.t_espaciofisico.id,'%(f_espacio)s')
    db.t_bitacora.f_espaciofisico.represent = lambda value,row: str(db(db.t_espaciofisico.id == value).select(db.t_espaciofisico.f_espacio))[26:]
    db.t_bitacora.f_espaciofisico.writable = False
    db.t_bitacora.f_espaciofisico.notnull = True

    #################
    #t_sustanciapeligrosa
    db.t_sustanciapeligrosa.id.readable=False
    db.t_sustanciapeligrosa.id.writable=False
    db.t_sustanciapeligrosa.f_cas.readable = False
    db.t_sustanciapeligrosa.f_cas.writable = False
    db.t_sustanciapeligrosa.f_cas.default = lambda value,row: str(db(db.t_materiales.id == row.f_nombre).select(db.t_materiales.f_cas))[19:]
    db.t_sustanciapeligrosa.f_nombre.requires = IS_IN_DB(db,db.t_materiales,'%(f_nombre)s')
    db.t_sustanciapeligrosa.f_nombre.represent = lambda value,row: str(db(db.t_materiales.id==value).select(db.t_materiales.f_nombre))[22:]
    db.t_sustanciapeligrosa.f_pureza.requires = IS_INT_IN_RANGE(0, 101)
    db.t_sustanciapeligrosa.f_estado.requires=IS_IN_DB(db,db.t_estado.f_estado,'%(f_estado)s')
