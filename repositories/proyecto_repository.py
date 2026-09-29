"""
proyecto_repository.py
----------------------
Repositorio para la entidad Proyecto.
Incluye operaciones CRUD, búsquedas dinámicas, filtros y conteo de tickets asociados.
"""

from typing import Optional, List
from database import get_connection
from models.proyecto import Proyecto


class ProyectoRepository:
    def get_by_id(self, proyecto_id: int) -> Optional[Proyecto]:
        """Recupera un proyecto por su ID."""
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("""
            SELECT id, nombre, descripcion, fecha_inicio, fecha_fin, estado, activo
            FROM proyectos
            WHERE id = ?;
        """, (proyecto_id,))
        row = cursor.fetchone()
        conn.close()
        return Proyecto.from_row(row) if row else None

    def list_all(self, solo_activos: bool = False) -> List[Proyecto]:
        """Lista proyectos, opcionalmente filtrando solo los activos."""
        conn = get_connection()
        cursor = conn.cursor()
        if solo_activos:
            cursor.execute("""
                SELECT id, nombre, descripcion, fecha_inicio, fecha_fin, estado, activo
                FROM proyectos
                WHERE activo = 1
                ORDER BY id DESC;
            """)
        else:
            cursor.execute("""
                SELECT id, nombre, descripcion, fecha_inicio, fecha_fin, estado, activo
                FROM proyectos
                ORDER BY id DESC;
            """)
        rows = cursor.fetchall()
        conn.close()
        return [Proyecto.from_row(r) for r in rows]

    def search_and_filter(self, query: str = "", estado: str = "", activo_filtro: Optional[bool] = None) -> List[Proyecto]:
        """Busca proyectos por coincidencia de nombre/descripción y aplica filtros combinados."""
        conn = get_connection()
        cursor = conn.cursor()

        sql = """
            SELECT id, nombre, descripcion, fecha_inicio, fecha_fin, estado, activo
            FROM proyectos
            WHERE 1=1
        """
        params = []

        if query:
            sql += " AND (nombre LIKE ? OR descripcion LIKE ?)"
            params.extend([f"%{query}%", f"%{query}%"])

        if estado and estado != "Todos":
            sql += " AND estado = ?"
            params.append(estado)

        if activo_filtro is not None:
            sql += " AND activo = ?"
            params.append(1 if activo_filtro else 0)

        sql += " ORDER BY id DESC;"

        cursor.execute(sql, params)
        rows = cursor.fetchall()
        conn.close()
        return [Proyecto.from_row(r) for r in rows]

    def create(self, proyecto: Proyecto) -> int:
        """Inserta un nuevo proyecto en la base de datos."""
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO proyectos (nombre, descripcion, fecha_inicio, fecha_fin, estado, activo)
            VALUES (?, ?, ?, ?, ?, ?);
        """, (
            proyecto.nombre.strip(),
            proyecto.descripcion.strip(),
            proyecto.fecha_inicio,
            proyecto.fecha_fin,
            proyecto.estado,
            int(proyecto.activo)
        ))
        new_id = cursor.lastrowid
        conn.commit()
        conn.close()
        return new_id

    def update(self, proyecto: Proyecto) -> bool:
        """Actualiza la información de un proyecto existente."""
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("""
            UPDATE proyectos
            SET nombre = ?, descripcion = ?, fecha_inicio = ?, fecha_fin = ?, estado = ?, activo = ?
            WHERE id = ?;
        """, (
            proyecto.nombre.strip(),
            proyecto.descripcion.strip(),
            proyecto.fecha_inicio,
            proyecto.fecha_fin,
            proyecto.estado,
            int(proyecto.activo),
            proyecto.id
        ))
        rows_affected = cursor.rowcount
        conn.commit()
        conn.close()
        return rows_affected > 0

    def deactivate(self, proyecto_id: int) -> bool:
        """Desactiva lógicamente un proyecto (activo = 0)."""
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("UPDATE proyectos SET activo = 0 WHERE id = ?;", (proyecto_id,))
        rows_affected = cursor.rowcount
        conn.commit()
        conn.close()
        return rows_affected > 0

    def delete(self, proyecto_id: int) -> bool:
        """Elimina físicamente un proyecto de la base de datos."""
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("DELETE FROM proyectos WHERE id = ?;", (proyecto_id,))
        rows_affected = cursor.rowcount
        conn.commit()
        conn.close()
        return rows_affected > 0

    def count_open_tickets(self, proyecto_id: int) -> int:
        """Retorna el número de tickets activos no cerrados en el proyecto (Pendiente o En Progreso)."""
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("""
            SELECT COUNT(*) AS total
            FROM tickets
            WHERE proyecto_id = ? AND activo = 1 AND estado IN ('Pendiente', 'En Progreso');
        """, (proyecto_id,))
        total = cursor.fetchone()["total"]
        conn.close()
        return total
