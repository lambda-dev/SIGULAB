app = request.application
response.title = settings.title
response.subtitle = settings.subtitle
response.meta.author = '%(author)s <%(author_email)s>' % settings
response.meta.keywords = settings.keywords
response.meta.description = settings.description
#pen = db(db.t_users_pendientes).count()

# user basico
response.menu = [
    ]
#tec, jefes y gestor
if (not auth.has_membership('Usuario Normal') and (not auth.has_membership('Administrador Personal')) and auth.is_logged_in()):
    response.menu += [
    [T('SMyDP'),False,None,[
            (T('Inventario'),URL('sustancias','select_inventario'),URL('sustancias','select_inventario')),
            (T('Listado de Sustancias'),URL('sustancias','sustanciapeligrosa_manage'),URL('sustancias','sustanciapeligrosa_manage')),
            ]],
    [T('Facturación'),URL('sustancias','view_compras'),URL('sustancias','view_compras')]
    ]

if not auth.has_membership('Usuario Normal') and not auth.has_membership('Técnico') and not auth.has_membership('Administrador Personal') and auth.is_logged_in():
    response.menu += [
    [T('Solicitudes'),False, None,[
      [T('Hacer Solicitud'), False, URL('solicitud','select_solicitud')],
      [T('Solicitudes Recibidas'), False, URL('solicitud','view_h')],
      [T('Prestamos'), False, URL('solicitud','view_k')],
      [T('Deudas'), False, URL('solicitud','view_o')]
      ]]
      ]

#dir o admin user
if (auth.has_membership('Director') or auth.has_membership('WebMaster') or auth.has_membership('Administrador Personal')) and (not auth.has_membership('Usuario Normal')):
    response.menu += [
    [T('Gestión Usuarios'),False, None,[
      #[T('Pendientes de confirmación ('+str(pen)+')'), False, URL('gestion','pendientes')],
      [T('Pendientes de confirmación'), False, URL('gestion','pendientes')],
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
