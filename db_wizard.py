######################################
db.define_table('table_solicitud',
    Field('f_sustancia', type='string',
          label=T('Sustancia')),
    Field('f_espaciofisico', type='string',
          label=T('Espaciofisico')),
    Field('f_seccion', type='string',
          label=T('Seccion')),
    Field('f_responsable', type='string',
          label=T('Responsable')),
    Field('f_solicitador', type='string',
          label=T('Solicitador')),
    Field('f_cantidadsolicitada', type='string',
          label=T('Cantidadsolicitada')),
    Field('f_estado', type='string',
          label=T('Estado')),
    Field('f_solicitud', type='string', 
          label=T('Fecha de Solicitud')),
    Field('f_respuesta', type='string', 
          label=T('Fecha de Respuesta')),

    format='%(f_sustancia)s',
    migrate=settings.migrate)

db.define_table('table_solicitud_archive',db.table_solicitud,Field('current_record','reference table_solicitud',readable=False,writable=False))
#####################################

