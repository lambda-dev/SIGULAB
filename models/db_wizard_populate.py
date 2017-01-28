from gluon.contrib.populate import populate
if db(db.auth_user).isempty():
     populate(db.t_cargo,10)
     populate(db.t_inventario,10)
     populate(db.t_bitacora,10)
     populate(db.t_personal,10)
     populate(db.t_laboratorio,10)
     populate(db.t_sustanciapeligrosa,10)
     populate(db.t_solicitud,10)
