# -*- coding: utf-8 -*-
@auth.requires(auth.has_membership('Director') \
  or auth.has_membership('Administrador Personal') \
  or auth.has_membership('WebMaster'))

def index():
    pen = db(db.t_users_pendientes).count()
    return dict(message="Index de Gestión", users_pen=pen)

@auth.requires(auth.has_membership('Director') \
  or auth.has_membership('Administrador Personal') \
  or auth.has_membership('WebMaster'))
def usuarios():
    form = SQLFORM.smartgrid(db.auth_user,onupdate=auth.archive,csv=False,details=False,linked_tables=['auth_membership'], create=auth.has_membership('WebMaster'))
    return locals()

@auth.requires(auth.has_membership('Director') \
  or auth.has_membership('Administrador Personal') \
  or auth.has_membership('WebMaster'))
def privilegios():
    #db.auth_membership.group_id.writable = False
    form = SQLFORM.smartgrid(db.auth_group,onupdate=auth.archive,csv=False,details=False,linked_tables=['auth_membership'],deletable = auth.has_membership('WebMaster'), searchable=auth.has_membership('WebMaster'))
    return locals()

@auth.requires(auth.has_membership('Director') \
  or auth.has_membership('Administrador Personal') \
  or auth.has_membership('WebMaster'))
def autorizados():
    form = SQLFORM.smartgrid(db.t_users_autorizados,onupdate=auth.archive,csv=False,details=False)
    return locals()

@auth.requires(auth.has_membership('Director') \
  or auth.has_membership('Administrador Personal') \
  or auth.has_membership('WebMaster'))
def pendientes():
    confirmar_usuario = lambda row: A('Confirmar', _href=URL(c='gestion',f='confirmar', args=[row.f_email, row.f_group]))
    eliminar_p = lambda row: A('Eliminar', _href=URL(c='gestion',f='eliminar_p', args=[row.f_email, row.f_group]))
    links = [confirmar_usuario, eliminar_p]
    form = SQLFORM.smartgrid(db.t_users_pendientes,onupdate=auth.archive,csv=False,create =False,details=False,deletable = False, links=links)
    return locals()

@auth.requires(auth.has_membership('Director') \
  or auth.has_membership('Administrador Personal') \
  or auth.has_membership('WebMaster'))
def confirmar():
    user_email = request.args[0]
    user_cargo = request.args[1]
    usuario = db(db.auth_user.email==user_email).select().first()
    usuario.update_record(autorizado=True)
    usuario.update_record(cargo=user_cargo)

    auth.del_membership(auth.id_group(role="Usuario Normal"), usuario.id)
    auth.add_membership(user_cargo, usuario.id)

    db(db.t_users_pendientes.f_email == user_email).delete()

    redirect(URL(c='gestion',f='pendientes'))

@auth.requires(auth.has_membership('Director') \
  or auth.has_membership('Administrador Personal') \
  or auth.has_membership('WebMaster'))
def eliminar_p():
    user_email = request.args[0]
    user_cargo = request.args[1]
    usuario = db(db.auth_user.email==user_email).select().first()

    auth.del_membership(auth.id_group(role="Usuario Normal"), usuario.id)

    db(db.t_users_pendientes.f_email == user_email).delete()
    db(db.auth_user.email == user_email).delete()

    redirect(URL(c='gestion',f='pendientes'))

@auth.requires(auth.has_membership('Director') \
  or auth.has_membership('Administrador Personal') \
  or auth.has_membership('WebMaster'))
def laboratorios():
    form = SQLFORM.smartgrid(db.t_laboratorio,onupdate=auth.archive,csv=False,details=False, linked_tables=['t_seccion'], deletable = auth.has_membership('WebMaster'))
    return locals()

@auth.requires(auth.has_membership('Director') \
  or auth.has_membership('Administrador Personal') \
  or auth.has_membership('WebMaster'))
def secciones():
    form = SQLFORM.smartgrid(db.t_seccion,onupdate=auth.archive, csv=False, details=False, linked_tables=['t_espaciofisico'], deletable = auth.has_membership('WebMaster'))
    return locals()

@auth.requires(auth.has_membership('Director') \
  or auth.has_membership('Administrador Personal') \
  or auth.has_membership('WebMaster'))
def espacios():
    db.t_tecs_esp.f_espaciofisico.writable = False
    form = SQLFORM.smartgrid(db.t_espaciofisico,onupdate=auth.archive,csv=False,details=False, linked_tables=['t_tecs_esp'])
    return locals()
