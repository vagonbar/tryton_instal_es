#!/usr/bin/env python3
# -*- coding: utf-8 -*
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
# instala_lib.py: biblioteca para instalación y manejo de Tryton
#

import os
import sys
import shutil
import subprocess
import threading


# variables de ambiente modificables por el usuario
DBUSER = "tryton"                   # usuario para PosgreSQL
DBNAME = "BDprueba"                 # base de datos en PostgreSQL
TRYTON_DB_DIR = "tryton-db"         # directorio para base de datos
VERSION="5.0"                       # versión de Tryton a instalar

# variables de ambiente para instalación
HOMEDIR = os.environ['HOME'] 
CONFIG_FILE = HOMEDIR + "/.config/tryton/" + VERSION + "/tryton.conf"
CONFIG_DIR = HOMEDIR + "/.config/tryton/"

devnull = open(os.devnull, 'w')     # para suprimir salida
SALIDA = devnull                    # dispositivo para mensajes
th = None       # thread para servidor


### FUNCIONES


## funciones auxiliares

def my_quit_fn():
    if SALIDA:
        SALIDA.close()
    sys.exit()


def invalid():
    print("Opción inválida!")
    #pass
    return


## funciones de configuración

def config_file():
    '''Verifica o crea archivo de configuración según modelo.
    '''
    try:
        os.makedirs(CONFIG_DIR + VERSION)
    except OSError as e:
        pass  # el directorio ya existe
    try:
        shutil.copy("./tryton.conf.model", CONFIG_FILE)      # contenido 
    except IOError as e:
        pass  # el archivo existe y es de solo lectura
    return


## funciones de bases de datos

def crear_bd(dbname=None):
    '''Crea base de datos en Tryton.
    '''
    #if not dbuser:
    #    dbuser = input("   Usuario BD:")
    if not dbname:
        dbname = input("   Nombre  BD:")
    try:
        subprocess.call(['./db_psql.sh', 'create', dbname])
    except subprocess.CalledProcessError as e:
        print("=== Tryton: error al crear base de datos.")
        print(e)
        return 2
    return dbname

def registrar_bd(dbname):
    '''Registrar base de datos en el servidor Tryton.
    '''
    try:
        #start_server()     # ver si es necesario
        subprocess.call(['./db_psql.sh', 'register', dbname, CONFIG_FILE])
        #stop_server()
    except subprocess.CalledProcessError as e:
        print("=== Tryton: error al registrar base de datos en Tryton")
        print(e)
        return 1

def mostrar_bd():
    '''Muestra bases de datos existentes.
    '''
    subprocess.check_call( ['./db_psql.sh', 'mostrar'] )
    return

def borrar_bd(dbuser=None, dbname=None):
    '''Borra base de datos.
    '''
    #if not dbuser:
    #    dbuser = input("   Usuario BD:")
    if not dbname:
        dbname = input("   Nombre  BD:")
    try:
        subprocess.call(['./db_psql.sh', 'drop', dbname])
        print("=== Tryton: borrando base de datos", dbname)
    except subprocess.CalledProcessError as e:
        print("=== Tryton: error al borrar base de datos", dbname)
        print(e)
    return


## funciones de servidor

def server_up():
    '''Verifica si el servidor fue arrancado al inicio.
    '''
    sal = subprocess.run(['ps', '-C', 'trytond'], capture_output=True)
    if "?" in str(sal.stdout):
        print("tryton server fue arrancado al inicio.")
        return True
    else:
        return False


def start_server():
    '''Arranca el servidor Tryton, si está instalado.
    '''
    if subprocess.call(['ps', '-C', 'trytond'],
            stdout=SALIDA, stderr=SALIDA) == 0:
        print("=== Tryton: el servidor ya está corriendo.")
        return
    if subprocess.call(['which', 'trytond'],
            stdout=SALIDA, stderr=SALIDA) != 0:
        print("=== Tryton: el servidor no está instalado.")
        return
    config_file()               # asegurar existencia de tryton.conf
    sal = subprocess.call(['trytond -c '+CONFIG_FILE+' &'], shell=True, 
            stdout=SALIDA, stderr=SALIDA)
    if sal != 0:
        print("=== Tryton: error al arrancar el servidor.")
    else:
        print("=== Tryton: arrancó el servidor.")
    return


def stop_server():
    '''Detiene el servidor Tryton.
    '''
    if subprocess.call(['ps', '-C', 'trytond'], 
            stdout=SALIDA, stderr=SALIDA) != 0:
        print("== Tryton: el servidor no está corriendo.")
        return
    try:
        subprocess.check_call(['killall', 'trytond'], 
            stdout=SALIDA, stderr=SALIDA)
        print("=== Tryton: detenido el servidor.")
        return
    except Exception as e:
        print("=== Tryton: error al detener el servidor Tryton.")
        return


## funciones de cliente

def start_client():
    '''Invoca el cliente Tryton, si está instalado.
    '''
    if subprocess.call(['which', 'tryton'], 
            stdout=SALIDA, stderr=SALIDA) != 0:
        print("=== Tryton: el cliente no está instalado.")
        return
    config_file()
    sal = subprocess.call(['tryton -c '+CONFIG_FILE+
            '>/dev/null 2>&1 &'], shell=True, 
            stdout=SALIDA, stderr=SALIDA)  # no mostrar GTK warnings
    if sal != 0:
        print("=== Tryton: error al arrancar el cliente.")
    else:
        print("=== Tryton: arrancó el cliente.")
    return


def stop_client():
    '''Detiene el cliente Tryton.
    '''
    if subprocess.call(['ps', '-C', 'tryton'],
            stdout=SALIDA, stderr=SALIDA) != 0:
        print("=== Tryton: el cliente no está corriendo.")
        return
    try:
        subprocess.check_call(['killall', '-KILL', 'tryton'],
            stdout=SALIDA, stderr=SALIDA)
        print("=== Tryton: detenido el cliente.")
        return
    except Exception as e:
        print("=== Tryton: error al detener el cliente.")
        #print(e)
        return




