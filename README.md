# SIGULAB
### Branch de Arnaldo
******************
## TODOs:

+ Quitar boton de back en `view_compras`
+ Permitir cambiar cantidades de donacion a uso interno a los jefes de seccion.
+ Jquery, bloquear descripcion al hacer una compra

******************
## 22 Febrero:

+ Agregadas sustancias pertenecientes a cada factura.

+ Creada vista para seleccionar si es una factura existente, o si se desea crear una nueva.

+ Al gestor, al ver la bitacora, se ve la fecha y hora en la cual fue hecha la transaccion.

## 19 Febrero:

+ Agregar unidades de medidas las sustancias y vistas.

+ Eliminadas tablas `t_consumos` y `t_ingresos`, no utilizadas.

+ Botón de edit para el WebMaster ahora redirecciona directamente a la interfaz de manejo de bases de datos de Web2Py.

+ Arreglada vista de peligrosidades en la tabla, solo se muestra la primera, y al hacer click en view se muestra todo.

+ Arreglado populate para sustancias.

+ Editada entrada en `languages/es.py`, entrada no traducida.

+ Eliminada redundancia (de `sustancia`) en desglose de inventario por espacio fisico.

+ Arreglados plurales y singulares de tablas.

+ Validación de formato (`.pdf`) al archivo de reporte.

+ Agregado `(*)` al crear entradas en las forms, usando: `modules/plugin_notemptymarker.py`, con la funcion `mark_not_empty(<tableObject>)`.
*<< Unicamente arreglado en tablas del inventario >>*

+ Validación de fecha maxima posible como fecha actual.

+ Redirección a ingresar una factura, cuando el ingreso de bitacora es hecho por `"Compra"`.

+ Agregado boton de facturas en el menu, vista `view_compras.html`.
*<< Discutir con el cliente, porque el modulo de facturacion no nos atañe >>*
