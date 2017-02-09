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

def sustancia_manage():
    return dict()

def secciones_manage():
    return dict()

def laboratorio_manage():
    form = SQLFORM.smartgrid(db.t_laboratorio,onupdate=auth.archive)
    return locals()

def bitacora_manage():
    form = SQLFORM.smartgrid(db.t_bitacora,onupdate=auth.archive)
    return locals()

def solicitudes_manage():
    return dict()

def solicitud_manage():
    form = SQLFORM.smartgrid(db.t_solicitud,onupdate=auth.archive)
    return locals()
