### we prepend t_ to tablenames and f_ to fieldnames for disambiguity

#editado por adolfo
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


###############################################
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
    Field('f_email', 'string', label=T('Email')),
    Field('f_group', 'integer', label=T('Privilegio'), requires=IS_IN_DB(db, db.auth_group.id, '%(role)s (%(id)s)'), represent = lambda value,row: str(db(db.auth_group.id == value).select(db.auth_group.role))[17:]),
    migrate=settings.migrate)

db.t_users_autorizados._plural = 'Usuarios Autorizados'
db.t_users_autorizados._singular = 'Usuario Autorizado'

db.t_users_pendientes._plural = 'Usuarios que requieren autorización'
db.t_users_pendientes._singular = 'Usuario que requiere autorización'

def check_autorizado(f, uid):
    row = db(db.t_users_autorizados.f_email == f['email']).select().first()
    usuario = db(db.auth_user.id==uid).select().first()

    if row is not None:
        if row.f_group == f['cargo']:
            auth.del_membership(auth.id_group(role="Usuario Normal"), usuario.id)
            auth.add_membership(row.f_group, usuario.id)
            usuario.update_record(autorizado = True)
        else:
            db.t_users_pendientes.insert(f_email=f['email'], f_group=f['cargo'])
            usuario.update_record(autorizado = False)

    else:
        db.t_users_pendientes.insert(f_email=f['email'], f_group=f['cargo'])
        usuario.update_record(autorizado = False)

def actualizar_privilegio(f, uid):
    usuario = db(db.auth_user.id==f['user_id']).select().first()

    if usuario.autorizado:
        auth.del_membership(auth.id_group(role="Usuario Normal"), usuario.id)


db.auth_user._after_insert.append(lambda f, uid: check_autorizado(f, uid))
db.auth_membership._after_insert.append(lambda f, uid: actualizar_privilegio(f, uid))

#####################################################################

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


#db.define_table('t_cargo_archive',db.t_cargo,Field('current_record','reference t_cargo',readable=False,writable=False))
########################################
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
    Field('f_peligrosidad', 'string', label=T('Peligrosidad'),requires=IS_IN_SET(['Inflamable','Tóxico','Tóxico para el ambiente','Corrosivo','Comburente','Nocivo','Explosivo','Irritante'],multiple = True), widget=SQLFORM.widgets.checkboxes.widget ),
    format='%(f_nombre)s',
    migrate=settings.migrate)
db.t_sustancias.id.readable=False
db.t_sustancias.id.writable=False
db.define_table('t_sustancias_archive',db.t_sustancias,Field('current_record','reference t_sustancias',readable=False,writable=False))


##########################################
db.define_table('t_laboratorio',
    Field('f_nombre', 'string', notnull=True, label=T('Nombre')),
    Field('f_jefe','integer', requires=IS_IN_DB(db,db.auth_user.id,'%(email)s'), label=T('Jefe de Laboratorio')),
    format='%(f_nombre)s',
    migrate=settings.migrate)

db.define_table('t_laboratorio_archive',db.t_laboratorio,Field('current_record','reference t_laboratorio',readable=False,writable=False))
db.t_laboratorio._plural = 'Laboratorios'
db.t_laboratorio._singular = 'Laboratorio'


########################################
db.define_table('t_seccion',
    Field('f_seccion','string',requires=IS_NOT_EMPTY(),label=T('Sección')),
    Field('f_laboratorio','integer',requires=IS_IN_DB(db,db.t_laboratorio.id), label=T('Laboratorio')),
    Field('f_jefe','integer', requires=IS_IN_DB(db,db.auth_user.id, '%(email)s'), label=T('Jefe de Sección')),
    migrate=settings.migrate,
    )
#db.t_seccion.f_jefe.represent = lambda value,row: str(db(db.t_users_autorizados.f_email == value).select(db.t_users_autorizados.f_email))[28:]
db.t_seccion._plural = 'Secciones'
db.t_seccion._singular = 'Sección'

########################################
db.define_table('t_espaciofisico',
    Field('f_espacio', 'string', requires=IS_NOT_EMPTY(), label=T('Espacio')),
    Field('f_direccion', 'string', requires=IS_NOT_EMPTY(), label=T('Direccion')),
    Field('f_seccion', 'integer',requires=IS_IN_DB(db,db.t_seccion.id,'%(f_laboratorio)s, seccion %(f_seccion)s'), label=T('Seccion')),
    Field('f_tecnico','integer', notnull = False,requires=IS_IN_DB(db,db.auth_user.id,'%(email)s'), label=T('Tecnico')),
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
    Field('f_laboratorio','string',requires=IS_IN_DB(db,db.t_laboratorio.id,'%(f_nombre)s'),readable=False,writable=False,
    compute = lambda r: str( db((db.t_seccion.id == r.f_seccion)).select(db.t_seccion.f_laboratorio) )[25:-2] ),
    format='%(f_sustancia)s',
    migrate=settings.migrate)

db.define_table('t_inventario_archive',db.t_inventario,Field('current_record','reference t_inventario',readable=False,writable=False))
db.t_inventario.id.readable = False


########################################
db.define_table('t_bitacora',
    Field('f_fechaingreso','date',label=T('Fecha'),notnull=True),
    Field('f_sustancia', 'integer',readable=False,writable=False,requires=IS_IN_DB(db,db.t_sustancias.id,'%(f_nombre)s'),
            represent=lambda f_sustancia,row: str(db(db.t_sustancias.id == f_sustancia).select(db.t_sustancias.f_nombre))[22:],
            notnull=True, label=T('Sustancia')),
    Field('f_proceso', 'string', notnull=True, label=T('Proceso')),
    Field('f_ingreso', 'float', default=0, label=T('Ingreso'),requires=IS_FLOAT_IN_RANGE(0,1e1000)),
    Field('f_consumo', 'float', default=0,label=T('Consumo'),requires=IS_FLOAT_IN_RANGE(0,1e1000)),
    Field('f_cantidad', 'float', label=T('Cantidad'),requires=IS_FLOAT_IN_RANGE(0,1e1000),writable=False,default=0),
    Field('f_fecha', 'datetime', label=T('FechaIngreso'),writable=False,readable=False, default=request.now),
    Field('f_espaciofisico', 'integer',readable=False, requires=IS_IN_DB(db,db.t_espaciofisico.id,'%(f_espacio)s') ,
    writable=False, represent= lambda value,row: str(db(db.t_espaciofisico.id == value).select(db.t_espaciofisico.f_espacio))[26:],
     label=T('Espacio Fisico'),notnull=True),
    Field('f_descripcion','text',label=T('Descripción'),readable=False),
    format='%(f_sustancia)s',
    migrate=settings.migrate)
db.t_bitacora.id.readable = False

db.define_table('t_bitacora_archive',db.t_bitacora,Field('current_record','reference t_bitacora',readable=False,writable=False))
db.t_bitacora.f_proceso.requires = IS_IN_SET(['Suministro del Almacen','Compra','Prestamo','Donacion','Practica de Laboratorio','Tesis','Proyecto de Investigacion','Servicio de Laboratorio'])

########################################
#vista para el inventario de Laboratorio, no ocupa espacio en la bd
db.executesql(
  'create or replace view v_laboratorio as\
    select ROW_NUMBER() OVER(order by f_nombre) as id,\
        s.f_nombre as f_sustancia, \
        SUM(i.f_cantidadonacion) as f_cantidadonacion, \
        SUM(i.f_cantidadusointerno) as f_cantidadusointerno, \
        SUM(i.f_total) as f_total,\
        i.f_laboratorio as f_laboratorio\
    from t_inventario i inner join t_sustancias s on (i.f_sustancia = s.id)\
    group by s.f_nombre,i.f_laboratorio')

db.define_table('v_laboratorio',
    Field('f_laboratorio',readable=False),
    Field('id'),
    Field('f_sustancia',label=T('Sustancia')),
    Field('f_cantidadonacion',label=T('Cantidad Donacion')),
    Field('f_cantidadusointerno',label=T('Cantidad Uso Interno')),
    Field('f_total',label=T('Total')),
    migrate=False
    )
db.v_laboratorio.id.readable=False
db.v_laboratorio.f_sustancia.represent= lambda name,row: A(name,_href=URL('sustancias','inventario_seccion',vars=dict(secc='t',
lab= row.f_laboratorio,
sust= str(db(db.t_sustancias.f_nombre == row.f_sustancia).select(db.t_sustancias.id))[17:-2])))


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
      i.f_seccion as f_seccion\
  from t_inventario i inner join t_sustancias s on (i.f_sustancia = s.id)\
  group by s.f_nombre,i.f_seccion,i.f_laboratorio\
  order by f_laboratorio,f_nombre,f_seccion;')

db.define_table('v_seccion',
    Field('f_laboratorio',readable = False),
    Field('id'),
    Field('f_seccion',readable=False,label = T('Sección')),
    Field('f_sustancia',label=T('Sustancia')),
    Field('f_cantidadonacion',label=T('Cantidad Donacion')),
    Field('f_cantidadusointerno',label=T('Cantidad Uso Interno')),
    Field('f_total',label=T('Total')),
    migrate=False
    )
db.v_seccion.id.readable=False
db.v_seccion.f_sustancia.represent = lambda name,row: A(name,_href=URL('sustancias','inventario_manage',vars=dict(secc=row.f_seccion,sust= str(db(db.t_sustancias.f_nombre == row.f_sustancia).select(db.t_sustancias.id))[17:-2]   )))
db.v_seccion.f_seccion.represent= lambda name,row: A(name,_href=URL('sustancias','inventario_manage',vars=dict(secc=row.f_seccion,sust=str(db(db.t_sustancias.f_nombre == row.f_sustancia).select(db.t_sustancias.id))[17:-2])))


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

#Por arreglar
#populate_db()
