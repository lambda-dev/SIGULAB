app = request.application
response.title = settings.title
response.subtitle = settings.subtitle
response.meta.author = '%(author)s <%(author_email)s>' % settings
response.meta.keywords = settings.keywords
response.meta.description = settings.description
pen = db(db.t_users_pendientes).count()

# Editado por Adolfo
# user basico
response.menu = [
    [T('Home'),URL('default','index')==URL(),URL('default','index')]
    ]
#tec, jefes y gestor
if not auth.has_membership('Usuario Normal') and auth.is_logged_in():
    response.menu += [
    [T('SMyDP'),False,None,[
            (T('Inventario'),URL('sustancias','select_inventario'),URL('sustancias','select_inventario')),
            (T('Listado de Sustancias'),URL('sustancias','sustanciapeligrosa_manage'),URL('sustancias','sustanciapeligrosa_manage')),
            ]],
    [T('Solicitudes'),False, None,[
    	(T('Entrada'), URL('s_entrada','entrada'), URL('s_entrada','entrada')),(T('Salida'), URL('s_entrada','salida'), URL('s_entrada','salida'))
    		]]
    ]
#dir o admin user
if auth.has_membership('Director') or auth.has_membership('WebMaster') or auth.has_membership('Administrador Personal'):
    response.menu += [
    [T('Gestión Usuarios'),False, None,[
      (T('Lista de Autorizados'), False, URL('gestion','autorizados')),
      (T('Usuarios Registrados'), False, URL('gestion','usuarios')),
      [T('Pendientes de confirmación ('+str(pen)+')'), False, URL('gestion','pendientes')], 
      [T('Privilegios'), False, URL('gestion','privilegios')],
      [T('Membresia'), False, URL('gestion','membresia')]
      ]],
    [T('Gestión Espacios'), False, None, [
      [T('Laboratorios'), False, URL('gestion','laboratorios')],
      [T('Secciones'), False, URL('gestion','secciones')]
    ]]
    ]
#superuser
if auth.has_membership('WebMaster'):
    response.menu += [
    [T('Editar'), False, URL('admin', 'default', 'design/%s' % app)]
    ]


#Original
# response.menu = [
# (T('Home'),URL('default','index')==URL(),URL('default','index'),[]),
# (T('SMyDP'),False,None,[
#         (T('Inventario'),URL('sustancias','select_inventario'),URL('sustancias','select_inventario')),
#         (T('Listado de Sustancias'),URL('sustancias','sustanciapeligrosa_manage'),URL('sustancias','sustanciapeligrosa_manage')),
#         ]),
# (T('Solicitudes'),False, None,[
#   (T('Entrada'), URL('s_entrada','entrada'), URL('s_entrada','entrada')),(T('Salida'), URL('s_entrada','salida'), URL('s_entrada','salida'))
#     ]),
# (T('Prestamos'),False, None,[
#   (T('Por devolver'), URL('s_entrada','p_por_devolver'), URL('s_entrada','p_por_devolver')),(T('Por recibir'), URL('s_entrada','p_por_recibir'), URL('s_entrada','p_por_recibir'))
#     ]),
# (T('Gestión'),False, None,[
#   (T('Usuarios'), URL('gestion','usuarios'), URL('gestion','usuarios')), (T('Privilegios'), URL('gestion','privilegios'), URL('gestion','privilegios'))
#     ]),
# #(T('Editar'), False, URL('admin', 'default', 'design/%s' % app)),
# #(T('Personal'),URL('default','personal_manage')==URL(),URL('default','personal_manage'),[]),
# #(T('Rol'),URL('default','rol_manage')==URL(),URL('default','rol_manage'),[]),
# #(T('Sustancia'),URL('default','sustancia_manage')==URL(),URL('default','sustancia_manage'),[]),
# #(T('Secciones'),URL('default','secciones_manage')==URL(),URL('default','secciones_manage'),[]),
# #(T('Laboratorio'),URL('default','laboratorio_manage')==URL(),URL('default','laboratorio_manage'),[]),
# #(T('Bitacora'),URL('default','bitacora_manage')==URL(),URL('default','bitacora_manage'),[]),
# #(T('Solicitudes'),URL('default','solicitudes_manage')==URL(),URL('default','solicitudes_manage'),[]),
# #(T('Sustanciapeligrosa'),URL('default','sustanciapeligrosa_manage')==URL(),URL('default','sustanciapeligrosa_manage'),[]),
# #(T('Cargo'),URL('default','cargo_manage')==URL(),URL('default','cargo_manage'),[]),
# #(T('Inventario'),URL('default','inventario_manage')==URL(),URL('default','inventario_manage'),[]),
# #(T('Solicitud'),URL('default','solicitud_manage')==URL(),URL('default','solicitud_manage'),[]),
# ]
