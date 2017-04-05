# -*- coding: utf-8 -*-
from plugin_notemptymarker import mark_not_empty

@auth.requires(auth.has_membership('Director') \
  or auth.has_membership('Administrador Personal') \
  or auth.has_membership('WebMaster'))

def index():
    pen = db(db.t_users_pendientes).count()
    return dict(users_pen=pen)

@auth.requires(auth.has_membership('Director') \
  or auth.has_membership('Administrador Personal') \
  or auth.has_membership('WebMaster'))
def index_e():
    return dict()

@auth.requires(auth.has_membership('Director') \
  or auth.has_membership('Administrador Personal') \
  or auth.has_membership('WebMaster'))
def usuarios():
    if 'edit' in request.args or 'new' in request.args:
        mark_not_empty(db.auth_user)

    db.auth_user.id.readable=False
    query = (db.auth_user.autorizado == True and db.auth_user.email != "no_asig@usb.ve")
    if auth.has_membership('Director'):  
        form = SQLFORM.smartgrid(db.auth_user,constraints=dict(auth_user=query),csv=False,details=False,linked_tables=['auth_membership'], create=False, editable=False, deletable=False)
    else:
        form = SQLFORM.smartgrid(db.auth_user,constraints=dict(auth_user=query),ondelete=trig_delete,csv=False,details=False,linked_tables=['auth_membership'], create=False)
    return locals()

def trig_delete(table, rid):
    # Limpiamos los laboratorios, secciones y espacios donde estaba asignado el usuario, se coloca al user No Asignado
    db(db.t_laboratorio.f_jefe == rid).update(f_jefe = db(db.auth_user.email == 'no_asig@usb.ve').select(db.auth_user.id).first())

    db(db.t_seccion.f_jefe == rid).update(f_jefe = db(db.auth_user.email == 'no_asig@usb.ve').select(db.auth_user.id).first())

    db(db.t_tecs_esp.f_tecnico == rid).delete()

@auth.requires(auth.has_membership('Director') \
  or auth.has_membership('Administrador Personal') \
  or auth.has_membership('WebMaster'))
def privilegios():
    if 'edit' in request.args or 'new' in request.args:
        mark_not_empty(db.auth_group)

    db.auth_group.id.readable=False
    if auth.has_membership('Director'):
        form = SQLFORM.smartgrid(db.auth_group,onvalidation=validar_roles,csv=False,details=False,linked_tables=['auth_membership'],create=False, editable=False, deletable=False, searchable=False)
    else:
        form = SQLFORM.smartgrid(db.auth_group,onvalidation=validar_roles,csv=False,details=False,linked_tables=['auth_membership'],deletable = auth.has_membership('WebMaster'), searchable=auth.has_membership('WebMaster'))
    return locals()

def validar_roles(form):
    if 'edit' in request.args:
      if form.vars.group_id == 2:
        if db(db.auth_membership.group_id == 2).count() >= 1:
          form.errors.group_id = T('No puede haber más de un Director')

      elif form.vars.group_id == 5:
        n_jefes = db(db.auth_membership.group_id == 5).count()
        n_labs = db(db.t_laboratorio.id>0).count()
        if n_jefes >= n_labs:
          form.errors.group_id = T('No pueden haber más Jefes que Laboratorios')

@auth.requires(auth.has_membership('Director') \
  or auth.has_membership('Administrador Personal') \
  or auth.has_membership('WebMaster'))
def autorizados():
    if 'edit' in request.args or 'new' in request.args:
        mark_not_empty(db.t_users_autorizados)

    db.t_users_autorizados.id.readable=False
    if auth.has_membership('Director'):
        form = SQLFORM.smartgrid(db.t_users_autorizados,csv=False,details=False, create=False, editable=False, deletable=False)
    else:
        form = SQLFORM.smartgrid(db.t_users_autorizados,csv=False,details=False)
    return locals()

@auth.requires(auth.has_membership('Director') \
  or auth.has_membership('Administrador Personal') \
  or auth.has_membership('WebMaster'))
def pendientes():
    if 'edit' in request.args or 'new' in request.args:
        mark_not_empty(db.t_users_pendientes)
    confirmar_usuario = lambda row: A('Confirmar', _href=URL(c='gestion',f='confirmar', args=[row.f_email, row.f_group, row.f_seccion, row.f_laboratorio]))
    eliminar_p = lambda row: A('Eliminar', _href=URL(c='gestion',f='eliminar_p', args=[row.f_email, row.f_group, row.f_seccion, row.f_laboratorio]))
    links = [confirmar_usuario, eliminar_p]

    db.t_users_pendientes.id.readable=False
    if auth.has_membership('Director'):
        form = SQLFORM.smartgrid(db.t_users_pendientes,csv=False,create =False,details=False,deletable = False, editable=False, links=links)
    else:
        form = SQLFORM.smartgrid(db.t_users_pendientes,csv=False,create =False,details=False,deletable = False, links=links)
    return locals()

@auth.requires(auth.has_membership('Director') \
  or auth.has_membership('Administrador Personal') \
  or auth.has_membership('WebMaster'))
def confirmar():
    user_email = request.args[0]
    user_cargo = request.args[1]
    user_sec = request.args[2]
    user_lab = request.args[3]

    jefesec = db(db.auth_group.role == "Jefe de Sección").select(db.auth_group.id).first()
    jefelab = db(db.auth_group.role == "Jefe de Laboratorio").select(db.auth_group.id).first()
    direct = db(db.auth_group.role == "Director").select(db.auth_group.id).first()
 
    if int(user_cargo) == direct.id:
        if db(db.auth_membership.group_id == 2).count() >= 1:
            session.flash = "Ya existe un Director"
            redirect(URL(c='gestion',f='pendientes'))
            return
            
    elif int(user_cargo) == jefelab.id:
        n_jefes = db(db.auth_membership.group_id == 5).count()
        n_labs = db(db.t_laboratorio.id>0).count()
        if n_jefes >= n_labs:
            session.flash = T('No pueden haber más Jefes que Laboratorios')
            redirect(URL(c='gestion',f='pendientes'))
            return

        lab_empty = db(db.t_laboratorio.f_nombre=="Ninguno").select(db.t_laboratorio.id).first()
        if int(user_lab) == lab_empty.id:
            session.flash = T('El Laboratorio para el Jefe no puede ser vacio')
            redirect(URL(c='gestion',f='pendientes'))
            return

    elif int(user_cargo) == jefesec.id:
        sec_empty = db(db.t_seccion.f_seccion=="Ninguna").select(db.t_seccion.id).first()
        if int(user_sec) == sec_empty.id:
            session.flash = T('La Sección para el Jefe no puede ser vacia')
            redirect(URL(c='gestion',f='pendientes'))
            return

    usuario = db(db.auth_user.email==user_email).select().first()
    usuario.update_record(autorizado=True)
    usuario.update_record(cargo=user_cargo)
    usuario.update_record(f_laboratorio=user_lab)
    usuario.update_record(f_seccion=user_sec)

    # Si es jefe de lab
    if int(user_cargo) == jefelab.id:
        lab = db(db.t_laboratorio.id==int(user_lab)).select().first()
        lab.update_record(f_jefe=usuario.id)
        session.flash = T('Actualizado el Jefe de Laboratorio')

    # Si es jefe secc    
    elif int(user_cargo) == jefesec.id:
        sec = db(db.t_seccion.id==int(user_sec)).select().first()
        sec.update_record(f_jefe=usuario.id)
        session.flash = T('Actualizado el Jefe de Sección')

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
    session.flash = "El usuario ha sido eliminado"
    redirect(URL(c='gestion',f='pendientes'))

@auth.requires(auth.has_membership('Director') \
  or auth.has_membership('Administrador Personal') \
  or auth.has_membership('WebMaster'))
def laboratorios():
    if 'edit' in request.args or 'new' in request.args:
        mark_not_empty(db.t_laboratorio)

    db.t_laboratorio.id.readable=False
    db.t_seccion.f_laboratorio.readable=False
    query = (db.t_laboratorio.f_nombre != "Ninguno")
    try:
        lab_id = request.args[2]
        lab = db(db.t_laboratorio.id == lab_id).select(db.t_laboratorio.f_nombre).first()
    except:
        lab_id = None

    if auth.has_membership('Director'):
        form = SQLFORM.smartgrid(db.t_laboratorio,constraints=dict(t_laboratorio=query),onvalidation=validar_jefes,csv=False,details=False, linked_tables=['t_seccion'], deletable = False, editable=False, create=False)
    else:
        form = SQLFORM.smartgrid(db.t_laboratorio,constraints=dict(t_laboratorio=query),onvalidation=validar_jefes,csv=False, details=False,linked_tables=['t_seccion'], deletable = True, editable = True,)
    return locals()

def validar_jefes(form):
    if 'edit' in request.args:
        if form.vars.f_jefe != db(db.auth_user.email == 'no_asig@usb.ve').select(db.auth_user.id).first().id:

            # Buscamos si tiene privilegio de JefeLab
            es_jefe=False
            id_jl = db(db.auth_group.role == "Jefe de Laboratorio").select(db.auth_group.id).first().id
            privilegios = db(db.auth_membership.user_id == form.vars.f_jefe).select(db.auth_membership.group_id)
            for row in privilegios:
                print(id_jl)
                if row.group_id == id_jl:
                    es_jefe=True
                    break

            if not es_jefe:
                form.errors.f_jefe = T("El usuario no tiene el privilegio de Jefe de Laboratorio")
                return 

            for lab in db(db.t_laboratorio.id > 0).select(db.t_laboratorio.f_jefe, db.t_laboratorio.id): 
                if (lab.f_jefe == form.vars.f_jefe):
                    if (int(lab.id) != int(form.record_id)):
                        form.errors.f_jefe = T('No pueden haber Jefes que ocupen más de una Jefatura')

@auth.requires(auth.has_membership('Director') \
  or auth.has_membership('Administrador Personal') \
  or auth.has_membership('WebMaster'))
def secciones():
    if 'edit' in request.args or 'new' in request.args:
        mark_not_empty(db.t_seccion)

    db.t_seccion.id.readable=False
    db.t_espaciofisico.f_seccion.readable=False
    query = (db.t_seccion.f_seccion != "Ninguna")

    try:
        secc_id = request.args[2]
        secc = db(db.t_seccion.id == secc_id).select(db.t_seccion.f_seccion).first()
    except:
        secc_id = None

    if auth.has_membership('Director'):
        form = SQLFORM.smartgrid(db.t_seccion, constraints=dict(t_seccion=query),onvalidation=validar_jefes_sec, csv=False, details=False, linked_tables=['t_espaciofisico'], deletable = False, editable=False, create=False)
    else:
        form = SQLFORM.smartgrid(db.t_seccion, constraints=dict(t_seccion=query),onvalidation=validar_jefes_sec, csv=False, details=False, linked_tables=['t_espaciofisico'], deletable = auth.has_membership('WebMaster'))
    return locals()

def validar_jefes_sec(form):
    if 'edit' in request.args:
        if form.vars.f_jefe != db(db.auth_user.email == 'no_asig@usb.ve').select(db.auth_user.id).first().id:

            # Buscamos si tiene privilegio de JefeSec
            es_jefe=False
            id_js = db(db.auth_group.role == "Jefe de Sección").select(db.auth_group.id).first().id
            privilegios = db(db.auth_membership.user_id == form.vars.f_jefe).select(db.auth_membership.group_id)
            for row in privilegios:
                if row.group_id == id_js:
                    es_jefe=True
                    break

            if not es_jefe:
                form.errors.f_jefe = T("El usuario no tiene el privilegio de Jefe de Sección")
                return 

@auth.requires(auth.has_membership('Director') \
  or auth.has_membership('Administrador Personal') \
  or auth.has_membership('WebMaster'))
def espacios():
    inventario = lambda row: A('Inventario', _href=URL(c='sustancias', f='inventario_manage',vars=dict(esp = row.id) ) )
    links = [inventario]
    if 'edit' in request.args or 'new' in request.args:
        mark_not_empty(db.t_espaciofisico)
    db.t_tecs_esp.f_espaciofisico.writable = False

    db.t_espaciofisico.id.readable=False
    if auth.has_membership('Director'):
        form = SQLFORM.smartgrid(db.t_espaciofisico,csv=False,details=False, linked_tables=['t_tecs_esp'], editable=False, create=False, deletable=False,links = links)
    else:
        form = SQLFORM.smartgrid(db.t_espaciofisico,csv=False,details=False, linked_tables=['t_tecs_esp'],links=links)
    return locals()
