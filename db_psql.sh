#!/bin/bash
#
# Copyright 2022
#   Victor Gonzalez-Barbone
#   Universidad de la Republica, Uruguay.
# 
# This is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 3, or (at your option)
# any later version.
# 
# This software is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
# 
# You should have received a copy of the GNU General Public License
# along with this software; see the file COPYING.  If not, write to
# the Free Software Foundation, Inc., 51 Franklin Street,
# Boston, MA 02110-1301, USA.
#
#
# tryton_instalar.py: script para instalación de Tryton
# db_psql.sh: crea o borra usuario y base de datos PostgreSQL
#

# crear usuario y base de datos en PostgreSQL
DBACCION="$1"
DBNAME="$2"
if [ -z "$3" ]
then
    CONFFILE=~/.config/tryton/5.0/tryton.conf
else
    CONFFILE="$3"
fi

#echo "$DBACCION" "$DBUSER" "$DBNAME" "$CONFFILE"
#echo $DBACCION $DBUSER $DBNAME $CONFFILE
#if [ "$DBACCION" = "register" ]
#then
#  echo BIEN
#fi
#exit

if [ -z "$DBACCION" ]
then
  echo "db_psql.sh : crea, registra, consulta y borra bases de datos en Tryton"
  echo "uso:"
  echo "     bash db_psql.sh create nombre_bd [config_arch]"
  echo "     bash db_psql.sh register bd_nombre_bd [config_arch]"
  echo "     bash db_psql.sh drop nombre_bd [config arch]"
  echo "     bash db_psql.sh mostrar" 
  echo "     bash db_psql.sh createtryton"
  echo "     bash db_psql.sh droptryton"
  echo
fi

if [ "$DBACCION" = "createtryton" ]    # crea usuario tryton
then
    echo "=== Tryton: crea usuario tryton en PostgreSQL."
    sudo su - postgres -c \
        "createuser --createdb --no-createrole --no-superuser --pwprompt tryton"
elif [ "$DBACCION" = "droptryton" ]    # elimina usuario tryton
then
    echo "=== Tryton: borra usuario tryton en PostgreSQL."
    sudo su - postgres -c "dropuser tryton"
elif [ "$DBACCION" = "create" ]        # crea base de datos 
then
    echo "=== Tryton: crea base de datos PostgreSQL."
    sudo su - postgres -c "createdb --encoding=UNICODE --owner=tryton $DBNAME"
    sudo su - postgres -c "psql --list" | grep $DBNAME
elif [ "$DBACCION" = "register" ]      # registra base de datos en Tryton
then
    echo "=== Tryton: registra base de datos en Tryton."
    trytond-admin -v -c $CONFFILE -d $DBNAME --all
elif [ "$DBACCION" = "drop" ]
then
    echo "=== Tryton: borra base de datos PostgreSQL."
    sudo su - postgres -c "dropdb $DBNAME"
    sudo su - postgres -c "psql --list" | grep $DBNAME
elif [ "$DBACCION" = "mostrar" ]
then
    echo "=== Tryton: mostrar bases de datos existentes en PostgreSQL."
    sudo su - postgres -c "psql --list"
else
    echo "Tryton db_psql: acción desconocida."
fi





