"""
auth_service.py
---------------
Servicio de autenticación y autorización del sistema:
- Verificación segura de credenciales con hash SHA-256.
- Control de sesión de usuario y verificación de roles (admin / operator).
- Protección contra inicio de sesión con cuentas inactivas.
"""

from typing import Optional, Tuple
from database import hash_password
from models.usuario import Usuario
from repositories.usuario_repository import UsuarioRepository
from config import ROLE_ADMIN


class AuthService:
    _instancia: Optional["AuthService"] = None

    def __init__(self, usuario_repo: Optional[UsuarioRepository] = None):
        self.usuario_repo = usuario_repo or UsuarioRepository()
        self.usuario_actual: Optional[Usuario] = None

    @classmethod
    def get_instance(cls) -> "AuthService":
        """Patrón Singleton para mantener el estado de sesión global."""
        if cls._instancia is None:
            cls._instancia = cls()
        return cls._instancia

    def login(self, username: str, password: str) -> Tuple[bool, str, Optional[Usuario]]:
        """
        Autentica un usuario verificando que el hash de la contraseña coincida.
        Retorna (exito, mensaje_error, usuario).
        """
        username = username.strip()
        if not username:
            return False, "El nombre de usuario es obligatorio.", None

        if not password:
            return False, "La contraseña no puede estar vacía.", None

        usuario = self.usuario_repo.get_by_username(username)
        if not usuario:
            return False, "Credenciales incorrectas. Verifique usuario y contraseña.", None

        if not usuario.active:
            return False, "Esta cuenta de usuario ha sido desactivada por un administrador.", None

        # Comparación segura de hash SHA-256
        hash_ingresado = hash_password(password)
        if hash_ingresado != usuario.password_hash:
            return False, "Credenciales incorrectas. Verifique usuario y contraseña.", None

        self.usuario_actual = usuario
        return True, "Inicio de sesión exitoso.", usuario

    def logout(self):
        """Cierra la sesión del usuario actual."""
        self.usuario_actual = None

    def get_current_user(self) -> Optional[Usuario]:
        """Obtiene el usuario en sesión actual."""
        return self.usuario_actual

    def is_authenticated(self) -> bool:
        """Determina si hay una sesión activa."""
        return self.usuario_actual is not None

    def is_admin(self) -> bool:
        """Verifica si el usuario en sesión tiene rol de administrador."""
        return self.usuario_actual is not None and self.usuario_actual.role == ROLE_ADMIN
