import tkinter as tk

from modelo import MotorArteGenerativo
from controlador import ControladorArte
from vista import VistaApp

def centrar_ventana(ventana, ancho, alto):
    # Obtener el ancho y alto de la pantalla del usuario
    pantalla_ancho = ventana.winfo_screenwidth()
    pantalla_alto = ventana.winfo_screenheight()

    # Fórmulas matemáticas para encontrar el punto centro (X, Y)
    posicion_x = int((pantalla_ancho / 2) - (ancho / 2))
    posicion_y = int((pantalla_alto / 2) - (alto / 2))

    # Aplicar la geometría en formato oficial de Tkinter: "ancho x alto + X + Y"
    ventana.geometry(f"{ancho}x{alto}+{posicion_x}+{posicion_y}")

if __name__ == "__main__":
    # Creación del entorno raíz de la ventana
    root_window = tk.Tk()

    # Dimensiones de la app
    ancho_app = 1200
    alto_app = 750

    # Forzando a Tkinter a centrar la ventana en el monitor
    centrar_ventana(root_window, ancho_app, alto_app)
    
    # Inicializando la arquitectura MVC: Modelo, Vista y Controlador
    app = VistaApp(root_window, ControladorArte, MotorArteGenerativo)
    
    # Lanzando la interfaz gráfica
    root_window.mainloop() 