import os
import helpers
import database as db


def iniciar(): #creamos la función iniciar
    while True: 
        helpers.limpiar_pantalla() #limpiamos la pantalla

        print("========================")
        print("  Bienvenido al Gestor  ")
        print("========================")
        print("[1] Listar los clientes ")
        print("[2] Buscar un cliente   ")
        print("[3] Añadir un cliente   ")
        print("[4] Modificar un cliente")
        print("[5] Borrar un cliente   ")
        print("[6] Cerrar el Gestor    ")
        print("========================")

        opcion = input("> ")
        helpers.limpiar_pantalla() 

        if opcion == '1': 
            print("Listando los clientes...\n")
            for cliente in db.Clientes.lista: #recorremos la lista de clientes
                print(cliente)

        elif opcion == '2':
            print("Buscando un cliente...\n")
            dni = helpers.leer_texto(3, 3, "DNI (2 int y 1 char)").upper() #leemos el DNI
            cliente = db.Clientes.buscar(dni) #buscamos el cliente
            print(cliente) if cliente else print("Cliente no encontrado.")

        elif opcion == '3':
            print("Añadiendo un cliente...\n")

            dni = None
            while True:
                dni = helpers.leer_texto(3, 3, "DNI (2 int y 1 char)").upper()  # Leemos el DNI
                if helpers.dni_valido(dni, db.Clientes.lista):  # Comprobamos que el DNI sea válido
                    break

            nombre = helpers.leer_texto(2, 30, "Nombre (de 2 a 30 chars)").capitalize() #leemos el nombre y lo capitalizamos
            apellido = helpers.leer_texto(2, 30, "Apellido (de 2 a 30 chars)").capitalize() #leemos el apellido y lo capitalizamos
            db.Clientes.crear(dni, nombre, apellido) #creamos el cliente
            print("Cliente añadido correctamente.")

        elif opcion == '4':
            print("Modificando un cliente...\n")
            dni = helpers.leer_texto(3, 3, "DNI (2 int y 1 char)").upper() # Leemos el DNI del cliente a modificar y lo capitalizamos
            cliente = db.Clientes.buscar(dni) #buscamos el cliente
            if cliente:
                nombre = helpers.leer_texto(    #leemos el nombre y lo capitalizamos 
                    2, 30, f"Nombre (de 2 a 30 chars) [{cliente.nombre}]").capitalize()
                apellido = helpers.leer_texto( #leemos el apellido y lo capitalizamos
                    2, 30, f"Apellido (de 2 a 30 chars) [{cliente.apellido}]").capitalize()
                db.Clientes.modificar(cliente.dni, nombre, apellido)
                print("Cliente modificado correctamente.")
            else:
                print("Cliente no encontrado.")

        elif opcion == '5':
            print("Borrando un cliente...\n")
            dni = helpers.leer_texto(3, 3, "DNI (2 int y 1 char)").upper() # Leemos el DNI del cliente a borrar y lo capitalizamos
            print("Cliente borrado correctamente.") if db.Clientes.borrar(   #borramos el cliente
                dni) else print("Cliente no encontrado.")

        elif opcion == '6':
            print("Saliendo...\n")
            break

        input("\nPresiona ENTER para continuar...")
