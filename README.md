# Tryton: instalación y manejo

Instructivo y scripts para la instalación de Tryton ERP. Versión Tryton: 5.0

Palabras clave: Tryton, ERP, software de gestión, software de negocios.

Keywords: Tryton, ERP, business software.



[Tryton](https://www.tryton.org/) es una plataforma informática para el desarrollo de software de gestión comercial (ERP, Enterprise Resource Planning, planificación de recursos empresariales). Es un software de alto nivel, de propósito general, escrito en [Python](https://www.python.org/), desarrollado en un modelo de tres capas: el servidor Tryton, el cliente Tryton, y el sistema de manejo de base de datos ([PostgreSQL](https://www.postgresql.org/) o [SQLite](https://sqlite.org/index.html), de preferencia [PostgreSQL](https://www.postgresql.org/)). Tryton cuenta con una gran cantidad de módulos para tareas específicas, que pueden combinarse para implementar soluciones adecuadas a requerimientos diferentes. Los siguientes instructivos y scripts facilitan la instalación del servidor y el cliente Tryton en Linux. El servidor Tryton puede accederse también desde un cliente Tryton en MS Windows, disponible en la pàgina [Get Tryton](https://www.tryton.org/download), sección Desktop Client. 

## Instalación

Existen diferentes [formas de instalar Tryton](https://www.tryton.org/download):
- instalación con los paquetes de la distribución Linux. Tryton está disponible en la mayoría de las distribuciones Linux, aunque no siempre está disponible la última versión. 
- instalación con paquetes desde el sitio de Tryton. Permite instalar la última versión; hay disponibles paquetes ejecutables de cliente Tryton para MS Windows y Mac, pero para Linux el cliente Tryton debe instalarse desde código fuente.
- instalación desde código fuente. Para desarrolladores.

En este instructivo trataremos solo la instalación desde la distribución Linux. Usando un programa de gestión de paquetes como `Synaptic`, o desde la línea de comandos: 

    $ sudo apt install tryton-server tryton-server-doc

para instalar el servidor y los módulos de Tryton.

    $ sudo apt install tryton-client tryton-client-doc

para instalar el cliente.

La instalación de la distribución deja el servidor Tryton como un servicio a nivel de sistema: arranca el servidor al iniciar el equipo y lee la configuración de un archivo del sistema, `/etc/tryton/trytond.conf`. 

Si bien esta configuración a nivel de sistema puede ser conveniente en producción, para la experimentación y desarrollo de una aplicación específica usando los módulos de Tryton puede ser más conveniente una instalación a nivel de usuario no privilegiado. Esto permite mentener la configuración como un archivo de ese usuario, y manejarar el servidor a voluntad. 

## Configuración de sistema

La instalación desde la distribución arranca el servidor automáticamente al iniciar el equipo, y lee la configuración del servidor desde el archivo `/etc/tryton/trytond.conf`. El archivo de configuración es de solo lectura, por lo que requiere primero asignar permisos de escritura, modificar el archivo, y finalmente quitar los permisos de escritura:

    chmod ug+w /etc/tryton/trytond.conf
    sudo vi /etc/tryton/trytond.conf    # u otro editor 
    chmod a-x /etc/tryton/trytond.conf 

Para determinar el nombre del servicio asociado al servidor Tryton:
    
    $ systemctl list-units | grep tryton   # selecciona cadena "tryton"
    tryton-server.service
      loaded active running   Tryton Server WSGI App

El nombre del servicio es `tryton-server.service`. Para manejar el servicio,

    $ sudo systemctl start tryton-server.service    # arranca trytond
    $ sudo systemctl stop tryton-server.service     # detiene trytond
    $ sudo systemctl restart tryton-server.service  # re arranca trytond

Los archivos de configuración son:

    /etc/tryton/trytond.conf               # configuración
    /etc/tryton/trytond_log.conf           # configuración de log

La modificación del archivo de configuración `trytond.conf` requerida pra usar bases de datos PostgreSQL son las siguientes:
1. Cambiar parmisos para poder alterar el archivo:
    ```
    cd /etc/tryton
    sudo chmod ug+w trytond.conf
    sudo vi trytond.conf                    # o el editor preferido
    ```
2. Descomentar las líneas indicadas, para habilitar el uso de bases de datos PostgreSQL y la solicitud de acceso por clientes Tryton desde otras máquinas:
    ```
    [web]
    listen = 0.0.0.0:8000
    root = /usr/share/tryton-sao/www

    [database]
    uri = postgresql://tryton:tryton@localhost:5432/
    path = /var/lib/tryton
    list = True
    language = es
    ```
3. Reponer los permisos para impedir modificaciones.
    ```
    sudo chmod a-w trytond.conf
    ```

La configuración a nivel de sistema es recomendable para servidores Tryton en producción, cuando el desarrollo ha terminado. Con esta configuración, podrán acceder al equipo servidor clientes Tryton instalados en las otras  máquinas de la empresa.


## Configuración por usuario

Esta sección describe la configuración de Tryton para ser manejado por un usuario no privilegiado, aunque para algunas tareas se requieren permisos de supervisor.

### Deshabilitar arranque automático del servidor Tryton

La instalación de la distribución inicia el servidor Tryton automáticamente como parte del proceso de arranque de la máquina, reconocido como un proceso de nombre `trytond` (demonio de Tryton). Para permitir la configuración y el manejo por un usuario no privilegiado, es preciso deshabilitar el arranque automático del servidor Tryton al inicio.

1. Verificar arranque automático de `trytond`:
    ```
    $ ps -C trytond
    ```
Indica si `trytond` está corriendo; si en TTY indica "?" significa que `trytond` fue iniciado por el sistema.

2. Para deshabilitar el arranque al inicio:
    ```
    $ sudo systemctl disable tryton-server.service
    ```

3. Reiniciar el equipo.

4. Verificar que `trytond` no arrancó automáticamente:
    ```
    $ ps -C trytond
        PID TTY          TIME CMD

    ```
    No debe mostrar ningún proceso.

5. Para reponer el arranque automático al inicio:
    ```
    $ sudo systemctl enable tryton-server.service
    ```

### Tareas preliminares

El archivo `tryton.conf.model` provee una configuración básica de Tryton para el servidor y el cliente. Para habilitarla:

    $ cd <directorio de instalación de estos instructivos>
    $ mkdir ~/.config/tryton/5.0
    $ cp tryton.conf.model ~/.config/tryton/5.0/tryton.conf

El archivo de configuración debe contener al menos estas líneas:

    [database]
    uri = postgresql://tryton:tryton@localhost:5432/
    path = ~/tryton-db
    
    [web]
    listen = 0.0.0.0:8000

El script `db_psql.sh` provisto en este sitio permite realizar las tareas necesarias para la creación de usuario y bases de datos en PostgreSQL. 

El usuario `tryton`, contraseña `tryton`, será el dueño de todas las bases de datos PostgreSQL que use Tryton. Esto puede verse en la línea `uri` del archivo de configuración. Para crear este usuario:

    bash db_psql.sh createtryton
Esto se realiza por única vez, y el usuario `tryton` debe mantenerse mientras se usen bases de datos PostreSQL en Tryton.


El directorio de almacenamiento para las bases de datos será `~/tryton-db`, como puede verse en la línea `path` del archivo de configuración. Crear este directorio. 

    $ mkdir ~/tryton-db

### Script de gestión

El script `tryton-manager.py` permite realizar diversas tareas.

    $ python3 tryton-manager.py
    Tryton, scripts de gestión.
    -- Bases de datos
       1 : Crear y registrar base de datos.
       2 : Borrar base de datos.
       3 : Mostrar bases de datos.
    -- Cliente Tryton
       4 : Iniciar el cliente Tryton.
       5 : Detener el cliente Tryton.
    -- Servidor Tryton
       6 : Iniciar el servidor Tryton.
       7 : Detener el servidor Tryton.
       q : Salir
    Elija una opción: 

Usaremos este script para la creación de bases de datos y el manejo de cliente y servidor Tryton.

### Crear una base de datos

Esta sección describe la creación de una base de datos y su registro en Tryton usando el script `tryton-manager.py`.

1. Crear y registrar una base de datos de prueba, con la opción correspondiente del script. Nombre de la base de datos: DBprueba.  El registro de la base de datos en Tryton muestra los módulos instalados, puede demorar; finalmente, pide e-mail y contraseña de administrador.
    ```
    BDprueba     | tryton   | UTF8     | es_UY.UTF-8 | es_UY.UTF-8 |
    ...
    "admin" email for "BDprueba": <dirección de e-mail>
    "admin" password for "BDprueba": admprueba
    "admin" password confirmation: admprueba
    ```
    Al acceder a la base de datos desde el cliente Tryton, en la máquina local `localhost`, deberemos indicar el usuario `admin` con la contraseña `admprueba`.

2. Arrancar el servidor, con la opción correspondiente del script.

3. Arrancar el cliente, con la opción correspondiente del script. Abre la ventana del cliente Tryton.

    ![Cliente Tryton, inicio](./images/tryton-client-1.jpg)

4. Administrar la base de datos. En la ventana Usuario de Tryton, crear un perfil para acceder a la base de datos BDprueba:
    - botón Gestionar, abre Editor de perfiles
    ![Cliente Tryton, perfil](./images/tryton-client-2.jpg)
    - botón **\[\+\]** para agregar un perfil: 
        - Perfil: local_bdprueba
        - Servidor: localhost
        - Base de Datos: BDprueba
        - Nombre de usuario: admin
    - cerrar la ventana de gestión de perfiles.

    ![Cliente Tryton, perfil](./images/tryton-client-3.jpg)

    Conectar al servidor, botón `Conectar`. Cuando pide contraseña: `admprueba`. Queda en la ventana `Tryton - Administrator`.


    ![Tryton Client, ventana administrador](./images/tryton-client-admin.jpg)


## Cliente Tryton

### Acceso local

Con las opciones correspondientes del script, es posible arrancar y detener el cliente, como se indicó en la sección anterior. 

### Acceso remoto

Para acceder al servidor Tryton desde otra máquina:

1. Arrancar el cliente Tryton en la máquina remota:
    ```
    $ tryton-client &
   ```
2. Acceder al servidor. En la ventana Usuario de Tryton, crear un perfil para acceder a la base de datos BDprueba:
    - botón Gestionar, abre Editor de perfiles
    - botón **\[\+\]** para agregar un perfil: 
        - Perfil: remoto_bdprueba
        - Servidor: \<nombre del servidor\>:8000
        - Base de Datos: BDprueba
        - Nombre de usuario: admin
    - cerrar la ventana de gestión de perfiles.

    El \<nombre del servidor\> debe ser el nombre o el número IP de una máquina accesible en la red. Cuando pide contraseña: `admprueba`. Queda en la ventana `Tryton - Administrator`.



