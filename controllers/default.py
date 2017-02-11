# -*- coding: utf-8 -*-
### required - do no delete
def user(): return dict(form=auth())
def download(): return response.download(request,db)
def call(): return service()
### end requires
def index():
    return dict()

def error():
    return dict()
@auth.requires_login()
def sustancia_manage():
    return dict()
@auth.requires_login()
def secciones_manage():
    return dict()
@auth.requires_login()
def laboratorio_manage():
    form = SQLFORM.smartgrid(db.t_laboratorio,onupdate=auth.archive)
    return locals()
@auth.requires_login()
def bitacora_manage():
    form = SQLFORM.smartgrid(db.t_bitacora,onupdate=auth.archive)
    return locals()
@auth.requires_login()
def solicitudes_manage():
    return dict()
@auth.requires_login()
def solicitud_manage():
    form = SQLFORM.smartgrid(db.t_solicitud,onupdate=auth.archive)
    return locals()
