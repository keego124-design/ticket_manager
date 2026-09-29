"""
miembro_repository.py
---------------------
Repositorio para la entidad Miembro del Equipo.
Permite gestionar altas, modificaciones, bajas lógicas y validaciones de unicidad.
"""

from typing import Optional, List
from database import get_connection
from models.miembro import Miembro


class MiembroRepository:
    def get_by_id(self, miembro_id: int) -> Optional[Miembro]:
        """Obtiene un miembro por su identificador primario."""
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("""
            SELECT id, nombre, correo, telefono, activo
            FROM miembros
            WHERE id = ?;
        """, (miembro_id,))
        row = cursor.fetchone()
        conn.close()
        return Miembro.from_row(row) if row else None

    def get_by_email(self, correo: str, exclude_id: Optional[int] = None) -> Optional[Miembro]:
        """Busca un miembro por correo electrónico, útil para evitar duplicados."""
        conn = get_connection()
        cursor = conn.cursor()
        if exclude_id:
            cursor.execute("""
                SELECT id, nombre, correo, telefono, activo
                FROM miembros
                WHERE LOWER(correo) = LOWER(?) AND id != ?;
            """, (correo.strip(), exclude_id))
        else:
            cursor.execute("""
                SELECT id, nombre, correo, telefono, activo
                FROM miembros
                WHERE LOWER(correo) = LOWER(?);
            """, (correo.strip(),))
        row = cursor.fetchone()
        conn.close()
        return Miembro.from_row(row) if row else None

    def list_all(self, solo_activos: bool = False) -> List[Miembro]:
        """Lista miembros registrados, opcionalmente solo aquellos activos."""
        conn = get_connection()
        cursor = conn.cursor()
        if solo_activos:
            cursor.execute("""
                SELECT id, nombre, correo, telefono, activo
                FROM miembros
                WHERE activo = 1
                ORDER BY nombre ASC;
            """)
        else:
            cursor.execute("""
                SELECT id, nombre, correo, telefono, activo
                FROM miembros
                ORDER BY id DESC;
            """)
        rows = cursor.fetchall()
        conn.close()
        return [Miembro.from_row(r) for r in rows]

    def search_and_filter(self, query: str = "", activo_filtro: Optional[bool] = None) -> List[Miembro]:
        """Búsqueda por nombre/correo/teléfono y filtro por estado activo/inactivo."""
        conn = get_connection()
        cursor = conn.cursor()

        sql = """
            SELECT id, nombre, correo, telefono, activo
            FROM miembros
            WHERE 1=1
        """
        params = []

        if query:
            sql += " AND (nombre LIKE ? OR correo LIKE ? OR telefono LIKE ?)"
            params.extend([f"%{query}%", f"%{query}%", f"%{query}%"])

        if activo_filtro is not None:
            sql += " AND activo = ?"
            params.append(1 if activo_filtro else 0)

        sql += " ORDER BY id DESC;"

        cursor.execute(sql, params)
        rows = cursor.fetchall()
        conn.close()
        return [Miembro.from_row(r) for r in rows]

    def create(self, miembro: Miembro) -> int:
        """Crea un nuevo miembro en la base de datos."""
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO miembros (nombre, correo, telefono, activo)
            VALUES (?, ?, ?, ?);
        """, (miembro.nombre.strip(), miembro.correo.strip().lower(), miembro.telefono.strip(), int(miembro.activo)))
        new_id = cursor.lastrowid
        conn.commit()
        conn.close()
        return new_id

    def update(self, miembro: Miembro) -> bool:
        """Actualiza los datos del miembro especificado."""
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("""
            UPDATE miembros
            SET nombre = ?, correo = ?, telefono = ?, activo = ?
            WHERE id = ?;
        """, (
            miembro.nombre.strip(),
            miembro.correo.strip().lower(),
            miembro.telefono.strip(),
            int(miembro.activo),
            miembro.id
        ))
        rows_affected = cursor.rowcount
        conn.commit()
        conn.close()
        return rows_affected > 0

    def deactivate(self, miembro_id: int) -> bool:
        """Marca un miembro como inactivo en la base de datos."""
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("UPDATE miembros SET activo = 0 WHERE id = ?;", (miembro_id,))
        rows_affected = cursor.rowcount
        conn.commit()
        conn.close()
        return rows_affected > 0

    def delete(self, miembro_id: int) -> bool:
        """Elimina físicamente un miembro si no tiene tickets asociados."""
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("DELETE FROM miembros WHERE id = ?;", (miembro_id,))
        rows_affected = cursor.rowcount
        conn.commit()
        conn.close()
        return rows_affected > 0

    def count_assigned_tickets(self, miembro_id: int) -> int:
        """Retorna la cantidad total de tickets asignados a este miembro."""
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT COUNT(*) AS total FROM tickets WHERE miembro_id = ? AND activo = 1;", (miembro_id,))
        total = cursor.fetchone()["total"]
        conn.close()
        return total
