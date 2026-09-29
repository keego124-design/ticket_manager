"""
miembro.py
----------
Modelo de datos para Miembros del Equipo.
"""

from dataclasses import dataclass
from typing import Optional


@dataclass
class Miembro:
    id: Optional[int]
    nombre: str
    correo: str
    telefono: str
    activo: bool = True

    @classmethod
    def from_row(cls, row) -> "Miembro":
        """Convierte una fila de SQLite3 a una instancia de Miembro."""
        return cls(
            id=row["id"],
            nombre=row["nombre"],
            correo=row["correo"],
            telefono=row["telefono"] or "",
            activo=bool(row["activo"]),
        )
