
import reflex as rx

from CharlyBI.components.header import header # Importamos el componente header
from CharlyBI.components.footer import footer # Importamos el componente footer

# Definimos la página de inicio
def salir() -> rx.Component:
    return rx.box(
        # Header
        header(),

        #Cuerpo
        rx.box(
            rx.vstack(
                rx.text(""),
                rx.text(""),
                rx.text(""),
                rx.image(
                    src="/gracias.jpg",
                    width="400px",
                    height="200px",
                ),

                # Aquí puedes agregar más contenido
                spacing="4",  # Espacio entre elementos
                align="center",  # Alinear al centro
            ),
            bg="white",  # Fondo blanco
            flex="1",  # Ocupa el espacio restante
            padding="2em",  # Espaciado interno
        ),        

        #Footer
        footer(),

        # Estilos generales
        display="flex",
        flex_direction="column",
        min_height="100vh",  # Altura mínima de la pantalla
    )