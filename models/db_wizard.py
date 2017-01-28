### we prepend t_ to tablenames and f_ to fieldnames for disambiguity


########################################
db.define_table('t_cargo',
    Field('f_nombreCar','string',label=T('Nombre')),
    Field('f_permiso','string',label=T('Permiso')),
    format='%(f_nombreCar)s',
    migrate=settings.migrate)

db.define_table('t_cargo_archive',db.t_cargo,Field('current_record','reference t_cargo',readable=False,writable=False))

########################################
db.define_table('t_inventario',
    Field('f_sustancia', type='string',
          label=T('Sustancia')),
    Field('f_espaciofisico', type='string',
          label=T('Espaciofisico')),
    Field('f_seccion', type='string',
          label=T('Seccion')),
    Field('f_responsable', type='string',
          label=T('Responsable')),
    Field('f_cantidadonacion', type='string',
          label=T('Cantidadonacion')),
    Field('f_cantidadusointerno', type='string',
          label=T('Cantidadusointerno')),
    format='%(f_sustancia)s',
    migrate=settings.migrate)

db.define_table('t_inventario_archive',db.t_inventario,Field('current_record','reference t_inventario',readable=False,writable=False))

########################################
db.define_table('t_bitacora',
    Field('f_sustancia', type='string', notnull=True,
          label=T('SustanciaBita')),
    Field('f_proceso', type='string', notnull=True,
          label=T('Proceso')),
    Field('f_ingreso', type='string', notnull=True,
          label=T('Ingreso')),
    Field('f_consumo', type='string', notnull=True,
          label=T('Consumo')),
    Field('f_cantidad', type='string', notnull=True,
          label=T('CantidadBita')),
    Field('f_fecha', type='string', notnull=True,
          label=T('Fecha')),
    format='%(f_sustanciaBita)s',
    migrate=settings.migrate)

db.define_table('t_bitacora_archive',db.t_bitacora,Field('current_record','reference t_bitacora',readable=False,writable=False))

########################################
db.define_table('t_personal',
    Field('f_nombre', type='string', notnull=True,
          label=T('NombrePer')),
    Field('f_apellido', type='string', notnull=True,
          label=T('Apellido')),
    Field('f_correo', type='string', notnull=True,
          label=T('Correo')),
    Field('f_cargo', type='reference t_cargo', notnull=True,
          label=T('Cargo')),
    format='%(f_nombre)s',
    migrate=settings.migrate)

db.define_table('t_personal_archive',db.t_personal,Field('current_record','reference t_personal',readable=False,writable=False))

########################################
db.define_table('t_laboratorio',
    Field('f_nombre', type='string', notnull=True,
          label=T('Nombre')),
    Field('f_nombresec', type='string',
          label=T('Nombresec')),
    Field('f_espaciofisico', type='string',
          label=T('Espaciofisico')),
    format='%(f_nombre)s',
    migrate=settings.migrate)

db.define_table('t_laboratorio_archive',db.t_laboratorio,Field('current_record','reference t_laboratorio',readable=False,writable=False))

########################################
db.define_table('t_sustanciapeligrosa',
    Field('f_nombre', type='string',
          label=T('Nombre')),
    Field('f_cas', type='string',
          label=T('Cas')),
    Field('f_pureza', type='string',
          label=T('Pureza')),
    Field('f_estado', type='string',
          label=T('Estado')),
    Field('f_control', type='string',
          label=T('Control')),
    Field('f_peligrosidad', type='string',
          label=T('Peligrosidad')),
    format='%(f_nombre)s',
    migrate=settings.migrate)

db.define_table('t_sustanciapeligrosa_archive',db.t_sustanciapeligrosa,Field('current_record','reference t_sustanciapeligrosa',readable=False,writable=False))

########################################
db.define_table('t_solicitud',
    Field('f_sustancia', type='string',
          label=T('Sustancia')),
    Field('f_espaciofisico', type='string',
          label=T('Espaciofisico')),
    Field('f_seccion', type='string',
          label=T('Seccion')),
    Field('f_responsable', type='string',
          label=T('Responsable')),
    Field('f_solicitador', type='string',
          label=T('Solicitador')),
    Field('f_cantidadsolicitada', type='string',
          label=T('Cantidadsolicitada')),
    Field('f_estado', type='string',
          label=T('Estado')),
    format='%(f_sustancia)s',
    migrate=settings.migrate)

db.define_table('t_solicitud_archive',db.t_solicitud,Field('current_record','reference t_solicitud',readable=False,writable=False))
