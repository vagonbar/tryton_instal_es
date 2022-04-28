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
# tryton-manager.py: script para gestionar Tryton
#


import sys


#from instal_lib import start_client, stop_client, start_server, stop_server, mostrar_bd, server_up, my_quit_fn, invalid
from lib_tryton_manager import *


# mensajes de título y ayuda
txt_titulo = "\n\nTryton, scripts de gestión."
txt_ayuda = '''\
Uso:
    python3 trytongest <opción>
      --help   muestra esta ayuda
      --menu   muestra menù para instalar y desinstalar cliente y servidor.
'''


def crea_reg_bd():
    '''Crea y registra una base de datos.
    '''
    bdname = crear_bd()
    registrar_bd(bdname)
    return


def menu():
    # verificar disponibilidad de archivos
    """try:
        subprocess.check_call(["ls", "tryton.conf.model"], stdout=SALIDA,
            stderr=SALIDA)
        subprocess.check_call(["ls", "db_psql.sh"], stdout=SALIDA,
            stderr=SALIDA)
    except subprocess.CalledProcessError as e:"""
    if os.access('tryton.conf.model', os.R_OK) and \
            os.access('db_psql.sh', os.R_OK):
        pass            # están archivos y son legibles
    else:
        print("=== Tryton: no se encuentran archivos. Debe correr este")
        print("    script desde el directorio donde fue descomprimido.")
        #print(e)
        if SALIDA:
            SALIDA.close()
        sys.exit()

    menu = {
        #"I1":("Verificar requerimientos.", verif_reqs), 
        #"I2":("Instalar el servidor Tryton.", inst_server),
        #"I3":("Instalar el cliente Tryton", inst_client),
        #"I4":("Desinstalar cliente y servidor (conserva los paquetes).", \
        #    desinst),
        "4":("Iniciar el cliente Tryton.", start_client),
        "5":("Detener el cliente Tryton.", stop_client),
        "6":("Iniciar el servidor Tryton.", start_server),
        "7":("Detener el servidor Tryton.", stop_server),
        "1":("Crear y registrar base de datos.", crea_reg_bd), 
        "2":("Borrar base de datos.", borrar_bd),
        "3":("Mostrar bases de datos.", mostrar_bd),
        "q":("Salir",my_quit_fn)
       }
    ans = ""
    while not ans == 'q':
        print(txt_titulo)
        
        #for key in sorted(menu.keys()):
        #    print("   " + key + ": " + menu[key][0])

        #print("-- Instalar / desinstalar Tryton")
        #for key in ["I1", "I2", "I3", "I4"]:
        #    print("   " + key + " : " + menu[key][0])
        print("-- Bases de datos")
        for key in ["1", "2", "3"]:
            print("   " + key + " : " + menu[key][0])
        print("-- Cliente Tryton")
        for key in ["4", "5"]:
            print("   " + key + " : " + menu[key][0])
        print("-- Servidor Tryton")
        for key in ["6", "7"]:
            print("   " + key + " : " + menu[key][0])
        print("   q : " + menu["q"][0])
            
        ans = input("Elija una opción: ")
        menu.get(ans,[None,invalid])[1]()



if __name__ == "__main__":

    # procesar argumentos de línea de comando
    if "-v" in sys.argv:
        SALIDA = None     # muestra mensajes.
    if "--help" in sys.argv:
        print(txt_ayuda)
    elif "--menu" in sys.argv:
        menu()
    else:
        menu()
        #print(txt_ayuda)


