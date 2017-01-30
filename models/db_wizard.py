### we prepend t_ to tablenames and f_ to fieldnames for disambiguity


########################################
#db.define_table('t_cargo',
#    Field('f_nombreCar','string',label=T('Nombre')),
#    Field('f_permiso','string',label=T('Permiso')),
#    format='%(f_nombreCar)s',
#    migrate=settings.migrate)

#db.define_table('t_cargo_archive',db.t_cargo,Field('current_record','reference t_cargo',readable=False,writable=False))
########################################
db.define_table('t_materiales',
               Field('f_nombre','string',readable=False,writable=False,requires=IS_NOT_EMPTY()),
               format='%(f_nombre)s')
db.t_materiales.f_nombre.requires=IS_NOT_IN_DB(db,db.t_materiales.f_nombre)

########################################
db.define_table('t_estado',
               Field('f_estado','string',readable=False,writable=False),
               format='%(f_estado)s')

########################################
db.define_table('t_laboratorio',
    Field('f_nombre', 'string', notnull=True, label=T('Nombre')),
    Field('f_jefe','integer', requires=IS_IN_DB(db,db.auth_user.id,'%(first_name)s %(last_name)s'), label=T('Jefe de Laboratorio')),
    format='%(f_nombre)s',
    migrate=settings.migrate)

db.define_table('t_laboratorio_archive',db.t_laboratorio,Field('current_record','reference t_laboratorio',readable=False,writable=False))

########################################
db.define_table('t_seccion',
    Field('f_seccion','string',requires=IS_NOT_EMPTY(),label=T('Sección')),
    Field('f_laboratorio','string',requires=IS_IN_DB(db,db.t_laboratorio.f_nombre,'%(f_nombre)s'), label=T('Laboratorio')),
    Field('f_jefe','integer', requires=IS_IN_DB(db,db.auth_user.id,'%(first_name)s %(last_name)s'), label=T('Jefe de Seccion')),
    format='%(f_nombre)s'
    )

########################################
db.define_table('t_espaciofisico',
    Field('f_espacio', 'string', requires=IS_NOT_EMPTY(), label=T('Espacio')),
    Field('f_direccion', 'string', requires=IS_NOT_EMPTY(), label=T('Direccion')),
    Field('f_seccion', 'integer',requires=IS_IN_DB(db,db.t_seccion.id,'%(f_laboratorio)s, seccion %(f_seccion)s'), label=T('Seccion')),
    Field('f_tecnico','integer', requires=IS_IN_DB(db,db.auth_user.id,'%(first_name)s %(last_name)s'), label=T('Tecnico')),
    format='%(f_espacio)s',
    migrate=settings.migrate)

########################################
db.define_table('t_inventario',
    Field('f_sustancia', 'integer', label=T('Sustancia'),requires=IS_IN_DB(db,db.t_materiales.id,'%(f_nombre)s')\
    ,represent= lambda name,row: \
                A(str(db(db.t_materiales.id==name).select(db.t_materiales.f_nombre))[22:],_href=URL('sustancias','view_bitacora',args=[name]))),
    Field('f_espaciofisico', 'integer', requires=IS_IN_DB(db,db.t_espaciofisico.id,'%(f_espacio)s') , label=T('Espaciofisico')),
    Field('f_cantidadonacion', 'integer', label=T('Cantida Donacion')),
    Field('f_cantidadusointerno', 'integer',label=T('Cantidad Uso Interno')),
    Field('f_total','integer',default=0,label=T('Cantidad Total'),readable=False,writable=False),
    format='%(f_sustancia)s',
    migrate=settings.migrate)

db.define_table('t_inventario_archive',db.t_inventario,Field('current_record','reference t_inventario',readable=False,writable=False))

########################################
db.define_table('t_bitacora',
    Field('f_sustancia', 'integer',requires=IS_IN_DB(db,db.t_materiales.id,'%(f_nombre)s'),
            represent=lambda f_sustancia,row: str(db(db.t_materiales.id == f_sustancia).select(db.t_materiales.f_nombre))[22:],
            notnull=True, label=T('Sustancia')),
    Field('f_proceso', 'string', notnull=True, label=T('Proceso')),
    Field('f_ingreso', 'integer', label=T('Ingreso')),
    Field('f_consumo', 'integer', label=T('Consumo')),
    Field('f_cantidad', 'integer', label=T('Cantidad')),
    Field('f_fecha', 'datetime', notnull=True, label=T('Fecha')),
    Field('f_espaciofisico', 'integer', requires=IS_IN_DB(db,db.t_espaciofisico.id,'%(f_espacio)s') , label=T('Espaciofisico')),
    format='%(f_sustancia)s',
    migrate=settings.migrate)

db.define_table('t_bitacora_archive',db.t_bitacora,Field('current_record','reference t_bitacora',readable=False,writable=False))

########################################
#db.define_table('t_personal',
#    Field('f_nombre', 'string', notnull=True, label=T('NombrePer')),
#    Field('f_apellido', 'string', notnull=True, label=T('Apellido')),
#    Field('f_correo', 'string', notnull=True, label=T('Correo')),
#    Field('f_cargo', 'reference t_cargo', notnull=True, label=T('Cargo')),
#    format='%(f_nombre)s',
#    migrate=settings.migrate)

#db.define_table('t_personal_archive',db.t_personal,Field('current_record','reference t_personal',readable=False,writable=False))



########################################
db.define_table('t_sustanciapeligrosa',
    Field('f_nombre', 'string', label=T('Nombre')),
    Field('f_cas', 'string', label=T('Cas')),
    Field('f_pureza', 'integer',requires=IS_INT_IN_RANGE(0, 101), label=T('Pureza')),
    Field('f_estado', 'string', requires=IS_IN_DB(db,db.t_estado.f_estado,'%(f_estado)s'), label=T('Estado')),
    Field('f_control', 'string', label=T('Control')),
    Field('f_peligrosidad', 'string', label=T('Peligrosidad')),
    format='%(f_nombre)s',
    migrate=settings.migrate)

db.define_table('t_sustanciapeligrosa_archive',db.t_sustanciapeligrosa,Field('current_record','reference t_sustanciapeligrosa',readable=False,writable=False))

########################################
db.define_table('t_solicitud',
    Field('f_sustancia', 'string', label=T('Sustancia')),
    Field('f_espaciofisico', 'string', label=T('Espaciofisico')),
    Field('f_seccion', 'string', label=T('Seccion')),
    Field('f_responsable', 'string', label=T('Responsable')),
    Field('f_solicitador', 'string', label=T('Solicitador')),
    Field('f_cantidadsolicitada', 'string', label=T('Cantidadsolicitada')),
    Field('f_estado', 'string', label=T('Estado')),
    format='%(f_sustancia)s',
    migrate=settings.migrate)

db.define_table('t_solicitud_archive',db.t_solicitud,Field('current_record','reference t_solicitud',readable=False,writable=False))
