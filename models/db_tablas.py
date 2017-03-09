### we prepend t_ to tablenames and f_ to fieldnames for disambiguity


if db(db.auth_group).isempty():
    db.auth_group.insert(role='WebMaster',description='Super Usuario')
    db.auth_group.insert(role='Director',description='Director de la Unidad de Laboratorio')
    db.auth_group.insert(role='Administrador Personal',description='Administrador de Personal')
    db.auth_group.insert(role='Gestor de Sustancias',description='Gestor de Sustancias')
    db.auth_group.insert(role='Jefe de Laboratorio',description='Jefe de Laboratorio')
    db.auth_group.insert(role='Jefe de Sección',description='Jefe de Sección')
    db.auth_group.insert(role='Técnico',description='Técnico de Laboratorio')
    db.auth_group.insert(role='Usuario Normal',description='Usuario recien registrado')

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

#############################################
db.define_table('t_laboratorio',
    Field('f_nombre', 'string', notnull=True, label=T('Nombre'), requires=IS_NOT_EMPTY()),
    Field('f_jefe','integer', requires=IS_IN_DB(db,db.auth_user.id,'%(first_name)s %(last_name)s',zero=None), label=T('Jefe de Laboratorio')),
    migrate=settings.migrate)

db.define_table('t_laboratorio_archive',db.t_laboratorio,Field('current_record','reference t_laboratorio',readable=False,writable=False))
db.t_laboratorio._plural = 'Laboratorios'
db.t_laboratorio._singular = 'Laboratorio'
db.t_laboratorio.f_jefe.represent = lambda value,row: db(db.auth_user.id == value).select().first()['first_name']+" "+db(db.auth_user.id == value).select().first()['last_name'] if value is not None else None


########################################
db.define_table('t_seccion',
    Field('f_seccion','string',requires=IS_NOT_EMPTY(),label=T('Sección')),
    Field('f_laboratorio','reference t_laboratorio',requires=IS_IN_DB(db,db.t_laboratorio.id,'%(f_nombre)s',zero=None), label=T('Laboratorio')),
    Field('f_jefe','integer', notnull=False, requires=IS_IN_DB(db,db.auth_user.id, '%(first_name)s %(last_name)s',zero=None), label=T('Jefe de Sección')),
    migrate=settings.migrate)

db.t_seccion._plural = 'Secciones'
db.t_seccion._singular = 'Sección'
db.t_seccion.f_laboratorio.represent = lambda value,row: db(db.t_laboratorio.id == value).select().first()['f_nombre'] if value is not None else None
db.t_seccion.f_jefe.represent = lambda value,row: db(db.auth_user.id == value).select().first()['first_name']+" "+db(db.auth_user.id == value).select().first()['last_name'] if value is not None else None


########################################
db.define_table('t_espaciofisico',
    Field('f_espacio', 'string', requires=IS_NOT_EMPTY(), label=T('Espacio')),
    Field('f_direccion', 'string', requires=IS_NOT_EMPTY(), label=T('Dirección')),
    Field('f_seccion', 'reference t_seccion', requires=IS_IN_DB(db,db.t_seccion.id,'%(f_seccion)s',zero=None), label=T('Sección')),
    format='%(f_espacio)s',
    migrate=settings.migrate)

db.t_espaciofisico.f_seccion.represent= lambda value,row: db(db.t_seccion.id == value).select().first()['f_seccion'] if value is not None else None
db.t_espaciofisico._plural = 'Espacios Físicos'
db.t_espaciofisico._singular = 'Espacio Físico'


########################################
db.define_table('t_tecs_esp',
    Field('f_espaciofisico', 'reference t_espaciofisico', label=T('Espacio')),
    Field('f_tecnico', 'integer', requires=IS_IN_DB(db,db.auth_user.id, '%(first_name)s %(last_name)s',zero=None), label=T('Técnico')),
    migrate=settings.migrate)

db.t_tecs_esp.f_espaciofisico.represent= lambda value,row: db(db.t_espaciofisico.id == value).select().first()['f_direccion'] if value is not None else None
db.t_tecs_esp.f_tecnico.represent= lambda value,row: db(db.auth_user.id == value).select().first()['first_name']+" "+db(db.auth_user.id == value).select().first()['last_name'] if value is not None else None
db.t_tecs_esp._plural = 'Técnicos'
db.t_tecs_esp._singular = 'Técnicos'

#db.auth_user.f_seccion.requires = IS_IN_DB(db, db.t_seccion.id, '%(f_seccion)s')
#db.auth_user.f_laboratorio.requires = IS_IN_DB(db, db.t_laboratorio.id, '%(f_nombre)s')

###############################################

db.define_table('t_users_pendientes',
    Field('f_email', 'string', label=T('Email'), requires = IS_EMAIL(error_message='Email inválido')),
    Field('f_group', 'integer', label=T('Privilegio'), requires=IS_IN_DB(db, db.auth_group.id, '%(role)s (%(id)s)',zero=None), represent = lambda value,row: str(db(db.auth_group.id == value).select(db.auth_group.role))[17:]),
    Field('f_seccion', 'integer', label=T('Sección'), requires=IS_IN_DB(db,db.t_seccion.id,'%(f_seccion)s', zero=None)),
    Field('f_laboratorio', 'integer', requires=IS_IN_DB(db,db.t_laboratorio.id,'%(f_nombre)s',zero=None), label=T('Laboratorio')),
    migrate=settings.migrate)

db.t_users_pendientes.f_laboratorio.represent = lambda value,row: db(db.t_laboratorio.id == value).select().first()['f_nombre'] if value is not None else None
db.t_users_pendientes.f_seccion.represent= lambda value,row: db(db.t_seccion.id == value).select().first()['f_seccion'] if value is not None else None

################################################
#editado por adolfo
if db(db.auth_user).isempty():
        db.auth_user.insert(first_name='Super',last_name='Usuario',email='webmaster@sigulab.com',password=db.auth_user.password.validate('0000')[0])
        db.auth_membership.insert(user_id=(db(db.auth_user.email == 'webmaster@sigulab.com').select(db.auth_user.id).first()),\
            group_id=auth.id_group(role="WebMaster"));

db.auth_membership._plural = 'Membresías'
db.auth_membership._singular = 'Membresía'

db.auth_group._plural = 'Privilegios'
db.auth_group._singular = 'Privilegio'

db.auth_user._plural = 'Usuarios Registrados'
db.auth_user._singular = 'Usuario Registrado'


db.define_table('t_users_autorizados',
    Field('f_email', 'string', label=T('Email'), requires = IS_EMAIL(error_message='Email inválido')),
    Field('f_group', 'integer', label=T('Privilegio'), requires=IS_IN_DB(db, db.auth_group.id, '%(role)s (%(id)s)',zero=None), represent = lambda value,row: str(db(db.auth_group.id == value).select(db.auth_group.role))[17:] if value is not None else None),
    Field('f_laboratorio', 'integer', requires=IS_IN_DB(db,db.t_laboratorio.id,'%(f_nombre)s',zero=None), label=T('Laboratorio')),
    Field('f_seccion', 'integer', label=T('Sección'), requires=IS_IN_DB(db,db.t_seccion.id,'%(f_seccion)s', zero=None)),
    migrate=settings.migrate)

db.t_users_pendientes.f_laboratorio.represent = lambda value,row: db(db.t_laboratorio.id == value).select().first()['f_nombre'] if value is not None else None
db.t_users_pendientes.f_seccion.represent= lambda value,row: db(db.t_seccion.id == value).select().first()['f_seccion'] if value is not None else None

db.t_users_autorizados._plural = 'Usuarios Autorizados'
db.t_users_autorizados._singular = 'Usuario Autorizado'

db.t_users_pendientes._plural = 'Usuarios que requieren autorización'
db.t_users_pendientes._singular = 'Usuario que requiere autorización'

def check_autorizado(f, uid):
    row = db(db.t_users_autorizados.f_email == f['email']).select().first()

    usuario = db(db.auth_user.id==uid).select().first()
    if usuario.autorizado:
        auth.del_membership(auth.id_group(role="Usuario Normal"), usuario.id)
        auth.add_membership(f['cargo'], usuario.id)
        return
    elif (row is not None) and row.f_group == f['cargo'] and row.f_laboratorio==f['f_laboratorio'] and row.f_seccion==f['f_seccion']:
        auth.del_membership(auth.id_group(role="Usuario Normal"), usuario.id)
        auth.add_membership(row.f_group, usuario.id)
        db(db.t_users_autorizados.f_email == usuario.email).delete()
        usuario.update_record(autorizado = True)
        return
    else:
        db.t_users_pendientes.insert(f_email=f['email'], f_group=f['cargo'], f_seccion=f['f_seccion'], f_laboratorio=f['f_laboratorio'])
        auth.add_membership(auth.id_group(role='Usuario Normal'), usuario.id)
        usuario.update_record(autorizado = False)

        to = []
        id_admin_u = auth.id_group(role='Administrador Personal')
        admins = db(db.auth_membership.group_id == id_admin_u).select(db.auth_user.email, \
        join=db.auth_user.on(db.auth_membership.user_id == db.auth_user.id))

        for admin in admins:
            to.append(admin['email'])

        s = 'Nuevo usuario pendiente por confirmar'
        m = 'Se ha registrado un nuevo usuario en SIGULAB, pero está pendiente de confirmación por un Administrador de Usuarios'
        mail.send(to=to, subject=s, message=m)

    usuario.update_record(autorizado = False)

def actualizar_privilegio(f, uid):
    usuario = db(db.auth_user.id==f['user_id']).select().first()

    if usuario.autorizado:
        auth.del_membership(auth.id_group(role='Usuario Normal'), usuario.id)

db.auth_user._after_insert.append(lambda f, uid: check_autorizado(f, uid))
db.auth_membership._after_insert.append(lambda f, uid: actualizar_privilegio(f, uid))

########################################
db.define_table('t_regimenes',
    Field('f_nombre','string',label=T('Nombre')),
    format = '%(f_nombre)s')

if db(db.t_regimenes).isempty():
    db.t_regimenes.insert(f_nombre='RL4')
    db.t_regimenes.insert(f_nombre='RL7')
    db.t_regimenes.insert(f_nombre='RL4 y RL7')
    db.t_regimenes.insert(f_nombre='N/A')


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
    Field('f_nombre', 'string', label=T('Nombre'),requires=IS_NOT_EMPTY()),
    Field('f_cas', 'string', label=T('Cas'),requires=IS_NOT_EMPTY()),
    Field('f_pureza', 'integer',requires=IS_INT_IN_RANGE(0, 101), label=T('Pureza')),
    Field('f_estado', 'integer', requires=IS_IN_DB(db,db.t_estado.id,'%(f_estado)s'), label=T('Estado'),
    represent = lambda value,row: str(db(db.t_estado.id == value).select(db.t_estado.f_estado))[18:] ),
    Field('f_control', 'integer', label=T('Control'), requires=IS_IN_DB(db,db.t_regimenes.id,'%(f_nombre)s'),
    represent = lambda value,row: str(db(db.t_regimenes.id == value).select(db.t_regimenes.f_nombre))[21:] ),
    Field('f_peligrosidad', 'list:string', label=T('Peligrosidad'),requires=IS_IN_SET(['Inflamable','Tóxico','Tóxico para el ambiente','Corrosivo','Comburente','Nocivo','Explosivo','Irritante'],multiple = True),
    widget=SQLFORM.widgets.checkboxes.widget),
    Field('f_reporte','upload',label=T('MSDS'),requires=IS_NULL_OR(IS_UPLOAD_FILENAME(extension='pdf'))),
    format='%(f_nombre)s',
    migrate=settings.migrate)

db.t_sustancias.id.readable=False
db.t_sustancias.id.writable=False
db.define_table('t_sustancias_archive',db.t_sustancias,Field('current_record','reference t_sustancias',readable=False,writable=False))
db.t_sustancias.f_reporte.readable=(auth.has_membership('Gestor de Sustancias')or auth.has_membership('WebMaster'))
db.t_sustancias._singular='Listado de Sustancias'
db.t_sustancias._plural='Listado de Sustancias'


########################################
db.define_table('t_inventario',
    Field('f_sustancia', 'integer', label=T('Sustancia'),requires=IS_IN_DB(db,db.t_sustancias.id,'%(f_nombre)s')\
    ,represent= lambda name,row: \
                A(str(db(db.t_sustancias.id==row.f_sustancia).select(db.t_sustancias.f_nombre))[22:],_href=URL('sustancias','view_bitacora',vars=dict(sust=row.f_sustancia,esp=row.f_espaciofisico)))),
    Field('f_espaciofisico', 'integer',readable=False,writable=False ,requires=IS_IN_DB(db,db.t_espaciofisico.id,'%(f_espacio)s') ,
    represent= lambda value,row: str(db(db.t_espaciofisico.id == value).select(db.t_espaciofisico.f_direccion))[29:-2],
    label=T('Espaciofisico')),
    Field('f_cantidadonacion', 'float',default=0,label=T('Cantidad Donacion'),requires=IS_FLOAT_IN_RANGE(0,1e1000)),
    Field('f_cantidadusointerno', 'float',default=0,label=T('Cantidad Uso Interno'),requires=IS_FLOAT_IN_RANGE(0,1e1000)),
    Field('f_total','float',label=T('Cantidad Total'),writable=False,compute=lambda r:r.f_cantidadonacion+r.f_cantidadusointerno,requires=IS_FLOAT_IN_RANGE(0,1e1000)),
    Field('f_seccion','integer',readable=False,writable=False,requires=IS_IN_DB(db,db.t_seccion.id,'%(f_seccion)s'),label=T('Sección'),
    compute = lambda r: long(str(db(db.t_espaciofisico.id == r.f_espaciofisico).select(db.t_espaciofisico.f_seccion))[26:]) ),
    Field('f_laboratorio','string',requires=IS_IN_DB(db,db.t_laboratorio.id,'%(f_nombre)s'),readable=False,writable=False,
    compute = lambda r: str( db((db.t_seccion.id == r.f_seccion)).select(db.t_seccion.f_laboratorio) )[25:-2] ),
    Field('f_unidad','string',requires=IS_IN_SET(['mL','L','g','Kg','cm'+chr(0x00B3)]),
    compute= lambda r: 'mL' if str( db( (db.t_sustancias.id == r.f_sustancia)&(db.t_estado.id == db.t_sustancias.f_estado) ).select(db.t_estado.f_estado) )[19:-2] == 'Líquido' else 'cm'+chr(0x00B3)
    if str( db( (db.t_sustancias.id == r.f_sustancia)&(db.t_estado.id == db.t_sustancias.f_estado) ).select(db.t_estado.f_estado) )[19:-2] == 'Gaseoso' else 'g',
    label=T('Unidad')),
    format='%(f_sustancia)s',
    migrate=settings.migrate)

db.define_table('t_inventario_archive',db.t_inventario,Field('current_record','reference t_inventario',readable=False,writable=False))
db.t_inventario.id.readable = False
db.t_inventario._plural='Inventario'
db.t_inventario._singular='Inventario'


########################################
db.define_table('t_bitacora',
    Field('f_fechaingreso','date',label=T('Fecha'),notnull=True,
            requires=IS_DATE_IN_RANGE(maximum=request.now.date(),error_message='Debe introducir una fecha menor a la actual.')),
    Field('f_sustancia', 'integer',readable=False,writable=False,requires=IS_IN_DB(db,db.t_sustancias.id,'%(f_nombre)s'),
            represent=lambda f_sustancia,row: str(db(db.t_sustancias.id == f_sustancia).select(db.t_sustancias.f_nombre))[22:],
            notnull=True, label=T('Sustancia')),
    Field('f_proceso', 'string', notnull=True, label=T('Proceso')),
    Field('f_ingreso', 'float', default=0, label=T('Ingreso'),requires=IS_FLOAT_IN_RANGE(0,1e1000)),
    Field('f_consumo', 'float', default=0,label=T('Consumo'),requires=IS_FLOAT_IN_RANGE(0,1e1000)),
    Field('f_unidad','string',readable=False),
    Field('f_cantidad', 'float', label=T('Cantidad'),requires=IS_FLOAT_IN_RANGE(0,1e1000),writable=False,default=0),
    Field('f_fecha', 'datetime', label=T('Fecha de Transacción'),writable=False,readable=False, default=request.now),
    Field('f_espaciofisico', 'integer',readable=False, requires=IS_IN_DB(db,db.t_espaciofisico.id,'%(f_espacio)s') ,
    writable=False, represent= lambda value,row: str(db(db.t_espaciofisico.id == value).select(db.t_espaciofisico.f_espacio))[26:],
     label=T('Espacio Fisico'),notnull=True),
    Field('f_descripcion','text',label=T('Descripción'),readable=False),
    format='%(f_sustancia)s',
    migrate=settings.migrate)

db.t_bitacora.id.readable = False
db.define_table('t_bitacora_archive',db.t_bitacora,Field('current_record','reference t_bitacora',readable=False,writable=False))
db.t_bitacora.f_proceso.requires = IS_IN_SET(['Suministro del Almacen','Compra','Prestamo','Donacion','Practica de Laboratorio','Tesis','Proyecto de Investigacion','Servicio de Laboratorio'])
db.t_bitacora._singular='Bitacora'
db.t_bitacora._plural='Bitacora'


########################################
#vista para el inventario de Laboratorio, no ocupa espacio en la bd
db.executesql(
  'create or replace view v_laboratorio as\
    select ROW_NUMBER() OVER(order by f_nombre) as id,\
        s.f_nombre as f_sustancia, \
        SUM(i.f_cantidadonacion) as f_cantidadonacion, \
        SUM(i.f_cantidadusointerno) as f_cantidadusointerno, \
        SUM(i.f_total) as f_total,\
        i.f_laboratorio as f_laboratorio,\
        i.f_unidad as f_unidad\
    from t_inventario i inner join t_sustancias s on (i.f_sustancia = s.id)\
    group by s.f_nombre,i.f_laboratorio,i.f_unidad')

db.define_table('v_laboratorio',
    Field('f_laboratorio',readable=False),
    Field('id'),
    Field('f_sustancia',label=T('Sustancia')),
    Field('f_cantidadonacion',label=T('Cantidad Donacion')),
    Field('f_cantidadusointerno',label=T('Cantidad Uso Interno')),
    Field('f_total',label=T('Total')),
    Field('f_unidad',label=T('Unidad')),
    migrate=False)

db.v_laboratorio.id.readable=False
db.v_laboratorio.f_sustancia.represent= lambda name,row: A(name,_href=URL('sustancias','inventario_seccion',vars=dict(secc='t',
lab= row.f_laboratorio,
sust= str(db(db.t_sustancias.f_nombre == row.f_sustancia).select(db.t_sustancias.id))[17:-2])))
db.v_laboratorio._singular=db.t_laboratorio._singular
db.v_laboratorio._plural=db.t_laboratorio._plural


########################################
#vista para el inventario de Laboratorio, no ocupa espacio en la bd
db.executesql(
'create or replace view v_seccion as\
  select ROW_NUMBER() OVER(order by f_laboratorio,f_nombre,f_seccion) as id,\
      s.f_nombre as f_sustancia, \
      SUM(i.f_cantidadonacion) as f_cantidadonacion, \
      SUM(i.f_cantidadusointerno) as f_cantidadusointerno, \
      SUM(i.f_total) as f_total,\
      i.f_laboratorio as f_laboratorio,\
      i.f_seccion as f_seccion,\
      i.f_unidad as f_unidad\
  from t_inventario i inner join t_sustancias s on (i.f_sustancia = s.id)\
  group by s.f_nombre,i.f_seccion,i.f_laboratorio,i.f_unidad\
  order by f_laboratorio,f_nombre,f_seccion;')

db.define_table('v_seccion',
    Field('f_laboratorio',readable = False),
    Field('id'),
    Field('f_seccion',readable=False,label = T('Sección')),
    Field('f_sustancia',label=T('Sustancia')),
    Field('f_cantidadonacion',label=T('Cantidad Donacion')),
    Field('f_cantidadusointerno',label=T('Cantidad Uso Interno')),
    Field('f_total',label=T('Total')),
    Field('f_unidad',label=T('Unidad')),
    migrate=False)

db.v_seccion.id.readable=False
db.v_seccion.f_sustancia.represent = lambda name,row: A(name,_href=URL('sustancias','inventario_manage',vars=dict(secc=row.f_seccion,sust= str(db(db.t_sustancias.f_nombre == row.f_sustancia).select(db.t_sustancias.id))[17:-2]   )))
db.v_seccion.f_seccion.represent= lambda name,row: A( str(db(db.t_seccion.id == name).select(db.t_seccion.f_seccion))[21:-2],
_href=URL('sustancias','inventario_manage',vars=dict(secc=row.f_seccion,sust=str(db(db.t_sustancias.f_nombre == row.f_sustancia).select(db.t_sustancias.id))[17:-2])))
db.v_seccion._singular=db.t_seccion._singular
db.v_seccion._plural=db.t_seccion._plural


########################################
db.define_table('t_facturas',
    Field('f_numero','string',label=T('Numero de Factura'),requires=IS_NOT_EMPTY()),
    Field('f_fecha','date',label=T('Fecha de Compra'),notnull=True,requires=IS_DATE_IN_RANGE(maximum=request.now.date(),error_message='Debe introducir una fecha menor a la actual.')),
    Field('f_proveedor','string',label=T('Proveedor'),requires=IS_NOT_EMPTY()),
    Field('f_sustancia','list:string',label=T('Sustancias'),readable=False,writable=False,default=""),
    migrate=settings.migrate)
db.t_facturas.id.readable=False
db.t_facturas._singular='Facturas'
db.t_facturas._plural='Facturas'


########################################
db.define_table('t_solicitud',
    Field('f_sustancia', 'integer', label=T('Sustancia'),requires=IS_IN_DB(db,db.t_sustancias.id,'%(f_nombre)s')\
    ,represent=  lambda value,row: db(db.t_sustancias.id == value).select().first()['f_nombre']),
    Field('f_cantidad', 'integer', label=T('Cantidad')),
    Field('f_fecha_solicitud','date',label=T('Fecha Solicitud'),notnull=True),
    Field('f_fecha_tope', 'date',label=T('Fecha Tope'),notnull=True,
            requires=IS_DATE_IN_RANGE(minimum=request.now.date(),error_message='Debe introducir una fecha menor a la actual.')),
    Field('f_espacio_fisico', 'integer',readable=False,writable=False ,requires=IS_IN_DB(db,db.t_espaciofisico.id,'%(f_espacio)s') ,
    represent= lambda value,row: #str(db(db.t_espaciofisico.id == value).select(db.t_espaciofisico.f_espacio))[27:-2] + " - " +
    str(db(db.t_espaciofisico.id == value).select(db.t_espaciofisico.f_direccion))[29:-2],
    label=T('Espaciofisico')),
    Field('f_cantidad_devuelta', 'integer', label=T('Cantidad Recolectada')),
    Field('f_responsable', 'string', label=T('Responsable')),
    Field('f_Tipo', 'string', label=T('Tipo de Solicitud'), requires=IS_IN_SET(['Donación','Préstamo']), notnull=True),
    )
db.t_solicitud.id.readable=False


########################################
db.define_table('t_solicitud_respuesta',
    Field('f_sustancia', 'integer', label=T('Sustancia'),requires=IS_IN_DB(db,db.t_sustancias.id,'%(f_nombre)s')\
    ,represent= lambda value,row: db(db.t_sustancias.id == value).select().first()['f_nombre']),
    Field('f_cantidad', 'integer', label=T('Cantidad')),
    Field('f_fecha_aceptado','date',label=T('Fecha Aceptado'),notnull=True),
    Field('f_fecha_entregado','date',label=T('Fecha Entregado')),
    Field('f_fecha_recibido','date',label=T('Fecha Recibido')),
    Field('f_tipo', 'string', label=T('Tipo de Solicitud'), requires=IS_IN_SET(['Donación','Préstamo']), notnull=True),
    Field('f_fecha_devolucion','date',label=T('Fecha Devolución')),
    Field('f_cantidad_devuelta', 'integer', label=T('Cantidad Devuelta')),
    Field('f_espacio_fisico_s', 'integer',readable=False,writable=False ,requires=IS_IN_DB(db,db.t_espaciofisico.id,'%(f_espacio)s') ,
    represent= lambda value,row: #str(db(db.t_espaciofisico.id == value).select(db.t_espaciofisico.f_espacio))[27:-2] + " - " +
    str(db(db.t_espaciofisico.id == value).select(db.t_espaciofisico.f_direccion))[29:-2],
    label=T('Espaciofisico Solicitante')),
    Field('f_espacio_fisico_d', 'integer',readable=False,writable=False ,requires=IS_IN_DB(db,db.t_espaciofisico.id,'%(f_espacio)s') ,
    represent= lambda value,row: #str(db(db.t_espaciofisico.id == value).select(db.t_espaciofisico.f_espacio))[27:-2] + " - " +
    str(db(db.t_espaciofisico.id == value).select(db.t_espaciofisico.f_direccion))[29:-2],
    label=T('Espacio Fisico Donante')),    Field('f_solicitud', 'reference t_solicitud', label=T('Solicitud Asociada')),
    Field('f_entregado', 'integer', label=T('Entregado'))
    )

#Field('f_espacio_fisico_s', 'reference t_espaciofisico', label=T('Espacio Físico Solicitante'), represent= lambda value,row: db(db.t_espaciofisico.id == value).select().first()['f_direccion']),
#Field('f_espacio_fisico_d', 'reference t_espaciofisico', label=T('Espacio Físico Donante'), represent= lambda value,row: db(db.t_espaciofisico.id == value).select().first()['f_direccion']),
db.t_solicitud_respuesta.id.readable=False


########################################
db.define_table('t_solicitud_prestamo',
    Field('f_sustancia', 'integer', label=T('Sustancia'),requires=IS_IN_DB(db,db.t_sustancias.id,'%(f_nombre)s')\
    ,represent= lambda value,row: db(db.t_sustancias.id == value).select().first()['f_nombre']),
    Field('f_solicitud', 'reference t_solicitud_respuesta', label=T('Solicitud Asociada')),
    Field('f_fecha_aceptado','date',label=T('Fecha Aceptado'),notnull=True),
    Field('f_fecha_recibido','date',label=T('Fecha Recibido')),
    Field('f_cantidad', 'integer', label=T('Cantidad')),
    Field('f_recibido', 'integer', label=T('Recibido'))
    )

db.t_solicitud_prestamo.id.readable=False


########################################
db.executesql(
'create or replace view v_solicitud as\
  select ROW_NUMBER() OVER(order by f_espaciofisico) as id,\
      s.f_sustancia as f_sustancia, \
      s.f_cantidad as f_cantidad, \
      s.f_espacio_fisico as f_espacio_fisico, \
      s.f_Tipo as f_Tipo,\
      s.id as f_id,\
      i.f_espaciofisico as f_espaciofisico\
  from t_inventario i inner join t_solicitud s on (i.f_sustancia = s.f_sustancia)\
  order by f_espaciofisico;')

db.define_table('v_solicitud',
    Field('f_sustancia',label=T('Sustancia')),
    Field('id'),
    Field('f_cantidad',label = T('Cantidad')),
    Field('f_espacio_fisico',label=T('Espacio Físico')),
    Field('f_Tipo',label=T('Tipo')),
    Field('f_id',label=T('ids')),
    Field('f_espaciofisico',label=T('Espacio Físico Donante')),
    migrate=False
    )

db.v_solicitud.id.readable=False
db.v_solicitud.f_sustancia.represent=  lambda value,row: db(db.t_sustancias.id == value).select().first()['f_nombre']
db.v_solicitud.f_espaciofisico.represent= lambda value,row: str(db(db.t_espaciofisico.id == value).select(db.t_espaciofisico.f_direccion))[29:-2]
db.v_solicitud.f_espacio_fisico.represent= lambda value,row: str(db(db.t_espaciofisico.id == value).select(db.t_espaciofisico.f_direccion))[29:-2]

