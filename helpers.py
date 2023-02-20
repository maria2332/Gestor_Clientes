import re
import os
import platform


def limpiar_pantalla(): # Función para limpiar la pantalla
    os.system('cls') if platform.system() == "Windows" else os.system('clear')


def leer_texto(longitud_min=0, longitud_max=100, mensaje=None): # Función para leer texto
    print(mensaje) if mensaje else None
    while True:
        texto = input("> ")
        if len(texto) >= longitud_min and len(texto) <= longitud_max: # Comprobamos que el texto cumpla las restricciones de longitud
            return texto


def dni_valido(dni, lista): # Función para validar el DNI
    if not re.match('[0-9]{2}[A-Z]$', dni): # Comprobamos que el DNI cumpla el formato
        print("DNI incorrecto, debe cumplir el formato.")
        return False
    for cliente in lista: # Comprobamos que el DNI no esté utilizado por otro cliente
        if cliente.dni == dni: 
            print("DNI utilizado por otro cliente.")
            return False
    return True
