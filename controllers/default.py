# -*- coding: utf-8 -*-
### required - do no delete
def user(): return dict(form=auth())
def login():
     return dict(form=auth.login())

def reset():
     return dict(form=auth.request_reset_password())
def download(): return response.download(request,db)
def call(): return service()
### end requires
def index():
    return dict()

def error():
    return dict()

def onvalidation(form):
    #print(form.vars)
    lab_none = db(db.t_laboratorio.f_nombre == 'Ninguno').select(db.t_laboratorio.id).first()
    sec_none = db(db.t_seccion.f_seccion == 'Ninguna').select(db.t_seccion.id).first()

    if form.vars.f_laboratorio == lab_none.id and form.vars.f_seccion != sec_none.id:
        form.errors.f_laboratorio = T('No puede estar vacio si elegiste una sección')
        #print(form.errors)

    #if form.errors: # form has errors
       #response.flash = 'Registration form processed, please check your email'


def onaccept(form): # form accepted
    user = db(db.auth_user.email == form.vars.email).select().first()

    if user.autorizado:
        jefesec = db(db.auth_group.role == "Jefe de Sección").select(db.auth_group.id).first()
        jefelab = db(db.auth_group.role == "Jefe de Laboratorio").select(db.auth_group.id).first()
        # Si es jefe de lab
        if form.vars.cargo == jefelab.id:
            lab = db(db.t_laboratorio.id==form.vars.f_laboratorio).select().first()
            lab.update_record(f_jefe=user.id)

        # Si es jefe secc
        elif form.vars.cargo == jefesec.id:
            sec = db(db.t_seccion.id==form.vars.f_seccion).select().first()
            sec.update_record(f_jefe=user.id)
