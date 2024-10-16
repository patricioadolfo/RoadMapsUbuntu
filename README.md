<h1>PostgreSQL</h1>

<h3>Instalacion</h3>

<code>sudo apt-get install postgresql postgresql-contrib</code>

<h1>Apache</h1>

<h3>Instalacion de apache</h3>

<code>sudo apt-get install apache2
 sudo apt-get install libapache2-mod-wsgi-py3</code>
 
Utilizar usuario con permisos root, sino crearlo y darle permisos sudoers 

<code>adduser webuser
 gpasswd -a webuser sudo
 su - webuser
 cd ~
 mkdir www</code>

<h3>Comandos apache</h3>

```
sudo systemctl start apache2.service

sudo systemctl stop apache2.service

sudo systemctl restart apache2.service

sudo systemctl status apache2.service

sudo apache2ctl configtest
```

Logs de ERROR: sudo nano /var/log/apache2/error.log

Config Proyecto: sudo nano /etc/apache2/sites-available/*proyecto*.conf

<h3>Firewall</h3>

Chequear firewall, comprobar su estado, dar permisos a apache de no tenerlos  <code>sudo ufw COMAND</code>
```
Commands:

     enable                          enables the firewall

     disable                         disables the firewall

     default ARG                     set default policy

     logging LEVEL                   set logging to LEVEL

     allow ARGS                      add allow rule

     deny ARGS                       add deny rule

     reject ARGS                     add reject rule

     limit ARGS                      add limit rule

     delete RULE|NUM                 delete RULE

     insert NUM RULE                 insert RULE at NUM

     prepend RULE                    prepend RULE

     route RULE                      add route RULE

     route delete RULE|NUM           delete route RULE

     route insert NUM RULE           insert route RULE at NUM

     reload                          reload firewall

     reset                           reset firewall

     status                          show firewall status

     status numbered                 show firewall status as numbered list of RULES

     status verbose                  show verbose firewall status

     show ARG                        show firewall report

     version                         display version information

Application profile commands:

     app list                        list application profiles

     app info PROFILE                show information on PROFILE

     app update PROFILE              update PROFILE

     app default ARG                 set default application policy
```

<h1>Proyecto</h1>

<h2>1.Instalación</h2>

<code>sudo apt-get install python-pip
 sudo pip install virtualenv</code>

<h2>2.Repositorio Git</h2>

Descargar repo de github y crear un entorno vitual dentro de las carpeta principal del proyecto, una vez en el entorno virtual instalar dependencias para el proyecto

<code>cd ~/www
 git clone *url_del_repo*
 cd *folder_repo* 
 virtualenv -p python3 venv
 source venv/bin/activate</code>

Dentro del entorno virtual instalar dependencias para Django y Sphinx

<code>pip install django
 pip install djangorestframework
 pip install markdown       
 pip install django-filter  
 pip install django-qr-code
 pip install psycopg
 pip install django-dbbackup
 pip install sphinx-rtd-theme
 pip install django-docs
 pip install sphinx</code>

<h2>3.Configuracion de Base de Datos</h2>

Desde postgrest se crea la base de datos y se le da permisos al usuario postgrest con contraseña redefinida <code>sudo -u postgres psql</code>

```python
postgres=# CREATE DATABASE road;
postgres=# \connect road;
postgres=# ALTER USER postgres with encrypted password 'route53902';
postgres=# GRANT ALL PRIVILEGES ON road TO postgrest
postgres=# \q
```

Una vez creada la base de datos PostgreSQL se crea un archivo.json para almacenar los datos de conexión entre DJango y PostgreSQL de modo de no detallarlos en settings.py y proteger la base de datos <code>sudo touch /etc/env-production.json  sudo nano /etc/env-production.json</code>

```python
####################################################################

  GNU nano 6.2                             /etc/env-production.json                                       
{
        "ENGINE": "django.db.backends.postgresql",
        "NAME": "road",
        "USER": "postgres",
        "PASSWORD": "route53902",
        "HOST": "localhost",
        "PORT": ""
}

####################################################################
```

Se configura settings.py para que leer los datos almacenados en env-production.json <code>sudo nano *ruta_settings.py*/settings.py</code>

```python

####################################################################
  GNU nano 6.2                                    settings.py *                                           

import json

with open('/etc/env-production.json') as env_file:
        ENVIRONMENT = json.load(env_file)

ALLOWED_HOSTS = ['192.168.0.14']

DATABASES = {
    'default':
        {
        'ENGINE': ENVIRONMENT.get('ENGINE'),
        'NAME': ENVIRONMENT.get('NAME'),
        'USER': ENVIRONMENT.get('USER'),
        'PASSWORD': ENVIRONMENT.get('PASSWORD'),
        'HOST': ENVIRONMENT.get('HOST'),
        'PORT': ENVIRONMENT.get('PORT'),
    }
}

STATIC_ROOT = os.path.join(BASE_DIR, 'static_root')
#####################################################################
```

<h2>4.Configuracion de Apache</h2>

<code>sudo rm /etc/apache2/sites-available/000-default.conf
 sudo nano /etc/apache2/sites-available/*nombre_web*.conf</code>

```python
  GNU nano 6.2                    /etc/apache2/sites-available/RoadMaps.conf *                            

<VirtualHost *:80>      
        ServerAdmin patricio
        ServerName 192.168.0.14
        ServerAlias django

        DocumentRoot /home/patricio/www/RoadMaps
        
        ErrorLog ${APACHE_LOG_DIR}/error.log
        CustomLog ${APACHE_LOG_DIR}/access.log combined

        <Directory "/home/patricio/www/RoadMaps">
           Options Indexes FollowSymLinks
           AllowOverride All
           Require all granted
           Allow from All
        </Directory>

        Alias /static /home/patricio/www/RoadMaps/route/static
        <Directory /home/patricio/www/RoadMaps/route/static>
                Require all granted
                Allow from All
        </Directory>

        <Directory /home/patricio/www/RoadMaps/RouteMaps>
                <Files wsgi.py>
                        Require all granted
                        Allow from All
                </Files>
        </Directory>

        WSGIDaemonProcess RoadMaps python-path=/home/patricio/www/RoadMaps/ python-home=/home/patricio/ww>
        WSGIProcessGroup RoadMaps
        WSGIScriptAlias / /home/patricio/www/RoadMaps/RouteMaps/wsgi.py

</VirtualHost>
```

Añadir proyecto a apache <code>sudo a2ensite *nombre_web*.conf</code>y se reinicia el servidor <code>sudo service apache2 reload</code>.Se agrega el usuario creado <code>sudo adduser *usuario* www-data</code>, se les da los permisos al usuario <code>sudo chown -R webuser:www-data /home/*usuario*/www</code> y a la carpeta del proyecto <code>sudo chmod 777 /home/*usuario*/www</code>


<h2>5.Email</h2>

<h3>Configura GMail</h3>

Cómo crear y usar contraseñas de aplicaciones

Importante: Para crear una contraseña de la aplicación, necesitas tener activada la Verificación en 2 pasos en tu Cuenta de Google.

Si usas la Verificación en 2 pasos y recibes un error de "contraseña incorrecta" cuando accedes, intenta usar una contraseña de la aplicación.

Crea y administra las contraseñas de aplicaciones. Es posible que debas acceder a tu Cuenta de Google. https://myaccount.google.com/apppasswords

<h3>Configura Django</h3>

Configura la zona horari en settings.py

```python

TIME_ZONE = 'America/Buenos_Aires'

```

En settings.py añade 'django.contrib.sites', Dentro de admin ingresar a sites y agregar el dominio a cual pertenece el proyecto,  

```python

INSTALLED_APPS = [
    'django.contrib.sites',
    ]

SITE_ID = 2 # id dominio

EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'

EMAIL_HOST = 'smtp.gmail.com'
EMAIL_HOST_USER = 'email@gmail.com'
EMAIL_HOST_PASSWORD = 'phypqmgffzjzuhgz'
EMAIL_PORT = '587'
EMAIL_USE_TLS = True
DEFAULT_FROM_EMAIL = 'Notificación <email@gmail.com>'
```

<h2>6.Backup</h2>

Configuración para Backup de base de datos

```python
mkdir /my/backup/dir/

INSTALLED_APPS = (
    ...
    'dbbackup',  # django-dbbackup
)

DBBACKUP_STORAGE = 'django.core.files.storage.FileSystemStorage'
DBBACKUP_STORAGE_OPTIONS = {'location': '/my/backup/dir/'}

```
Para generar backup <code>python manage.py dbbackup</code>

Restaurar copia de backup <code>python manage.py dbrestore</code>

python manage.py collectstatic

<h2>7.Mantenimiento de Base de Datos</h2>

Conetar a la base de datos portgresql y ejecutar comando VACUUM

<code>sudo -u postgres psql</code>

```python
psql (14.13 (Ubuntu 14.13-0ubuntu0.22.04.1))
Type "help" for help.

postgres=# \connect road
You are now connected to database "road" as user "postgres".
road=# VACUUM ANALYZE;
VACUUM
road=# 

```

<h2>8. Estados Creados en Base de Datos</h2>

        ID      State   Descriptions
	8	8	ENTREGADO
	7	7	IGNORADO
	6	6	EN LINEA
	5	5	FUERA DE LINEA
	4	4	CREADO
	3	3	RECIBIDO
	2	2	EN CAMINO
	1	1	PREPARADO

Crear un nodo de origen con el nombre Destino para vincular con los destinos creados en la tabla Destinos