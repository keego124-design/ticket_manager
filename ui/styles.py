"""
styles.py
---------
Configuración de estilos gráficos centralizada para Tkinter y ttk:
- Selección de tema nativo limpio (clam).
- Paleta de colores, tipografías y configuración de Treeviews.
"""

from tkinter import ttk
from config import (
    COLOR_PRIMARIO,
    COLOR_PRIMARIO_OSCURO,
    COLOR_FONDO,
    COLOR_BLANCO,
    COLOR_TEXTO,
    COLOR_BORDE,
)

# Tipografías estandarizadas
FONT_FAMILY = "Segoe UI"
FONT_TITLE = (FONT_FAMILY, 14, "bold")
FONT_SUBTITLE = (FONT_FAMILY, 11, "bold")
FONT_REGULAR = (FONT_FAMILY, 10)
FONT_BOLD = (FONT_FAMILY, 10, "bold")
FONT_SMALL = (FONT_FAMILY, 9)
FONT_KPI = (FONT_FAMILY, 20, "bold")


def configurar_estilos(root):
    """Aplica la configuración global de estilos ttk a la aplicación."""
    style = ttk.Style(root)

    # Usar tema 'clam' para mejor soporte de personalización en Windows
    temas = style.theme_names()
    if "clam" in temas:
        style.theme_use("clam")

    # 1. Configuración de Frames generales
    style.configure("TFrame", background=COLOR_FONDO)
    style.configure("White.TFrame", background=COLOR_BLANCO)
    style.configure("Card.TFrame", background=COLOR_BLANCO, relief="solid", borderwidth=1)

    # 2. Etiquetas
    style.configure("TLabel", background=COLOR_FONDO, foreground=COLOR_TEXTO, font=FONT_REGULAR)
    style.configure("White.TLabel", background=COLOR_BLANCO, foreground=COLOR_TEXTO, font=FONT_REGULAR)
    style.configure("Title.TLabel", font=FONT_TITLE, foreground=COLOR_PRIMARIO_OSCURO, background=COLOR_FONDO)
    style.configure("Subtitle.TLabel", font=FONT_SUBTITLE, foreground=COLOR_TEXTO, background=COLOR_FONDO)
    style.configure("Header.TLabel", font=(FONT_FAMILY, 12, "bold"), foreground=COLOR_BLANCO, background=COLOR_PRIMARIO)

    # 3. Botones generales ttk
    style.configure(
        "Primary.TButton",
        font=FONT_BOLD,
        background=COLOR_PRIMARIO,
        foreground=COLOR_BLANCO,
        borderwidth=0,
        padding=(12, 6)
    )
    style.map(
        "Primary.TButton",
        background=[("active", COLOR_PRIMARIO_OSCURO), ("disabled", COLOR_BORDE)]
    )

    style.configure(
        "Secondary.TButton",
        font=FONT_REGULAR,
        padding=(10, 5)
    )

    # 4. Configuración de Treeview (Tablas de datos legibles)
    style.configure(
        "Treeview",
        background=COLOR_BLANCO,
        foreground=COLOR_TEXTO,
        fieldbackground=COLOR_BLANCO,
        font=FONT_REGULAR,
        rowheight=26,
        borderwidth=1,
    )
    style.map(
        "Treeview",
        background=[("selected", COLOR_PRIMARIO)],
        foreground=[("selected", COLOR_BLANCO)]
    )

    style.configure(
        "Treeview.Heading",
        background="#E1E5EA",
        foreground=COLOR_TEXTO,
        font=FONT_BOLD,
        padding=(6, 6)
    )
    style.map(
        "Treeview.Heading",
        background=[("active", "#CFD8DC")]
    )

    # 5. LabelFrames
    style.configure("TLabelframe", background=COLOR_FONDO, borderwidth=1, relief="solid")
    style.configure("TLabelframe.Label", font=FONT_BOLD, foreground=COLOR_PRIMARIO_OSCURO, background=COLOR_FONDO)

    # 6. Notebook (Pestañas)
    style.configure("TNotebook", background=COLOR_FONDO)
    style.configure("TNotebook.Tab", font=FONT_BOLD, padding=(14, 6))
    style.map(
        "TNotebook.Tab",
        background=[("selected", COLOR_BLANCO), ("active", "#E0E0E0")],
        foreground=[("selected", COLOR_PRIMARIO), ("active", COLOR_TEXTO)]
    )
