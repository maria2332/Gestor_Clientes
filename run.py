import ui
import sys
import menu

if __name__ == "__main__":  
    if len(sys.argv) > 1 and sys.argv[1] == "-t": # Comprobamos si se ha pasado el argumento -t
        menu.iniciar() # Iniciamos el gestor en modo texto
    else:
        app = ui.MainWindow() # Iniciamos el gestor en modo gráfico
        app.mainloop() # Bucle principal de la aplicación
