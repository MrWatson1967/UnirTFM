import reflex as rx
import matplotlib.pyplot as plt
import seaborn as sns
import io
import base64
from PIL import Image

#Componentes y Utilidades
from CharlyBI.components.header import header # Importamos el componente header
from CharlyBI.components.footer import footer # Importamos el componente footer
from CharlyBI.generales import * # Importamos todas las funciones de generales
from datetime import datetime

#Paginas
from CharlyBI.pages.salir import salir  # Importamos la pagina salir

class TicproEstado(rx.State):
    opcion_seleccionada: str = "Puntos de Venta"  # Opción seleccionada en el combo
    fecha_inicial: str = datetime.now().strftime("%Y-%m-%d")  # Fecha inicial (hoy)
    fecha_final: str = datetime.now().strftime("%Y-%m-%d")  # Fecha final (hoy)
    datos_ventas: list[dict] = []  # Datos de ventas
    chart_url: str = ""

    @rx.event
    def cambiar_filtro(self, filtro: str):
        #Actualiza el filtro seleccionado y carga los datos correspondientes en el combo.
        self.filtro_seleccionado = filtro
        self.actualizar_combo()

    @rx.event
    def cambiar_opcion(self, opcion: str):
        #Actualiza la opción seleccionada en el combo.
        self.opcion_seleccionada = opcion

    @rx.event
    def cambiar_fecha_inicial(self, fecha: str):
        #Actualiza la fecha inicial.
        self.fecha_inicial = fecha

    @rx.event
    def cambiar_fecha_final(self, fecha: str):
        #Actualiza la fecha final.
        self.fecha_final = fecha

    @rx.event
    def generar_diagrama(self):
        import pandas as pd

        self.datos_ventas = obtener_upt(self.opcion_seleccionada, self.fecha_inicial, self.fecha_final)

        data = pd.DataFrame(self.datos_ventas)
        data = data.sort_values("UPT", ascending=False)  # orden descendente        

        # Crear el gráfico con Seaborn
        plt.figure(figsize=(6, 4))
        #sns.barplot(data=data, y="Descripcion", x="Valor", palette="Blues_d")
        #sns.barplot(data=data, y="Descripcion", x="Valor", palette="mako")
        #sns.barplot(data=data, y="Descripcion", x="Valor", palette="rocket")
        sns.barplot(data=data, x="UPT", y="Descripcion", palette="coolwarm")
        plt.title("Unidades Por Ticket (UPT)")

        # Guardar en memoria
        buf = io.BytesIO()
        plt.savefig(buf, format="png", bbox_inches="tight")
        plt.close()
        buf.seek(0)
        img = Image.open(buf)
        buffered = io.BytesIO()
        img.save(buffered, format="PNG")
        img_str = base64.b64encode(buffered.getvalue()).decode()

        # Actualizar estado
        self.chart_url = f"data:image/png;base64,{img_str}"


def upt() -> rx.Component:
    return rx.box(
        # Header
        header(),

        # Cuerpo 
        rx.hstack(

            #Sección controles a la derecha
            rx.box(
                rx.vstack(
                    
                    # Combo para seleccionar "Puntos de Venta" o "Vendedores"
                    rx.hstack(
                        rx.text("Contenido del eje Y: ", width="200px"),
                        rx.select(
                            ["Puntos de Venta", "Vendedores"],  # Opciones del combo
                            placeholder="Seleccione una opción",  # Texto de placeholder
                            default_value="Puntos de Venta",  # Valor por defecto
                            on_change=TicproEstado.cambiar_opcion,  # Manejar cambio de opción
                            width="50%",  # Ancho
                        ),
                        spacing="2",  # Espacio entre el texto y el combo
                    ),

                    # Selector de fecha inicial
                    rx.hstack(
                        rx.text("Fecha Inicial: ", width="200px"),
                        rx.input(
                            type="date",
                            value=TicproEstado.fecha_inicial,  # Valor inicial
                            on_change=TicproEstado.cambiar_fecha_inicial,  # Manejar cambio de fecha
                            width="58%",  # Ancho
                        ),
                        spacing="2",  # Espacio entre el texto y el combo
                    ),

                    # Selector de fecha final
                    rx.hstack(
                        rx.text("Fecha Final: ", width="200px"),
                        rx.input(
                            type="date",
                            value=TicproEstado.fecha_final,  # Valor inicial
                            on_change=TicproEstado.cambiar_fecha_final,  # Manejar cambio de fecha
                            width="58%",  # Ancho
                        ),
                        spacing="2",  # Espacio entre el texto y el combo
                    ),

                    # Botón para generar el diagrama
                    rx.button(
                        "Generar Diagrama",
                        color_scheme="blue",
                        on_click=TicproEstado.generar_diagrama
                    ),
                    spacing="4",  # Espacio entre elementos
                    align="center",  # Alinear al centro
                ),
                bg="white",  # Fondo blanco
                padding="1em",  # Espaciado interno
                border="10px solid #e2e8f0",  # Borde
                border_radius="lg",  # Bordes redondeados
                box_shadow="lg",  # Sombra para resaltar la caja
                width="50%",  # Ancho de la caja de controles                
            ),

            # Sección de gráfica (derecha)
            rx.box(
                rx.cond(
                    TicproEstado.chart_url != "",
                    rx.image(src=TicproEstado.chart_url, width="100%"),
                    rx.text("Haz clic en el botón para generar el gráfico.")
                ),
                width="50%",
                bg="gray.100",
                padding="2em"
            ),
            spacing="4",
            align="start",
            padding="2em"
        ),

        # Footer
        footer(),

        # Estilos generales
        display="flex",
        flex_direction="column",
        min_height="100vh",  # Altura mínima de la pantalla        

    )
