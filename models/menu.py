app = request.application
response.title = settings.title
response.subtitle = settings.subtitle
response.meta.author = '%(author)s <%(author_email)s>' % settings
response.meta.keywords = settings.keywords
response.meta.description = settings.description
response.logo = A(IMG(_src=URL('static', 'images/logo-ulab.png'), _href=URL('default', 'index'),_style='height:50px;width:auto;'),_class='navbar-brand',_style='transform:translateY(-10px);')
pen = db(db.t_users_pendientes).count()

# user basico
response.menu = []
#tec, jefes y gestor
if (auth.has_membership('Técnico') or auth.has_membership('Jefe de Sección') or auth.has_membership('Jefe de Laboratorio') or \
  auth.has_membership('Gestor de Sustancias') or auth.has_membership('Director') or auth.has_membership('WebMaster')) and auth.is_logged_in() and (not auth.has_membership('Usuario Normal')):
    response.menu += [
    [T('SMyDP'),False,None,[
            (T('Inventario'),URL('sustancias','select_inventario'),URL('sustancias','select_inventario')),
            (T('Listado de Sustancias'),URL('sustancias','sustanciapeligrosa_manage'),URL('sustancias','sustanciapeligrosa_manage')),
            ]],
    [T('Facturación'),URL('sustancias','view_compras'),URL('sustancias','view_compras')],
    [T('Solicitudes'),False, None,[
      [T('Mis Solicitudes'), False, URL('solicitud','select_solicitud', vars=dict(f=1))],
      [T('Solicitudes Recibidas'), False, URL('solicitud','select_solicitud', vars=dict(f=2))],
      [T('Prestamos'), False, URL('solicitud','select_solicitud', vars=dict(f=3))],
      [T('Deudas'), False, URL('solicitud','select_solicitud',vars=dict(f=4))]
      ]]
      ]

#dir o admin user
if (auth.has_membership('Director') or auth.has_membership('WebMaster') or auth.has_membership('Administrador Personal')) and (not auth.has_membership('Usuario Normal')):
    response.menu += [
    [T('Gestión Usuarios'),False, None,[
      [T('Pendientes de confirmación ('+str(pen)+')'), False, URL('gestion','pendientes')],
      [T('Usuarios Autorizados'), False, URL('gestion','autorizados')],
      [T('Usuarios Registrados'), False, URL('gestion','usuarios')],
      [T('Privilegios'), False, URL('gestion','privilegios')]
      ]],
    [T('Gestión Espacios'), False, None, [
      [T('Laboratorios'), False, URL('gestion','laboratorios')],
      [T('Secciones'), False, URL('gestion','secciones')],
      [T('Espacios Físicos'), False, URL('gestion','espacios')]
    ]]
    ]
#superuser
if auth.has_membership('WebMaster') and (not auth.has_membership('Usuario Normal')):
    response.menu += [
    [T('Editar'), False, URL(c='appadmin',f='index')]
    ]
