"""
ticket_view.py
--------------
Módulo central de gestión de Tickets:
- Demuestra la consulta con SQL JOIN en el Treeview mostrando
  el nombre real del Proyecto y del Miembro asignado.
- Controles de búsqueda y filtros combinados (Proyecto, Miembro, Prioridad, Estado).
- Modal para creación y edición cumpliendo todas las reglas de negocio:
  * Regla 1: No crear en proyectos cerrados.
  * Regla 2: No asignar a miembros inactivos.
  * Regla 3: Confirmación obligatoria al reabrir tickets Completados/Cancelados.
  * Regla 8: Registro automático de fecha de cierre.
"""

import tkinter as tk
from tkinter import ttk, messagebox
from datetime import datetime
from typing import Optional
from services.ticket_service import TicketService
from services.proyecto_service import ProyectoService
from services.miembro_service import MiembroService
from models.ticket import Ticket
from config import (
    COLOR_FONDO,
    COLOR_BLANCO,
    COLOR_TEXTO,
    COLOR_PRIMARIO,
    COLOR_PELIGRO,
    COLOR_EXITO,
    PRIORIDADES_TICKET,
    ESTADOS_TICKET,
)
from ui.styles import FONT_TITLE, FONT_SUBTITLE, FONT_REGULAR, FONT_BOLD, FONT_SMALL


class FormularioTicketModal(tk.Toplevel):
    """Diálogo modal para crear o editar un ticket con validaciones de negocio."""
    def __init__(
        self,
        parent,
        ticket_service: TicketService,
        proyecto_service: ProyectoService,
        miembro_service: MiembroService,
        ticket: Optional[Ticket] = None,
        on_success=None
    ):
        super().__init__(parent)
        self.ticket_service = ticket_service
        self.proyecto_service = proyecto_service
        self.miembro_service = miembro_service
        self.ticket = ticket
        self.on_success = on_success

        modo = "Editar Ticket" if ticket else "Nuevo Ticket"
        self.title(f"{modo} - Ticket Management System")
        self.geometry("560x580")
        self.resizable(False, False)
        self.configure(bg=COLOR_FONDO)
        self.grab_set()

        self._cargar_catalogos()
        self._construir_formulario()

    def _cargar_catalogos(self):
        """Carga proyectos y miembros disponibles según reglas."""
        # Si es nuevo, solo proyectos activos.
        self.proyectos = self.proyecto_service.listar_proyectos(solo_activos=True)
        # Si es nuevo, solo miembros activos (Regla 2).
        self.miembros = self.miembro_service.listar_miembros(solo_activos=True)

        # Mapeos para comboboxes: texto -> id
        self.map_proyectos = {f"#{p.id} - {p.nombre} ({p.estado})": p.id for p in self.proyectos}
        self.map_miembros = {f"#{m.id} - {m.nombre}": m.id for m in self.miembros}

    def _construir_formulario(self):
        frame = tk.Frame(self, bg=COLOR_BLANCO, bd=1, relief="solid", padx=20, pady=15)
        frame.pack(padx=20, pady=20, fill="both", expand=True)

        # Título del Ticket
        tk.Label(frame, text="Título del Ticket *", font=FONT_BOLD, bg=COLOR_BLANCO).pack(anchor="w")
        self.ent_titulo = ttk.Entry(frame, font=FONT_REGULAR)
        self.ent_titulo.pack(fill="x", pady=(2, 10))

        # Proyecto (Combobox)
        tk.Label(frame, text="Proyecto Asociado (Regla 1 y 5) *", font=FONT_BOLD, bg=COLOR_BLANCO).pack(anchor="w")
        self.combo_proyecto = ttk.Combobox(
            frame, values=list(self.map_proyectos.keys()), state="readonly", font=FONT_REGULAR
        )
        self.combo_proyecto.pack(fill="x", pady=(2, 10))

        # Miembro del Equipo (Combobox)
        tk.Label(frame, text="Miembro Asignado (Regla 2 y 6) *", font=FONT_BOLD, bg=COLOR_BLANCO).pack(anchor="w")
        self.combo_miembro = ttk.Combobox(
            frame, values=list(self.map_miembros.keys()), state="readonly", font=FONT_REGULAR
        )
        self.combo_miembro.pack(fill="x", pady=(2, 10))

        # Fila: Prioridad, Estado y Fecha Límite
        f_opciones = tk.Frame(frame, bg=COLOR_BLANCO)
        f_opciones.pack(fill="x", pady=(0, 10))

        # Prioridad
        tk.Label(f_opciones, text="Prioridad *", font=FONT_SMALL, bg=COLOR_BLANCO).grid(row=0, column=0, sticky="w")
        self.combo_prioridad = ttk.Combobox(
            f_opciones, values=PRIORIDADES_TICKET, state="readonly", font=FONT_REGULAR, width=12
        )
        self.combo_prioridad.grid(row=1, column=0, padx=(0, 10), pady=2)
        self.combo_prioridad.set(PRIORIDADES_TICKET[1])  # Media por defecto

        # Estado
        tk.Label(f_opciones, text="Estado *", font=FONT_SMALL, bg=COLOR_BLANCO).grid(row=0, column=1, sticky="w")
        self.combo_estado = ttk.Combobox(
            f_opciones, values=ESTADOS_TICKET, state="readonly", font=FONT_REGULAR, width=14
        )
        self.combo_estado.grid(row=1, column=1, padx=(0, 10), pady=2)
        self.combo_estado.set(ESTADOS_TICKET[0])  # Pendiente por defecto

        # Fecha Límite
        tk.Label(f_opciones, text="Fecha Límite (YYYY-MM-DD) *", font=FONT_SMALL, bg=COLOR_BLANCO).grid(row=0, column=2, sticky="w")
        self.ent_limite = ttk.Entry(f_opciones, font=FONT_REGULAR, width=16)
        self.ent_limite.grid(row=1, column=2, pady=2)

        # Descripción
        tk.Label(frame, text="Descripción Detallada", font=FONT_REGULAR, bg=COLOR_BLANCO).pack(anchor="w")
        self.txt_desc = tk.Text(frame, height=5, font=FONT_REGULAR, relief="groove", bd=1)
        self.txt_desc.pack(fill="both", expand=True, pady=(2, 15))

        # Botones
        f_botones = tk.Frame(frame, bg=COLOR_BLANCO)
        f_botones.pack(fill="x")

        ttk.Button(f_botones, text="Cancelar", command=self.destroy).pack(side="right", padx=5)
        btn_guardar = tk.Button(
            f_botones,
            text="Guardar Ticket",
            font=FONT_BOLD,
            bg=COLOR_PRIMARIO,
            fg=COLOR_BLANCO,
            command=self._guardar
        )
        btn_guardar.pack(side="right", padx=5)

        # Si editamos, poblar los valores
        if self.ticket:
            self.ent_titulo.insert(0, self.ticket.titulo)
            self.txt_desc.insert("1.0", self.ticket.descripcion)
            self.combo_prioridad.set(self.ticket.prioridad)
            self.combo_estado.set(self.ticket.estado)
            self.ent_limite.insert(0, self.ticket.fecha_limite)

            # Seleccionar proyecto
            for k, pid in self.map_proyectos.items():
                if pid == self.ticket.proyecto_id:
                    self.combo_proyecto.set(k)
                    break

            # Seleccionar miembro
            for k, mid in self.map_miembros.items():
                if mid == self.ticket.miembro_id:
                    self.combo_miembro.set(k)
                    break
        else:
            # Sugerir fecha límite a 7 días en el futuro
            from datetime import timedelta
            sugerida = (datetime.now() + timedelta(days=7)).strftime("%Y-%m-%d")
            self.ent_limite.insert(0, sugerida)

    def _guardar(self):
        titulo = self.ent_titulo.get().strip()
        proy_txt = self.combo_proyecto.get()
        miembro_txt = self.combo_miembro.get()
        prioridad = self.combo_prioridad.get()
        estado = self.combo_estado.get()
        limite = self.ent_limite.get().strip()
        desc = self.txt_desc.get("1.0", tk.END).strip()

        proyecto_id = self.map_proyectos.get(proy_txt, 0)
        miembro_id = self.map_miembros.get(miembro_txt, 0)

        confirmacion_reapertura = False

        if self.ticket:
            # Intentar actualizar
            exito, mensaje = self.ticket_service.actualizar_ticket(
                ticket_id=self.ticket.id,
                proyecto_id=proyecto_id,
                miembro_id=miembro_id,
                titulo=titulo,
                descripcion=desc,
                prioridad=prioridad,
                nuevo_estado=estado,
                fecha_limite=limite,
                confirmacion_reapertura=False
            )

            # Regla de Negocio 3: Si requiere confirmación para regresar a Pendiente
            if not exito and mensaje == "REQUIERE_CONFIRMACION_REAPERTURA":
                confirmar = messagebox.askyesno(
                    "Regla de Negocio 3: Confirmación de Reapertura",
                    f"El ticket '{self.ticket.titulo}' actualmente está {self.ticket.estado}.\n\n"
                    "¿Está seguro de que desea reabrirlo y regresarlo a estado Pendiente?",
                    icon="warning",
                    parent=self
                )
                if not confirmar:
                    return

                # Reintentar con confirmación concedida
                exito, mensaje = self.ticket_service.actualizar_ticket(
                    ticket_id=self.ticket.id,
                    proyecto_id=proyecto_id,
                    miembro_id=miembro_id,
                    titulo=titulo,
                    descripcion=desc,
                    prioridad=prioridad,
                    nuevo_estado=estado,
                    fecha_limite=limite,
                    confirmacion_reapertura=True
                )
        else:
            # Crear nuevo ticket
            exito, mensaje, _ = self.ticket_service.crear_ticket(
                proyecto_id=proyecto_id,
                miembro_id=miembro_id,
                titulo=titulo,
                descripcion=desc,
                prioridad=prioridad,
                estado=estado,
                fecha_limite=limite
            )

        if exito:
            messagebox.showinfo("Éxito", mensaje, parent=self)
            if self.on_success:
                self.on_success()
            self.destroy()
        else:
            messagebox.showerror("Error de Regla de Negocio", mensaje, parent=self)


class TicketView(ttk.Frame):
    def __init__(self, parent):
        super().__init__(parent)
        self.ticket_service = TicketService()
        self.proyecto_service = ProyectoService()
        self.miembro_service = MiembroService()
        self._construir_interfaz()

    def _construir_interfaz(self):
        # 1. Cabecera y acciones
        f_superior = tk.Frame(self, bg=COLOR_FONDO)
        f_superior.pack(fill="x", padx=25, pady=(20, 10))

        tk.Label(
            f_superior,
            text="Gestión de Tickets de Trabajo (SQL JOIN)",
            font=FONT_TITLE,
            bg=COLOR_FONDO,
            fg=COLOR_TEXTO
        ).pack(side="left")

        f_acciones = tk.Frame(f_superior, bg=COLOR_FONDO)
        f_acciones.pack(side="right")

        btn_nuevo = tk.Button(
            f_acciones,
            text="+ Nuevo Ticket",
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
        ttk.Button(f_acciones, text="Completar ✓", command=lambda: self._cambio_rapido_estado("Completado")).pack(side="left", padx=5)
        ttk.Button(f_acciones, text="Desactivar", command=self._desactivar_ticket).pack(side="left", padx=5)

        # 2. Barra de Búsqueda y Filtros Combinados (SQL JOIN)
        f_filtros = tk.Frame(self, bg=COLOR_BLANCO, bd=1, relief="solid", padx=15, pady=10)
        f_filtros.pack(fill="x", padx=25, pady=5)

        # Fila 1 de Filtros: Búsqueda y Proyecto
        f_f1 = tk.Frame(f_filtros, bg=COLOR_BLANCO)
        f_f1.pack(fill="x", pady=2)

        tk.Label(f_f1, text="Buscar por título/desc:", font=FONT_REGULAR, bg=COLOR_BLANCO).pack(side="left", padx=(0, 5))
        self.ent_busqueda = ttk.Entry(f_f1, width=28)
        self.ent_busqueda.pack(side="left", padx=5)
        self.ent_busqueda.bind("<KeyRelease>", lambda e: self.cargar_datos())

        tk.Label(f_f1, text="Proyecto:", font=FONT_REGULAR, bg=COLOR_BLANCO).pack(side="left", padx=(15, 5))
        self.proyectos_lista = self.proyecto_service.listar_proyectos()
        opciones_proy = ["Todos"] + [f"#{p.id} - {p.nombre}" for p in self.proyectos_lista]
        self.combo_filtro_proy = ttk.Combobox(f_f1, values=opciones_proy, state="readonly", width=25)
        self.combo_filtro_proy.set("Todos")
        self.combo_filtro_proy.pack(side="left", padx=5)
        self.combo_filtro_proy.bind("<<ComboboxSelected>>", lambda e: self.cargar_datos())

        # Fila 2 de Filtros: Miembro, Prioridad y Estado
        f_f2 = tk.Frame(f_filtros, bg=COLOR_BLANCO)
        f_f2.pack(fill="x", pady=(6, 2))

        tk.Label(f_f2, text="Miembro Asignado:", font=FONT_REGULAR, bg=COLOR_BLANCO).pack(side="left", padx=(0, 5))
        self.miembros_lista = self.miembro_service.listar_miembros()
        opciones_miem = ["Todos"] + [f"#{m.id} - {m.nombre}" for m in self.miembros_lista]
        self.combo_filtro_miem = ttk.Combobox(f_f2, values=opciones_miem, state="readonly", width=22)
        self.combo_filtro_miem.set("Todos")
        self.combo_filtro_miem.pack(side="left", padx=5)
        self.combo_filtro_miem.bind("<<ComboboxSelected>>", lambda e: self.cargar_datos())

        tk.Label(f_f2, text="Prioridad:", font=FONT_REGULAR, bg=COLOR_BLANCO).pack(side="left", padx=(15, 5))
        self.combo_filtro_prio = ttk.Combobox(f_f2, values=["Todas"] + PRIORIDADES_TICKET, state="readonly", width=10)
        self.combo_filtro_prio.set("Todas")
        self.combo_filtro_prio.pack(side="left", padx=5)
        self.combo_filtro_prio.bind("<<ComboboxSelected>>", lambda e: self.cargar_datos())

        tk.Label(f_f2, text="Estado:", font=FONT_REGULAR, bg=COLOR_BLANCO).pack(side="left", padx=(15, 5))
        self.combo_filtro_est = ttk.Combobox(f_f2, values=["Todos"] + ESTADOS_TICKET, state="readonly", width=12)
        self.combo_filtro_est.set("Todos")
        self.combo_filtro_est.pack(side="left", padx=5)
        self.combo_filtro_est.bind("<<ComboboxSelected>>", lambda e: self.cargar_datos())

        ttk.Button(f_f2, text="Limpiar Filtros", command=self._limpiar_filtros).pack(side="right")

        # 3. Treeview con SQL JOIN explícito
        f_tabla = tk.Frame(self, bg=COLOR_FONDO)
        f_tabla.pack(fill="both", expand=True, padx=25, pady=(5, 20))

        cols = ("id", "titulo", "proyecto", "miembro", "prioridad", "estado", "fecha_creacion", "fecha_limite", "fecha_cierre")
        self.tree = ttk.Treeview(f_tabla, columns=cols, show="headings")

        self.tree.heading("id", text="#")
        self.tree.heading("titulo", text="Título del Ticket")
        self.tree.heading("proyecto", text="Proyecto (SQL JOIN)")
        self.tree.heading("miembro", text="Miembro Asignado (SQL JOIN)")
        self.tree.heading("prioridad", text="Prioridad")
        self.tree.heading("estado", text="Estado")
        self.tree.heading("fecha_creacion", text="F. Creación")
        self.tree.heading("fecha_limite", text="F. Límite")
        self.tree.heading("fecha_cierre", text="F. Cierre (Regla 8)")

        self.tree.column("id", width=40, anchor="center")
        self.tree.column("titulo", width=220)
        self.tree.column("proyecto", width=180)
        self.tree.column("miembro", width=160)
        self.tree.column("prioridad", width=85, anchor="center")
        self.tree.column("estado", width=95, anchor="center")
        self.tree.column("fecha_creacion", width=85, anchor="center")
        self.tree.column("fecha_limite", width=85, anchor="center")
        self.tree.column("fecha_cierre", width=85, anchor="center")

        scroll_y = ttk.Scrollbar(f_tabla, orient="vertical", command=self.tree.yview)
        scroll_x = ttk.Scrollbar(f_tabla, orient="horizontal", command=self.tree.xview)
        self.tree.configure(yscrollcommand=scroll_y.set, xscrollcommand=scroll_x.set)

        self.tree.pack(side="left", fill="both", expand=True)
        scroll_y.pack(side="right", fill="y")
        scroll_x.pack(side="bottom", fill="x")

        self.tree.bind("<Double-1>", lambda e: self._abrir_modal_editar())

        self.cargar_datos()

    def _limpiar_filtros(self):
        self.ent_busqueda.delete(0, tk.END)
        self.combo_filtro_proy.set("Todos")
        self.combo_filtro_miem.set("Todos")
        self.combo_filtro_prio.set("Todas")
        self.combo_filtro_est.set("Todos")
        self.cargar_datos()

    def cargar_datos(self):
        """Consulta con filtros y repuebla la tabla de tickets con los datos de SQL JOIN."""
        query = self.ent_busqueda.get().strip()

        proy_sel = self.combo_filtro_proy.get()
        proy_id = int(proy_sel.split(" - ")[0].replace("#", "")) if proy_sel != "Todos" else None

        miem_sel = self.combo_filtro_miem.get()
        miem_id = int(miem_sel.split(" - ")[0].replace("#", "")) if miem_sel != "Todos" else None

        prio_sel = self.combo_filtro_prio.get()
        prio = prio_sel if prio_sel != "Todas" else ""

        est_sel = self.combo_filtro_est.get()
        estado = est_sel if est_sel != "Todos" else ""

        for item in self.tree.get_children():
            self.tree.delete(item)

        tickets = self.ticket_service.buscar_y_filtrar(
            query=query,
            proyecto_id=proy_id,
            miembro_id=miem_id,
            prioridad=prio,
            estado=estado,
            solo_activos=True
        )

        for t in tickets:
            self.tree.insert("", "end", values=(
                t.id,
                t.titulo,
                t.proyecto_nombre or f"#{t.proyecto_id}",
                t.miembro_nombre or f"#{t.miembro_id}",
                t.prioridad,
                t.estado,
                t.fecha_creacion,
                t.fecha_limite,
                t.fecha_cierre or "-"
            ))

    def _obtener_ticket_seleccionado(self) -> Optional[Ticket]:
        item = self.tree.selection()
        if not item:
            messagebox.showwarning("Selección requerida", "Por favor selecciona un ticket de la tabla.")
            return None
        ticket_id = int(self.tree.item(item, "values")[0])
        return self.ticket_service.obtener_ticket(ticket_id)

    def _abrir_modal_crear(self):
        FormularioTicketModal(
            self.winfo_toplevel(),
            self.ticket_service,
            self.proyecto_service,
            self.miembro_service,
            on_success=self.cargar_datos
        )

    def _abrir_modal_editar(self):
        ticket = self._obtener_ticket_seleccionado()
        if ticket:
            FormularioTicketModal(
                self.winfo_toplevel(),
                self.ticket_service,
                self.proyecto_service,
                self.miembro_service,
                ticket=ticket,
                on_success=self.cargar_datos
            )

    def _cambio_rapido_estado(self, nuevo_estado: str):
        ticket = self._obtener_ticket_seleccionado()
        if not ticket:
            return

        confirmar = messagebox.askyesno(
            "Confirmación",
            f"¿Deseas marcar el ticket #{ticket.id} '{ticket.titulo}' como '{nuevo_estado}'?",
            icon="question"
        )
        if not confirmar:
            return

        exito, mensaje = self.ticket_service.cambiar_estado(ticket.id, nuevo_estado)
        if exito:
            messagebox.showinfo("Éxito", mensaje)
            self.cargar_datos()
        else:
            messagebox.showerror("Error", mensaje)

    def _desactivar_ticket(self):
        ticket = self._obtener_ticket_seleccionado()
        if not ticket:
            return

        confirmar = messagebox.askyesno(
            "Confirmar Desactivación",
            f"¿Deseas desactivar el ticket #{ticket.id} '{ticket.titulo}'?",
            icon="warning"
        )
        if not confirmar:
            return

        exito, mensaje = self.ticket_service.desactivar_ticket(ticket.id)
        if exito:
            messagebox.showinfo("Éxito", mensaje)
            self.cargar_datos()
        else:
            messagebox.showerror("Error", mensaje)
