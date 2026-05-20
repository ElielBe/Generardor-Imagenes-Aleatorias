import random
from PIL import Image, ImageDraw, ImageFilter

class MotorArteGenerativo:
    @staticmethod
    def generar_lienzo(semilla_color, semilla_forma1, semilla_forma2, ancho=600, alto=600):
        rng_color = random.Random(semilla_color)
        rng_shape1 = random.Random(semilla_forma1)
        rng_shape2 = random.Random(semilla_forma2)

        imagen = Image.new("RGB", (ancho, alto), color=(12, 12, 18))
        draw = ImageDraw.Draw(imagen, "RGBA")

        # Paleta de Colores
        paleta = []
        for _ in range(10):
            paleta.append((
                rng_color.randint(80, 255),
                rng_color.randint(80, 255),
                rng_color.randint(80, 255),
                rng_color.randint(40, 80)
            ))

        # Densidad y comportamiento
        num_trazos = rng_shape1.randint(100, 350)
        largo_trazo = rng_shape2.randint(50, 200)

        # Renderizado no estructurado
        for _ in range(num_trazos):
            x = rng_shape1.uniform(0, ancho)
            y = rng_shape1.uniform(0, alto)
            color = rng_color.choice(paleta)
            grosor = rng_shape2.randint(1, 3)

            puntos = [(x, y)]
            for _ in range(largo_trazo):
                x += rng_shape2.uniform(-7, 7)
                y += rng_shape2.uniform(-7, 7)
                puntos.append((x, y))

            if len(puntos) > 1:
                draw.line(puntos, fill=color, width=grosor, joint="curve")

        return imagen.filter(ImageFilter.SMOOTH_MORE)