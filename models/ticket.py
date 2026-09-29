"""
ticket.py
---------
Modelo de datos para Tickets de trabajo.
"""

from dataclasses import dataclass
from typing import Optional


@dataclass
class Ticket:
    id: Optional[int]
    proyecto_id: int
    miembro_id: int
    titulo: str
    descripcion: str
    prioridad: str  # Baja, Media, Alta, Crítica
    estado: str     # Pendiente, En Progreso, Completado, Cancelado
    fecha_creacion: str  # YYYY-MM-DD
    fecha_limite: str    # YYYY-MM-DD
    fecha_cierre: Optional[str] = None  # YYYY-MM-DD
    activo: bool = True

    # Campos derivados de consultas JOIN para visualización
    proyecto_nombre: Optional[str] = None
    miembro_nombre: Optional[str] = None

    def esta_completado(self) -> bool:
        """Determina si el ticket está marcado como Completado."""
        return self.estado.strip().lower() == "completado"

    def esta_cancelado(self) -> bool:
        """Determina si el ticket está marcado como Cancelado."""
        return self.estado.strip().lower() == "cancelado"

    def esta_abierto(self) -> bool:
        """Determina si el ticket sigue activo o pendiente de resolución."""
        return self.estado in ("Pendiente", "En Progreso")

    @classmethod
    def from_row(cls, row) -> "Ticket":
        """Convierte una fila de SQLite3 a una instancia de Ticket."""
        keys = row.keys() if hasattr(row, "keys") else []
        return cls(
            id=row["id"],
            proyecto_id=row["proyecto_id"],
            miembro_id=row["miembro_id"],
            titulo=row["titulo"],
            descripcion=row["descripcion"] or "",
            prioridad=row["prioridad"],
            estado=row["estado"],
            fecha_creacion=row["fecha_creacion"],
            fecha_limite=row["fecha_limite"],
            fecha_cierre=row["fecha_cierre"] if ("fecha_cierre" in keys and row["fecha_cierre"]) else None,
            activo=bool(row["activo"]),
            proyecto_nombre=row["proyecto"] if "proyecto" in keys else None,
            miembro_nombre=row["miembro"] if "miembro" in keys else None,
        )
