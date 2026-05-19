import os

class ControladorArte:
    def __init__(self, vista, modelo_clase):
        self.vista = vista
        self.modelo = modelo_clase()
        # Lista de listas o tuplas mutables: [nombre, img_pil, s_color, s_f1, s_f2, id_unico]
        self.historial_imagenes = []  
        self.output_dir = "galeria_arte"
        os.makedirs(self.output_dir, exist_ok=True)

    def procesar_peticion_arte(self, s_color, s_forma1, s_forma2):
        s_color = s_color.strip() or "Anonimo"
        s_forma1 = s_forma1.strip() or "Anonimo"
        s_forma2 = s_forma2.strip() or "Anonimo"

        # Identificador único para comparar
        id_combinacion = f"{s_color}_{s_forma1}_{s_forma2}".lower().replace(" ", "_")

        # Buscar si la combinación ya existe en el historial
        indice_existente = -1
        for i, elemento in enumerate(self.historial_imagenes):
            if elemento[5] == id_combinacion:
                indice_existente = i
                break

        if indice_existente != -1:
            # Extraer el elemento de su posición antigua
            elemento_repetido = self.historial_imagenes.pop(indice_existente)
            
            # Moverlo al final de la lista de forma limpia
            self.historial_imagenes.append(elemento_repetido)
            
            # Forzar a la vista a renderizar los cambios inmediatamente
            self.vista.mostrar_imagen_principal(elemento_repetido[1])
            self.vista.actualizar_panel_historial(self.historial_imagenes)
            return False

        # Solicitar nueva generación al modelo
        img_generada = self.modelo.generar_lienzo(s_color, s_forma1, s_forma2)

        # Guardar en disco
        nombre_archivo = f"{s_color}_{s_forma1}_{s_forma2}".replace(" ", "_") + ".png"
        ruta_completa = os.path.join(self.output_dir, nombre_archivo)
        img_generada.save(ruta_completa)

        # Registrar al final
        self.historial_imagenes.append([nombre_archivo, img_generada, s_color, s_forma1, s_forma2, id_combinacion])

        # Actualizar vista
        self.vista.mostrar_imagen_principal(img_generada)
        self.vista.actualizar_panel_historial(self.historial_imagenes)
        return True

    def recuperar_de_historial(self, index):
        if 0 <= index < len(self.historial_imagenes):
            elemento = self.historial_imagenes[index]
            self.vista.mostrar_imagen_principal(elemento[1])