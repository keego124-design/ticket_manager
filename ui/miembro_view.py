"""
miembro_view.py
---------------
Vista para la gestión integral (CRUD) de Miembros del Equipo:
- Listado en ttk.Treeview.
- Búsqueda en tiempo real por nombre, correo y teléfono.
- Modal para creación/edición con validación de expresiones regulares de correo.
- Regla 2: Gestión de miembros inactivos para impedir asignaciones erróneas.
"""

import tkinter as tk
from tkinter import ttk, messagebox
from typing import Optional
from services.miembro_service import MiembroService
from models.miembro import Miembro
from config import (
    COLOR_FONDO,
    COLOR_BLANCO,
    COLOR_TEXTO,
    COLOR_PRIMARIO,
)
from ui.styles import FONT_TITLE, FONT_REGULAR, FONT_BOLD, FONT_SMALL


class FormularioMiembroModal(tk.Toplevel):
    """Diálogo modal para crear o editar un miembro del equipo."""
    def __init__(self, parent, service: MiembroService, miembro: Optional[Miembro] = None, on_success=None):
        super().__init__(parent)
        self.service = service
        self.miembro = miembro
        self.on_success = on_success

        modo = "Editar Miembro" if miembro else "Nuevo Miembro"
        self.title(f"{modo} - Ticket Management System")
        self.geometry("450x340")
        self.resizable(False, False)
        self.configure(bg=COLOR_FONDO)
        self.grab_set()

        self._construir_formulario()

    def _construir_formulario(self):
        frame = tk.Frame(self, bg=COLOR_BLANCO, bd=1, relief="solid", padx=20, pady=15)
        frame.pack(padx=20, pady=20, fill="both", expand=True)

        # Nombre
        tk.Label(frame, text="Nombre Completo *", font=FONT_BOLD, bg=COLOR_BLANCO).pack(anchor="w")
        self.ent_nombre = ttk.Entry(frame, font=FONT_REGULAR)
        self.ent_nombre.pack(fill="x", pady=(2, 10))

        # Correo Electrónico
        tk.Label(frame, text="Correo Electrónico (Regex) *", font=FONT_BOLD, bg=COLOR_BLANCO).pack(anchor="w")
        self.ent_correo = ttk.Entry(frame, font=FONT_REGULAR)
        self.ent_correo.pack(fill="x", pady=(2, 10))

        # Teléfono
        tk.Label(frame, text="Teléfono de Contacto", font=FONT_REGULAR, bg=COLOR_BLANCO).pack(anchor="w")
        self.ent_telefono = ttk.Entry(frame, font=FONT_REGULAR)
        self.ent_telefono.pack(fill="x", pady=(2, 10))

        # Activo
        self.var_activo = tk.BooleanVar(value=True)
        self.chk_activo = ttk.Checkbutton(frame, text="Miembro Activo (Puede recibir tickets)", variable=self.var_activo)
        self.chk_activo.pack(anchor="w", pady=(0, 15))

        # Botones
        f_botones = tk.Frame(frame, bg=COLOR_BLANCO)
        f_botones.pack(fill="x", pady=5)

        ttk.Button(f_botones, text="Cancelar", command=self.destroy).pack(side="right", padx=5)
        btn_guardar = tk.Button(
            f_botones,
            text="Guardar Miembro",
            font=FONT_BOLD,
            bg=COLOR_PRIMARIO,
            fg=COLOR_BLANCO,
            command=self._guardar
        )
        btn_guardar.pack(side="right", padx=5)

        if self.miembro:
            self.ent_nombre.insert(0, self.miembro.nombre)
            self.ent_correo.insert(0, self.miembro.correo)
            self.ent_telefono.insert(0, self.miembro.telefono)
            self.var_activo.set(self.miembro.activo)

    def _guardar(self):
        nombre = self.ent_nombre.get().strip()
        correo = self.ent_correo.get().strip()
        telefono = self.ent_telefono.get().strip()
        activo = self.var_activo.get()

        if self.miembro:
            exito, mensaje = self.service.actualizar_miembro(
                self.miembro.id, nombre, correo, telefono, activo
            )
        else:
            exito, mensaje, _ = self.service.crear_miembro(
                nombre, correo, telefono, activo
            )

        if exito:
            messagebox.showinfo("Éxito", mensaje, parent=self)
            if self.on_success:
                self.on_success()
            self.destroy()
        else:
            messagebox.showerror("Error de Validación", mensaje, parent=self)


class MiembroView(ttk.Frame):
    def __init__(self, parent):
        super().__init__(parent)
        self.service = MiembroService()
        self._construir_interfaz()

    def _construir_interfaz(self):
        # 1. Cabecera y acciones
        f_superior = tk.Frame(self, bg=COLOR_FONDO)
        f_superior.pack(fill="x", padx=25, pady=(20, 10))

        tk.Label(f_superior, text="Equipo de Trabajo", font=FONT_TITLE, bg=COLOR_FONDO, fg=COLOR_TEXTO).pack(side="left")

        f_acciones = tk.Frame(f_superior, bg=COLOR_FONDO)
        f_acciones.pack(side="right")

        btn_nuevo = tk.Button(
            f_acciones,
            text="+ Nuevo Miembro",
            font=FONT_BOLD,
            bg=COLOR_PRIMARIO,
            fg=COLOR_BLANCO,
            padx=10,
            pady=4,
            relief="flat",
            cursor="hand2",
            command=self._abrir_modal_crear
        )
        btn_nuevo.pack(side="left", padx=5)

        ttk.Button(f_acciones, text="Editar", command=self._abrir_modal_editar).pack(side="left", padx=5)
        ttk.Button(f_acciones, text="Desactivar / Activar", command=self._toggle_activo).pack(side="left", padx=5)
        ttk.Button(f_acciones, text="Eliminar", command=self._eliminar_miembro).pack(side="left", padx=5)

        # 2. Búsqueda y Filtros
        f_filtros = tk.Frame(self, bg=COLOR_BLANCO, bd=1, relief="solid", padx=15, pady=8)
        f_filtros.pack(fill="x", padx=25, pady=5)

        tk.Label(f_filtros, text="Buscar:", font=FONT_REGULAR, bg=COLOR_BLANCO).pack(side="left", padx=(0, 5))
        self.ent_busqueda = ttk.Entry(f_filtros, width=30)
        self.ent_busqueda.pack(side="left", padx=5)
        self.ent_busqueda.bind("<KeyRelease>", lambda e: self.cargar_datos())

        self.var_filtro_activos = tk.BooleanVar(value=False)
        chk_solo_activos = ttk.Checkbutton(
            f_filtros, text="Solo Miembros Activos", variable=self.var_filtro_activos, command=self.cargar_datos
        )
        chk_solo_activos.pack(side="left", padx=15)

        ttk.Button(f_filtros, text="Limpiar Filtros", command=self._limpiar_filtros).pack(side="right")

        # 3. Treeview de Miembros
        f_tabla = tk.Frame(self, bg=COLOR_FONDO)
        f_tabla.pack(fill="both", expand=True, padx=25, pady=(5, 20))

        cols = ("id", "nombre", "correo", "telefono", "activo")
        self.tree = ttk.Treeview(f_tabla, columns=cols, show="headings")

        self.tree.heading("id", text="#")
        self.tree.heading("nombre", text="Nombre del Miembro")
        self.tree.heading("correo", text="Correo Electrónico")
        self.tree.heading("telefono", text="Teléfono")
        self.tree.heading("activo", text="Estado")

        self.tree.column("id", width=40, anchor="center")
        self.tree.column("nombre", width=240)
        self.tree.column("correo", width=250)
        self.tree.column("telefono", width=140)
        self.tree.column("activo", width=100, anchor="center")

        scroll_y = ttk.Scrollbar(f_tabla, orient="vertical", command=self.tree.yview)
        self.tree.configure(yscrollcommand=scroll_y.set)

        self.tree.pack(side="left", fill="both", expand=True)
        scroll_y.pack(side="right", fill="y")

        self.tree.bind("<Double-1>", lambda e: self._abrir_modal_editar())

        self.cargar_datos()

    def _limpiar_filtros(self):
        self.ent_busqueda.delete(0, tk.END)
        self.var_filtro_activos.set(False)
        self.cargar_datos()

    def cargar_datos(self):
        query = self.ent_busqueda.get().strip()
        solo_activos = True if self.var_filtro_activos.get() else None

        for item in self.tree.get_children():
            self.tree.delete(item)

        miembros = self.service.buscar_y_filtrar(query=query, activo_filtro=solo_activos)
        for m in miembros:
            self.tree.insert("", "end", values=(
                m.id,
                m.nombre,
                m.correo,
                m.telefono,
                "Activo" if m.activo else "Inactivo"
            ))

    def _obtener_miembro_seleccionado(self) -> Optional[Miembro]:
        item = self.tree.selection()
        if not item:
            messagebox.showwarning("Selección requerida", "Por favor selecciona un miembro de la tabla.")
            return None
        miembro_id = int(self.tree.item(item, "values")[0])
        return self.service.obtener_miembro(miembro_id)

    def _abrir_modal_crear(self):
        FormularioMiembroModal(self.winfo_toplevel(), self.service, on_success=self.cargar_datos)

    def _abrir_modal_editar(self):
        miembro = self._obtener_miembro_seleccionado()
        if miembro:
            FormularioMiembroModal(self.winfo_toplevel(), self.service, miembro=miembro, on_success=self.cargar_datos)

    def _toggle_activo(self):
        miembro = self._obtener_miembro_seleccionado()
        if not miembro:
            return

        nuevo_estado = not miembro.activo
        accion = "activar" if nuevo_estado else "desactivar"

        confirmar = messagebox.askyesno(
            "Confirmación",
            f"¿Deseas {accion} a '{miembro.nombre}'?\n\n"
            "Nota: Si se desactiva, no podrá recibir asignaciones de nuevos tickets.",
            icon="question"
        )
        if not confirmar:
            return

        exito, mensaje = self.service.actualizar_miembro(
            miembro.id, miembro.nombre, miembro.correo, miembro.telefono, nuevo_estado
        )
        if exito:
            messagebox.showinfo("Éxito", f"Miembro {accion}do correctamente.")
            self.cargar_datos()
        else:
            messagebox.showerror("Error", mensaje)

    def _eliminar_miembro(self):
        miembro = self._obtener_miembro_seleccionado()
        if not miembro:
            return

        confirmar = messagebox.askyesno(
            "Confirmar Eliminación",
            f"¿Deseas eliminar permanentemente a '{miembro.nombre}'?\n\n"
            "Nota: Solo procederá si no tiene tickets asociados en el historial.",
            icon="warning"
        )
        if not confirmar:
            return

        exito, mensaje = self.service.eliminar_miembro(miembro.id)
        if exito:
            messagebox.showinfo("Éxito", mensaje)
            self.cargar_datos()
        else:
            messagebox.showerror("No se puede eliminar", mensaje)
