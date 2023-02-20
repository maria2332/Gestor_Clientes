import csv
import config


class Cliente: #creamos la clase Cliente
    def __init__(self, dni, nombre, apellido): #creamos el método __init__ con los atributos dni, nombre y apellido
        self.dni = dni
        self.nombre = nombre
        self.apellido = apellido

    def __str__(self): #creamos el método __str__ para que nos devuelva el dni, nombre y apellido
        return f"({self.dni}) {self.nombre} {self.apellido}"

    def to_dict(self): #creamos el método to_dict para que nos devuelva el dni, nombre y apellido en formato diccionario
        return {'dni': self.dni, 'nombre': self.nombre, 'apellido': self.apellido}


class Clientes:

    lista = []
    with open(config.DATABASE_PATH, newline='\n') as fichero:   
        reader = csv.reader(fichero, delimiter=';')
        for dni, nombre, apellido in reader:
            cliente = Cliente(dni, nombre, apellido)
            lista.append(cliente)

    @staticmethod #creamos el método estático buscar
    def buscar(dni):
        for cliente in Clientes.lista:
            if cliente.dni == dni:
                return cliente

    @staticmethod #creamos el método estático crear
    def crear(dni, nombre, apellido):
        cliente = Cliente(dni, nombre, apellido)
        Clientes.lista.append(cliente)
        Clientes.guardar()
        return cliente

    @staticmethod #creamos el método estático modificar
    def modificar(dni, nombre, apellido):
        for indice, cliente in enumerate(Clientes.lista):
            if cliente.dni == dni:
                Clientes.lista[indice].nombre = nombre
                Clientes.lista[indice].apellido = apellido
                Clientes.guardar()
                return Clientes.lista[indice]

    @staticmethod #creamos el método estático borrar
    def borrar(dni):
        for indice, cliente in enumerate(Clientes.lista):
            if cliente.dni == dni:
                cliente = Clientes.lista.pop(indice)
                Clientes.guardar()
                return cliente

    @staticmethod #creamos el método estático guardar
    def guardar():
        with open(config.DATABASE_PATH, 'w', newline='\n') as fichero:
            writer = csv.writer(fichero, delimiter=';')
            for cliente in Clientes.lista:
                writer.writerow((cliente.dni, cliente.nombre, cliente.apellido))
