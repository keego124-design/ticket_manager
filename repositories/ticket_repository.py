"""
ticket_repository.py
--------------------
Repositorio para la entidad Ticket.
IMPLEMENTA OBLIGATORIAMENTE CONSULTAS CON SQL JOIN:
Combina las tablas 'tickets', 'proyectos' y 'miembros' para proyectar nombres reales
en lugar de identificadores foráneos, tanto en el listado principal como en reportes.
"""

from typing import Optional, List, Dict, Any
from database import get_connection
from models.ticket import Ticket


class TicketRepository:
    def get_by_id(self, ticket_id: int) -> Optional[Ticket]:
        """
        Obtiene un ticket por ID ejecutando un SQL JOIN para cargar
        el nombre del proyecto y del miembro asignado.
        """
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("""
            SELECT 
                tickets.id,
                tickets.proyecto_id,
                tickets.miembro_id,
                tickets.titulo,
                tickets.descripcion,
                tickets.prioridad,
                tickets.estado,
                tickets.fecha_creacion,
                tickets.fecha_limite,
                tickets.fecha_cierre,
                tickets.activo,
                proyectos.nombre AS proyecto,
                miembros.nombre AS miembro
            FROM tickets
            JOIN proyectos ON tickets.proyecto_id = proyectos.id
            JOIN miembros ON tickets.miembro_id = miembros.id
            WHERE tickets.id = ?;
        """, (ticket_id,))
        row = cursor.fetchone()
        conn.close()
        return Ticket.from_row(row) if row else None

    def list_all_with_join(self, solo_activos: bool = True) -> List[Ticket]:
        """
        Consulta principal demostrando SQL JOIN explícito entre:
        - tickets
        - proyectos (tickets.proyecto_id = proyectos.id)
        - miembros  (tickets.miembro_id = miembros.id)
        """
        conn = get_connection()
        cursor = conn.cursor()

        condicion = "WHERE tickets.activo = 1" if solo_activos else ""

        query = f"""
            SELECT
                tickets.id,
                tickets.proyecto_id,
                tickets.miembro_id,
                tickets.titulo,
                tickets.descripcion,
                tickets.prioridad,
                tickets.estado,
                tickets.fecha_creacion,
                tickets.fecha_limite,
                tickets.fecha_cierre,
                tickets.activo,
                proyectos.nombre AS proyecto,
                miembros.nombre AS miembro
            FROM tickets
            JOIN proyectos ON tickets.proyecto_id = proyectos.id
            JOIN miembros ON tickets.miembro_id = miembros.id
            {condicion}
            ORDER BY tickets.id DESC;
        """

        cursor.execute(query)
        rows = cursor.fetchall()
        conn.close()
        return [Ticket.from_row(r) for r in rows]

    def search_and_filter(
        self,
        query: str = "",
        proyecto_id: Optional[int] = None,
        miembro_id: Optional[int] = None,
        prioridad: str = "",
        estado: str = "",
        solo_activos: bool = True
    ) -> List[Ticket]:
        """
        Filtros multicriterio sobre la consulta SQL JOIN:
        Permite buscar por texto en el título o descripción, y filtrar
        simultáneamente por proyecto, miembro asignado, prioridad y estado.
        """
        conn = get_connection()
        cursor = conn.cursor()

        sql = """
            SELECT
                tickets.id,
                tickets.proyecto_id,
                tickets.miembro_id,
                tickets.titulo,
                tickets.descripcion,
                tickets.prioridad,
                tickets.estado,
                tickets.fecha_creacion,
                tickets.fecha_limite,
                tickets.fecha_cierre,
                tickets.activo,
                proyectos.nombre AS proyecto,
                miembros.nombre AS miembro
            FROM tickets
            JOIN proyectos ON tickets.proyecto_id = proyectos.id
            JOIN miembros ON tickets.miembro_id = miembros.id
            WHERE 1=1
        """
        params: List[Any] = []

        if solo_activos:
            sql += " AND tickets.activo = 1"

        if query:
            sql += " AND (tickets.titulo LIKE ? OR tickets.descripcion LIKE ?)"
            params.extend([f"%{query}%", f"%{query}%"])

        if proyecto_id and proyecto_id > 0:
            sql += " AND tickets.proyecto_id = ?"
            params.append(proyecto_id)

        if miembro_id and miembro_id > 0:
            sql += " AND tickets.miembro_id = ?"
            params.append(miembro_id)

        if prioridad and prioridad != "Todas":
            sql += " AND tickets.prioridad = ?"
            params.append(prioridad)

        if estado and estado != "Todos":
            sql += " AND tickets.estado = ?"
            params.append(estado)

        sql += " ORDER BY tickets.id DESC;"

        cursor.execute(sql, params)
        rows = cursor.fetchall()
        conn.close()
        return [Ticket.from_row(r) for r in rows]

    def create(self, ticket: Ticket) -> int:
        """Crea un nuevo ticket en la base de datos."""
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO tickets (
                proyecto_id, miembro_id, titulo, descripcion, prioridad,
                estado, fecha_creacion, fecha_limite, fecha_cierre, activo
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?);
        """, (
            ticket.proyecto_id,
            ticket.miembro_id,
            ticket.titulo.strip(),
            ticket.descripcion.strip(),
            ticket.prioridad,
            ticket.estado,
            ticket.fecha_creacion,
            ticket.fecha_limite,
            ticket.fecha_cierre,
            int(ticket.activo)
        ))
        new_id = cursor.lastrowid
        conn.commit()
        conn.close()
        return new_id

    def update(self, ticket: Ticket) -> bool:
        """Actualiza la información completa de un ticket."""
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("""
            UPDATE tickets
            SET proyecto_id = ?, miembro_id = ?, titulo = ?, descripcion = ?,
                prioridad = ?, estado = ?, fecha_limite = ?, fecha_cierre = ?, activo = ?
            WHERE id = ?;
        """, (
            ticket.proyecto_id,
            ticket.miembro_id,
            ticket.titulo.strip(),
            ticket.descripcion.strip(),
            ticket.prioridad,
            ticket.estado,
            ticket.fecha_limite,
            ticket.fecha_cierre,
            int(ticket.activo),
            ticket.id
        ))
        rows_affected = cursor.rowcount
        conn.commit()
        conn.close()
        return rows_affected > 0

    def update_status(self, ticket_id: int, nuevo_estado: str, fecha_cierre: Optional[str] = None) -> bool:
        """Actualiza el estado de un ticket y opcionalmente su fecha de cierre."""
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("""
            UPDATE tickets
            SET estado = ?, fecha_cierre = ?
            WHERE id = ?;
        """, (nuevo_estado, fecha_cierre, ticket_id))
        rows_affected = cursor.rowcount
        conn.commit()
        conn.close()
        return rows_affected > 0

    def deactivate(self, ticket_id: int) -> bool:
        """Desactiva un ticket (baja lógica)."""
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("UPDATE tickets SET activo = 0 WHERE id = ?;", (ticket_id,))
        rows_affected = cursor.rowcount
        conn.commit()
        conn.close()
        return rows_affected > 0

    def delete(self, ticket_id: int) -> bool:
        """Elimina físicamente un ticket."""
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("DELETE FROM tickets WHERE id = ?;", (ticket_id,))
        rows_affected = cursor.rowcount
        conn.commit()
        conn.close()
        return rows_affected > 0

    # -------------------------------------------------------------
    # CONSULTAS PARA REPORTES Y MÉTRICAS
    # -------------------------------------------------------------

    def get_open_tickets(self) -> List[Ticket]:
        """Obtiene todos los tickets en estado Pendiente o En Progreso con JOIN."""
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("""
            SELECT
                tickets.id,
                tickets.proyecto_id,
                tickets.miembro_id,
                tickets.titulo,
                tickets.descripcion,
                tickets.prioridad,
                tickets.estado,
                tickets.fecha_creacion,
                tickets.fecha_limite,
                tickets.fecha_cierre,
                tickets.activo,
                proyectos.nombre AS proyecto,
                miembros.nombre AS miembro
            FROM tickets
            JOIN proyectos ON tickets.proyecto_id = proyectos.id
            JOIN miembros ON tickets.miembro_id = miembros.id
            WHERE tickets.activo = 1 AND tickets.estado IN ('Pendiente', 'En Progreso')
            ORDER BY tickets.fecha_limite ASC;
        """)
        rows = cursor.fetchall()
        conn.close()
        return [Ticket.from_row(r) for r in rows]

    def get_overdue_tickets(self, fecha_actual: str) -> List[Ticket]:
        """
        Retorna los tickets cuya fecha_limite es menor a la fecha_actual
        y su estado NO es 'Completado' ni 'Cancelado', utilizando SQL JOIN.
        """
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("""
            SELECT
                tickets.id,
                tickets.proyecto_id,
                tickets.miembro_id,
                tickets.titulo,
                tickets.descripcion,
                tickets.prioridad,
                tickets.estado,
                tickets.fecha_creacion,
                tickets.fecha_limite,
                tickets.fecha_cierre,
                tickets.activo,
                proyectos.nombre AS proyecto,
                miembros.nombre AS miembro
            FROM tickets
            JOIN proyectos ON tickets.proyecto_id = proyectos.id
            JOIN miembros ON tickets.miembro_id = miembros.id
            WHERE tickets.activo = 1
              AND tickets.estado NOT IN ('Completado', 'Cancelado')
              AND tickets.fecha_limite < ?
            ORDER BY tickets.fecha_limite ASC;
        """, (fecha_actual,))
        rows = cursor.fetchall()
        conn.close()
        return [Ticket.from_row(r) for r in rows]

    def count_by_status(self) -> List[Dict[str, Any]]:
        """Conteo de tickets agrupados por estado."""
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("""
            SELECT estado, COUNT(*) AS total
            FROM tickets
            WHERE activo = 1
            GROUP BY estado
            ORDER BY total DESC;
        """)
        rows = cursor.fetchall()
        conn.close()
        return [{"estado": r["estado"], "total": r["total"]} for r in rows]

    def count_by_project(self) -> List[Dict[str, Any]]:
        """Conteo de tickets por proyecto utilizando JOIN."""
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("""
            SELECT proyectos.nombre AS proyecto, COUNT(tickets.id) AS total
            FROM proyectos
            LEFT JOIN tickets ON proyectos.id = tickets.proyecto_id AND tickets.activo = 1
            WHERE proyectos.activo = 1
            GROUP BY proyectos.id, proyectos.nombre
            ORDER BY total DESC;
        """)
        rows = cursor.fetchall()
        conn.close()
        return [{"proyecto": r["proyecto"], "total": r["total"]} for r in rows]

    def count_by_priority(self) -> List[Dict[str, Any]]:
        """Conteo de tickets agrupados por prioridad."""
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("""
            SELECT prioridad, COUNT(*) AS total
            FROM tickets
            WHERE activo = 1
            GROUP BY prioridad
            ORDER BY total DESC;
        """)
        rows = cursor.fetchall()
        conn.close()
        return [{"prioridad": r["prioridad"], "total": r["total"]} for r in rows]
