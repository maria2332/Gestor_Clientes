import helpers
import database as db
from tkinter import *
from tkinter import ttk
from tkinter.messagebox import askokcancel, WARNING


class CenterWidgetMixin: # Mixin para centrar la ventana
    def center(self): #creamos el método center
        self.update() #actualizamos la ventana
        w = self.winfo_width()  #obtenemos el ancho de la ventana
        h = self.winfo_height() #obtenemos el alto de la ventana
        ws = self.winfo_screenwidth()   #obtenemos el ancho de la pantalla
        hs = self.winfo_screenheight()  #obtenemos el alto de la pantalla
        x = int(ws/2 - w/2)     #calculamos la posición x
        y = int(hs/2 - h/2)     #calculamos la posición y
        self.geometry(f"{w}x{h}+{x}+{y}")   #establecemos la posición de la ventana


class CreateClientWindow(Toplevel, CenterWidgetMixin): #creamos la clase CreateClientWindow que hereda de Toplevel y CenterWidgetMixin
    def __init__(self, parent): #creamos el método __init__ con el atributo parent
        super().__init__(parent) #llamamos al método __init__ de la clase padre
        self.title("Crear cliente") #establecemos el título de la ventana
        self.build()    #llamamos al método build
        self.center()   #llamamos al método center
        self.transient(parent)  #establecemos la ventana como transient
        self.grab_set() #establecemos la ventana como grab_set

    def build(self):  #creamos el método build
        frame = Frame(self)     #creamos el frame
        frame.pack(padx=20, pady=10)    #establecemos el padding del frame

        Label(frame, text="DNI (2 ints y 1 upper char)").grid(row=0, column=0)  #creamos el label DNI
        Label(frame, text="Nombre (de 2 a 30 chars)").grid(row=0, column=1)  #creamos el label Nombre
        Label(frame, text="Apellido (de 2 a 30 chars)").grid(row=0, column=2)   #creamos el label Apellido

        dni = Entry(frame)  #creamos el entry DNI
        dni.grid(row=1, column=0)   #establecemos la posición del entry DNI
        dni.bind("<KeyRelease>", lambda event: self.validate(event, 0))   #establecemos el evento KeyRelease para validar el entry DNI
        nombre = Entry(frame)
        nombre.grid(row=1, column=1)
        nombre.bind("<KeyRelease>", lambda event: self.validate(event, 1))
        apellido = Entry(frame)
        apellido.grid(row=1, column=2)
        apellido.bind("<KeyRelease>", lambda event: self.validate(event, 2))

        frame = Frame(self) #creamos el frame
        frame.pack(pady=10) #establecemos el padding del frame

        crear = Button(frame, text="Crear", command=self.create_client) #creamos el botón Crear
        crear.configure(state=DISABLED) #establecemos el estado del botón Crear como deshabilitado
        crear.grid(row=0, column=0) #establecemos la posición del botón Crear
        Button(frame, text="Cancelar", command=self.close).grid(row=0, column=1)    #creamos el botón Cancelar

        self.validaciones = [0, 0, 0]   #creamos la lista validaciones
        self.crear = crear  
        self.dni = dni  
        self.nombre = nombre
        self.apellido = apellido

    def create_client(self):   #creamos el método create_client
        self.master.treeview.insert( #insertamos los datos en el treeview
            parent='', index='end', iid=self.dni.get(),     #establecemos el parent, index e iid
            values=(self.dni.get(), self.nombre.get(), self.apellido.get()))    #establecemos los valores
        db.Clientes.crear(self.dni.get(), self.nombre.get(), self.apellido.get())   #insertamos los datos en la base de datos
        self.close()    #llamamos al método close

    def close(self):
        self.destroy()
        self.update()

    def validate(self, event, index):   #creamos el método validate
        valor = event.widget.get()  
        valido = helpers.dni_valido(valor, db.Clientes.lista) if index == 0 \
            else (valor.isalpha() and len(valor) >= 2 and len(valor) <= 30) 
        event.widget.configure({"bg": "Green" if valido else "Red"})
        # Cambiar el estado del botón en base a las validaciones
        self.validaciones[index] = valido   #establecemos el valor de la lista validaciones
        self.crear.config(state=NORMAL if self.validaciones == [1, 1, 1] else DISABLED)  #establecemos el estado del botón Crear


class EditClientWindow(Toplevel, CenterWidgetMixin):    #creamos la clase EditClientWindow que hereda de Toplevel y CenterWidgetMixin
    def __init__(self, parent): #creamos el método __init__ con el atributo parent
        super().__init__(parent)    #llamamos al método __init__ de la clase padre
        self.title("Actualizar cliente")    #establecemos el título de la ventana
        self.build()    #llamamos al método build
        self.center()   #llamamos al método center
        self.transient(parent)     #establecemos la ventana como transient
        self.grab_set()   #establecemos la ventana como grab_set

    def build(self):    #creamos el método build
        frame = Frame(self)    #creamos el frame
        frame.pack(padx=20, pady=10)    #establecemos el padding del frame

        Label(frame, text="DNI (no editable)").grid(row=0, column=0)    #creamos el label DNI
        Label(frame, text="Nombre (de 2 a 30 chars)").grid(row=0, column=1)   #creamos el label Nombre
        Label(frame, text="Apellido (de 2 a 30 chars)").grid(row=0, column=2)   #creamos el label Apellido

        dni = Entry(frame)  #creamos el entry DNI
        dni.grid(row=1, column=0)   #establecemos la posición del entry DNI
        nombre = Entry(frame)   #creamos el entry Nombre
        nombre.grid(row=1, column=1)    #establecemos la posición del entry Nombre
        nombre.bind("<KeyRelease>", lambda event: self.validate(event, 0))  #establecemos el evento KeyRelease para validar el entry Nombre
        apellido = Entry(frame) #creamos el entry Apellido
        apellido.grid(row=1, column=2)  #establecemos la posición del entry Apellido
        apellido.bind("<KeyRelease>", lambda event: self.validate(event, 1))    #establecemos el evento KeyRelease para validar el entry Apellido

        cliente = self.master.treeview.focus()  #establecemos el cliente
        campos = self.master.treeview.item(cliente, 'values')   #establecemos los campos
        dni.insert(0, campos[0])    #insertamos los datos en el entry DNI
        dni.config(state=DISABLED)  #establecemos el estado del entry DNI como deshabilitado
        nombre.insert(0, campos[1]) #insertamos los datos en el entry Nombre
        apellido.insert(0, campos[2])   #insertamos los datos en el entry Apellido
    
        frame = Frame(self) #creamos el frame
        frame.pack(pady=10) #establecemos el padding del frame

        actualizar = Button(frame, text="Actualizar", command=self.edit_client) #creamos el botón Actualizar
        actualizar.grid(row=0, column=0)    #establecemos la posición del botón Actualizar
        Button(frame, text="Cancelar", command=self.close).grid(row=0, column=1)    #creamos el botón Cancelar

        self.validaciones = [1, 1]  #creamos la lista validaciones
        self.actualizar = actualizar    #establecemos el valor de la lista actualizar
        self.dni = dni  #establecemos el valor de la lista dni
        self.nombre = nombre    #establecemos el valor de la lista nombre
        self.apellido = apellido    #establecemos el valor de la lista apellido

    def edit_client(self):  #creamos el método edit_client
        cliente = self.master.treeview.focus()      #establecemos el cliente
        self.master.treeview.item(cliente, values=( #establecemos los valores
            self.dni.get(), self.nombre.get(), self.apellido.get()))        
        db.Clientes.modificar(self.dni.get(), self.nombre.get(), self.apellido.get())   #modificamos los datos en la base de datos
        self.close()    #llamamos al método close

    def close(self):    #creamos el método close
        self.destroy()  #destruimos la ventana
        self.update()   #actualizamos la ventana

    def validate(self, event, index):   #creamos el método validate
        valor = event.widget.get()  #establecemos el valor del entry
        valido = (valor.isalpha() and len(valor) >= 2 and len(valor) <= 30) #establecemos la validación
        event.widget.configure({"bg": "Green" if valido else "Red"})    #establecemos el color del entry
        # Cambiar el estado del botón en base a las validaciones
        self.validaciones[index] = valido   #establecemos el valor de la lista validaciones
        self.actualizar.config(state=NORMAL if self.validaciones == [1, 1] else DISABLED)   #establecemos el estado del botón Actualizar


class MainWindow(Tk, CenterWidgetMixin):    #creamos la clase MainWindow que hereda de Tk y CenterWidgetMixin
    def __init__(self): #creamos el método __init__
        super().__init__()
        self.title("Gestor de clientes")
        self.build()
        self.center()

    def build(self):   #creamos el método build
        frame = Frame(self) #creamos el frame
        frame.pack()   #empaquetamos el frame

        treeview = ttk.Treeview(frame) #creamos el treeview
        treeview['columns'] = ('DNI', 'Nombre', 'Apellido') #establecemos las columnas

        treeview.column("#0", width=0, stretch=NO) #establecemos el ancho de la columna 0
        treeview.column("DNI", anchor=CENTER)   #establecemos el ancho de la columna DNI
        treeview.column("Nombre", anchor=CENTER)    #establecemos el ancho de la columna Nombre
        treeview.column("Apellido", anchor=CENTER)  #establecemos el ancho de la columna Apellido

        treeview.heading("DNI", text="DNI", anchor=CENTER)  #establecemos el encabezado de la columna DNI
        treeview.heading("Nombre", text="Nombre", anchor=CENTER)    #establecemos el encabezado de la columna Nombre
        treeview.heading("Apellido", text="Apellido", anchor=CENTER)    #establecemos el encabezado de la columna Apellido

        scrollbar = Scrollbar(frame) #creamos el scrollbar
        scrollbar.pack(side=RIGHT, fill=Y) #empaquetamos el scrollbar
        treeview['yscrollcommand'] = scrollbar.set  #establecemos el comando del scrollbar

        for cliente in db.Clientes.lista:  #recorremos la lista de clientes
            treeview.insert(    #insertamos los clientes en el treeview
                parent='', index='end', iid=cliente.dni,    #establecemos el id del cliente como su DNI
                values=(cliente.dni, cliente.nombre, cliente.apellido)) #establecemos los valores del cliente

        treeview.pack() #empaquetamos el treeview

        frame = Frame(self) #creamos el frame
        frame.pack(pady=20) #empaquetamos el frame

        Button(frame, text="Crear", command=self.create).grid(row=0, column=0)  #creamos el botón crear
        Button(frame, text="Modificar", command=self.edit).grid(row=0, column=1)    #creamos el botón modificar
        Button(frame, text="Borrar", command=self.delete).grid(row=0, column=2) #creamos el botón borrar

        self.treeview = treeview    #establecemos el treeview como atributo de la clase

    def delete(self):   #creamos el método delete
        cliente = self.treeview.focus() #obtenemos el cliente seleccionado
        if cliente:
            campos = self.treeview.item(cliente, "values") #obtenemos los valores del cliente
            confirmar = askokcancel(    #creamos un cuadro de diálogo para confirmar el borrado
                title="Confirmar borrado",  #establecemos el título del cuadro de diálogo
                message=f"¿Borrar {campos[1]} {campos[2]}?",    #establecemos el mensaje del cuadro de diálogo
                icon=WARNING)   #establecemos el icono del cuadro de diálogo
            if confirmar:   
                self.treeview.delete(cliente)   #borramos el cliente del treeview
                db.Clientes.borrar(campos[0])   #borramos el cliente de la base de datos

    def create(self):   #creamos el método create
        CreateClientWindow(self)    #creamos una ventana para crear un cliente

    def edit(self): #creamos el método edit
        if self.treeview.focus():   #comprobamos que haya un cliente seleccionado
            EditClientWindow(self)  #creamos una ventana para editar un cliente


if __name__ == "__main__":
    app = MainWindow()  #creamos la ventana principal
    app.mainloop()  #ejecutamos el bucle principal
