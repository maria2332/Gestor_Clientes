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
        self.validaciones[index] = valido
        self.crear.config(state=NORMAL if self.validaciones == [1, 1, 1] else DISABLED)


class EditClientWindow(Toplevel, CenterWidgetMixin):
    def __init__(self, parent):
        super().__init__(parent)
        self.title("Actualizar cliente")
        self.build()
        self.center()
        self.transient(parent)
        self.grab_set()

    def build(self):
        frame = Frame(self)
        frame.pack(padx=20, pady=10)

        Label(frame, text="DNI (no editable)").grid(row=0, column=0)
        Label(frame, text="Nombre (de 2 a 30 chars)").grid(row=0, column=1)
        Label(frame, text="Apellido (de 2 a 30 chars)").grid(row=0, column=2)

        dni = Entry(frame)
        dni.grid(row=1, column=0)
        nombre = Entry(frame)
        nombre.grid(row=1, column=1)
        nombre.bind("<KeyRelease>", lambda event: self.validate(event, 0))
        apellido = Entry(frame)
        apellido.grid(row=1, column=2)
        apellido.bind("<KeyRelease>", lambda event: self.validate(event, 1))

        cliente = self.master.treeview.focus()
        campos = self.master.treeview.item(cliente, 'values')
        dni.insert(0, campos[0])
        dni.config(state=DISABLED)
        nombre.insert(0, campos[1])
        apellido.insert(0, campos[2])

        frame = Frame(self)
        frame.pack(pady=10)

        actualizar = Button(frame, text="Actualizar", command=self.edit_client)
        actualizar.grid(row=0, column=0)
        Button(frame, text="Cancelar", command=self.close).grid(row=0, column=1)

        self.validaciones = [1, 1]
        self.actualizar = actualizar
        self.dni = dni
        self.nombre = nombre
        self.apellido = apellido

    def edit_client(self):
        cliente = self.master.treeview.focus()
        self.master.treeview.item(cliente, values=(
            self.dni.get(), self.nombre.get(), self.apellido.get()))
        db.Clientes.modificar(self.dni.get(), self.nombre.get(), self.apellido.get())
        self.close()

    def close(self):
        self.destroy()
        self.update()

    def validate(self, event, index):
        valor = event.widget.get()
        valido = (valor.isalpha() and len(valor) >= 2 and len(valor) <= 30)
        event.widget.configure({"bg": "Green" if valido else "Red"})
        # Cambiar el estado del botón en base a las validaciones
        self.validaciones[index] = valido
        self.actualizar.config(state=NORMAL if self.validaciones == [1, 1] else DISABLED)


class MainWindow(Tk, CenterWidgetMixin):
    def __init__(self):
        super().__init__()
        self.title("Gestor de clientes")
        self.build()
        self.center()

    def build(self):
        frame = Frame(self)
        frame.pack()

        treeview = ttk.Treeview(frame)
        treeview['columns'] = ('DNI', 'Nombre', 'Apellido')

        treeview.column("#0", width=0, stretch=NO)
        treeview.column("DNI", anchor=CENTER)
        treeview.column("Nombre", anchor=CENTER)
        treeview.column("Apellido", anchor=CENTER)

        treeview.heading("DNI", text="DNI", anchor=CENTER)
        treeview.heading("Nombre", text="Nombre", anchor=CENTER)
        treeview.heading("Apellido", text="Apellido", anchor=CENTER)

        scrollbar = Scrollbar(frame)
        scrollbar.pack(side=RIGHT, fill=Y)
        treeview['yscrollcommand'] = scrollbar.set

        for cliente in db.Clientes.lista:
            treeview.insert(
                parent='', index='end', iid=cliente.dni,
                values=(cliente.dni, cliente.nombre, cliente.apellido))

        treeview.pack()

        frame = Frame(self)
        frame.pack(pady=20)

        Button(frame, text="Crear", command=self.create).grid(row=0, column=0)
        Button(frame, text="Modificar", command=self.edit).grid(row=0, column=1)
        Button(frame, text="Borrar", command=self.delete).grid(row=0, column=2)

        self.treeview = treeview

    def delete(self):
        cliente = self.treeview.focus()
        if cliente:
            campos = self.treeview.item(cliente, "values")
            confirmar = askokcancel(
                title="Confirmar borrado",
                message=f"¿Borrar {campos[1]} {campos[2]}?",
                icon=WARNING)
            if confirmar:
                self.treeview.delete(cliente)
                db.Clientes.borrar(campos[0])

    def create(self):
        CreateClientWindow(self)

    def edit(self):
        if self.treeview.focus():
            EditClientWindow(self)


if __name__ == "__main__":
    app = MainWindow()
    app.mainloop()
