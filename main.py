"""
main.py
-------
Punto de entrada principal para el 'Ticket Management System'.
- Inicializa la base de datos SQLite y carga datos de prueba automáticos si está vacía.
- Presenta la pantalla de autenticación (LoginWindow).
- Conduce a la ventana principal (MainWindow) al validar credenciales y maneja cierres de sesión.
"""

import sys
import tkinter as tk
from database import init_database
from models.usuario import Usuario
from ui.login_window import LoginWindow
from ui.main_window import MainWindow


class AppCoordinator:
    """Coordinador del ciclo de vida de la aplicación."""
    def __init__(self):
        # 1. Asegurar la creación de base de datos y datos semilla
        try:
            init_database()
        except Exception as e:
            print(f"[!] Error crítico al inicializar la base de datos: {e}")
            sys.exit(1)

        self.login_window: LoginWindow = None
        self.main_window: MainWindow = None

    def start(self):
        """Inicia el flujo de la aplicación mostrando el Login."""
        self._mostrar_login()

    def _mostrar_login(self):
        self.login_window = LoginWindow(on_login_success=self._on_login_success)
        self.login_window.mainloop()

    def _on_login_success(self, usuario: Usuario):
        """Callback ejecutado cuando el usuario ingresa credenciales válidas."""
        self.main_window = MainWindow(usuario=usuario, on_logout=self._on_logout)
        self.main_window.mainloop()

    def _on_logout(self):
        """Callback ejecutado al presionar 'Cerrar Sesión' en la ventana principal."""
        self._mostrar_login()


def main():
    app = AppCoordinator()
    app.start()


if __name__ == "__main__":
    main()
