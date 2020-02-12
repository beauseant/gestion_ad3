Gestión Active Directory desde Python
==========

Programa en python para gestionar los usuarios de un servidor Active Directory basado en un Windows Server 2k. Se utiliza la libreria python-ldap como base para poder realizar todas las operaciones.
--------------

Programa que muestra como acceder a un servidor Active Directory basado en Windows desde python. 

**Condiciones iniciales:**

- Tener instaladas las librerias de python: python-ldap y datetime en el sistema.
- Un fichero de configuración .ini con los datos de acceso al sistema (usuario del ldap, cn...) se muestra el fichero *configuracionejemplo.ini* como ejemplo a seguir.

**Objetivos**

- Crear una libreria que permita sacar un listado de todos los usuarios que se encuentran en el sistema. Es decir, la rama Users del active directory.
- Sacar un listado de todos los usuarios que tengan las cuentas caducadas desde X días.
- Obtener un listado de todos los usuarios que haga Y días que no entren al sistema.
- Enviar un correo a los usuarios que tengan las cuentas caducadas avisando que la cuenta caducará en breve.
- Fijar una fecha de caducidad a los usuarios que lleven Y días sin entrar al sistema.

Con esta librería, por lo tanto, es posible administrar a los usuarios de un entorno Windows desde una consola python. Se puede crear un programa que se ejecute en el cron del sistema cada 30 días y que haga un barrido de las cuentas a punto de caducar y avise a los usuarios. De esta forma, evitamos que los usuarios se encuentren las cuentas caducadas. También podemos gestionar las cuentas inactivas durante mucho tiempo para poder borrarlas o fijarles una fecha de caducidad.
