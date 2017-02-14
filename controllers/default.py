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

@auth.requires(auth.has_membership('Director') \
  or auth.has_membership('Administrador Personal') \
  or auth.has_membership('WebMaster')\
  or auth.has_membership('Jefe de Laboratorio') \
  or auth.has_membership('Jefe de Sección') \
  or auth.has_membership('Técnico')\
  or auth.has_membership('Gestor de Sustancias'))
def sustancia_manage():
    return dict()

@auth.requires(auth.has_membership('Director') \
  or auth.has_membership('Administrador Personal') \
  or auth.has_membership('WebMaster')\
  or auth.has_membership('Jefe de Laboratorio') \
  or auth.has_membership('Jefe de Sección') \
  or auth.has_membership('Técnico')\
  or auth.has_membership('Gestor de Sustancias'))
def secciones_manage():
    return dict()

@auth.requires(auth.has_membership('Director') \
  or auth.has_membership('Administrador Personal') \
  or auth.has_membership('WebMaster')\
  or auth.has_membership('Jefe de Laboratorio') \
  or auth.has_membership('Jefe de Sección') \
  or auth.has_membership('Técnico')\
  or auth.has_membership('Gestor de Sustancias'))
def laboratorio_manage():
    form = SQLFORM.smartgrid(db.t_laboratorio,onupdate=auth.archive)
    return locals()

@auth.requires(auth.has_membership('Director') \
  or auth.has_membership('Administrador Personal') \
  or auth.has_membership('WebMaster')\
  or auth.has_membership('Jefe de Laboratorio') \
  or auth.has_membership('Jefe de Sección') \
  or auth.has_membership('Técnico')\
  or auth.has_membership('Gestor de Sustancias'))
def bitacora_manage():
    form = SQLFORM.smartgrid(db.t_bitacora,onupdate=auth.archive)
    return locals()

@auth.requires(auth.has_membership('Director') \
  or auth.has_membership('Administrador Personal') \
  or auth.has_membership('WebMaster')\
  or auth.has_membership('Jefe de Laboratorio') \
  or auth.has_membership('Jefe de Sección') \
  or auth.has_membership('Técnico')\
  or auth.has_membership('Gestor de Sustancias'))
def solicitudes_manage():
    return dict()

@auth.requires(auth.has_membership('Director') \
  or auth.has_membership('Administrador Personal') \
  or auth.has_membership('WebMaster')\
  or auth.has_membership('Jefe de Laboratorio') \
  or auth.has_membership('Jefe de Sección') \
  or auth.has_membership('Técnico')\
  or auth.has_membership('Gestor de Sustancias'))
def solicitud_manage():
    form = SQLFORM.smartgrid(db.t_solicitud,onupdate=auth.archive)
    return locals()
