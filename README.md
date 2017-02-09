# SIGULAB
Branch de Adolfo
******************
Ya está disponible 'gestion de usuarios' y 'gestion de privlegios'
También arreglé algunas opciones:

+ Usuarios al registrarse tienen que ser aceptados por admin
(Es por db pero esto viendo como simplificarlo)

+ Al registrarse se unen automaticamente al grupo 'Usuario' cuyo unico
permiso/privilegio es ver la pagina inicial.

+ En el menu aparecen las opciones segun el rango. Tecnicos, jefes de lab/sec no 
pueden ver, ni acceder a gestion de usuarios/privilegios.

+ Me falta modificar los otros controladores para que usuarios sin privilegio no puedan
acceder a diferentes secciones.