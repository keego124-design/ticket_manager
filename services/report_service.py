"""
report_service.py
-----------------
Servicio para la generación de reportes analíticos y métricas del sistema:
- Tickets Abiertos.
- Tickets Vencidos (Overdue): due_date < hoy y estado not in ('Completado', 'Cancelado').
- Agrupación por Estado.
- Conteo por Proyecto.
- Conteo por Prioridad.
- Resumen ejecutivo para el Dashboard.
"""

from datetime import datetime
from typing import List, Dict, Any, Optional
from models.ticket import Ticket
from repositories.ticket_repository import TicketRepository
from repositories.proyecto_repository import ProyectoRepository
from repositories.miembro_repository import MiembroRepository


class ReportService:
    def __init__(
        self,
        ticket_repo: Optional[TicketRepository] = None,
        proyecto_repo: Optional[ProyectoRepository] = None,
        miembro_repo: Optional[MiembroRepository] = None
    ):
        self.ticket_repo = ticket_repo or TicketRepository()
        self.proyecto_repo = proyecto_repo or ProyectoRepository()
        self.miembro_repo = miembro_repo or MiembroRepository()

    def get_open_tickets(self) -> List[Ticket]:
        """Reporte A: Tickets actualmente abiertos (Pendiente o En Progreso)."""
        return self.ticket_repo.get_open_tickets()

    def get_overdue_tickets(self) -> List[Ticket]:
        """
        Reporte B: Tickets vencidos (Overdue).
        Calcula si la fecha límite ya venció respecto al día de hoy
        y el ticket sigue sin completarse ni cancelarse.
        """
        hoy_str = datetime.now().strftime("%Y-%m-%d")
        return self.ticket_repo.get_overdue_tickets(hoy_str)

    def get_tickets_by_status(self) -> List[Dict[str, Any]]:
        """Reporte C: Tickets agrupados y contabilizados por estado."""
        return self.ticket_repo.count_by_status()

    def get_tickets_by_project(self) -> List[Dict[str, Any]]:
        """Reporte D: Conteo de tickets asignados por proyecto."""
        return self.ticket_repo.count_by_project()

    def get_tickets_by_priority(self) -> List[Dict[str, Any]]:
        """Reporte E: Conteo de tickets clasificados por nivel de prioridad."""
        return self.ticket_repo.count_by_priority()

    def get_dashboard_summary(self) -> Dict[str, Any]:
        """
        Retorna indicadores clave de rendimiento (KPIs) para la vista general:
        - Total de tickets
        - Tickets abiertos
        - Tickets vencidos
        - Tickets completados
        - Proyectos activos
        - Miembros activos
        """
        hoy_str = datetime.now().strftime("%Y-%m-%d")
        todos_tickets = self.ticket_repo.list_all_with_join(solo_activos=True)
        vencidos = self.ticket_repo.get_overdue_tickets(hoy_str)
        proyectos_activos = self.proyecto_repo.list_all(solo_activos=True)
        miembros_activos = self.miembro_repo.list_all(solo_activos=True)

        total_tickets = len(todos_tickets)
        abiertos = sum(1 for t in todos_tickets if t.estado in ("Pendiente", "En Progreso"))
        completados = sum(1 for t in todos_tickets if t.estado == "Completado")
        cancelados = sum(1 for t in todos_tickets if t.estado == "Cancelado")

        return {
            "total_tickets": total_tickets,
            "tickets_abiertos": abiertos,
            "tickets_vencidos": len(vencidos),
            "tickets_completados": completados,
            "tickets_cancelados": cancelados,
            "total_proyectos_activos": len(proyectos_activos),
            "total_miembros_activos": len(miembros_activos),
        }
