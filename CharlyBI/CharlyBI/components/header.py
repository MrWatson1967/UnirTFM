import reflex as rx

def header() -> rx.Component:
    return rx.box(
        rx.hstack(
            rx.image(src="/logo.png", width="80px", height="50px"),  # Logo
                rx.heading("CharlyBi - Productividad Fuerza de Ventas ", size="4", color="white"),  # Nombre de la aplicación
            spacing="3",  # Espacio entre el logo y el texto
            align="center",  # Alinear verticalmente al centro
        ),
        bg="black",  # Fondo negro
        padding="1em",  # Espaciado interno
        width="100%",  # Ancho completo
    )