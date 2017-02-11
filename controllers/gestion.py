# -*- coding: utf-8 -*-
@auth.requires(auth.has_membership('Director') \
  or auth.has_membership('Administrador Personal') \
  or auth.has_membership('WebMaster'))
def index(): 
    return dict(message="Index de Gestión")

@auth.requires(auth.has_membership('Director') \
  or auth.has_membership('Administrador Personal') \
  or auth.has_membership('WebMaster'))
def usuarios():
    form = SQLFORM.smartgrid(db.auth_user,onupdate=auth.archive,csv=False,details=False,linked_tables=['auth_membership'])#,links=links)
    return locals()

@auth.requires(auth.has_membership('Director') \
  or auth.has_membership('Administrador Personal') \
  or auth.has_membership('WebMaster'))
def privilegios():
    form = SQLFORM.smartgrid(db.auth_group,onupdate=auth.archive,csv=False,details=False,linked_tables=['auth_membership'])
    return locals()

@auth.requires(auth.has_membership('Director') \
  or auth.has_membership('Administrador Personal') \
  or auth.has_membership('WebMaster'))
def autorizados():
    form = SQLFORM.smartgrid(db.t_users_autorizados,onupdate=auth.archive,csv=False,details=False)
    return locals()

