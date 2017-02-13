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

if db(db.auth_user).isempty():
        db.auth_user.insert(first_name='Super',last_name='Usuario',email='webmaster@sigulab.com',password=db.auth_user.password.validate('0000')[0])
        db.auth_membership.insert(user_id=(db(db.auth_user.email == 'webmaster@sigulab.com').select(db.auth_user.id).first()),\
            group_id=db(db.auth_group.role == "WebMaster").select(db.auth_group.id).first());

db.auth_membership._plural = 'Membresías'
db.auth_membership._singular = 'Membresía'

db.auth_group._plural = 'Privilegios'
db.auth_group._singular = 'Privilegio'

db.auth_user._plural = 'Usuarios Registrados'
db.auth_user._singular = 'Usuario Registrado'

db.define_table('t_users_autorizados',
    Field('f_email', 'string', label=T('Email')),
    Field('f_group', 'string', label=T('Privilegio'), requires=IS_IN_DB(db, db.auth_group.id, '%(role)s (%(id)s)'), represent = lambda value,row: str(db(db.auth_group.id == value).select(db.auth_group.role))[17:]))

db.t_users_autorizados._plural = 'Usuarios Autorizados'
db.t_users_autorizados._singular = 'Usuario Autorizado'
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
    Field('f_jefe','string', requires=IS_IN_DB(db,db.t_users_autorizados,'%(f_email)s'), label=T('Jefe de Laboratorio')),
    format='%(f_nombre)s',
    migrate=settings.migrate)

db.define_table('t_laboratorio_archive',db.t_laboratorio,Field('current_record','reference t_laboratorio',readable=False,writable=False))

########################################
db.define_table('t_seccion',
    Field('f_seccion','string',requires=IS_NOT_EMPTY(),label=T('Sección')),
    Field('f_laboratorio','string',requires=IS_IN_DB(db,db.t_laboratorio.f_nombre,'%(f_nombre)s'), label=T('Laboratorio')),
    Field('f_jefe','string', requires=IS_IN_DB(db,db.t_users_autorizados,'%(f_email)s'), label=T('Jefe de Seccion')),
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
    Field('f_laboratorio','string',requires=IS_IN_DB(db,db.t_laboratorio.id,'%(f_nombre)s'),readable=False,writable=False,
    compute = lambda r: str( db((db.t_seccion.id == r.f_seccion)).select(db.t_seccion.f_laboratorio) )[25:-2] ),
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


######################################## Migracion de datos
####Sustancias

db.t_sustancias.insert(f_nombre='4-metilpentan-2-ona (Metilisobutilcetona)', f_cas='108-10-1', f_pureza='99', f_estado='2', f_control='1', f_peligrosidad='Inflamable')
db.t_sustancias.insert(f_nombre='Acetato de Etilo', f_cas='141-78-6', f_pureza='99', f_estado='2', f_control='1', f_peligrosidad='Inflamable')
db.t_sustancias.insert(f_nombre='Acetona', f_cas='67-64-1', f_pureza='99', f_estado='2', f_control='1', f_peligrosidad='Inflamable')
db.t_sustancias.insert(f_nombre='Ácido Antranílico', f_cas='118-92-3', f_pureza='99', f_estado='2', f_control='1', f_peligrosidad='Inflamable')
db.t_sustancias.insert(f_nombre='Ácido Clorhídrico', f_cas='7647-01-0', f_pureza='37', f_estado='2', f_control='1', f_peligrosidad='Tóxico')
db.t_sustancias.insert(f_nombre='Ácido Fenilacético y sus sales', f_cas='103-82-2', f_pureza='99', f_estado='2', f_control='1', f_peligrosidad='Comburente')
db.t_sustancias.insert(f_nombre='Ácido Nítrico', f_cas='7697-37-2', f_pureza='5', f_estado='2', f_control='2', f_peligrosidad='Tóxico')
db.t_sustancias.insert(f_nombre='Ácido Pícrico (trinitrofenol)', f_cas='88-89-1', f_pureza='3', f_estado='1', f_control='2', f_peligrosidad='Explosivo')
db.t_sustancias.insert(f_nombre='Ácido Sulfúrico', f_cas='7664-93-9', f_pureza='97', f_estado='2', f_control='3', f_peligrosidad='Corrosivo')
db.t_sustancias.insert(f_nombre='Aluminio en polvo', f_cas='7429-90-5', f_pureza='99', f_estado='1', f_control='2', f_peligrosidad='Inflamable')
db.t_sustancias.insert(f_nombre='Amoníaco Anhídrico', f_cas='7664-41-7', f_pureza='99', f_estado='2', f_control='1', f_peligrosidad='Nocivo')
db.t_sustancias.insert(f_nombre='Amoníaco en disolución acuosa', f_cas='001336-21-6', f_pureza='25', f_estado='2', f_control='1', f_peligrosidad='Corrosivo')
db.t_sustancias.insert(f_nombre='Anhídrico acético', f_cas='108-24-7', f_pureza='99', f_estado='2', f_control='1', f_peligrosidad='Inflamable')
db.t_sustancias.insert(f_nombre='Azidas (de sodio)', f_cas='26628-22-8', f_pureza='99', f_estado='1', f_control='2', f_peligrosidad='Tóxico')
db.t_sustancias.insert(f_nombre='Benceno', f_cas='71-43-2', f_pureza='99', f_estado='2', f_control='2', f_peligrosidad='Inflamable')
db.t_sustancias.insert(f_nombre='Butanona (metilcetona)', f_cas='78-93-3', f_pureza='99', f_estado='2', f_control='1', f_peligrosidad='Inflamable')
db.t_sustancias.insert(f_nombre='Carbonato de Sodio', f_cas='497-19-8', f_pureza='99', f_estado='1', f_control='1', f_peligrosidad='Corrosivo')
db.t_sustancias.insert(f_nombre='Clorato de Potasio', f_cas='3811-04-9', f_pureza='99', f_estado='1', f_control='2', f_peligrosidad='Comburente')
db.t_sustancias.insert(f_nombre='Clorato de Sodio', f_cas='7775-09-9', f_pureza='99', f_estado='1', f_control='2', f_peligrosidad='Comburente')
db.t_sustancias.insert(f_nombre='Cloroformo', f_cas='67-66-3', f_pureza='99', f_estado='2', f_control='1', f_peligrosidad='Nocivo')
db.t_sustancias.insert(f_nombre='Diclorometano', f_cas='75-09-2', f_pureza='99', f_estado='2', f_control='1', f_peligrosidad='Nocivo')
db.t_sustancias.insert(f_nombre='Dinitrofenol', f_cas='51-28-5', f_pureza='99', f_estado='1', f_control='2', f_peligrosidad='Nocivo')
db.t_sustancias.insert(f_nombre='Dinitrotolueno', f_cas='606-20-2', f_pureza='99', f_estado='1', f_control='2', f_peligrosidad='Nocivo')
db.t_sustancias.insert(f_nombre='Etanol', f_cas='64-17-5', f_pureza='99', f_estado='2', f_control='1', f_peligrosidad='Inflamable')
db.t_sustancias.insert(f_nombre='Eter Etílico', f_cas='60-29-7', f_pureza='99', f_estado='2', f_control='1', f_peligrosidad='Explosivo')
db.t_sustancias.insert(f_nombre='Fósforo blanco', f_cas='7723-14-0', f_pureza='99', f_estado='1', f_control='2', f_peligrosidad='Inflamable')

db.t_sustancias.insert(f_nombre='Fulminato de Mercurio', f_cas='', f_pureza='', f_estado='', f_control='2', f_peligrosidad='N/A')
db.t_sustancias.insert(f_nombre='Heptano', f_cas='142-82-5', f_pureza='99', f_estado='2', f_control='1', f_peligrosidad='Inflamable')
db.t_sustancias.insert(f_nombre='Hexano', f_cas='110-54-3', f_pureza='99', f_estado='2', f_control='1', f_peligrosidad='Inflamable')
db.t_sustancias.insert(f_nombre='Hidrogenocarbonato (Bicarbonato) de Sodio', f_cas='144-55-8', f_pureza='99', f_estado='1', f_control='1', f_peligrosidad='Irritante')
db.t_sustancias.insert(f_nombre='Hipoclorito de calcio', f_cas='7778-54-3', f_pureza='68', f_estado='1', f_control='2', f_peligrosidad='Corrosivo')
db.t_sustancias.insert(f_nombre='Hipoclorito de Sodio', f_cas='7681-52-9', f_pureza='', f_estado='2', f_control='2', f_peligrosidad='Corrosivo')
db.t_sustancias.insert(f_nombre='Metanol', f_cas='67-56-1', f_pureza='99', f_estado='2', f_control='1', f_peligrosidad='Inflamable')
db.t_sustancias.insert(f_nombre='Nitrato de Amonio (salitre de chile)', f_cas='6484-52-2', f_pureza='99', f_estado='1', f_control='2', f_peligrosidad='Explosivo')
db.t_sustancias.insert(f_nombre='Nitrato de Bismuto', f_cas='7697-37-2', f_pureza='99', f_estado='1', f_control='2', f_peligrosidad='Corrosivo')
db.t_sustancias.insert(f_nombre='Nitrato de Calcio', f_cas='13477-34-4', f_pureza='99', f_estado='1', f_control='2', f_peligrosidad='Tóxico')
db.t_sustancias.insert(f_nombre='Nitrato de Plata', f_cas='7761-88-8', f_pureza='99', f_estado='1', f_control='2', f_peligrosidad='Corrosivo')
db.t_sustancias.insert(f_nombre='Nitrato de Plomo', f_cas='10099-74-8', f_pureza='99', f_estado='1', f_control='2', f_peligrosidad='Tóxico')
db.t_sustancias.insert(f_nombre='Nitrato de Potasio', f_cas='7757-79-1', f_pureza='99', f_estado='1', f_control='2', f_peligrosidad='Comburente')
db.t_sustancias.insert(f_nombre='Nitrato de Sodio', f_cas='7631-99-4', f_pureza='99', f_estado='1', f_control='2', f_peligrosidad='Comburente')
db.t_sustancias.insert(f_nombre='Nitrito de Sodio', f_cas='7632-00-0', f_pureza='99', f_estado='1', f_control='2', f_peligrosidad='Comburente')
db.t_sustancias.insert(f_nombre='Nitrobenceno', f_cas='98-95-3', f_pureza='99', f_estado='2', f_control='2', f_peligrosidad='Nocivo')
db.t_sustancias.insert(f_nombre='Nitrocelulosa', f_cas='9004-70-0', f_pureza='12', f_estado='1', f_control='2', f_peligrosidad='Inflamable')
db.t_sustancias.insert(f_nombre='Nitroglicerina', f_cas='55-63-0', f_pureza='1', f_estado='1', f_control='2', f_peligrosidad='Explosivo')
db.t_sustancias.insert(f_nombre='Perclorato de Potasio', f_cas='7778-74-7', f_pureza='99', f_estado='1', f_control='2', f_peligrosidad='Comburente')
db.t_sustancias.insert(f_nombre='Perclorato de Sodio', f_cas='7601-89-0', f_pureza='99', f_estado='1', f_control='2', f_peligrosidad='Comburente')
db.t_sustancias.insert(f_nombre='Permanganato de Potasio', f_cas='7722-64-7', f_pureza='99', f_estado='1', f_control='3', f_peligrosidad='Comburente')
db.t_sustancias.insert(f_nombre='Sesquicarbonato de Sodio', f_cas='6106-20-3', f_pureza='99', f_estado='1', f_control='1', f_peligrosidad='Corrosivo')
db.t_sustancias.insert(f_nombre='Sulfato de Amonio', f_cas='7783-20-2', f_pureza='99', f_estado='1', f_control='2', f_peligrosidad='Corrosivo')
db.t_sustancias.insert(f_nombre='Sulfato de Magnesio', f_cas='7487-88-9', f_pureza='65', f_estado='1', f_control='2', f_peligrosidad='Irritante')
db.t_sustancias.insert(f_nombre='Sulfuro de Potasio', f_cas='1312-73-8', f_pureza='99', f_estado='1', f_control='2', f_peligrosidad='Inflamable')
db.t_sustancias.insert(f_nombre='Tetrahidrofurano', f_cas='109-99-9', f_pureza='99', f_estado='2', f_control='1', f_peligrosidad='Inflamable')
db.t_sustancias.insert(f_nombre='Tolueno', f_cas='108-88-3', f_pureza='99', f_estado='2', f_control='1', f_peligrosidad='Inflamable')
db.t_sustancias.insert(f_nombre='Trinitrotolueno (TNT)', f_cas='118-96-7', f_pureza='99', f_estado='1', f_control='2', f_peligrosidad='Explosivo')
db.t_sustancias.insert(f_nombre='Urea', f_cas='57-13-6 ', f_pureza='', f_estado='1', f_control='2', f_peligrosidad='Irritante')
db.t_sustancias.insert(f_nombre='4-metilpentan-2-ona (Metilisobutilcetona)', f_cas='108-10-1', f_pureza='99', f_estado='2', f_control='1', f_peligrosidad='Tóxico')
db.t_sustancias.insert(f_nombre='Acetato de Etilo', f_cas='141-78-6', f_pureza='99', f_estado='2', f_control='1', f_peligrosidad='Irritante')
db.t_sustancias.insert(f_nombre='Acetona', f_cas='67-64-1', f_pureza='99', f_estado='2', f_control='1', f_peligrosidad='Tóxico')
db.t_sustancias.insert(f_nombre='Ácido Antranílico', f_cas='118-92-3', f_pureza='99', f_estado='2', f_control='1', f_peligrosidad='Comburente')
db.t_sustancias.insert(f_nombre='Ácido Clorhídrico', f_cas='7647-01-0', f_pureza='37', f_estado='2', f_control='1', f_peligrosidad='Corrosivo')
db.t_sustancias.insert(f_nombre='Ácido Nítrico', f_cas='7697-37-2', f_pureza='5', f_estado='2', f_control='2', f_peligrosidad='Irritante')
db.t_sustancias.insert(f_nombre='Ácido Pícrico (trinitrofenol)', f_cas='88-89-1', f_pureza='3', f_estado='1', f_control='2', f_peligrosidad='Tóxico')
db.t_sustancias.insert(f_nombre='Ácido Sulfúrico', f_cas='7664-93-9', f_pureza='97', f_estado='2', f_control='3', f_peligrosidad='Irritante')
db.t_sustancias.insert(f_nombre='Amoníaco Anhídrico', f_cas='7664-41-7', f_pureza='99', f_estado='2', f_control='1', f_peligrosidad='Inflamable')
db.t_sustancias.insert(f_nombre='Amoníaco en disolución acuosa', f_cas='001336-21-6', f_pureza='25', f_estado='2', f_control='1', f_peligrosidad='Tóxico')
db.t_sustancias.insert(f_nombre='Anhídrico acético', f_cas='108-24-7', f_pureza='99', f_estado='2', f_control='1', f_peligrosidad='Nocivo')
db.t_sustancias.insert(f_nombre='Benceno', f_cas='71-43-2', f_pureza='99', f_estado='2', f_control='2', f_peligrosidad='Tóxico')
db.t_sustancias.insert(f_nombre='Butanona (metilcetona)', f_cas='78-93-3', f_pureza='99', f_estado='2', f_control='1', f_peligrosidad='Tóxico')
db.t_sustancias.insert(f_nombre='Carbonato de Sodio', f_cas='497-19-8', f_pureza='99', f_estado='1', f_control='1', f_peligrosidad='Irritante')
db.t_sustancias.insert(f_nombre='Clorato de Potasio', f_cas='3811-04-9', f_pureza='99', f_estado='1', f_control='2', f_peligrosidad='Tóxico')
db.t_sustancias.insert(f_nombre='Clorato de Sodio', f_cas='7775-09-9', f_pureza='99', f_estado='1', f_control='2', f_peligrosidad='Tóxico')
db.t_sustancias.insert(f_nombre='Cloroformo', f_cas='67-66-3', f_pureza='99', f_estado='2', f_control='1', f_peligrosidad='Tóxico')
db.t_sustancias.insert(f_nombre='Diclorometano', f_cas='75-09-2', f_pureza='99', f_estado='2', f_control='1', f_peligrosidad='Inflamable')
db.t_sustancias.insert(f_nombre='Dinitrofenol', f_cas='51-28-5', f_pureza='99', f_estado='1', f_control='2', f_peligrosidad='Tóxico')
db.t_sustancias.insert(f_nombre='Etanol', f_cas='64-17-5', f_pureza='99', f_estado='2', f_control='1', f_peligrosidad='Irritante')
db.t_sustancias.insert(f_nombre='Eter Etílico', f_cas='60-29-7', f_pureza='99', f_estado='2', f_control='1', f_peligrosidad='Nocivo')
db.t_sustancias.insert(f_nombre='Fósforo blanco', f_cas='7723-14-0', f_pureza='99', f_estado='1', f_control='2', f_peligrosidad='Nocivo')

db.t_sustancias.insert(f_nombre='Heptano', f_cas='142-82-5', f_pureza='99', f_estado='2', f_control='1', f_peligrosidad='Irritante')
db.t_sustancias.insert(f_nombre='Hipoclorito de calcio', f_cas='7778-54-3', f_pureza='68', f_estado='1', f_control='2', f_peligrosidad='Irritante')
db.t_sustancias.insert(f_nombre='Hipoclorito de Sodio', f_cas='7681-52-9', f_pureza='', f_estado='2', f_control='2', f_peligrosidad='Tóxico')
db.t_sustancias.insert(f_nombre='Metanol', f_cas='67-56-1', f_pureza='99', f_estado='2', f_control='1', f_peligrosidad='Irritante')
db.t_sustancias.insert(f_nombre='Nitrato de Bismuto', f_cas='7697-37-2', f_pureza='99', f_estado='1', f_control='2', f_peligrosidad='Tóxico')
db.t_sustancias.insert(f_nombre='Nitrato de Plata', f_cas='7761-88-8', f_pureza='99', f_estado='1', f_control='2', f_peligrosidad='Tóxico')
db.t_sustancias.insert(f_nombre='Nitrato de Plomo', f_cas='10099-74-8', f_pureza='99', f_estado='1', f_control='2', f_peligrosidad='Tóxico')
db.t_sustancias.insert(f_nombre='Nitrato de Potasio', f_cas='7757-79-1', f_pureza='99', f_estado='1', f_control='2', f_peligrosidad='Tóxico')
db.t_sustancias.insert(f_nombre='Nitrato de Sodio', f_cas='7631-99-4', f_pureza='99', f_estado='1', f_control='2', f_peligrosidad='Tóxico')
db.t_sustancias.insert(f_nombre='Nitrito de Sodio', f_cas='7632-00-0', f_pureza='99', f_estado='1', f_control='2', f_peligrosidad='Tóxico')
db.t_sustancias.insert(f_nombre='Nitrobenceno', f_cas='98-95-3', f_pureza='99', f_estado='2', f_control='2', f_peligrosidad='Tóxico')
db.t_sustancias.insert(f_nombre='Perclorato de Potasio', f_cas='7778-74-7', f_pureza='99', f_estado='1', f_control='2', f_peligrosidad='Tóxico')
db.t_sustancias.insert(f_nombre='Perclorato de Sodio', f_cas='7601-89-0', f_pureza='99', f_estado='1', f_control='2', f_peligrosidad='Nocivo')
db.t_sustancias.insert(f_nombre='Permanganato de Potasio', f_cas='7722-64-7', f_pureza='99', f_estado='1', f_control='3', f_peligrosidad='Corrosivo')
db.t_sustancias.insert(f_nombre='Sesquicarbonato de Sodio', f_cas='6106-20-3', f_pureza='99', f_estado='1', f_control='1', f_peligrosidad='Irritante')
db.t_sustancias.insert(f_nombre='Sulfato de Amonio', f_cas='7783-20-2', f_pureza='99', f_estado='1', f_control='2', f_peligrosidad='Irritante')
db.t_sustancias.insert(f_nombre='Sulfuro de Potasio', f_cas='1312-73-8', f_pureza='99', f_estado='1', f_control='2', f_peligrosidad='Corrosivo')
db.t_sustancias.insert(f_nombre='Tetrahidrofurano', f_cas='109-99-9', f_pureza='99', f_estado='2', f_control='1', f_peligrosidad='Irritante')
db.t_sustancias.insert(f_nombre='Tolueno', f_cas='108-88-3', f_pureza='99', f_estado='2', f_control='1', f_peligrosidad='Tóxico')
db.t_sustancias.insert(f_nombre='Trinitrotolueno (TNT)', f_cas='118-96-7', f_pureza='99', f_estado='1', f_control='2', f_peligrosidad='Nocivo')
db.t_sustancias.insert(f_nombre='Urea', f_cas='57-13-6 ', f_pureza='', f_estado='1', f_control='2', f_peligrosidad='Comburente')


#####Deberian ser RL8 pero este regimen aun no esta implementado
db.t_sustancias.insert(f_nombre='Fósforos rojos o amorfos', f_cas='7723-14-0', f_pureza='99', f_estado='1', f_control='4', f_peligrosidad='Inflamable')
db.t_sustancias.insert(f_nombre='Fósforos rojos o amorfos', f_cas='7723-14-0', f_pureza='99', f_estado='1', f_control='4', f_peligrosidad='Nocivo')

#####Usuarios


db.t_users_autorizados.insert(f_email='cherrera@usb.ve',f_group='5')
db.t_users_autorizados.insert(f_email='chickani@usb.ve',f_group='5')
db.t_users_autorizados.insert(f_email='eprato@usb.ve',f_group='5')
db.t_users_autorizados.insert(f_email='jrodrig@usb.ve',f_group='5')
db.t_users_autorizados.insert(f_email='jwalter@usb.ve',f_group='5')
db.t_users_autorizados.insert(f_email='mcmarque@usb.ve',f_group='3')
db.t_users_autorizados.insert(f_email='rcastell@usb.ve',f_group='5')
db.t_users_autorizados.insert(f_email='wsequera@usb.ve',f_group='5')
db.t_users_autorizados.insert(f_email='adegouveia@usb.ve',f_group='7')
db.t_users_autorizados.insert(f_email='aguillon@usb.ve',f_group='7')
db.t_users_autorizados.insert(f_email='antoniovidal@usb.ve',f_group='6')
db.t_users_autorizados.insert(f_email='ccorrale@usb.ve',f_group='6')
db.t_users_autorizados.insert(f_email='hcmarquez@usb.ve',f_group='7')
db.t_users_autorizados.insert(f_email='iacosta@usb.ve',f_group='7')
db.t_users_autorizados.insert(f_email='jesu.alberto.pinto.alayon@gmail',f_group='7')
db.t_users_autorizados.insert(f_email='jmelendez@usb.ve',f_group='6')
db.t_users_autorizados.insert(f_email='jwrengifo@usb.ve',f_group='6')
db.t_users_autorizados.insert(f_email='luisalas@usb.ve',f_group='7')
db.t_users_autorizados.insert(f_email='mdacosta@usb.ve',f_group='7')
db.t_users_autorizados.insert(f_email='mggomez@usb.ve',f_group='6')
db.t_users_autorizados.insert(f_email='npulido@usb.ve',f_group='7')
db.t_users_autorizados.insert(f_email='ragarcia@usb.ve',f_group='7')
db.t_users_autorizados.insert(f_email='rcorreia@usb.ve',f_group='7')
db.t_users_autorizados.insert(f_email='sdiaz@usb.ve',f_group='6')
db.t_users_autorizados.insert(f_email='vmonagas@usb.ve',f_group='7')
db.t_users_autorizados.insert(f_email='07-41753@usb.ve',f_group='7')
db.t_users_autorizados.insert(f_email='13-89428@usb.ve',f_group='7')
db.t_users_autorizados.insert(f_email='adesousa@usb.ve',f_group='7')
db.t_users_autorizados.insert(f_email='cherrera@usb.ve',f_group='6')
db.t_users_autorizados.insert(f_email='dalizo@usb.ve',f_group='7')
db.t_users_autorizados.insert(f_email='dannyvalera@usb.ve',f_group='7')
db.t_users_autorizados.insert(f_email='deisyperdomo@usb.ve',f_group='6')
db.t_users_autorizados.insert(f_email='eklein@usb.ve',f_group='6')
db.t_users_autorizados.insert(f_email='eliergalarraga@usb.ve',f_group='6')
db.t_users_autorizados.insert(f_email='elucci@usb.ve',f_group='6')
db.t_users_autorizados.insert(f_email='epenott@usb.ve',f_group='6')
db.t_users_autorizados.insert(f_email='erikapedraza@usb.ve',f_group='6')
db.t_users_autorizados.insert(f_email='ezambrano@usb.ve',f_group='7')
db.t_users_autorizados.insert(f_email='freddyrojas@usb.ve',f_group='7')
db.t_users_autorizados.insert(f_email='ggedler@usb.ve',f_group='7')
db.t_users_autorizados.insert(f_email='grincon@usb.ve ',f_group='6')
db.t_users_autorizados.insert(f_email='imelendez@usb.ve',f_group='7')
db.t_users_autorizados.insert(f_email='lubesv@usb.ve',f_group='6')
db.t_users_autorizados.insert(f_email='luhidalgo@usb.ve',f_group='7')
db.t_users_autorizados.insert(f_email='mariaesthermoline@usb.ve',f_group='6')
db.t_users_autorizados.insert(f_email='msabino@usb.ve   ',f_group='6')
db.t_users_autorizados.insert(f_email='nciguela@usb.ve',f_group='7')
db.t_users_autorizados.insert(f_email='nelsonaraujo@usb.ve',f_group='6')
db.t_users_autorizados.insert(f_email='noeliarodriguez@usb.ve',f_group='7')
db.t_users_autorizados.insert(f_email='oscaruiz@usb.ve',f_group='7')
db.t_users_autorizados.insert(f_email='pmoncada@usb.ve',f_group='7')
db.t_users_autorizados.insert(f_email='psuarez@usb.ve ',f_group='6')
db.t_users_autorizados.insert(f_email='rmichell@usb.ve',f_group='6')
db.t_users_autorizados.insert(f_email='ronaldvargas@usb.ve',f_group='6')
db.t_users_autorizados.insert(f_email='sdeleon@usb.ve',f_group='7')
db.t_users_autorizados.insert(f_email='vfigueroa@usb.ve',f_group='7')
db.t_users_autorizados.insert(f_email='vlandaeta@usb.ve',f_group='6')
db.t_users_autorizados.insert(f_email='ymunoz@usb.ve',f_group='7')
db.t_users_autorizados.insert(f_email='gvillega@usb.ve',f_group='7')
db.t_users_autorizados.insert(f_email='jesusrojas@usb.ve',f_group='7')
db.t_users_autorizados.insert(f_email='ralejos@usb.ve',f_group='7')
db.t_users_autorizados.insert(f_email='marchena@usb.ve',f_group='7')
db.t_users_autorizados.insert(f_email='rlugo@usb.ve',f_group='7')
db.t_users_autorizados.insert(f_email='zsierra@usb.ve',f_group='7')
db.t_users_autorizados.insert(f_email='aalcalde@usb.ve',f_group='7')
db.t_users_autorizados.insert(f_email='abenitez@usb.ve',f_group='7')
db.t_users_autorizados.insert(f_email='alvarezf@usb.ve',f_group='7')
db.t_users_autorizados.insert(f_email='amendoza@usb.ve',f_group='6')
db.t_users_autorizados.insert(f_email='amolina@usb.ve',f_group='6')
db.t_users_autorizados.insert(f_email='amolina@usb.ve',f_group='6')
db.t_users_autorizados.insert(f_email='cvitanza@usb.ve',f_group='7')
db.t_users_autorizados.insert(f_email='dgraciano@usb.ve',f_group='7')
db.t_users_autorizados.insert(f_email='fmflores@usb.ve',f_group='7')
db.t_users_autorizados.insert(f_email='grodrig@usb.ve',f_group='7')
db.t_users_autorizados.insert(f_email='guillent@usb.ve',f_group='7')
db.t_users_autorizados.insert(f_email='hgalezo@usb.ve',f_group='7')
db.t_users_autorizados.insert(f_email='hrojas@usb.ve',f_group='7')
db.t_users_autorizados.insert(f_email='ialvarado@usb.ve',f_group='7')
db.t_users_autorizados.insert(f_email='jmoreno@usb.ve',f_group='7')
db.t_users_autorizados.insert(f_email='jyannuzzo@usb.ve',f_group='7')
db.t_users_autorizados.insert(f_email='kaponte@usb.ve',f_group='7')
db.t_users_autorizados.insert(f_email='magonzal@usb.ve',f_group='7')
db.t_users_autorizados.insert(f_email='mnino@usb.ve',f_group='6')
db.t_users_autorizados.insert(f_email='nleon@usb.ve',f_group='6')
db.t_users_autorizados.insert(f_email='psoto@usb.ve',f_group='7')
db.t_users_autorizados.insert(f_email='racosta@usb.ve',f_group='6')
db.t_users_autorizados.insert(f_email='seijascarla@usb.ve',f_group='7')
db.t_users_autorizados.insert(f_email='sovilla@usb.ve',f_group='6')
db.t_users_autorizados.insert(f_email='xhung@usb.ve',f_group='6')
db.t_users_autorizados.insert(f_email='violetta@usb.ve',f_group='6')
db.t_users_autorizados.insert(f_email='aamerio@usb.ve',f_group='6')
db.t_users_autorizados.insert(f_email='adenisraga@usb.ve',f_group='6')
db.t_users_autorizados.insert(f_email='chechelev@usb.ve',f_group='6')
db.t_users_autorizados.insert(f_email='dleal@usb.ve',f_group='6')
db.t_users_autorizados.insert(f_email='elsacardenas@usb.ve',f_group='6')
db.t_users_autorizados.insert(f_email='fabiolarojas@usb.ve',f_group='7')
db.t_users_autorizados.insert(f_email='gjean@usb.ve',f_group='7')
db.t_users_autorizados.insert(f_email='hrssca@hotmail.com',f_group='6')
db.t_users_autorizados.insert(f_email='jgutierr@usb.ve',f_group='6')
db.t_users_autorizados.insert(f_email='kgomez@usb.ve',f_group='6')
db.t_users_autorizados.insert(f_email='mbolivar@usb.ve',f_group='7')
db.t_users_autorizados.insert(f_email='mbolivar@usb.ve',f_group='7')
db.t_users_autorizados.insert(f_email='oescobar@usb.ve',f_group='6')
db.t_users_autorizados.insert(f_email='scovino@usb.ve',f_group='7')
db.t_users_autorizados.insert(f_email='tomasgrt@usb.ve',f_group='7')
db.t_users_autorizados.insert(f_email='tomasgrt@usb.ve',f_group='7')
db.t_users_autorizados.insert(f_email='tomasgrt@usb.ve',f_group='7')
db.t_users_autorizados.insert(f_email='tomasgrt@usb.ve',f_group='7')
db.t_users_autorizados.insert(f_email='wsanchez@usb.ve',f_group='7')
db.t_users_autorizados.insert(f_email='bchirinos@usb.ve',f_group='7')
db.t_users_autorizados.insert(f_email='lualvare@usb.ve',f_group='7')
db.t_users_autorizados.insert(f_email='wgonzal@usb.ve',f_group='2')
db.t_users_autorizados.insert(f_email='yortega@usb.ve',f_group='1')

###Laboratorios
db.t_laboratorio.insert(f_nombre='LaboratorioA',f_jefe='jrodrig@usb.ve')
db.t_laboratorio.insert(f_nombre='LaboratorioB',f_jefe='cherrera@usb.ve')
db.t_laboratorio.insert(f_nombre='LaboratorioC',f_jefe='jwalter@usb.ve ')
db.t_laboratorio.insert(f_nombre='LaboratorioD',f_jefe='rcastell@usb.ve')
db.t_laboratorio.insert(f_nombre='LaboratorioE',f_jefe='eprato@usb.ve')
db.t_laboratorio.insert(f_nombre='LaboratorioF',f_jefe='wsequera@usb.ve')
db.t_laboratorio.insert(f_nombre='LaboratorioG',f_jefe='chickani@usb.ve')

##Secciones
db.t_seccion.insert(f_seccion='Alta Tensión',f_laboratorio='LaboratorioA',f_jefe='jrodrig@usb.ve')
db.t_seccion.insert(f_seccion='Conversión de Energía Eléctrica',f_laboratorio='LaboratorioA',f_jefe='jwrengifo@usb.ve')
db.t_seccion.insert(f_seccion='Conversión de Energía Mecánica',f_laboratorio='LaboratorioA',f_jefe='antoniovidal@usb.ve')
db.t_seccion.insert(f_seccion='Desarrollo de Modelos y Prototipos',f_laboratorio='LaboratorioA',f_jefe='jrodrig@usb.ve')
db.t_seccion.insert(f_seccion='Dinámica de Máquinas',f_laboratorio='LaboratorioA',f_jefe='sdiaz@usb.ve')
db.t_seccion.insert(f_seccion='Fenómenos de Transporte',f_laboratorio='LaboratorioA',f_jefe='jmelendez@usb.ve')
db.t_seccion.insert(f_seccion='Mecánica Computacional',f_laboratorio='LaboratorioA',f_jefe='grodriguez@usb.ve')
db.t_seccion.insert(f_seccion='Mecánica de Fluidos',f_laboratorio='LaboratorioA',f_jefe='ccorrale@usb.ve')
db.t_seccion.insert(f_seccion='Operaciones Unitarias',f_laboratorio='LaboratorioA',f_jefe='mggomez@usb.ve')
db.t_seccion.insert(f_seccion='Sistemas de Potencia',f_laboratorio='LaboratorioA',f_jefe='jrodrig@usb.ve')

db.t_seccion.insert(f_seccion='Alimentos',f_laboratorio='LaboratorioB',f_jefe='elucci@usb.ve')
db.t_seccion.insert(f_seccion='Bioterio',f_laboratorio='LaboratorioB',f_jefe='deisyperdomo@usb.ve')
db.t_seccion.insert(f_seccion='Biología Celular',f_laboratorio='LaboratorioB',f_jefe='nelsonaraujo@usb.ve ')
db.t_seccion.insert(f_seccion='Biología de Organismos',f_laboratorio='LaboratorioB',f_jefe='psuarez@usb.ve')
db.t_seccion.insert(f_seccion='Biología Marina',f_laboratorio='LaboratorioB',f_jefe='eklein@usb.ve')
db.t_seccion.insert(f_seccion='Ecología',f_laboratorio='LaboratorioB',f_jefe='erikapedraza@usb.ve')
db.t_seccion.insert(f_seccion='Físico Química',f_laboratorio='LaboratorioB',f_jefe='ronaldvargas@usb.ve')
db.t_seccion.insert(f_seccion='Nutrición',f_laboratorio='LaboratorioB',f_jefe='mariaesthermoline@usb.ve')
db.t_seccion.insert(f_seccion='Polímeros',f_laboratorio='LaboratorioB',f_jefe='epenott@usb.ve')
db.t_seccion.insert(f_seccion='Procesos Químicos',f_laboratorio='LaboratorioB',f_jefe='grincon@usb.ve ')
db.t_seccion.insert(f_seccion='Química Analítica',f_laboratorio='LaboratorioB',f_jefe='cherrera@usb.ve')
db.t_seccion.insert(f_seccion='Química General',f_laboratorio='LaboratorioB',f_jefe='')
db.t_seccion.insert(f_seccion='Química Inorgánica',f_laboratorio='LaboratorioB',f_jefe='lubesv@usb.ve')
db.t_seccion.insert(f_seccion='Química Orgánica',f_laboratorio='LaboratorioB',f_jefe='eliergalarraga@usb.ve')

db.t_seccion.insert(f_seccion='Redes, Electrónica Analógica y Digital',f_laboratorio='LaboratorioC',f_jefe='jwalter@usb.ve ')
db.t_seccion.insert(f_seccion='Procesamiento de Señales y Sistemas',f_laboratorio='LaboratorioC',f_jefe='')
db.t_seccion.insert(f_seccion='Comunicaciones',f_laboratorio='LaboratorioC',f_jefe='jwalter@usb.ve ')
db.t_seccion.insert(f_seccion='Instrumentación y Control de Procesos y Sistemas',f_laboratorio='LaboratorioC',f_jefe='')
db.t_seccion.insert(f_seccion='Centro de Automatización Industrial',f_laboratorio='LaboratorioC',f_jefe='')
db.t_seccion.insert(f_seccion='Electrónica de Potencia',f_laboratorio='LaboratorioC',f_jefe='jwalter@usb.ve ')
db.t_seccion.insert(f_seccion='Sistemas Digitales',f_laboratorio='LaboratorioC',f_jefe='')
db.t_seccion.insert(f_seccion='Telecomunicaciones',f_laboratorio='LaboratorioC',f_jefe='')
db.t_seccion.insert(f_seccion='Mecatrónica',f_laboratorio='LaboratorioC',f_jefe='jwalter@usb.ve ')
db.t_seccion.insert(f_seccion='Control Automático',f_laboratorio='LaboratorioC',f_jefe='')
db.t_seccion.insert(f_seccion='Acústica y Comunicaciones',f_laboratorio='LaboratorioC',f_jefe='')
db.t_seccion.insert(f_seccion='Estado Sólido',f_laboratorio='LaboratorioC',f_jefe='')
db.t_seccion.insert(f_seccion='Biomecánica',f_laboratorio='LaboratorioC',f_jefe='')
db.t_seccion.insert(f_seccion='Sistemas Biomédicos',f_laboratorio='LaboratorioC',f_jefe='')
db.t_seccion.insert(f_seccion='Procesamiento de Señales y Sistemas',f_laboratorio='LaboratorioC',f_jefe='jwalter@usb.ve ')
db.t_seccion.insert(f_seccion='Grupo de Redes Electrónicas y Telemática Aplicada (GRETA)',f_laboratorio='LaboratorioC',f_jefe='')
db.t_seccion.insert(f_seccion='Grupo de Procesamiento de Señales (GPS)',f_laboratorio='LaboratorioC',f_jefe='')
db.t_seccion.insert(f_seccion='Grupo de Telecomunicaciones (GTEL)',f_laboratorio='LaboratorioC',f_jefe='')
db.t_seccion.insert(f_seccion='Grupo de Centro y Automatización Industrial (CAI)',f_laboratorio='LaboratorioC',f_jefe='')
db.t_seccion.insert(f_seccion='Grupo de Sistemas Industriales de Electrónica de Potencia (SIEP)',f_laboratorio='LaboratorioC',f_jefe='')
db.t_seccion.insert(f_seccion='Grupo de Laboratorio de Investigación en Sistemas de Información (LISI)',f_laboratorio='LaboratorioC',f_jefe='')
db.t_seccion.insert(f_seccion='Grupo de Mecatrónica',f_laboratorio='LaboratorioC',f_jefe='')
db.t_seccion.insert(f_seccion='Grupo de Biomecánica',f_laboratorio='LaboratorioC',f_jefe='')
db.t_seccion.insert(f_seccion='Laboratorio de Control Automático (LCA).',f_laboratorio='LaboratorioC',f_jefe='')
db.t_seccion.insert(f_seccion='Grupo de Energía Alternativa (GEA)',f_laboratorio='LaboratorioC',f_jefe='')
db.t_seccion.insert(f_seccion='Grupo de Laboratorio de Electrónica de Estados Sólidos (LEES)',f_laboratorio='LaboratorioC',f_jefe='')
db.t_seccion.insert(f_seccion='Grupo de Biomecánica, Rehabilitación y Procesamiento de Señales (GBRPS)',f_laboratorio='LaboratorioC',f_jefe='')

db.t_seccion.insert(f_seccion='Biofísica',f_laboratorio='LaboratorioD',f_jefe='severeynerika@usb.ve')
db.t_seccion.insert(f_seccion='Espectroscopía Laser ',f_laboratorio='LaboratorioD',f_jefe='rcastell@usb.ve')
db.t_seccion.insert(f_seccion='Física de Estado Sólido',f_laboratorio='LaboratorioD',f_jefe='abello@usb.ve')
db.t_seccion.insert(f_seccion='Física Nuclear',f_laboratorio='LaboratorioD',f_jefe='hbarros@usb.ve')
db.t_seccion.insert(f_seccion='Geofísica',f_laboratorio='LaboratorioD',f_jefe='cizarra@usb.ve')
db.t_seccion.insert(f_seccion='Laboratorio de Demostraciones',f_laboratorio='LaboratorioD',f_jefe='')
db.t_seccion.insert(f_seccion='Laboratorios Avanzados y de Post-grado',f_laboratorio='LaboratorioD',f_jefe='')
db.t_seccion.insert(f_seccion='Laboratorios Básicos',f_laboratorio='LaboratorioD',f_jefe='')
db.t_seccion.insert(f_seccion='Laboratorios Intermedios',f_laboratorio='LaboratorioD',f_jefe='')
db.t_seccion.insert(f_seccion='Simulaciones de la Materia Condensada',f_laboratorio='LaboratorioD',f_jefe='eguerre@usb.ve')
db.t_seccion.insert(f_seccion='Óptica',f_laboratorio='LaboratorioD',f_jefe='')
db.t_seccion.insert(f_seccion='Óptica e Interferometría',f_laboratorio='LaboratorioD',f_jefe='rescal@usb.ve')
db.t_seccion.insert(f_seccion='Óptica Moderna y Aplicada',f_laboratorio='LaboratorioD',f_jefe='clladera@usb.ve')
db.t_seccion.insert(f_seccion='Plasma Contínua y Pulsada',f_laboratorio='LaboratorioD',f_jefe='jgruiz@usb.ve')
db.t_seccion.insert(f_seccion='Psicofisiología y Conducta Humana ',f_laboratorio='LaboratorioD',f_jefe='lguarino@usb.ve')
db.t_seccion.insert(f_seccion='Sólidos I',f_laboratorio='LaboratorioD',f_jefe='')

db.t_seccion.insert(f_seccion='Cerámica y Suelos',f_laboratorio='LaboratorioE',f_jefe='neilmartinez@usb.ve')
db.t_seccion.insert(f_seccion='Coordinación de Actividades Técnicas',f_laboratorio='LaboratorioE',f_jefe='')
db.t_seccion.insert(f_seccion='Coordinación de Aseguramiento de la Calidad ',f_laboratorio='LaboratorioE',f_jefe='hrojas@usb.ve')
db.t_seccion.insert(f_seccion='Coordinación de Mantenimiento y Sistemas',f_laboratorio='LaboratorioE',f_jefe='')
db.t_seccion.insert(f_seccion='Corrosión',f_laboratorio='LaboratorioE',f_jefe='amendoza@usb.ve')
db.t_seccion.insert(f_seccion='Materiales',f_laboratorio='LaboratorioE',f_jefe='')
db.t_seccion.insert(f_seccion='Metalurgia Química',f_laboratorio='LaboratorioE',f_jefe='amolina@usb.ve')
db.t_seccion.insert(f_seccion='Metrología Dimensional',f_laboratorio='LaboratorioE',f_jefe='racosta@usb.ve')
db.t_seccion.insert(f_seccion='Microscopía Electrónica',f_laboratorio='LaboratorioE',f_jefe='amolina@usb.ve')
db.t_seccion.insert(f_seccion='Polímeros',f_laboratorio='LaboratorioE',f_jefe='nleon@usb.ve')
db.t_seccion.insert(f_seccion='Procesos Metalmecánicos',f_laboratorio='LaboratorioE',f_jefe='racosta@usb.ve')
db.t_seccion.insert(f_seccion='Procesos Metalúrgicos',f_laboratorio='LaboratorioE',f_jefe='mnino@usb.ve')

db.t_seccion.insert(f_seccion='Aulas Computarizadas',f_laboratorio='LaboratorioF',f_jefe='yudith@ldc.usb.ve  ')
db.t_seccion.insert(f_seccion='Computacional de Ciencia Política',f_laboratorio='LaboratorioF',f_jefe='avargas@usb.ve  ')
db.t_seccion.insert(f_seccion='Informática Educativa',f_laboratorio='LaboratorioF',f_jefe='mrivas@usb.ve  ')
db.t_seccion.insert(f_seccion='Lengua - José Santos Urriola',f_laboratorio='LaboratorioF',f_jefe='nmagdaleno@usb.ve  ')
db.t_seccion.insert(f_seccion='Computación',f_laboratorio='LaboratorioF',f_jefe='adiserio@usb.ve')
db.t_seccion.insert(f_seccion='Redes y Bases de Datos',f_laboratorio='LaboratorioF',f_jefe='mgoncalves@ldc.usb.ve')
db.t_seccion.insert(f_seccion='Diseño Asistido por Computadora',f_laboratorio='LaboratorioF',f_jefe='mscembo@usb.ve ')
db.t_seccion.insert(f_seccion='Matemáticas y Estadísticas Computacionales',f_laboratorio='LaboratorioF',f_jefe='jacob@usb.ve ')
db.t_seccion.insert(f_seccion='Centro de Estadística y Software Matemático',f_laboratorio='LaboratorioF',f_jefe='Isabel.llatas@gmail.com ')
db.t_seccion.insert(f_seccion='Bases de Datos',f_laboratorio='LaboratorioF',f_jefe='mgoncalves@ldc.usb.ve')
db.t_seccion.insert(f_seccion='Computación Gráfica y Multimedia',f_laboratorio='LaboratorioF',f_jefe='')
db.t_seccion.insert(f_seccion='Geomática Urbana',f_laboratorio='LaboratorioF',f_jefe='lusitano@usb.ve ')
db.t_seccion.insert(f_seccion='Inteligencia Artificial',f_laboratorio='LaboratorioF',f_jefe='martinez@ldc.usb.ve ')
db.t_seccion.insert(f_seccion='Investigación en Sistemas de Información',f_laboratorio='LaboratorioF',f_jefe='emendez@usb.ve')
db.t_seccion.insert(f_seccion='Lenguajes y Algoritmos',f_laboratorio='LaboratorioF',f_jefe='gpalma@ldc.usb.ve')
db.t_seccion.insert(f_seccion='Digital de Música',f_laboratorio='LaboratorioF',f_jefe='aizarra@usb.ve')
db.t_seccion.insert(f_seccion='Sistemas Paralelos y Distribuidos',f_laboratorio='LaboratorioF',f_jefe='figueira@ldc.usb.ve ')
db.t_seccion.insert(f_seccion='Computación de Alto Rendimiento',f_laboratorio='LaboratorioF',f_jefe='eduardo@ldc.usb.ve ')
db.t_seccion.insert(f_seccion='Estudios Tecnológicos',f_laboratorio='LaboratorioF',f_jefe='yudith@ldc.usb.ve')
db.t_seccion.insert(f_seccion='Idiomas Asistido por Computadoras ',f_laboratorio='LaboratorioF',f_jefe='camayora@usb.ve ')

db.t_seccion.insert(f_seccion='Conversión de Energía Electrica',f_laboratorio='LaboratorioD',f_jefe='')
db.t_seccion.insert(f_seccion='Conversión de Energía Mecánica',f_laboratorio='LaboratorioD',f_jefe='elsacardenas@usb.ve')
db.t_seccion.insert(f_seccion='Aeronaves',f_laboratorio='LaboratorioD',f_jefe='aamerio@usb.ve')
db.t_seccion.insert(f_seccion='Procesos Mecánicos de Fabricación y Materiales',f_laboratorio='LaboratorioD',f_jefe='')
db.t_seccion.insert(f_seccion='Física',f_laboratorio='LaboratorioD',f_jefe='chechelev@usb.ve')
db.t_seccion.insert(f_seccion='Fundamentos de Circuitos Eléctricos',f_laboratorio='LaboratorioD',f_jefe='hrssca@hotmail.com')
db.t_seccion.insert(f_seccion='Digitales',f_laboratorio='LaboratorioD',f_jefe='')
db.t_seccion.insert(f_seccion='Intrumentación y Control',f_laboratorio='LaboratorioD',f_jefe='dleal@usb.ve')
db.t_seccion.insert(f_seccion='Biomédica',f_laboratorio='LaboratorioD',f_jefe='kgomez@usb.ve')
db.t_seccion.insert(f_seccion='Tecnologías de la Información',f_laboratorio='LaboratorioD',f_jefe='chikhani@usb.ve')
db.t_seccion.insert(f_seccion='Telemática',f_laboratorio='LaboratorioD',f_jefe='jgutierr@usb.ve')
db.t_seccion.insert(f_seccion='Comunicaciones',f_laboratorio='LaboratorioD',f_jefe='oescobar@usb.ve')
db.t_seccion.insert(f_seccion='Idiomas',f_laboratorio='LaboratorioD',f_jefe='adenisraga@usb.ve')
db.t_seccion.insert(f_seccion='Alimentos y Bebidas',f_laboratorio='LaboratorioD',f_jefe='')
