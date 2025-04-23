import reflex as rx
import pandas as pd

#Componentes y Utilidades
from CharlyBI.components.header import header # Importamos el componente header
from CharlyBI.components.footer import footer # Importamos el componente footer
from CharlyBI.generales import * # Importamos todas las funciones de generales

#Paginas
from CharlyBI.pages.salir import salir  # Importamos la pagina salir

class CargarEstado(rx.State):
    mensaje: str = ""  # Mensaje de éxito o error
    cadena: str = "" # para armar el insert

    @rx.event
    async def manejar_archivo(self, strArchivo: list[rx.UploadFile]):
        """
        Maneja el archivo seleccionado por el usuario.
        """
        try:
            archivo = strArchivo[0]
            contenido = await archivo.read()  # Leer el contenido del archivo

            # Guardar el archivo temporalmente
            with open(archivo.filename, "wb") as f:
                f.write(contenido)

        except Exception as e:
            self.mensaje = f"Error al manejar el archivo: {e}"


        """
        Lee el archivo CSV y lo sube a SQL Server.
        """
        try:
            # Conectar a SQL Server
            conexion = conectar_sql_server()
            if not conexion:
                self.mensaje = "Error al conectar a SQL Server."
                return

            # Leer el archivo CSV
            df = pd.read_csv(archivo.filename, sep=",", low_memory=False)
            df = df.astype("string")
            df = df.fillna("")            

            # lista con los valores del df
            lista_valores = df.values.tolist()

            if archivo.filename == "./cnArticulos.csv":
                self.cadena = "INSERT INTO dimArticulos VALUES(?,?)"
            elif archivo.filename == "./cnBodegas.csv":
                self.cadena = "INSERT INTO dimBodegas VALUES(?,?)"
            elif archivo.filename == "./cnCategorias.csv":
                self.cadena = "INSERT INTO dimCategorias VALUES(?,?)"
            elif archivo.filename == "./cnSubcategorias.csv":
                self.cadena = "INSERT INTO dimSubcategorias VALUES(?,?)"
            elif archivo.filename == "./cnVendedores.csv":
                self.cadena = "INSERT INTO dimVendedores VALUES(?,?)"
            elif archivo.filename == "./cnVentas.csv":
                self.cadena = "INSERT INTO facVentas VALUES(?,?,?,?,?,?,?,?,?,?,?)"
            else:
                self.mensaje = "Por favor seleccione un archivo válido"

            # Insertar los datos en la tabla
            cursor = conexion.cursor()
            cursor.executemany(self.cadena, lista_valores)
            conexion.commit()
            cursor.close()
            conexion.close()

            self.mensaje = "Archivo cargado exitosamente."
        except Exception as e:
            self.mensaje = f"Error al cargar el archivo: {e}"




def cargar() -> rx.Component:
    return rx.box(
        # Header
        header(),

        # Cuerpo (Formulario de carga)
        rx.box(
            rx.vstack(
                rx.text(""),
                rx.text("Seleccione el archivo que desea cargar:"),
                
                rx.upload(
                    rx.button("Seleccionar archivo",
                              color="white",
                              bg="black",
                              ),  # Botón para seleccionar archivo
                    border="1px solid #e2e8f0",
                    padding="1em",
                    border_radius="lg",
                    id="upCargar",
                    max_files=1,
                ),  

                rx.text(""),
                rx.text(f"Selección: {rx.selected_files("upCargar")}"),

                rx.hstack(
                    rx.button(" Cargar ", 
                              color_scheme="blue",
                              on_click=CargarEstado.manejar_archivo(
                                  rx.upload_files(upload_id="upCargar")
                              ),
                              ),  # Botón Aceptar
                    rx.link(
                        rx.button("Cancelar", color_scheme="red"),  # Botón Cancelar
                        on_click = rx.clear_selected_files("upCargar"),
                        href="/",  # Redirigir a la página de inicio
                    ),
                    spacing="4",  # Espacio entre los botones
                ),
                rx.text(CargarEstado.mensaje),  # Mostrar mensaje de éxito o error
                spacing="4",  # Espacio entre elementos
                align="center",  # Alinear al centro
            ),
            bg="white",  # Fondo blanco
            flex="1",  # Ocupa el espacio restante
            padding="2em",  # Espaciado interno
        ),

        # Footer
        footer(),

        # Estilos generales
        display="flex",
        flex_direction="column",
        min_height="100vh",
    )