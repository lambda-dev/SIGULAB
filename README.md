# SIGULAB
Branch de Adolfo
******************

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

