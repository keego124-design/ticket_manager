"""
proyecto.py
-----------
Modelo de datos para Proyectos.
"""

from dataclasses import dataclass
from typing import Optional


@dataclass
class Proyecto:
    id: Optional[int]
    nombre: str
    descripcion: str
    fecha_inicio: str  # Formato YYYY-MM-DD
    fecha_fin: str     # Formato YYYY-MM-DD
    estado: str        # Planificación, En Progreso, Completado, Cerrado
    activo: bool = True

    def esta_cerrado(self) -> bool:
        """Determina si el proyecto se encuentra en estado Cerrado."""
        return self.estado.strip().lower() == "cerrado"

    @classmethod
    def from_row(cls, row) -> "Proyecto":
        """Convierte una fila de SQLite3 a una instancia de Proyecto."""
        return cls(
            id=row["id"],
            nombre=row["nombre"],
            descripcion=row["descripcion"] or "",
            fecha_inicio=row["fecha_inicio"],
            fecha_fin=row["fecha_fin"],
            estado=row["estado"],
            activo=bool(row["activo"]),
        )
