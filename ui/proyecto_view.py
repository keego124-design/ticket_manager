"""
proyecto_view.py
----------------
Vista para la gestión completa (CRUD) de Proyectos:
- Listado detallado en ttk.Treeview.
- Búsqueda en tiempo real y filtrado por estado.
- Formularios modales para Alta y Edición con validaciones.
- Cumplimiento de Regla 4: Bloqueo de eliminación si tiene tickets abiertos.
"""

import tkinter as tk
from tkinter import ttk, messagebox
from typing import Optional
from services.proyecto_service import ProyectoService
from models.proyecto import Proyecto
from config import (
    COLOR_FONDO,
    COLOR_BLANCO,
    COLOR_TEXTO,
    COLOR_PRIMARIO,
    COLOR_PELIGRO,
    COLOR_EXITO,
    ESTADOS_PROYECTO,
)
from ui.styles import FONT_TITLE, FONT_SUBTITLE, FONT_REGULAR, FONT_BOLD, FONT_SMALL


class FormularioProyectoModal(tk.Toplevel):
    """Diálogo modal para crear o editar un proyecto."""
    def __init__(self, parent, service: ProyectoService, proyecto: Optional[Proyecto] = None, on_success=None):
        super().__init__(parent)
        self.service = service
        self.proyecto = proyecto
        self.on_success = on_success

        modo = "Editar Proyecto" if proyecto else "Nuevo Proyecto"
        self.title(f"{modo} - Ticket Management System")
        self.geometry("480x420")
        self.resizable(False, False)
        self.configure(bg=COLOR_FONDO)
        self.grab_set()  # Hacerlo modal

        self._construir_formulario()

    def _construir_formulario(self):
        frame = tk.Frame(self, bg=COLOR_BLANCO, bd=1, relief="solid", padx=20, pady=15)
        frame.pack(padx=20, pady=20, fill="both", expand=True)

        # Nombre
        tk.Label(frame, text="Nombre del Proyecto *", font=FONT_BOLD, bg=COLOR_BLANCO).pack(anchor="w")
        self.ent_nombre = ttk.Entry(frame, font=FONT_REGULAR)
        self.ent_nombre.pack(fill="x", pady=(2, 10))

        # Descripción
        tk.Label(frame, text="Descripción", font=FONT_REGULAR, bg=COLOR_BLANCO).pack(anchor="w")
        self.ent_desc = tk.Text(frame, height=4, font=FONT_REGULAR, relief="groove", bd=1)
        self.ent_desc.pack(fill="x", pady=(2, 10))

        # Fechas (Inicio y Fin)
        f_fechas = tk.Frame(frame, bg=COLOR_BLANCO)
        f_fechas.pack(fill="x", pady=(0, 10))

        tk.Label(f_fechas, text="Fecha Inicio (YYYY-MM-DD) *", font=FONT_SMALL, bg=COLOR_BLANCO).grid(row=0, column=0, sticky="w")
        self.ent_inicio = ttk.Entry(f_fechas, font=FONT_REGULAR, width=18)
        self.ent_inicio.grid(row=1, column=0, padx=(0, 10), pady=2)

        tk.Label(f_fechas, text="Fecha Fin (YYYY-MM-DD) *", font=FONT_SMALL, bg=COLOR_BLANCO).grid(row=0, column=1, sticky="w")
        self.ent_fin = ttk.Entry(f_fechas, font=FONT_REGULAR, width=18)
        self.ent_fin.grid(row=1, column=1, pady=2)

        # Estado
        tk.Label(frame, text="Estado del Proyecto *", font=FONT_BOLD, bg=COLOR_BLANCO).pack(anchor="w")
        self.combo_estado = ttk.Combobox(frame, values=ESTADOS_PROYECTO, state="readonly", font=FONT_REGULAR)
        self.combo_estado.pack(fill="x", pady=(2, 10))
        self.combo_estado.set(ESTADOS_PROYECTO[0])

        # Checkbox Activo
        self.var_activo = tk.BooleanVar(value=True)
        self.chk_activo = ttk.Checkbutton(frame, text="Proyecto Activo en el sistema", variable=self.var_activo)
        self.chk_activo.pack(anchor="w", pady=(0, 15))

        # Botones Guardar / Cancelar
        f_botones = tk.Frame(frame, bg=COLOR_BLANCO)
        f_botones.pack(fill="x", pady=5)

        ttk.Button(f_botones, text="Cancelar", command=self.destroy).pack(side="right", padx=5)
        btn_guardar = tk.Button(
            f_botones,
            text="Guardar Proyecto",
            font=FONT_BOLD,
            bg=COLOR_PRIMARIO,
            fg=COLOR_BLANCO,
            command=self._guardar
        )
        btn_guardar.pack(side="right", padx=5)

        # Si estamos editando, cargar valores iniciales
        if self.proyecto:
            self.ent_nombre.insert(0, self.proyecto.nombre)
            self.ent_desc.insert("1.0", self.proyecto.descripcion)
            self.ent_inicio.insert(0, self.proyecto.fecha_inicio)
            self.ent_fin.insert(0, self.proyecto.fecha_fin)
            self.combo_estado.set(self.proyecto.estado)
            self.var_activo.set(self.proyecto.activo)

    def _guardar(self):
        nombre = self.ent_nombre.get().strip()
        desc = self.ent_desc.get("1.0", tk.END).strip()
        inicio = self.ent_inicio.get().strip()
        fin = self.ent_fin.get().strip()
        estado = self.combo_estado.get()
        activo = self.var_activo.get()

        if self.proyecto:
            exito, mensaje = self.service.actualizar_proyecto(
                self.proyecto.id, nombre, desc, inicio, fin, estado, activo
            )
        else:
            exito, mensaje, _ = self.service.crear_proyecto(
                nombre, desc, inicio, fin, estado, activo
            )

        if exito:
            messagebox.showinfo("Éxito", mensaje, parent=self)
            if self.on_success:
                self.on_success()
            self.destroy()
        else:
            messagebox.showerror("Error de Validación", mensaje, parent=self)


class ProyectoView(ttk.Frame):
    def __init__(self, parent):
        super().__init__(parent)
        self.service = ProyectoService()
        self._construir_interfaz()

    def _construir_interfaz(self):
        # 1. Título y botones de acción
        f_superior = tk.Frame(self, bg=COLOR_FONDO)
        f_superior.pack(fill="x", padx=25, pady=(20, 10))

        tk.Label(f_superior, text="Gestión de Proyectos", font=FONT_TITLE, bg=COLOR_FONDO, fg=COLOR_TEXTO).pack(side="left")

        f_acciones = tk.Frame(f_superior, bg=COLOR_FONDO)
        f_acciones.pack(side="right")

        btn_nuevo = tk.Button(
            f_acciones,
            text="+ Nuevo Proyecto",
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
        ttk.Button(f_acciones, text="Desactivar", command=self._desactivar_proyecto).pack(side="left", padx=5)
        ttk.Button(f_acciones, text="Eliminar", command=self._eliminar_proyecto).pack(side="left", padx=5)

        # 2. Barra de Búsqueda y Filtros
        f_filtros = tk.Frame(self, bg=COLOR_BLANCO, bd=1, relief="solid", padx=15, pady=8)
        f_filtros.pack(fill="x", padx=25, pady=5)

        tk.Label(f_filtros, text="Buscar:", font=FONT_REGULAR, bg=COLOR_BLANCO).pack(side="left", padx=(0, 5))
        self.ent_busqueda = ttk.Entry(f_filtros, width=25)
        self.ent_busqueda.pack(side="left", padx=5)
        self.ent_busqueda.bind("<KeyRelease>", lambda e: self.cargar_datos())

        tk.Label(f_filtros, text="Estado:", font=FONT_REGULAR, bg=COLOR_BLANCO).pack(side="left", padx=(15, 5))
        self.combo_filtro_estado = ttk.Combobox(
            f_filtros, values=["Todos"] + ESTADOS_PROYECTO, state="readonly", width=15
        )
        self.combo_filtro_estado.set("Todos")
        self.combo_filtro_estado.pack(side="left", padx=5)
        self.combo_filtro_estado.bind("<<ComboboxSelected>>", lambda e: self.cargar_datos())

        self.var_filtro_activos = tk.BooleanVar(value=False)
        chk_solo_activos = ttk.Checkbutton(
            f_filtros, text="Solo Activos", variable=self.var_filtro_activos, command=self.cargar_datos
        )
        chk_solo_activos.pack(side="left", padx=15)

        ttk.Button(f_filtros, text="Limpiar Filtros", command=self._limpiar_filtros).pack(side="right")

        # 3. Treeview de Proyectos
        f_tabla = tk.Frame(self, bg=COLOR_FONDO)
        f_tabla.pack(fill="both", expand=True, padx=25, pady=(5, 20))

        cols = ("id", "nombre", "descripcion", "fecha_inicio", "fecha_fin", "estado", "activo")
        self.tree = ttk.Treeview(f_tabla, columns=cols, show="headings")

        self.tree.heading("id", text="#")
        self.tree.heading("nombre", text="Nombre del Proyecto")
        self.tree.heading("descripcion", text="Descripción")
        self.tree.heading("fecha_inicio", text="Fecha Inicio")
        self.tree.heading("fecha_fin", text="Fecha Fin")
        self.tree.heading("estado", text="Estado")
        self.tree.heading("activo", text="Activo")

        self.tree.column("id", width=40, anchor="center")
        self.tree.column("nombre", width=220)
        self.tree.column("descripcion", width=300)
        self.tree.column("fecha_inicio", width=95, anchor="center")
        self.tree.column("fecha_fin", width=95, anchor="center")
        self.tree.column("estado", width=110, anchor="center")
        self.tree.column("activo", width=70, anchor="center")

        scroll_y = ttk.Scrollbar(f_tabla, orient="vertical", command=self.tree.yview)
        self.tree.configure(yscrollcommand=scroll_y.set)

        self.tree.pack(side="left", fill="both", expand=True)
        scroll_y.pack(side="right", fill="y")

        self.tree.bind("<Double-1>", lambda e: self._abrir_modal_editar())

        self.cargar_datos()

    def _limpiar_filtros(self):
        self.ent_busqueda.delete(0, tk.END)
        self.combo_filtro_estado.set("Todos")
        self.var_filtro_activos.set(False)
        self.cargar_datos()

    def cargar_datos(self):
        """Aplica filtros y repuebla el Treeview."""
        query = self.ent_busqueda.get().strip()
        estado = self.combo_filtro_estado.get()
        solo_activos = True if self.var_filtro_activos.get() else None

        for item in self.tree.get_children():
            self.tree.delete(item)

        proyectos = self.service.buscar_y_filtrar(query=query, estado=estado, activo_filtro=solo_activos)
        for p in proyectos:
            self.tree.insert("", "end", values=(
                p.id,
                p.nombre,
                p.descripcion,
                p.fecha_inicio,
                p.fecha_fin,
                p.estado,
                "Sí" if p.activo else "No"
            ))

    def _obtener_proyecto_seleccionado(self) -> Optional[Proyecto]:
        item = self.tree.selection()
        if not item:
            messagebox.showwarning("Selección requerida", "Por favor selecciona un proyecto de la tabla.")
            return None
        proyecto_id = int(self.tree.item(item, "values")[0])
        return self.service.obtener_proyecto(proyecto_id)

    def _abrir_modal_crear(self):
        FormularioProyectoModal(self.winfo_toplevel(), self.service, on_success=self.cargar_datos)

    def _abrir_modal_editar(self):
        proyecto = self._obtener_proyecto_seleccionado()
        if proyecto:
            FormularioProyectoModal(self.winfo_toplevel(), self.service, proyecto=proyecto, on_success=self.cargar_datos)

    def _desactivar_proyecto(self):
        proyecto = self._obtener_proyecto_seleccionado()
        if not proyecto:
            return

        confirmar = messagebox.askyesno(
            "Confirmación",
            f"¿Deseas cambiar el estado activo del proyecto '{proyecto.nombre}'?",
            icon="warning"
        )
        if not confirmar:
            return

        exito, mensaje = self.service.desactivar_proyecto(proyecto.id)
        if exito:
            messagebox.showinfo("Éxito", mensaje)
            self.cargar_datos()
        else:
            messagebox.showerror("No se puede desactivar", mensaje)

    def _eliminar_proyecto(self):
        proyecto = self._obtener_proyecto_seleccionado()
        if not proyecto:
            return

        confirmar = messagebox.askyesno(
            "Confirmación de Eliminación",
            f"¿Estás seguro de ELIMINAR permanentemente el proyecto '{proyecto.nombre}'?\n\n"
            "Nota: Solo procederá si no tiene tickets asociados en el sistema.",
            icon="warning"
        )
        if not confirmar:
            return

        exito, mensaje = self.service.eliminar_proyecto(proyecto.id)
        if exito:
            messagebox.showinfo("Éxito", mensaje)
            self.cargar_datos()
        else:
            messagebox.showerror("Regla de Negocio / Error", mensaje)
