# -*- coding: utf-8 -*-
# try something like
@auth.requires(auth.has_membership('Director') \
  or auth.has_membership('Administrador Personal') \
  or auth.has_membership('WebMaster')\
  or auth.has_membership('Jefe de Laboratorio') \
  or auth.has_membership('Jefe de Sección') \
  or auth.has_membership('Técnico')\
  or auth.has_membership('Gestor de Sustancias'))
def index():
    return dict()

@auth.requires(auth.has_membership('Director') \
  or auth.has_membership('Administrador Personal') \
  or auth.has_membership('WebMaster')\
  or auth.has_membership('Jefe de Laboratorio') \
  or auth.has_membership('Jefe de Sección') \
  or auth.has_membership('Técnico')\
  or auth.has_membership('Gestor de Sustancias'))
def sustancias():
    return dict()
    
@auth.requires(auth.has_membership('Director') \
  or auth.has_membership('Administrador Personal') \
  or auth.has_membership('WebMaster')\
  or auth.has_membership('Jefe de Laboratorio') \
  or auth.has_membership('Jefe de Sección') \
  or auth.has_membership('Técnico')\
  or auth.has_membership('Gestor de Sustancias'))
def desechos():
    return dict()
