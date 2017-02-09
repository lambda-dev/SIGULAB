# -*- coding: utf-8 -*-
@auth.requires(auth.has_membership(group_id=1) or auth.has_membership(group_id=2))
def index(): 
    return dict(message="hello from gestion.py")

@auth.requires(auth.has_membership(group_id=1) or auth.has_membership(group_id=2))
def usuarios():
    form = SQLFORM.smartgrid(db.auth_user,onupdate=auth.archive)
    return locals()

@auth.requires(auth.has_membership(group_id=1) or auth.has_membership(group_id=2))
def privilegios():
    form = SQLFORM.smartgrid(db.auth_group,onupdate=auth.archive)
    return locals()

