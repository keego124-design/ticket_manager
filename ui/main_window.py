"""
main_window.py
--------------
Ventana principal de la aplicación:
- Barra lateral de navegación (Sidebar) con accesos directos a Dashboard, Proyectos, Miembros, Tickets y Reportes.
- Barra superior con información del usuario autenticado y su rol (admin/operator).
- Contenedor dinámico para alternar entre vistas sin recrear la ventana.
- Soporte para redimensionamiento fluido y cierre seguro de sesión.
"""

import tkinter as tk
from tkinter import ttk, messagebox
from typing import Callable
from models.usuario import Usuario
from services.auth_service import AuthService
from ui.dashboard_view import DashboardView
from ui.proyecto_view import ProyectoView
from ui.miembro_view import MiembroView
from ui.ticket_view import TicketView
from ui.report_view import ReportView
from ui.styles import configurar_estilos, FONT_FAMILY, FONT_TITLE, FONT_BOLD, FONT_REGULAR, FONT_SMALL
from config import (
    COLOR_PRIMARIO,
    COLOR_PRIMARIO_OSCURO,
    COLOR_SECUNDARIO,
    COLOR_SECUNDARIO_HOVER,
    COLOR_FONDO,
    COLOR_BLANCO,
    COLOR_TEXTO,
    COLOR_BORDE,
)


class MainWindow(tk.Tk):
    def __init__(self, usuario: Usuario, on_logout: Callable[[], None]):
        super().__init__()
        self.usuario = usuario
        self.on_logout = on_logout
        self.auth_service = AuthService.get_instance()

        self.title("Ticket Management System - Tópicos Avanzados de Programación")
        self.geometry("1100x700")
        self.minsize(950, 600)
        self.configure(bg=COLOR_FONDO)

        # Aplicar estilos gráficos centralizados
        configurar_estilos(self)

        self._centrar_ventana()
        self._construir_estructura()

        # Abrir el Dashboard por defecto
        self.cambiar_vista("dashboard")

    def _centrar_ventana(self):
        self.update_idletasks()
        ancho = 1100
        alto = 700
        x = (self.winfo_screenwidth() // 2) - (ancho // 2)
        y = (self.winfo_screenheight() // 2) - (alto // 2)
        self.geometry(f"{ancho}x{alto}+{x}+{y}")

    def _construir_estructura(self):
        # 1. Barra de Encabezado Superior (Header)
        self.frame_header = tk.Frame(self, bg=COLOR_PRIMARIO, height=50)
        self.frame_header.pack(side="top", fill="x")

        lbl_logo = tk.Label(
            self.frame_header,
            text=" 🎫 Ticket Management System",
            font=FONT_TITLE,
            bg=COLOR_PRIMARIO,
            fg=COLOR_BLANCO
        )
        lbl_logo.pack(side="left", padx=15, pady=8)

        # Información del usuario en sesión
        f_user_info = tk.Frame(self.frame_header, bg=COLOR_PRIMARIO)
        f_user_info.pack(side="right", padx=15)

        rol_badge = "ADMINISTRADOR" if self.usuario.es_admin() else "OPERADOR"
        lbl_user = tk.Label(
            f_user_info,
            text=f"Conectado: {self.usuario.username}  |  Rol: [{rol_badge}]",
            font=FONT_BOLD,
            bg=COLOR_PRIMARIO,
            fg="#E3F2FD"
        )
        lbl_user.pack(side="left", padx=10)

        # 2. Contenedor Principal (Sidebar + Vista Activa)
        self.frame_cuerpo = tk.Frame(self, bg=COLOR_FONDO)
        self.frame_cuerpo.pack(fill="both", expand=True)

        # Barra lateral izquierda (Sidebar)
        self.frame_sidebar = tk.Frame(self.frame_cuerpo, bg=COLOR_SECUNDARIO, width=220)
        self.frame_sidebar.pack(side="left", fill="y")
        self.frame_sidebar.pack_propagate(False)

        # Contenedor de la vista dinámica
        self.frame_contenido = tk.Frame(self.frame_cuerpo, bg=COLOR_FONDO)
        self.frame_contenido.pack(side="right", fill="both", expand=True)

        self._construir_sidebar()

        # Diccionario para almacenar las instancias de vistas
        self.vistas = {}

    def _construir_sidebar(self):
        tk.Label(
            self.frame_sidebar,
            text="MENÚ PRINCIPAL",
            font=(FONT_FAMILY, 9, "bold"),
            bg=COLOR_SECUNDARIO,
            fg="#90A4AE",
            pady=15
        ).pack(anchor="w", padx=20)

        self.botones_menu = {}
        items_menu = [
            ("dashboard", "📊  Dashboard"),
            ("proyectos", "📁  Proyectos"),
            ("miembros",  "👥  Equipo de Trabajo"),
            ("tickets",   "🎫  Tickets (SQL JOIN)"),
            ("reportes",  "📈  Reportes y Gráficos"),
        ]

        for clave, texto in items_menu:
            btn = tk.Button(
                self.frame_sidebar,
                text=texto,
                font=FONT_BOLD,
                bg=COLOR_SECUNDARIO,
                fg=COLOR_BLANCO,
                activebackground=COLOR_SECUNDARIO_HOVER,
                activeforeground=COLOR_BLANCO,
                bd=0,
                anchor="w",
                padx=20,
                pady=10,
                cursor="hand2",
                command=lambda c=clave: self.cambiar_vista(c)
            )
            btn.pack(fill="x", pady=1)
            self.botones_menu[clave] = btn

        # Espaciador inferior para empujar el botón de Logout hacia abajo
        tk.Frame(self.frame_sidebar, bg=COLOR_SECUNDARIO).pack(fill="both", expand=True)

        # Botón de Cerrar Sesión
        btn_logout = tk.Button(
            self.frame_sidebar,
            text="🚪  Cerrar Sesión",
            font=FONT_BOLD,
            bg="#263238",
            fg="#FF8A80",
            activebackground="#37474F",
            activeforeground="#FF8A80",
            bd=0,
            anchor="w",
            padx=20,
            pady=12,
            cursor="hand2",
            command=self._cerrar_sesion
        )
        btn_logout.pack(side="bottom", fill="x")

    def cambiar_vista(self, nombre_vista: str):
        """Alterna el contenido principal hacia la vista seleccionada."""
        # Resaltar el botón activo en la barra lateral
        for clave, btn in self.botones_menu.items():
            if clave == nombre_vista:
                btn.config(bg=COLOR_PRIMARIO, fg=COLOR_BLANCO)
            else:
                btn.config(bg=COLOR_SECUNDARIO, fg=COLOR_BLANCO)

        # Ocultar vista actual si existe
        for v in self.vistas.values():
            v.pack_forget()

        # Crear o mostrar la vista solicitada
        if nombre_vista not in self.vistas:
            if nombre_vista == "dashboard":
                self.vistas["dashboard"] = DashboardView(self.frame_contenido, on_navigate=self.cambiar_vista)
            elif nombre_vista == "proyectos":
                self.vistas["proyectos"] = ProyectoView(self.frame_contenido)
            elif nombre_vista == "miembros":
                self.vistas["miembros"] = MiembroView(self.frame_contenido)
            elif nombre_vista == "tickets":
                self.vistas["tickets"] = TicketView(self.frame_contenido)
            elif nombre_vista == "reportes":
                self.vistas["reportes"] = ReportView(self.frame_contenido)

        vista_activa = self.vistas[nombre_vista]
        vista_activa.pack(fill="both", expand=True)

        # Refrescar datos al navegar hacia la vista
        if hasattr(vista_activa, "cargar_datos"):
            vista_activa.cargar_datos()
        elif hasattr(vista_activa, "actualizar_todos_los_reportes"):
            vista_activa.actualizar_todos_los_reportes()

    def _cerrar_sesion(self):
        confirmar = messagebox.askyesno(
            "Cerrar Sesión",
            "¿Estás seguro de que deseas cerrar la sesión actual?",
            icon="question"
        )
        if confirmar:
            self.auth_service.logout()
            self.destroy()
            self.on_logout()
