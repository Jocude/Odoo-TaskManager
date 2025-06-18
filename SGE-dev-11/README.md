# Introducción

Proyecto final SGE con Odoo, Docker, Docker Compose, Git y GitHub.

- [Introducción](#introducción)
- [Preparación del repo y del entorno](#preparación-del-repo-y-del-entorno)
  - [_Fork_ del repositorio original](#fork-del-repositorio-original)
  - [Creación de rama de desarrollo y clonación del repositorio en local](#creación-de-rama-de-desarrollo-y-clonación-del-repositorio-en-local)
  - [Instalación de extensiones útiles](#instalación-de-extensiones-útiles)
  - [Inicialización de Odoo y creación de la primera base de datos](#inicialización-de-odoo-y-creación-de-la-primera-base-de-datos)
  - [Primer _commit_](#primer-commit)
  - [Comando _odoo scaffold_](#comando-odoo-scaffold)
- [Próximos pasos...](#próximos-pasos)

# Preparación del repo y del entorno

## _Fork_ del repositorio original

Inicia sesión en tu cuenta de GitHub, haz un _fork_ de [javnitram/SGE-odoo-it-yourself](https://github.com/javnitram/SGE-odoo-it-yourself) y llama al tuyo SGE-odoo-dev**Z**-**XX**, donde **Z** es la **letra de tu grupo (A, B, V)** y **XX** es el valor correspondiente a tu número de puesto, según **los dígitos del hostname de clase**.

![Fork](https://github.com/user-attachments/assets/a384ed5f-e5aa-4ba2-90ae-f78e09338793)

## Creación de rama de desarrollo y clonación del repositorio en local

En tu repositorio, además de tener una rama _main_ o _master_, crea una rama con nombre **develop**. Esta será tu rama de desarrollo.

![Branch](https://github.com/user-attachments/assets/6ff047cd-3375-4685-a536-d6e0e557cab1)

Vas a usar esa rama para desarrollar tu propio módulo de Odoo. Para ello, deberás clonar la rama en local con Visual Studio Code.

Primero, si no lo has hecho anteriormente, deberás autorizar el acceso a GitHub desde Visual Studio Code.

![Autorizar GitHub en Visual Studio Code](https://user-images.githubusercontent.com/1954675/214658283-2563168c-9a89-4950-b5d8-3b492c748d0a.gif)

A continuación, clona el repositorio (es posible que GitHub te pida autorizar permisos adicionales)

![Git Clone](https://user-images.githubusercontent.com/1954675/214662378-484a9aaa-1be2-4ded-ac78-b3b997bc2fb7.gif)

Asegúrate de estar apuntando a la rama de desarrollo: **develop**

![Checkout](https://user-images.githubusercontent.com/1954675/214665198-03e8f2b6-670c-4384-9ced-557ea86e6632.gif)

Considera guardar tu workspace (área de trabajo) de Visual Studio Code.

## Instalación de extensiones útiles

A diferencia de anteriores proyectos basados en el repo [javnitram/SGE-odoo-dockerized](https://github.com/javnitram/SGE-odoo-dockerized), en esta última entrega, vamos a prescindir de pgAdmin 4 y del script que usábamos para gestionar Docker Compose. En su lugar, hay que usar las extensiones oportunas de Visual Studio Code. Busca por estos identificadores, de modo que por cada uno encontrarás exactamente una extensión para instalar:

- ```jigar-patel.OdooSnippets```
- ```ms-python.python```
- ```ms-azuretools.vscode-Docker```
- ```ckolkman.vscode-postgres```

Tras instalar estas extensiones, obtendrás nuevas funciones en Visual Studio Code, a las cuales puedes acceder rápidamente desde la paleta de comandos con el atajo ```Control + Shift + P```. Asimismo, también podrás observar dos nuevos iconos en la barra de actividad (a la izquierda), uno correspondiente a la extensión de Docker y otro a la de PostgreSQL, nos familiarizaremos con ellas durante las demostraciones en clase.

![Iconos barra lateral](https://user-images.githubusercontent.com/1954675/214654250-62f53d6f-4200-4bf4-89fb-b20d320a1f95.gif)

## Inicialización de Odoo y creación de la primera base de datos

![Inicialización de Odoo](https://user-images.githubusercontent.com/1954675/214669540-193c94c0-81d8-451e-9cac-f8a8c3a03afd.gif)

Lanza los contenedores usando la extensión de Docker en Visual Studio. Desde la propia extensión puedes lanzar también tu navegador por defecto para conectar al servicio Odoo en su puerto expuesto.

Crea tu base de datos de Odoo con la configuración que consideres oportuna.

![Primera base de datos Odoo](https://user-images.githubusercontent.com/1954675/214677032-1a1958ef-8f9e-4942-9cdf-8a09673c50b5.png)

Como recuerdas de anteriores prácticas, es razonable que en ocasiones tengas problemas para acceder desde la máquina anfitriona a ficheros creados desde un contenedor (o viceversa). Cuando haya importantes cambios en el contenido de los volúmenes compartidos entre host y contenedores, ejecuta ```./set_permissions.sh```.

Dicho script te orientará para que arranques los contenedores y vuelvas a invocarlo si es el único modo de recuperar el acceso completo. Esto es necesario en aquellos equipos Linux en los que no podemos ser root ni ejecutar sudo.

## Primer _commit_

Al iniciar Odoo por primera vez y configurar nuestra primera base de datos, hemos asignado una _master password_. Como recuerdas, esta contraseña queda cifrada en el fichero de configuración ```odoo.conf```, que también se ha actualizado para eliminar comentarios. Todo esto hace que Git detecte que el fichero ha sido modificado respecto a su contenido previo. Puedes observar cómo el fichero queda en estado **M** (_Modified_, modificado) y comparar las diferencias producidas en la modificación.

![Odoo conf modificado y diff](https://user-images.githubusercontent.com/1954675/214678982-2358dff2-57ab-47ed-a57d-6371750c886d.png)

En Git, los estados de un archivo son:

- **U (Untracked)**: El archivo no está siendo rastreado por Git (nuevo y aún no agregado al repositorio).
- **A (Added)**: El archivo ha sido agregado al área de preparación (staging area) con `git add` pero aún no confirmado (committed).
- **M (Modified)**: El archivo ha sido modificado desde el último commit, pero no se ha agregado al área de preparación o está modificado en staging.
- **D (Deleted)**: El archivo ha sido eliminado y Git ha detectado este cambio.

Estos estados reflejan las diferencias entre el repositorio, el área de preparación y el sistema de archivos local.

Este repositorio está configurado para sincronizar únicamente código y configuración, por lo que ningún _commit_ hará un _backup_ del estado de tu servidor Odoo ni del servidor de base de datos. Recuerda que un sistema de control de versiones no está para esas cosas y, por eso, se han configurado reglas específicas en ficheros _.gitignore_ en algunos directorios.

```text
.vscode
# Python byte-compiled / optimized / DLL files
__pycache__/
*.py[cod]
*$py.class

# Backups and sql dump files
*.sql
*.tgz
*.tar.gz
*.zip
```

Haz tu primer _commit_ (esto es confirmar los cambios en el repositorio local de Git) y _push_ (sincronizar cambios locales hacia el repositorio remoto, en este caso GitHub).

Es posible que la primera vez debas configurar tu nombre de usuario y dirección de correo electrónico. Esto es importante porque cada Git commit utiliza esta información para firjarla de forma inmutable en los commits que empiezas a crear:

```
git config --global user.name "John Doe"
git config --global user.email johndoe.example.com
```

Podemos hacer esta configuración sólo una vez si pasamos la opción --global, para que Git siempre use esa información para cualquier cosa que haga en ese sistema. Si deseas anular esto con un nombre o dirección de correo electrónico diferente para proyectos específicos, puedes ejecutar el comando sin la opción ```--global``` cuando estés en ese proyecto.

Muchas de las herramientas GUI te ayudarán a hacer esto cuando las ejecutes por primera vez.

## Comando _odoo scaffold_

Usando la extensión de Docker de Visual Studio Code, localiza la función que te permita abrir una shell en el contenedor de Odoo.

Dentro del contenedor, ejecuta:

```bash
odoo scaffold prueba /mnt/extra-addons
```

![odoo scaffold](https://user-images.githubusercontent.com/1954675/214684898-0bcdea9c-887e-4224-aba1-7e842a223883.gif)

Observa el contenido de ese directorio desde el propio contenedor y desde el volumen mapeado en el anfitrión. Este comando ha generado una estructura mínima de directorios y ficheros para agilizar el desarrollo de un módulo en Odoo. Explora el contenido del directorio _prueba_ desde Visual Studio Code, si tienes algún problema para modificar los ficheros, recuerda ejecutar ```./set_permissions.sh```.

# Próximos pasos...

Crea tu propio módulo de Odoo de acuerdo a los apuntes de clase y al enunciado de la práctica que se te ha proporcionado en el aula virtual.

Debes utilizar Git y GitHub. Para ello, se espera que hagas varios _commits_ y _pushes_ en tu rama de desarrollo y finalmente hagas un _merge_ a tu rama _main_ cuando hayas desarrollado y probado tu módulo.

Si finalizas tu desarrollo con éxito y aprovechas la potencia de Git y GitHub, podrás realizar un _pull request_, es decir, una petición al propietario del repositorio original para que valore tu propuesta e integre tus cambios (_merge_). Es especialmente conveniente que tu proyecto proporcione datos de demo o hagas un _export_ de la base de datos con ```pg_dump``` o alguna utilidad gráfica.

Quien clone el repositorio original y despliegue el entorno podrá probar tu módulo y todos los otros que hayan quedado integrados.
