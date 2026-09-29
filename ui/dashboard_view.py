"""
dashboard_view.py
-----------------
Panel principal de control (Dashboard):
- Métricas clave en tarjetas ejecutivas (KPIs).
- Lista de tickets urgentes o vencidos en tiempo real.
- Resumen visual del estado de salud del sistema.
"""

import tkinter as tk
from tkinter import ttk
from typing import Callable, Optional
from services.report_service import ReportService
from config import (
    COLOR_FONDO,
    COLOR_BLANCO,
    COLOR_TEXTO,
    COLOR_TEXTO_SECUNDARIO,
    COLOR_PRIMARIO,
    COLOR_PELIGRO,
    COLOR_EXITO,
    COLOR_ADVERTENCIA,
)
from ui.styles import FONT_TITLE, FONT_SUBTITLE, FONT_REGULAR, FONT_BOLD, FONT_KPI, FONT_SMALL


class DashboardView(ttk.Frame):
    def __init__(self, parent, on_navigate: Optional[Callable[[str], None]] = None):
        super().__init__(parent)
        self.on_navigate = on_navigate
        self.report_service = ReportService()
        self._construir_interfaz()

    def _construir_interfaz(self):
        # 1. Título del Dashboard
        frame_header = tk.Frame(self, bg=COLOR_FONDO)
        frame_header.pack(fill="x", padx=25, pady=(20, 10))

        tk.Label(
            frame_header,
            text="Panel de Control General",
            font=FONT_TITLE,
            bg=COLOR_FONDO,
            fg=COLOR_TEXTO
        ).pack(side="left")

        btn_refrescar = ttk.Button(frame_header, text="↻ Actualizar Métricas", command=self.cargar_datos)
        btn_refrescar.pack(side="right")

        # 2. Contenedor de Tarjetas KPI
        self.frame_kpis = tk.Frame(self, bg=COLOR_FONDO)
        self.frame_kpis.pack(fill="x", padx=25, pady=10)

        # 3. Sección inferior: Tickets urgentes / vencidos
        frame_inferior = tk.LabelFrame(
            self,
            text=" ⚠️ Atención Requerida: Tickets Vencidos o Próximos ",
            font=FONT_SUBTITLE,
            bg=COLOR_BLANCO,
            fg=COLOR_PELIGRO,
            padx=15,
            pady=15
        )
        frame_inferior.pack(fill="both", expand=True, padx=25, pady=(10, 20))

        # Tabla de tickets vencidos
        columnas = ("id", "titulo", "proyecto", "miembro", "prioridad", "fecha_limite", "estado")
        self.tree_vencidos = ttk.Treeview(frame_inferior, columns=columnas, show="headings", height=8)

        self.tree_vencidos.heading("id", text="#")
        self.tree_vencidos.heading("titulo", text="Título del Ticket")
        self.tree_vencidos.heading("proyecto", text="Proyecto Asociado (JOIN)")
        self.tree_vencidos.heading("miembro", text="Asignado a (JOIN)")
        self.tree_vencidos.heading("prioridad", text="Prioridad")
        self.tree_vencidos.heading("fecha_limite", text="Fecha Límite")
        self.tree_vencidos.heading("estado", text="Estado")

        self.tree_vencidos.column("id", width=40, anchor="center")
        self.tree_vencidos.column("titulo", width=220)
        self.tree_vencidos.column("proyecto", width=180)
        self.tree_vencidos.column("miembro", width=150)
        self.tree_vencidos.column("prioridad", width=90, anchor="center")
        self.tree_vencidos.column("fecha_limite", width=100, anchor="center")
        self.tree_vencidos.column("estado", width=100, anchor="center")

        scroll_y = ttk.Scrollbar(frame_inferior, orient="vertical", command=self.tree_vencidos.yview)
        self.tree_vencidos.configure(yscrollcommand=scroll_y.set)

        self.tree_vencidos.pack(side="left", fill="both", expand=True)
        scroll_y.pack(side="right", fill="y")

        self.cargar_datos()

    def _crear_kpi_card(self, parent, titulo: str, valor: str, color_borde: str, col: int):
        card = tk.Frame(parent, bg=COLOR_BLANCO, bd=1, relief="solid", padx=15, pady=12)
        card.grid(row=0, column=col, padx=8, pady=5, sticky="nsew")
        parent.columnconfigure(col, weight=1)

        # Barra de color superior decorativa
        barra = tk.Frame(card, bg=color_borde, height=4)
        barra.pack(fill="x", pady=(0, 6))

        tk.Label(card, text=titulo, font=FONT_SMALL, bg=COLOR_BLANCO, fg=COLOR_TEXTO_SECUNDARIO).pack(anchor="w")
        tk.Label(card, text=valor, font=FONT_KPI, bg=COLOR_BLANCO, fg=color_borde).pack(anchor="w", pady=(2, 0))

    def cargar_datos(self):
        """Consulta métricas y refresca las tarjetas y la tabla de tickets vencidos."""
        # Limpiar tarjetas anteriores
        for widget in self.frame_kpis.winfo_children():
            widget.destroy()

        summary = self.report_service.get_dashboard_summary()

        self._crear_kpi_card(self.frame_kpis, "Total Tickets", str(summary["total_tickets"]), COLOR_PRIMARIO, 0)
        self._crear_kpi_card(self.frame_kpis, "Tickets Abiertos", str(summary["tickets_abiertos"]), COLOR_ADVERTENCIA, 1)
        self._crear_kpi_card(self.frame_kpis, "Tickets Vencidos", str(summary["tickets_vencidos"]), COLOR_PELIGRO, 2)
        self._crear_kpi_card(self.frame_kpis, "Tickets Resueltos", str(summary["tickets_completados"]), COLOR_EXITO, 3)
        self._crear_kpi_card(self.frame_kpis, "Proyectos Activos", str(summary["total_proyectos_activos"]), "#5E35B1", 4)

        # Cargar tickets vencidos
        for item in self.tree_vencidos.get_children():
            self.tree_vencidos.delete(item)

        vencidos = self.report_service.get_overdue_tickets()
        for t in vencidos:
            self.tree_vencidos.insert("", "end", values=(
                t.id,
                t.titulo,
                t.proyecto_nombre or f"Proyecto #{t.proyecto_id}",
                t.miembro_nombre or f"Miembro #{t.miembro_id}",
                t.prioridad,
                t.fecha_limite,
                t.estado
            ))
