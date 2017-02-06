### we prepend t_ to tablenames and f_ to fieldnames for disambiguity

if db(db.auth_group).isempty():
    db.auth_group.insert(role='Director',description='Director de la Unidad de Laboratorio')
    db.auth_group.insert(role='Administrador Personal',description='Administrador de Personal')
    db.auth_group.insert(role='Gestor de Sustancias',description='Gestor de Sustancias')
    db.auth_group.insert(role='Jefe de Laboratorio',description='Jefe de Laboratorio')
    db.auth_group.insert(role='Jefe de Sección',description='Jefe de Sección')
    db.auth_group.insert(role='Técnico',description='Técnico de Laboratorio')


if db(db.auth_permission).isempty():
    db.auth_permission.insert(name='director',table_name='t_sustancias',
                            group_id=(db(db.auth_group.role == "Director").select(db.auth_group.id).first()))
    db.auth_permission.insert(name='gestor',table_name='t_sustancias',
                            group_id=db(db.auth_group.role == "Gestor de Sustancias").select(db.auth_group.id).first())
    db.auth_permission.insert(name='tecnico',table_name='t_inventario',
                            group_id=db(db.auth_group.role == "Técnico").select(db.auth_group.id).first())
    db.auth_permission.insert(name='jefeseccion',table_name='t_inventario',
                            group_id=db(db.auth_group.role == "Jefe de Sección").select(db.auth_group.id).first())
    db.auth_permission.insert(name='jefelab',table_name='t_inventario',
                            group_id=db(db.auth_group.role == "Jefe de Laboratorio").select(db.auth_group.id).first())

########################################
db.define_table('t_regimenes',
    Field('f_nombre','string',label=T('Nombre')),
    format = '%(f_nombre)s')

if db(db.t_regimenes).isempty():
    db.t_regimenes.insert(f_nombre='RL4')
    db.t_regimenes.insert(f_nombre='RL7')
    db.t_regimenes.insert(f_nombre='RL4 y RL7')
    db.t_regimenes.insert(f_nombre='N/A')
##########################################
db.define_table('t_ingresos',
    Field('f_nombre',label=T('Nombre')),
    format='%(f_nombre)s'
)
if db(db.t_ingresos).isempty():
    db.t_ingresos.insert(f_nombre='Suministro de Almacén')
    db.t_ingresos.insert(f_nombre='Compra a Proveedor')
    db.t_ingresos.insert(f_nombre='Préstamo')
    db.t_ingresos.insert(f_nombre='Donación')
##########################################
db.define_table('t_consumos',
    Field('f_nombre',label=T('Nombre')),
    format='%(f_nombre)s'
)
if db(db.t_consumos).isempty():
    db.t_consumos.insert(f_nombre='Práctica de Laboratorio')
    db.t_consumos.insert(f_nombre='Tesis')
    db.t_consumos.insert(f_nombre='Proyecto de Investigación')
    db.t_consumos.insert(f_nombre='Servicio de Laboratorio')
#    Field('f_permiso','string',label=T('Permiso')),
#    format='%(f_nombreCar)s',
#    migrate=settings.migrate)

#db.define_table('t_cargo_archive',db.t_cargo,Field('current_record','reference t_cargo',readable=False,writable=False))
########################################


db.define_table('t_materiales',
               Field('f_nombre','string',requires=IS_NOT_EMPTY()),
               Field('f_cas','string',requires=IS_NOT_EMPTY()),
               format='%(f_nombre)s')
db.t_materiales.f_cas.requires=IS_NOT_IN_DB(db,db.t_materiales.f_cas)
db.t_materiales.f_nombre.requires=IS_NOT_IN_DB(db,db.t_materiales.f_nombre)

########################################
db.define_table('t_estado',
               Field('f_estado','string',readable=False,writable=False),
               format='%(f_estado)s')

if db(db.t_estado).isempty():
    db.t_estado.insert(f_estado='Sólido')
    db.t_estado.insert(f_estado='Líquido')
    db.t_estado.insert(f_estado='Gaseoso')

########################################

db.define_table('t_sustancias',
    Field('f_nombre', 'string', label=T('Nombre')),
    Field('f_cas', 'string', label=T('Cas')),
    Field('f_pureza', 'integer',requires=IS_INT_IN_RANGE(0, 101), label=T('Pureza')),
    Field('f_estado', 'integer', requires=IS_IN_DB(db,db.t_estado.id,'%(f_estado)s'), label=T('Estado'),
    represent = lambda value,row: str(db(db.t_estado.id == value).select(db.t_estado.f_estado))[18:] ),
    Field('f_control', 'integer', label=T('Control'), requires=IS_IN_DB(db,db.t_regimenes.id,'%(f_nombre)s'),
    represent = lambda value,row: str(db(db.t_regimenes.id == value).select(db.t_regimenes.f_nombre))[21:] ),
    Field('f_peligrosidad', 'string', label=T('Peligrosidad')),
    format='%(f_nombre)s',
    migrate=settings.migrate)
db.t_sustancias.id.readable=False
db.t_sustancias.id.writable=False
db.define_table('t_sustancias_archive',db.t_sustancias,Field('current_record','reference t_sustancias',readable=False,writable=False))




##########################################
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
db.t_espaciofisico.id.represent= lambda value,row: str(row.f_espacio)[27:]

########################################
db.define_table('t_inventario',
    Field('f_sustancia', 'integer', label=T('Sustancia'),requires=IS_IN_DB(db,db.t_sustancias.id,'%(f_nombre)s')\
    ,represent= lambda name,row: \
                A(str(db(db.t_sustancias.id==name).select(db.t_sustancias.f_nombre))[22:],_href=URL('sustancias','view_bitacora',vars=dict(sust=row.f_sustancia,esp=row.f_espaciofisico)))),
    Field('f_espaciofisico', 'integer',readable=False,writable=False ,requires=IS_IN_DB(db,db.t_espaciofisico.id,'%(f_espacio)s') ,
    represent= lambda value,row: str(db(db.t_espaciofisico.id == value).select(db.t_espaciofisico.f_espacio))[27:],
    label=T('Espaciofisico')),
    Field('f_cantidadonacion', 'float',default=0,label=T('Cantidad Donacion'),requires=IS_FLOAT_IN_RANGE(0,1e1000)),
    Field('f_cantidadusointerno', 'float',default=0,label=T('Cantidad Uso Interno'),requires=IS_FLOAT_IN_RANGE(0,1e1000)),
    Field('f_total','float',label=T('Cantidad Total'),writable=False,compute=lambda r:r.f_cantidadonacion+r.f_cantidadusointerno,requires=IS_FLOAT_IN_RANGE(0,1e1000)),
    Field('f_seccion','integer',readable=False,writable=False,requires=IS_IN_DB(db,db.t_seccion.id,'%(f_seccion)s'),label=T('Sección'),
    compute = lambda r: long(str(db(db.t_espaciofisico.id == r.f_espaciofisico).select(db.t_espaciofisico.f_seccion))[26:]) ),
    format='%(f_sustancia)s',
    migrate=settings.migrate)

db.define_table('t_inventario_archive',db.t_inventario,Field('current_record','reference t_inventario',readable=False,writable=False))
db.t_inventario.id.readable = False

########################################
db.define_table('t_bitacora',
    Field('f_fechaingreso','datetime',label=T('Fecha')),
    Field('f_sustancia', 'integer',readable=False,writable=False,requires=IS_IN_DB(db,db.t_sustancias.id,'%(f_nombre)s'),
            represent=lambda f_sustancia,row: str(db(db.t_sustancias.id == f_sustancia).select(db.t_sustancias.f_nombre))[22:],
            notnull=True, label=T('Sustancia')),
    Field('f_proceso', 'string', notnull=True, label=T('Proceso')),
    Field('f_ingreso', 'float', default=0, label=T('Ingreso'),requires=IS_FLOAT_IN_RANGE(0,1e1000)),
    Field('f_consumo', 'float', default=0,label=T('Consumo'),requires=IS_FLOAT_IN_RANGE(0,1e1000)),
    Field('f_cantidad', 'float', label=T('Cantidad'),requires=IS_FLOAT_IN_RANGE(0,1e1000),writable=False,default=0,compute=lambda r:
    r.f_ingreso-r.f_consumo+float ( str ( db( (db.t_inventario.f_sustancia == r.f_sustancia) & (db.t_inventario.f_espaciofisico == r.f_espaciofisico) ).select(db.t_inventario.f_cantidadusointerno) )[33:]) ),
    Field('f_fecha', 'datetime', label=T('FechaIngreso'),writable=False,readable=False, default=request.now),
    Field('f_espaciofisico', 'integer',readable=False, requires=IS_IN_DB(db,db.t_espaciofisico.id,'%(f_espacio)s') ,
    writable=False, represent= lambda value,row: str(db(db.t_espaciofisico.id == value).select(db.t_espaciofisico.f_espacio))[26:],
     label=T('Espacio Fisico'),notnull=True),
    Field('f_descripcion','text',label=T('Descripción'),readable=False),
    format='%(f_sustancia)s',
    migrate=settings.migrate)
db.t_bitacora.id.readable = False

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
