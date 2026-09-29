"""
ticket_service.py
-----------------
Servicio de lógica de negocio para la gestión de tickets.
Implementa rigurosamente las reglas del dominio:
- Regla 1: No crear tickets en proyectos cerrados.
- Regla 2: Un miembro inactivo no puede recibir nuevos tickets.
- Regla 3: Un ticket Completado o Cancelado no puede regresar a Pendiente sin confirmación explícita.
- Regla 5: El ticket debe pertenecer a un proyecto existente y activo.
- Regla 6: El ticket debe tener un miembro de equipo asignado válido y activo.
- Regla 7: Fecha límite válida en formato ISO YYYY-MM-DD.
- Regla 8: Registro automático de fecha de cierre al marcarlo como Completado.
"""

from datetime import datetime
from typing import List, Tuple, Optional
from models.ticket import Ticket
from repositories.ticket_repository import TicketRepository
from repositories.proyecto_repository import ProyectoRepository
from repositories.miembro_repository import MiembroRepository
from config import PRIORIDADES_TICKET, ESTADOS_TICKET


class TicketService:
    def __init__(
        self,
        ticket_repo: Optional[TicketRepository] = None,
        proyecto_repo: Optional[ProyectoRepository] = None,
        miembro_repo: Optional[MiembroRepository] = None
    ):
        self.ticket_repo = ticket_repo or TicketRepository()
        self.proyecto_repo = proyecto_repo or ProyectoRepository()
        self.miembro_repo = miembro_repo or MiembroRepository()

    def _validar_fecha(self, fecha_str: str) -> Optional[datetime]:
        """Valida formato de fecha ISO YYYY-MM-DD."""
        try:
            return datetime.strptime(fecha_str.strip(), "%Y-%m-%d")
        except ValueError:
            return None

    def validar_datos(
        self,
        proyecto_id: int,
        miembro_id: int,
        titulo: str,
        descripcion: str,
        prioridad: str,
        estado: str,
        fecha_limite: str,
        es_creacion: bool = True
    ) -> Tuple[bool, str]:
        """Valida exhaustivamente los datos y el cumplimiento de las reglas de negocio."""
        # 1. Título
        titulo = titulo.strip()
        if not titulo:
            return False, "El título del ticket es obligatorio."
        if len(titulo) < 3:
            return False, "El título debe contener al menos 3 caracteres."

        # 2. Proyecto existente (Regla 5)
        if not proyecto_id or proyecto_id <= 0:
            return False, "Regla de Negocio: Debe seleccionar un proyecto para el ticket."

        proyecto = self.proyecto_repo.get_by_id(proyecto_id)
        if not proyecto:
            return False, "Regla de Negocio: El proyecto seleccionado no existe en el sistema."

        if not proyecto.activo:
            return False, "Regla de Negocio: No se pueden asociar tickets a proyectos inactivos."

        # Regla 1: Un ticket no puede ser creado dentro de un proyecto cerrado
        if es_creacion and proyecto.esta_cerrado():
            return False, "Regla de Negocio 1: No es posible crear un ticket dentro de un proyecto que se encuentra 'Cerrado'."

        # 3. Miembro asignado (Regla 6)
        if not miembro_id or miembro_id <= 0:
            return False, "Regla de Negocio: Debe seleccionar un miembro de equipo para asignar el ticket."

        miembro = self.miembro_repo.get_by_id(miembro_id)
        if not miembro:
            return False, "Regla de Negocio: El miembro asignado no existe."

        # Regla 2: Un miembro inactivo no puede recibir nuevos tickets
        if es_creacion and not miembro.activo:
            return False, f"Regla de Negocio 2: El miembro '{miembro.nombre}' está marcado como INACTIVO y no puede recibir nuevos tickets."

        # 4. Prioridad y Estado válidos
        if prioridad not in PRIORIDADES_TICKET:
            return False, f"Prioridad inválida. Debe ser: {', '.join(PRIORIDADES_TICKET)}."

        if estado not in ESTADOS_TICKET:
            return False, f"Estado inválido. Debe ser: {', '.join(ESTADOS_TICKET)}."

        # 5. Fecha Límite (Regla 7)
        dt_limite = self._validar_fecha(fecha_limite)
        if not dt_limite:
            return False, "Regla de Negocio 7: La fecha límite es inválida. Debe usar formato YYYY-MM-DD (Ej. 2026-10-15)."

        return True, ""

    def crear_ticket(
        self,
        proyecto_id: int,
        miembro_id: int,
        titulo: str,
        descripcion: str,
        prioridad: str,
        estado: str,
        fecha_limite: str
    ) -> Tuple[bool, str, Optional[int]]:
        """Crea un ticket validando las reglas de negocio."""
        valido, mensaje = self.validar_datos(
            proyecto_id, miembro_id, titulo, descripcion, prioridad, estado, fecha_limite, es_creacion=True
        )
        if not valido:
            return False, mensaje, None

        hoy_str = datetime.now().strftime("%Y-%m-%d")
        # Regla 8: Si nace como completado, fijar fecha de cierre
        fecha_cierre = hoy_str if estado == "Completado" else None

        ticket = Ticket(
            id=None,
            proyecto_id=proyecto_id,
            miembro_id=miembro_id,
            titulo=titulo.strip(),
            descripcion=descripcion.strip(),
            prioridad=prioridad,
            estado=estado,
            fecha_creacion=hoy_str,
            fecha_limite=fecha_limite.strip(),
            fecha_cierre=fecha_cierre,
            activo=True
        )
        try:
            nuevo_id = self.ticket_repo.create(ticket)
            return True, "Ticket registrado exitosamente.", nuevo_id
        except Exception as e:
            return False, f"Error al guardar ticket en la base de datos: {e}", None

    def actualizar_ticket(
        self,
        ticket_id: int,
        proyecto_id: int,
        miembro_id: int,
        titulo: str,
        descripcion: str,
        prioridad: str,
        nuevo_estado: str,
        fecha_limite: str,
        confirmacion_reapertura: bool = False
    ) -> Tuple[bool, str]:
        """
        Actualiza un ticket existente.
        Valida Regla 3: Si estaba Completado o Cancelado y pasa a Pendiente,
        requiere confirmación explícita (confirmacion_reapertura = True).
        """
        ticket_actual = self.ticket_repo.get_by_id(ticket_id)
        if not ticket_actual:
            return False, "El ticket especificado no existe."

        # Regla 3: Verificar transición hacia Pendiente desde Completado o Cancelado
        estaba_cerrado = ticket_actual.estado in ("Completado", "Cancelado")
        pasa_a_pendiente = nuevo_estado == "Pendiente"
        if estaba_cerrado and pasa_a_pendiente and not confirmacion_reapertura:
            return False, "REQUIERE_CONFIRMACION_REAPERTURA"

        valido, mensaje = self.validar_datos(
            proyecto_id, miembro_id, titulo, descripcion, prioridad, nuevo_estado, fecha_limite, es_creacion=False
        )
        if not valido:
            return False, mensaje

        # Regla 8: Registrar automáticamente fecha de cierre al completarse
        hoy_str = datetime.now().strftime("%Y-%m-%d")
        if nuevo_estado == "Completado":
            fecha_cierre = ticket_actual.fecha_cierre or hoy_str
        elif nuevo_estado == "Cancelado":
            fecha_cierre = ticket_actual.fecha_cierre or hoy_str
        else:
            fecha_cierre = None  # Si se reabre, se elimina la fecha de cierre

        ticket_actualizado = Ticket(
            id=ticket_id,
            proyecto_id=proyecto_id,
            miembro_id=miembro_id,
            titulo=titulo.strip(),
            descripcion=descripcion.strip(),
            prioridad=prioridad,
            estado=nuevo_estado,
            fecha_creacion=ticket_actual.fecha_creacion,
            fecha_limite=fecha_limite.strip(),
            fecha_cierre=fecha_cierre,
            activo=ticket_actual.activo
        )

        try:
            exito = self.ticket_repo.update(ticket_actualizado)
            if exito:
                return True, "Ticket actualizado exitosamente."
            return False, "No se pudo actualizar el ticket."
        except Exception as e:
            return False, f"Error al actualizar ticket en base de datos: {e}"

    def cambiar_estado(self, ticket_id: int, nuevo_estado: str, confirmacion_reapertura: bool = False) -> Tuple[bool, str]:
        """Cambio rápido de estado de un ticket aplicando las reglas de negocio."""
        ticket = self.ticket_repo.get_by_id(ticket_id)
        if not ticket:
            return False, "El ticket no existe."

        if ticket.estado == nuevo_estado:
            return True, f"El ticket ya se encuentra en estado '{nuevo_estado}'."

        estaba_cerrado = ticket.estado in ("Completado", "Cancelado")
        pasa_a_pendiente = nuevo_estado == "Pendiente"

        if estaba_cerrado and pasa_a_pendiente and not confirmacion_reapertura:
            return False, "REQUIERE_CONFIRMACION_REAPERTURA"

        hoy_str = datetime.now().strftime("%Y-%m-%d")
        fecha_cierre = hoy_str if nuevo_estado in ("Completado", "Cancelado") else None

        try:
            exito = self.ticket_repo.update_status(ticket_id, nuevo_estado, fecha_cierre)
            if exito:
                return True, f"Estado del ticket actualizado a '{nuevo_estado}'."
            return False, "No se pudo actualizar el estado."
        except Exception as e:
            return False, f"Error al cambiar estado: {e}"

    def desactivar_ticket(self, ticket_id: int) -> Tuple[bool, str]:
        """Desactiva un ticket (baja lógica)."""
        try:
            exito = self.ticket_repo.deactivate(ticket_id)
            if exito:
                return True, "Ticket desactivado correctamente."
            return False, "No se encontró el ticket."
        except Exception as e:
            return False, f"Error al desactivar ticket: {e}"

    def eliminar_ticket(self, ticket_id: int) -> Tuple[bool, str]:
        """Eliminación física del ticket."""
        try:
            exito = self.ticket_repo.delete(ticket_id)
            if exito:
                return True, "Ticket eliminado físicamente."
            return False, "No se encontró el ticket."
        except Exception as e:
            return False, f"Error al eliminar ticket: {e}"

    def obtener_ticket(self, ticket_id: int) -> Optional[Ticket]:
        return self.ticket_repo.get_by_id(ticket_id)

    def listar_con_join(self, solo_activos: bool = True) -> List[Ticket]:
        """Ejecuta y retorna el listado de tickets usando la consulta SQL JOIN."""
        return self.ticket_repo.list_all_with_join(solo_activos=solo_activos)

    def buscar_y_filtrar(
        self,
        query: str = "",
        proyecto_id: Optional[int] = None,
        miembro_id: Optional[int] = None,
        prioridad: str = "",
        estado: str = "",
        solo_activos: bool = True
    ) -> List[Ticket]:
        return self.ticket_repo.search_and_filter(
            query=query,
            proyecto_id=proyecto_id,
            miembro_id=miembro_id,
            prioridad=prioridad,
            estado=estado,
            solo_activos=solo_activos
        )
