
import reflex as rx

#Componentes y Utilidades
from CharlyBI.components.header import header # Importamos el componente header
from CharlyBI.components.footer import footer # Importamos el componente footer
from CharlyBI.generales import * # Importamos todas las funciones de generales

#Paginas
from CharlyBI.pages.cargar import cargar # Importamos pagina de upload
from CharlyBI.pages.ranven import ranven # Importamos pagina ranquin de ventas
from CharlyBI.pages.ticpro import ticpro # Importamos pagina ticket promedio
from CharlyBI.pages.upt import upt # Importamos pagina unidades por ticket
from CharlyBI.pages.salir import salir  # Importamos la pagina salir


# Definimos la página de inicio
def index() -> rx.Component:
    return rx.box(
        # Header
        header(),

        # Cuerpo
        rx.box(
            rx.center(
                rx.hstack(
                    rx.link(
                        rx.image(
                            src="/upload.png",
                            width="200px",
                            height="100px",
                            border="2px solid #e2e8f0",
                            border_radius="lg",
                            _hover={"border": "2px solid #3182ce"},
                        ),
                        href="/cargar",
                    ),
                    rx.link(
                        rx.image(
                            src="/ranven.png",
                            width="200px",
                            height="100px",
                            border="2px solid #e2e8f0",
                            border_radius="lg",
                            _hover={"border": "2px solid #3182ce"},
                        ),
                        href="/ranven",
                    ),
                    rx.link(
                        rx.image(
                            src="/ticpro.png",
                            width="200px",
                            height="100px",
                            border="2px solid #e2e8f0",
                            border_radius="lg",
                            _hover={"border": "2px solid #3182ce"},
                        ),
                        href="/ticpro",
                    ),
                    rx.link(
                        rx.image(
                            src="/upt.png",
                            width="200px",
                            height="100px",
                            border="2px solid #e2e8f0",
                            border_radius="lg",
                            _hover={"border": "2px solid #3182ce"},
                        ),
                        href="/upt",
                    ),
                    rx.link(
                        rx.image(
                            src="/exit.png",
                            width="200px",
                            height="100px",
                            border="2px solid #e2e8f0",
                            border_radius="lg",
                            _hover={"border": "2px solid #3182ce"},
                        ),
                        href="/salir",
                    ),

                    # Repite para las otras imágenes...
                    spacing="4",

                ),
            ),
            bg="white",
            flex="1",
            padding="2em",
        ),


        # Footer
        footer(),

        # Estilos generales
        display="flex",
        flex_direction="column",
        min_height="100vh",  # Altura mínima de la pantalla
    )

# Crear la aplicación y agregar la página de inicio
app = rx.App()
app.add_page(index, route="/")  # Página de inicio en la ruta raíz ("/")
app.add_page(cargar, route="/cargar")  # Página Upload
app.add_page(ranven, route="/ranven")  # Página ranquin de ventas
app.add_page(ticpro, route="/ticpro")  # Página ranquin de ventas
app.add_page(upt, route="/upt")  # Página ranquin de ventas
app.add_page(salir, route="/salir")  # Página Salir