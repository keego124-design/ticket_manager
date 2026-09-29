"""
usuario.py
----------
Modelo de datos para Usuarios del Sistema.
"""

from dataclasses import dataclass
from typing import Optional


@dataclass
class Usuario:
    id: Optional[int]
    username: str
    password_hash: str
    role: str  # 'admin' o 'operator'
    active: bool = True

    def es_admin(self) -> bool:
        """Determina si el usuario cuenta con privilegios administrativos."""
        return self.role == "admin"

    @classmethod
    def from_row(cls, row) -> "Usuario":
        """Convierte una fila de SQLite3 (sqlite3.Row) a una instancia de Usuario."""
        return cls(
            id=row["id"],
            username=row["username"],
            password_hash=row["password_hash"],
            role=row["role"],
            active=bool(row["active"]),
        )
