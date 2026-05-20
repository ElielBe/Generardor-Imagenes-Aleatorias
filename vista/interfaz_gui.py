import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk

class VistaApp:
    def __init__(self, root, controlador_clase, modelo_clase):
        self.root = root
        self.root.title("Generador de Imágenes Artísticas")
        self.root.geometry("1200x750")
        self.root.configure(bg="#18181c")
        
        self.controlador = controlador_clase(self, modelo_clase)

        # Paneles principales
        self.frame_inputs = tk.Frame(root, bg="#22222a", padx=15, pady=15)
        self.frame_inputs.pack(side=tk.LEFT, fill=tk.Y)
        
        self.frame_canvas = tk.Frame(root, bg="#18181c")
        self.frame_canvas.pack(side=tk.LEFT, expand=True, fill=tk.BOTH)
        
        self.frame_historial = tk.Frame(root, bg="#1e1e24", padx=10, pady=15, width=320)
        self.frame_historial.pack(side=tk.RIGHT, fill=tk.Y)
        self.frame_historial.pack_propagate(False)

        self._construir_ui_inputs()
        self._construir_ui_central()
        self._construir_ui_historial()
        
        self.ejecutar_generacion()

    def _construir_ui_inputs(self):
        tk.Label(self.frame_inputs, text="SEMILLAS DE CREACIÓN", font=("Arial", 11, "bold"), fg="#ffffff", bg="#22222a").pack(pady=10)

        tk.Label(self.frame_inputs, text="Semilla Color:", fg="#a0a0b0", bg="#22222a").pack(anchor=tk.W, pady=2)
        self.entry_color = tk.Entry(self.frame_inputs, font=("Arial", 11), width=20, bg="#18181c", fg="white", insertbackground="white")
        self.entry_color.insert(0, "Cosmos")
        self.entry_color.pack(pady=5)

        tk.Label(self.frame_inputs, text="Semilla Forma 1:", fg="#a0a0b0", bg="#22222a").pack(anchor=tk.W, pady=2)
        self.entry_forma1 = tk.Entry(self.frame_inputs, font=("Arial", 11), width=20, bg="#18181c", fg="white", insertbackground="white")
        self.entry_forma1.insert(0, "Fractal")
        self.entry_forma1.pack(pady=5)

        tk.Label(self.frame_inputs, text="Semilla Forma 2:", fg="#a0a0b0", bg="#22222a").pack(anchor=tk.W, pady=2)
        self.entry_forma2 = tk.Entry(self.frame_inputs, font=("Arial", 11), width=20, bg="#18181c", fg="white", insertbackground="white")
        self.entry_forma2.insert(0, "Fluido")
        self.entry_forma2.pack(pady=5)

        self.btn_sorpresa = tk.Button(
            self.frame_inputs, text="🎲 SORPRENDERME", font=("Arial", 10, "bold"),
            bg="#374151", fg="#e5e7eb", activebackground="#4b5563", activeforeground="white",
            bd=0, padx=10, pady=6, command=self.randomizar_todo, cursor="hand2"
        )
        self.btn_sorpresa.pack(fill=tk.X, pady=5)

        self.btn_generar = tk.Button(
            self.frame_inputs, text="GENERAR IMAGEN", font=("Arial", 11, "bold"),
            bg="#4f46e5", fg="white", activebackground="#4338ca", activeforeground="white",
            bd=0, padx=10, pady=10, command=self.ejecutar_generacion, cursor="hand2"
        )
        self.btn_generar.pack(pady=10, fill=tk.X)

    def _construir_ui_central(self):
        self.label_principal = tk.Label(self.frame_canvas, bg="#0f0f12")
        self.label_principal.pack(expand=True)

    def _construir_ui_historial(self):
        tk.Label(self.frame_historial, text="GALERÍA DE SESIÓN", font=("Arial", 12, "bold"), fg="#ffffff", bg="#1e1e24").pack(pady=5)
        
        # Guardamos el canvas como variable de clase para acceder a él en los eventos
        self.canvas_scroll = tk.Canvas(self.frame_historial, bg="#1e1e24", bd=0, highlightthickness=0)
        scrollbar = ttk.Scrollbar(self.frame_historial, orient="vertical", command=self.canvas_scroll.yview)
        self.scroll_content = tk.Frame(self.canvas_scroll, bg="#1e1e24")

        self.scroll_content.bind(
            "<Configure>", 
            lambda e: self.canvas_scroll.configure(scrollregion=self.canvas_scroll.bbox("all"))
        )
        self.canvas_scroll.create_window((0, 0), window=self.scroll_content, anchor="nw", width=290) # Ancho fijo interno
        self.canvas_scroll.configure(yscrollcommand=scrollbar.set)
        
        self.canvas_scroll.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        self.canvas_scroll.bind_all("<MouseWheel>", self._on_mousewheel)

    def ejecutar_generacion(self):
        self.controlador.procesar_peticion_arte(
            self.entry_color.get(),
            self.entry_forma1.get(),
            self.entry_forma2.get()
        )

    def mostrar_imagen_principal(self, img_pil):
        self.img_tk_principal = ImageTk.PhotoImage(img_pil)
        self.label_principal.config(image=self.img_tk_principal)

    def actualizar_panel_historial(self, lista_historial):
        # Limpiar miniaturas anteriores
        for widget in self.scroll_content.winfo_children():
            widget.destroy()

        self.miniaturas_tk = []
        
        total_elementos = len(lista_historial)
        for i in range(total_elementos - 1, -1, -1):
            nombre, img_pil, c_seed, f1_seed, f2_seed, _ = lista_historial[i]

            # Contenedor de la Tarjeta
            frame_item = tk.Frame(self.scroll_content, bg="#282830", pady=8, padx=8, cursor="hand2")
            frame_item.pack(pady=8, fill=tk.X, anchor=tk.W)

            # Redimensionar miniatura
            img_thumb = img_pil.resize((85, 85), Image.Resampling.LANCZOS)
            img_tk_thumb = ImageTk.PhotoImage(img_thumb)
            self.miniaturas_tk.append(img_tk_thumb)

            lbl_thumb = tk.Label(frame_item, image=img_tk_thumb, bg="#18181c")
            lbl_thumb.pack(side=tk.LEFT, anchor="nw") # Anclado arriba a la izquierda

            # Contenedor de Textos e Info
            frame_info = tk.Frame(frame_item, bg="#282830")
            frame_info.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=8)

            # Nombre del archivo arriba
            texto_recortado = (nombre[:18] + '...') if len(nombre) > 21 else nombre
            lbl_texto = tk.Label(frame_info, text=texto_recortado, font=("Arial", 9, "bold"), fg="#ffffff", bg="#282830", anchor="w")
            lbl_texto.pack(fill=tk.X, pady=(0, 4))

            # Contenedor de Pastillas Verticales
            frame_pastillas = tk.Frame(frame_info, bg="#282830")
            frame_pastillas.pack(fill=tk.X, anchor="w")

            # Pastilla Color
            lbl_p_col = tk.Label(frame_pastillas, text=f"{c_seed}", font=("Arial", 8, "bold"), fg="#3b82f6", bg="#1d3557", padx=8, pady=2, anchor="w")
            lbl_p_col.pack(fill=tk.X, pady=2, anchor="w")

            # Pastilla Forma 1
            lbl_p_f1 = tk.Label(frame_pastillas, text=f"{f1_seed}", font=("Arial", 8, "bold"), fg="#10b981", bg="#134e4a", padx=8, pady=2, anchor="w")
            lbl_p_f1.pack(fill=tk.X, pady=2, anchor="w")

            # Pastilla Forma 2
            lbl_p_f2 = tk.Label(frame_pastillas, text=f"{f2_seed}", font=("Arial", 8, "bold"), fg="#a855f7", bg="#3b0764", padx=8, pady=2, anchor="w")
            lbl_p_f2.pack(fill=tk.X, pady=2, anchor="w")

            # Vincular evento de clic pasando el índice original 'i'
            binding_action = lambda event, idx=i: self.controlador.recuperar_de_historial(idx)
            
            frame_item.bind("<Button-1>", binding_action)
            lbl_thumb.bind("<Button-1>", binding_action)
            lbl_texto.bind("<Button-1>", binding_action)
            frame_info.bind("<Button-1>", binding_action)
            lbl_p_col.bind("<Button-1>", binding_action)
            lbl_p_f1.bind("<Button-1>", binding_action)
            lbl_p_f2.bind("<Button-1>", binding_action)
            
    def _on_mousewheel(self, event):
        self.canvas_scroll.yview_scroll(int(-1 * (event.delta / 120)), "units")

    def _randomizar_campo(self, campo_entry, tipo_banco):
        # Borra el texto actual de un Entry e inserta una palabra del banco del controlador.
        seeds = self.controlador.obtener_semillas_aleatorias()
        campo_entry.delete(0, tk.END)
        campo_entry.insert(0, seeds[tipo_banco])

    def randomizar_todo(self):
        # Cambia las tres cajas de texto al mismo tiempo con una combinación nueva.
        c, f1, f2 = self.controlador.obtener_semillas_aleatorias()
        
        self.entry_color.delete(0, tk.END)
        self.entry_color.insert(0, c)
        
        self.entry_forma1.delete(0, tk.END)
        self.entry_forma1.insert(0, f1)
        
        self.entry_forma2.delete(0, tk.END)
        self.entry_forma2.insert(0, f2)