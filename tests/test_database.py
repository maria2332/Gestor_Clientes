
import csv
import copy
import config
import helpers
import unittest
import database as db


class TestDatabase(unittest.TestCase): #creamos la clase TestDatabase que hereda de unittest.TestCase

    def setUp(self): #creamos el método setUp que se ejecuta antes de cada test
        db.Clientes.lista = [
            db.Cliente('15J', 'Marta', 'Pérez'),
            db.Cliente('48H', 'Manolo', 'López'),
            db.Cliente('28Z', 'Ana', 'García')
        ]

    def test_buscar_cliente(self):  #creamos el método test_buscar_cliente con cliente_existente y cliente_inexistente buscando por dni
        cliente_existente = db.Clientes.buscar('15J')
        cliente_inexistente = db.Clientes.buscar('99X')
        self.assertIsNotNone(cliente_existente)
        self.assertIsNone(cliente_inexistente)

    def test_crear_cliente(self): #creamos el método test_crear_cliente con nombre, apellido y dni
        nuevo_cliente = db.Clientes.crear('39X', 'Héctor', 'Costa')
        self.assertEqual(len(db.Clientes.lista), 4)
        self.assertEqual(nuevo_cliente.dni, '39X')
        self.assertEqual(nuevo_cliente.nombre, 'Héctor')
        self.assertEqual(nuevo_cliente.apellido, 'Costa')

    def test_modificar_cliente(self): #creamos el método test_modificar_cliente con cliente_a_modificar y cliente_modificado buscando por dni
        cliente_a_modificar = copy.copy(db.Clientes.buscar('28Z'))
        cliente_modificado = db.Clientes.modificar('28Z', 'Mariana', 'García')
        self.assertEqual(cliente_a_modificar.nombre, 'Ana')
        self.assertEqual(cliente_modificado.nombre, 'Mariana')

    def test_borrar_cliente(self): #creamos el método test_borrar_cliente con cliente_borrado y cliente_rebuscado buscando por dni
        cliente_borrado = db.Clientes.borrar('48H')
        cliente_rebuscado = db.Clientes.buscar('48H')
        self.assertEqual(cliente_borrado.dni, '48H')
        self.assertIsNone(cliente_rebuscado)

    def test_dni_valido(self): #creamos el método test_dni_valido con dni_valido y dni_invalido
        self.assertTrue(helpers.dni_valido('00A', db.Clientes.lista))
        self.assertFalse(helpers.dni_valido('232323S', db.Clientes.lista))
        self.assertFalse(helpers.dni_valido('F35', db.Clientes.lista))
        self.assertFalse(helpers.dni_valido('48H', db.Clientes.lista))

    def test_escritura_csv(self): #creamos el método test_escritura_csv con dni, nombre y apellido
        db.Clientes.borrar('48H')
        db.Clientes.borrar('15J')
        db.Clientes.modificar('28Z', 'Mariana', 'García')

        dni, nombre, apellido = None, None, None
        with open(config.DATABASE_PATH, newline='\n') as fichero: #abrimos el fichero csv
            reader = csv.reader(fichero, delimiter=';') #leemos el fichero csv
            dni, nombre, apellido = next(reader) 

        self.assertEqual(dni, '28Z') #comprobamos que los datos del fichero csv son correctos
        self.assertEqual(nombre, 'Mariana') 
        self.assertEqual(apellido, 'García')
