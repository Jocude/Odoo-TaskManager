#!/bin/bash
###############################################################################
# @author https://github.com/javnitram/
# GNU GENERAL PUBLIC LICENSE Version 3
# Attribution-ShareAlike 4.0 International (CC BY-SA 4.0)
###############################################################################

set -a # Marca variables y funciones para exportar

# VARIABLES GLOBALES
# Los nombres en SERVICES deben coincidir con los nombres de directorios en la
# ruta actual y con los servicios definidos en el fichero docker-compose.yml
# declare -a SERVICES=( odoo pgadmin4 ) No se está exportando correctamente como array
SERVICES="odoo pgadmin4" # Usar sin comillas dobles, queremos que cada valor se use independiente
RED_TEXT='\033[0;31m'
GREEN_TEXT='\033[0;32m'
RESET_TEXT='\033[0m' # No Color

function set_permissions_for_containers() {
    # Aplicamos permisos de acceso completo a los directorios de los contenedores
    # que se usan como punto de montaje. Así nos aseguramos de que los contenedores 
    # puedan escribir y de que el usuario del anfitrión pueda acceder.
    for i in $SERVICES; do
        docker ps --quiet --filter "name=^$i" | while read -r container_id; do
            grep --fixed-strings "./$i" docker-compose.yml | cut -d: -f2 | while read -r mount; do
                    # depurar con --tty
                    echo "Estableciendo permisos en el contenedor con id $container_id basado en la imagen $i, punto de montaje $mount"
                    docker exec --privileged --user root "$container_id" sh -c "/usr/bin/find $mount -type d -exec /bin/chmod 777 {} \;" 
                    docker exec --privileged --user root "$container_id" sh -c "/usr/bin/find $mount -type f -exec /bin/chmod 666 {} \;" 
                    docker exec --privileged --user root "$container_id" sh -c "/bin/chown -R $(id -u):$(id -g) $mount"
            done
        done
    done
}

function set_permissions_for_host() {
    # Aplicamos permisos de acceso completo a los directorios del host que usamos como 
    # volúmenes de tipo bind mount para tener persistencia. Así nos aseguramos de que
    # los contenedores puedan escribir y de que el usuario del anfitrión pueda acceder.
    error="false"
    for i in $SERVICES; do
        mkdir -p "$i" || error="true"
        find "$i" -type d -exec chmod 777 {} \; || error="true"
        find "$i" -type f -exec chmod 666 {} \; || error="true"
    done

    if $error; then
        echo -ne "${RED_TEXT}"
        cat << EOF >&2
        
    Ha habido problemas al asignar algunos permisos de directorios locales. Entre otras cosas, puede afectar a:
        - La correcta ejecución de los contenedores y persistencia de sus datos.
        - La correcta migración de los ficheros usados en los puntos de montaje a otros entornos.

    Si los contenedores están en ejecución, vuelve a lanzar "$0" tras hacer "docker-compose down".
    Si no, vuelve a lanzar "$0" tras hacer "docker-compose up -d".

EOF
        # EOF debe ser una línea exacta sin caracteres delante o detrás @see sintaxis HEREDOC (<<)
        echo -ne "${RESET_TEXT}"
        exit 1
    else
        echo -e "Permisos locales asignados correctamente.\n"
    fi
}

# Esta funcion gestiona permisos de los bind mounts, almacenamiento basado el montaje 
# de ficheros o directorios del anfitrión en el contenedor.
# Los bind mounts dependen del sistema ficheros subyacente y pueden dañar el sistema anfitrión. 
# Se recomienda usar volúmenes gestionados por Docker para hacer persistentes los datos de los
# contenedores, los bind mount son apropiados para compartir ficheros de configuración y código,
# como es el caso de este proyecto.
# @see https://docs.docker.com/storage/bind-mounts/
#      https://docs.docker.com/storage/#good-use-cases-for-bind-mounts
function set_permissions() {
    chmod o+rwx . # Los usuarios de alumno aplican 750 por defecto.
    set_permissions_for_containers
    set_permissions_for_host
}

function main() {
    set_permissions
}

if [ "${BASH_SOURCE[0]}" -ef "$0" ]
then
    # Están ejecutando directamente este script, no importándolo con source
    main "$@"
fi

