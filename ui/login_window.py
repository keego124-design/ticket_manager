"""
login_window.py
---------------
Pantalla de inicio de sesión con validación de credenciales:
- Campos de usuario y contraseña (enmascarada con '*').
- Mensajes de error amigables.
- Acceso por roles (admin y operator).
"""

import tkinter as tk
from tkinter import ttk, messagebox
from typing import Callable, Optional
from services.auth_service import AuthService
from models.usuario import Usuario
from config import COLOR_PRIMARIO, COLOR_FONDO, COLOR_BLANCO, COLOR_TEXTO, COLOR_TEXTO_SECUNDARIO
from ui.styles import FONT_FAMILY, FONT_TITLE, FONT_REGULAR, FONT_BOLD, FONT_SMALL


class LoginWindow(tk.Tk):
    def __init__(self, on_login_success: Callable[[Usuario], None]):
        super().__init__()
        self.on_login_success = on_login_success
        self.auth_service = AuthService.get_instance()

        self.title("Inicio de Sesión - Ticket Management System")
        self.geometry("440x480")
        self.resizable(False, False)
        self.configure(bg=COLOR_FONDO)

        # Centrar ventana en la pantalla
        self._centrar_ventana()
        self._construir_interfaz()

    def _centrar_ventana(self):
        self.update_idletasks()
        ancho = 440
        alto = 480
        x = (self.winfo_screenwidth() // 2) - (ancho // 2)
        y = (self.winfo_screenheight() // 2) - (alto // 2)
        self.geometry(f"{ancho}x{alto}+{x}+{y}")

    def _construir_interfaz(self):
        # 1. Cabecera visual
        frame_cabecera = tk.Frame(self, bg=COLOR_PRIMARIO, height=90)
        frame_cabecera.pack(fill="x")

        lbl_icono = tk.Label(
            frame_cabecera,
            text="🎫",
            font=(FONT_FAMILY, 24),
            bg=COLOR_PRIMARIO,
            fg=COLOR_BLANCO
        )
        lbl_icono.pack(pady=(10, 0))

        lbl_titulo = tk.Label(
            frame_cabecera,
            text="Ticket Management System",
            font=FONT_TITLE,
            bg=COLOR_PRIMARIO,
            fg=COLOR_BLANCO
        )
        lbl_titulo.pack(pady=(2, 10))

        # 2. Tarjeta central de inicio de sesión
        card = tk.Frame(self, bg=COLOR_BLANCO, bd=1, relief="solid", padx=25, pady=20)
        card.pack(padx=30, pady=20, fill="both", expand=True)

        tk.Label(
            card,
            text="Ingresa tus credenciales",
            font=FONT_BOLD,
            bg=COLOR_BLANCO,
            fg=COLOR_TEXTO
        ).pack(anchor="w", pady=(0, 15))

        # Campo Usuario
        tk.Label(card, text="Nombre de Usuario:", font=FONT_REGULAR, bg=COLOR_BLANCO, fg=COLOR_TEXTO).pack(anchor="w")
        self.entry_username = ttk.Entry(card, font=FONT_REGULAR)
        self.entry_username.pack(fill="x", pady=(4, 12))
        self.entry_username.focus()

        # Campo Contraseña
        tk.Label(card, text="Contraseña:", font=FONT_REGULAR, bg=COLOR_BLANCO, fg=COLOR_TEXTO).pack(anchor="w")
        self.entry_password = ttk.Entry(card, font=FONT_REGULAR, show="*")
        self.entry_password.pack(fill="x", pady=(4, 15))
        self.entry_password.bind("<Return>", lambda e: self._ejecutar_login())

        # Mensaje de error dinámico
        self.lbl_error = tk.Label(card, text="", font=FONT_SMALL, fg="#c62828", bg=COLOR_BLANCO, wraplength=320)
        self.lbl_error.pack(fill="x", pady=(0, 10))

        # Botón Iniciar Sesión
        btn_login = tk.Button(
            card,
            text="Iniciar Sesión",
            font=FONT_BOLD,
            bg=COLOR_PRIMARIO,
            fg=COLOR_BLANCO,
            activebackground="#0D47A1",
            activeforeground=COLOR_BLANCO,
            relief="flat",
            cursor="hand2",
            pady=8,
            command=self._ejecutar_login
        )
        btn_login.pack(fill="x", pady=(5, 10))

        # 3. Nota de credenciales de prueba para evaluador / profesor
        frame_demo = tk.LabelFrame(
            card,
            text=" Credenciales de Prueba ",
            font=FONT_SMALL,
            bg=COLOR_BLANCO,
            fg=COLOR_TEXTO_SECUNDARIO,
            padx=10,
            pady=5
        )
        frame_demo.pack(fill="x", pady=(10, 0))

        tk.Label(
            frame_demo,
            text="• Admin: admin / admin123\n• Operador: operador / operador123",
            font=FONT_SMALL,
            justify="left",
            bg=COLOR_BLANCO,
            fg=COLOR_TEXTO_SECUNDARIO
        ).pack(anchor="w")

    def _ejecutar_login(self):
        usuario_txt = self.entry_username.get().strip()
        pass_txt = self.entry_password.get()

        self.lbl_error.config(text="")

        if not usuario_txt:
            self.lbl_error.config(text="Por favor ingresa tu nombre de usuario.")
            self.entry_username.focus()
            return

        if not pass_txt:
            self.lbl_error.config(text="Por favor ingresa tu contraseña.")
            self.entry_password.focus()
            return

        exito, mensaje, usuario = self.auth_service.login(usuario_txt, pass_txt)

        if exito and usuario:
            self.destroy()
            self.on_login_success(usuario)
        else:
            self.lbl_error.config(text=mensaje)
            self.entry_password.delete(0, tk.END)
            self.entry_password.focus()
