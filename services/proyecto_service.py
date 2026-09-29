"""
proyecto_service.py
-------------------
Servicio de lógica de negocio para la gestión de proyectos:
- Validación de campos obligatorios y coherencia de fechas (inicio <= fin).
- Regla 4: Bloqueo de eliminación/desactivación si existen tickets abiertos.
- Preferencia por bajas lógicas (desactivación).
"""

from datetime import datetime
from typing import List, Tuple, Optional
from models.proyecto import Proyecto
from repositories.proyecto_repository import ProyectoRepository
from config import ESTADOS_PROYECTO


class ProyectoService:
    def __init__(self, proyecto_repo: Optional[ProyectoRepository] = None):
        self.repo = proyecto_repo or ProyectoRepository()

    def _validar_fecha(self, fecha_str: str) -> Optional[datetime]:
        """Valida que una cadena cumpla el formato de fecha ISO YYYY-MM-DD."""
        try:
            return datetime.strptime(fecha_str.strip(), "%Y-%m-%d")
        except ValueError:
            return None

    def validar_datos(
        self, nombre: str, descripcion: str, fecha_inicio: str, fecha_fin: str, estado: str
    ) -> Tuple[bool, str]:
        """Valida las reglas de integridad de datos para un proyecto."""
        nombre = nombre.strip()
        if not nombre:
            return False, "El nombre del proyecto es obligatorio."

        if len(nombre) < 3:
            return False, "El nombre del proyecto debe contener al menos 3 caracteres."

        dt_inicio = self._validar_fecha(fecha_inicio)
        if not dt_inicio:
            return False, "La fecha de inicio debe tener el formato YYYY-MM-DD (Ej. 2026-09-01)."

        dt_fin = self._validar_fecha(fecha_fin)
        if not dt_fin:
            return False, "La fecha de finalización debe tener el formato YYYY-MM-DD (Ej. 2026-12-31)."

        if dt_inicio > dt_fin:
            return False, "La fecha de inicio no puede ser posterior a la fecha de finalización."

        if estado not in ESTADOS_PROYECTO:
            return False, f"El estado debe ser uno de los permitidos: {', '.join(ESTADOS_PROYECTO)}."

        return True, ""

    def crear_proyecto(
        self, nombre: str, descripcion: str, fecha_inicio: str, fecha_fin: str, estado: str, activo: bool = True
    ) -> Tuple[bool, str, Optional[int]]:
        """Crea un proyecto tras validar sus reglas de negocio."""
        valido, mensaje = self.validar_datos(nombre, descripcion, fecha_inicio, fecha_fin, estado)
        if not valido:
            return False, mensaje, None

        proyecto = Proyecto(
            id=None,
            nombre=nombre.strip(),
            descripcion=descripcion.strip(),
            fecha_inicio=fecha_inicio.strip(),
            fecha_fin=fecha_fin.strip(),
            estado=estado,
            activo=activo
        )
        try:
            nuevo_id = self.repo.create(proyecto)
            return True, "Proyecto creado exitosamente.", nuevo_id
        except Exception as e:
            return False, f"Error al guardar en base de datos: {e}", None

    def actualizar_proyecto(
        self, proyecto_id: int, nombre: str, descripcion: str, fecha_inicio: str, fecha_fin: str, estado: str, activo: bool
    ) -> Tuple[bool, str]:
        """Actualiza un proyecto existente validando restricciones de negocio."""
        proyecto_existente = self.repo.get_by_id(proyecto_id)
        if not proyecto_existente:
            return False, "El proyecto especificado no existe."

        valido, mensaje = self.validar_datos(nombre, descripcion, fecha_inicio, fecha_fin, estado)
        if not valido:
            return False, mensaje

        # Si se intenta desactivar el proyecto o cerrarlo, verificar si tiene tickets abiertos
        if not activo or estado == "Cerrado":
            tickets_abiertos = self.repo.count_open_tickets(proyecto_id)
            if tickets_abiertos > 0:
                accion = "desactivar" if not activo else "cerrar"
                return False, f"No se puede {accion} este proyecto porque aún tiene {tickets_abiertos} ticket(s) abierto(s)."

        proyecto = Proyecto(
            id=proyecto_id,
            nombre=nombre.strip(),
            descripcion=descripcion.strip(),
            fecha_inicio=fecha_inicio.strip(),
            fecha_fin=fecha_fin.strip(),
            estado=estado,
            activo=activo
        )
        try:
            exito = self.repo.update(proyecto)
            if exito:
                return True, "Proyecto actualizado correctamente."
            return False, "No se pudo actualizar el proyecto."
        except Exception as e:
            return False, f"Error al actualizar en base de datos: {e}"

    def desactivar_proyecto(self, proyecto_id: int) -> Tuple[bool, str]:
        """
        Regla de Negocio 4:
        No se permite desactivar o eliminar un proyecto si tiene tickets abiertos.
        """
        tickets_abiertos = self.repo.count_open_tickets(proyecto_id)
        if tickets_abiertos > 0:
            return False, f"Regla de Negocio: No se puede desactivar el proyecto porque cuenta con {tickets_abiertos} ticket(s) abierto(s) pendientes de resolución."

        try:
            exito = self.repo.deactivate(proyecto_id)
            if exito:
                return True, "Proyecto desactivado correctamente."
            return False, "No se encontró el proyecto."
        except Exception as e:
            return False, f"Error en base de datos: {e}"

    def eliminar_proyecto(self, proyecto_id: int) -> Tuple[bool, str]:
        """
        Eliminación física con validación estricta de tickets abiertos
        y captura de restricciones de llave foránea.
        """
        tickets_abiertos = self.repo.count_open_tickets(proyecto_id)
        if tickets_abiertos > 0:
            return False, f"Regla de Negocio: No se puede eliminar el proyecto porque cuenta con {tickets_abiertos} ticket(s) abierto(s)."

        try:
            exito = self.repo.delete(proyecto_id)
            if exito:
                return True, "Proyecto eliminado físicamente de la base de datos."
            return False, "No se encontró el proyecto a eliminar."
        except Exception as e:
            # Captura violación de FK si existen tickets históricos
            return False, f"No se puede eliminar el proyecto por integridad referencial (tiene historial de tickets asociados). Considere desactivarlo: {e}"

    def obtener_proyecto(self, proyecto_id: int) -> Optional[Proyecto]:
        return self.repo.get_by_id(proyecto_id)

    def listar_proyectos(self, solo_activos: bool = False) -> List[Proyecto]:
        return self.repo.list_all(solo_activos=solo_activos)

    def buscar_y_filtrar(self, query: str = "", estado: str = "", activo_filtro: Optional[bool] = None) -> List[Proyecto]:
        return self.repo.search_and_filter(query=query, estado=estado, activo_filtro=activo_filtro)
