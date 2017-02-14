# SIGULAB
Branch de Adolfo
******************
12 Febrero:

Habemus registro por tabla!
+ Al registrarse usurio especifica su cargo. Luego al enviar ocurre:
  + Si el email + cargo coinciden con la lista de autorizacion, el usuario puede logearse y usar el sistema sin ningun otro problema
  + Si no esta el email en la tabla de autorizacion, o si puso un cargo diferente, se guarda en la tabla de pendientes y debe ser autorizado por el Administrador de Usuario. Este usuario solo puede logearse pero no tiene acceso a las otras partes del sistema.

+ Admin de Usuarios puede:
  + Añadir a la tabla de autorizacion para que los usuarios se registren
  + Aprobar, eliminar o editar la lista de pendientes para que esos usuarios puedan usar el sistema

+ Index de gestion muestra un aviso de cuantos usuarios pendientes están esperando.

TODO: 
+ Enviar email a los usuarios Administradores para que sepan cuando hay un pendiente nuevo
+ Validacion solo usa email + cargo. Me habian dicho que tambien hay que validar EspacioFisico + Seccion + Laboratorio.
+ ¿Como se le asigna al usuario esos datos? ¿Como hace si tiene mas de un EF, S o L?
¿Esos datos los da el usuario o el Admin? ¿Si son mas de 1, como se valida?




10 Febrero:

+ Está creada la tabla t_users_autorizados donde van los usuarios pre-aceptados. Habia entendido que esta tabla solo tiene email y cargo/rol/privilegio. Disponible nuevo menu en 'Gestion' para añadirlos.

TODO: Editar el proceso de registro para que complete solo si el email hace match en esta tabla *else* se envia email a usuarios con rango 'Administrador de Personal' para 
que los pre-acepten.

+ Creado rango/rol/privilegio 'WebMaster' para nosotros, por default se crea un user si 
la db esta vacia con email webmaster@sigulab.com y pass 0000. 

+ Edite los decoradores de auth para que usen el nombre del rol y no el id, ya que el id puede variar por instalación 

TODO: Acomodar en todos los controladores

TODO: Modificar heavymente el registro => Usuarios deben especificar ES/SEC/LAB y cargo.
      Triggers para añadir en db?

+ Disponible menu 'gestion de membresia' donde se listan todos los usuarios y todos sus privilegios asignados. Se pueden añadir/editar/eliminar por Direc/Admin U.

+ Asumo que el Director/Admin User NO puede añadir o eliminar CARGOS existentes:
  + Si añade nuevos no van a tener ningun efecto porque los permisos como tal están hard coded con los decoradores auth
  + Si borra alguno de los existente, bueno, muere esa funcionalidad hasta que se agrege otro con el mismo nombre.
  + Entonces solo user WebMaster pueden editar esto. 
 
********************************* 
8 Febrero:

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

