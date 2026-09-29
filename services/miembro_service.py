"""
miembro_service.py
------------------
Servicio de lógica de negocio para la gestión de miembros del equipo:
- Validación rigurosa de formato de correo electrónico mediante expresiones regulares.
- Validación de unicidad de correo.
- Regla 2: Gestión de estados activos/inactivos para evitar asignaciones incorrectas.
"""

import re
from typing import List, Tuple, Optional
from models.miembro import Miembro
from repositories.miembro_repository import MiembroRepository

# Expresión regular estándar para validación de correo electrónico
REGEX_EMAIL = r"^[\w\.-]+@[\w\.-]+\.\w+$"


class MiembroService:
    def __init__(self, miembro_repo: Optional[MiembroRepository] = None):
        self.repo = miembro_repo or MiembroRepository()

    def validar_datos(self, nombre: str, correo: str, telefono: str, exclude_id: Optional[int] = None) -> Tuple[bool, str]:
        """Valida que los campos cumplan con el formato y las reglas del sistema."""
        nombre = nombre.strip()
        if not nombre:
            return False, "El nombre del miembro es obligatorio."

        if len(nombre) < 3:
            return False, "El nombre debe contener al menos 3 caracteres."

        correo = correo.strip().lower()
        if not correo:
            return False, "El correo electrónico es obligatorio."

        if not re.match(REGEX_EMAIL, correo):
            return False, "El formato del correo electrónico es inválido (Ej: usuario@empresa.com)."

        # Validar que no exista otro miembro con el mismo correo
        existente = self.repo.get_by_email(correo, exclude_id=exclude_id)
        if existente:
            return False, f"Ya existe un miembro registrado con el correo '{correo}'."

        return True, ""

    def crear_miembro(self, nombre: str, correo: str, telefono: str, activo: bool = True) -> Tuple[bool, str, Optional[int]]:
        """Crea un nuevo miembro tras validar nombre y correo único."""
        valido, mensaje = self.validar_datos(nombre, correo, telefono)
        if not valido:
            return False, mensaje, None

        miembro = Miembro(
            id=None,
            nombre=nombre.strip(),
            correo=correo.strip().lower(),
            telefono=telefono.strip(),
            activo=activo
        )
        try:
            nuevo_id = self.repo.create(miembro)
            return True, "Miembro del equipo registrado exitosamente.", nuevo_id
        except Exception as e:
            return False, f"Error al guardar en base de datos: {e}", None

    def actualizar_miembro(self, miembro_id: int, nombre: str, correo: str, telefono: str, activo: bool) -> Tuple[bool, str]:
        """Actualiza los datos de un miembro existente."""
        existente = self.repo.get_by_id(miembro_id)
        if not existente:
            return False, "El miembro especificado no existe."

        valido, mensaje = self.validar_datos(nombre, correo, telefono, exclude_id=miembro_id)
        if not valido:
            return False, mensaje

        miembro = Miembro(
            id=miembro_id,
            nombre=nombre.strip(),
            correo=correo.strip().lower(),
            telefono=telefono.strip(),
            activo=activo
        )
        try:
            exito = self.repo.update(miembro)
            if exito:
                return True, "Datos del miembro actualizados correctamente."
            return False, "No se pudo actualizar el miembro."
        except Exception as e:
            return False, f"Error al actualizar en base de datos: {e}"

    def desactivar_miembro(self, miembro_id: int) -> Tuple[bool, str]:
        """Desactiva un miembro (baja lógica). No podrá recibir nuevos tickets."""
        try:
            exito = self.repo.deactivate(miembro_id)
            if exito:
                return True, "Miembro desactivado. No podrá recibir nuevos tickets."
            return False, "No se encontró el miembro."
        except Exception as e:
            return False, f"Error al desactivar miembro: {e}"

    def eliminar_miembro(self, miembro_id: int) -> Tuple[bool, str]:
        """Eliminación física validando integridad referencial."""
        tickets_asignados = self.repo.count_assigned_tickets(miembro_id)
        if tickets_asignados > 0:
            return False, f"No se puede eliminar este miembro porque tiene {tickets_asignados} ticket(s) asociados en el historial. Se sugiere desactivarlo."

        try:
            exito = self.repo.delete(miembro_id)
            if exito:
                return True, "Miembro eliminado de la base de datos."
            return False, "No se encontró el miembro."
        except Exception as e:
            return False, f"No se puede eliminar el miembro debido a restricciones de integridad: {e}"

    def obtener_miembro(self, miembro_id: int) -> Optional[Miembro]:
        return self.repo.get_by_id(miembro_id)

    def listar_miembros(self, solo_activos: bool = False) -> List[Miembro]:
        return self.repo.list_all(solo_activos=solo_activos)

    def buscar_y_filtrar(self, query: str = "", activo_filtro: Optional[bool] = None) -> List[Miembro]:
        return self.repo.search_and_filter(query=query, activo_filtro=activo_filtro)
