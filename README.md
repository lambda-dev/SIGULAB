# SIGULAB
Branch de Adolfo
*************************************
9 Marzo:
+ [NEW] Al REGISTRARSE un usuario AUTORIZADO (JEFELAB O JEFESEC) automaticamente se es añadido a la Jefatura que especifico y puede acceder al inventario

+ [NEW] Al CONFIRMAR un usuario PENDIENTE (JEFELAB O JEFESEC) automaticamente se es añadido a la Jefatura que especifico y puede acceder al inventario

+ [TODO] Aplicar mismo mecanismo a TECNICOS.


+ [FIXED] En la opción “editar” un usuario registrado, si se modifica el privilegio y se envía, no se modifica el privilegio en el vínculo de membresías del usuario.  En el ejemplo anterior, se modificó el privilegio del usuario “Gestión Sustancias y Desechos Peligrosos” y al presionar el vínculo “membresías” asociadas a este usuario no realizó el cambio y aparece “Usuario Normal”

+ [FIXED] Solo puede haber 1 único Director y tendrá ese privilegio usando el correo ulab@usb.ve. Se debe restringir la posibilidad de agregar más Directores 

+ [FIXED] Se debe restringir la posibilidad de agregar más Jefes de Laboratorios de los siete (7) que existen. 

+ [FIXED] Solo puede haber 1 único Jefe de Laboratorio (para cada Laboratorio) y NO hay jefes que ocupen más de una Jefatura de Laboratorio.

+ [FIXED] Director solo puede hacer operaciones de consulta

+ [FIXED] administrador de usuarios le debería aparecer ese nuevo registro en “Pendientes de Confirmación” y NO aparecer en la tabla de “usuarios registrados” hasta tanto no haya sido confirmado.

*********************************
7 Marzo:
+ [FIXED] Gestor Users solo puede entrar a modulo de gestión

+ [FIXED] Breadcrums en paginas de gestion + acomodos visuales

+ Pendiente:
  + [TODO] Director solo puede hacer operaciones de consulta
  + [TODO] administrador de usuarios le debería aparecer ese nuevo registro en “Pendientes de Confirmación” y NO aparecer en la tabla de “usuarios registrados” hasta tanto no haya sido confirmado.
  + [TODO] Solo puede haber 1 único Director y tendrá ese privilegio usando el correo ulab@usb.ve. Se debe restringir la posibilidad de agregar más Directores 
  + [TODO] Solo puede haber 1 único Jefe de Laboratorio (para cada Laboratorio) y NO hay jefes que ocupen más de una Jefatura de Laboratorio.  Se debe restringir la posibilidad de agregar más Jefes de Laboratorios de los siete (7) que existen. 


******************
3 Marzo:

[FIXED] En la membresía “Técnicos” no aparecen registros. 

[FIXED] ¿Se puede eliminar del campo “Jefe de Sección” el correo? O ¿Tiene alguna función el correo incluido en ese campo?. Preferiblemente, dejar solo el nombre. Si es para mostrar la información, debería estar en un campo separado. 

[FIXED] Página 5 y Pág 6 presentan error, aunque la información está completa para las Secciones

[FIXED] En el menú debe aparecer “Usuarios autorizados”, para que sea congruente con el título en la página (NO: Lista de autorizados)

[FIXED] Se agrega a la tabla de “usuarios registrados” y se debería eliminar de la lista de “usuarios autorizados” para no embasurar el sistema de información duplicada. 

[FIXED] Solicitar la Dependencia cuando se hace el registro es importante, porque aun habiéndose registrado con el privilegio correcto (por ejemplo Jefe de Laboratorio) no puede consultar nada pues no se sabe a cuál Laboratorio o Sección está asociado. 

[FIXED] Se debe establecer seguridad para confirmar la identidad de quien realiza el registro, a través del envío de un correo personalizado al propietario de la cuenta de correo, por ejemplo.

[FIXED] El formulario debería contener los campos “Laboratorio” y “Sección”, porque si el usuario no está autorizado, el administrador debe saber dónde buscar información para confirmar su vínculo con la ULAB.

[FIXED] Sustituir el nombre del campo “Cargo” por “Rol” (para un mismo rol, pueden haber muchos cargos. Por ejemplo, un Ingeniero Jefe no va a querer colocar que su cargo es técnico, pero puede entender que es el rol que desempeña dentro de la Sección).  

*********************************************

21 Febrero
+ Servicio de email activo con la cuenta ulab-smdp@usb.ve
  + Email para verificar registro
  + Email se envia cuando se añade user en lista de pendientes a los AdminUser

20 Febrero:

+ Añadidos (*) a todos los formularios de gestion de usuarios/espacios

TODO:
+ Aclarar con el cliente: 
  + Boton de eliminar que no les gusto y nunca encontramos en la presentacion
  + Eliminar cargo desde usuario

+ Habilitar emails para confirmar registro **IMPORTANTE**
  + Activar servidor smtp en private/appconfig.ini
  + Pedir un email de ulab para esto?
+ Emails para avisar que alguien se registró


14 Febrero:

+ Arreglado error en el registro [Se mantenía Usuario Normal+Otro cargo en usuario autorizados]

+ Añadido gestion de espacios fisicos, donde se listan
+ Como espacios fisicos-Tecnicos es N:N hice una tabla para guardar estas relaciones, en gestion de espacios se añaden los tecnicos.

*ES POSIBLE QUE ESO TE ROMPA ALGO, DEJÉ EL CAMPO F_TECNICO EN T_ESPACIOFISICO PARA EVITAR ERRORES PERO NO SE DEBE USAR*

TODO: Agregar espacios fisicos via populate.py
+ En teoria ya funciona TODO! :)


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