import reflex as rx

def footer() -> rx.Component:
    return rx.box(
        rx.center(
            rx.text("© 2025 CharlyBi. Todos los derechos reservados.     Versión 1.0.0", color="white"),
        ),
        bg="black",  # Fondo negro
        padding="1em",  # Espaciado interno
        width="100%",  # Ancho completo
        margin_top = "auto",
    ),
