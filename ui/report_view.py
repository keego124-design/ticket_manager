"""
report_view.py
--------------
Módulo de Reportes Analíticos del Sistema:
Implementa todos los reportes solicitados mediante consultas SQL agregadas y JOIN:
A. Tickets Abiertos
B. Tickets Vencidos (Overdue)
C. Conteo agrupado por Estado (con gráfico de barras nativo en Canvas)
D. Conteo agrupado por Proyecto (con gráfico de barras nativo en Canvas)
E. Conteo agrupado por Prioridad (con gráfico de barras nativo en Canvas)
"""

import tkinter as tk
from tkinter import ttk
from typing import List, Dict, Any
from services.report_service import ReportService
from config import (
    COLOR_FONDO,
    COLOR_BLANCO,
    COLOR_TEXTO,
    COLOR_PRIMARIO,
    COLOR_PELIGRO,
    COLOR_EXITO,
    COLOR_ADVERTENCIA,
    COLOR_BORDE,
)
from ui.styles import FONT_TITLE, FONT_SUBTITLE, FONT_REGULAR, FONT_BOLD, FONT_SMALL


class ReportView(ttk.Frame):
    def __init__(self, parent):
        super().__init__(parent)
        self.report_service = ReportService()
        self._construir_interfaz()

    def _construir_interfaz(self):
        # 1. Cabecera
        f_header = tk.Frame(self, bg=COLOR_FONDO)
        f_header.pack(fill="x", padx=25, pady=(20, 10))

        tk.Label(
            f_header,
            text="Centro de Reportes y Estadísticas del Sistema",
            font=FONT_TITLE,
            bg=COLOR_FONDO,
            fg=COLOR_TEXTO
        ).pack(side="left")

        btn_actualizar = ttk.Button(f_header, text="↻ Actualizar Reportes", command=self.actualizar_todos_los_reportes)
        btn_actualizar.pack(side="right")

        # 2. Pestañas (Notebook) para cada reporte
        self.notebook = ttk.Notebook(self)
        self.notebook.pack(fill="both", expand=True, padx=25, pady=(5, 20))

        # Pestaña B: Tickets Vencidos (Overdue)
        self.tab_vencidos = ttk.Frame(self.notebook)
        self.notebook.add(self.tab_vencidos, text=" ⚠️ Tickets Vencidos (Overdue) ")
        self._construir_tab_vencidos()

        # Pestaña A: Tickets Abiertos
        self.tab_abiertos = ttk.Frame(self.notebook)
        self.notebook.add(self.tab_abiertos, text=" 📋 Tickets Abiertos ")
        self._construir_tab_abiertos()

        # Pestaña C: Por Estado
        self.tab_estados = ttk.Frame(self.notebook)
        self.notebook.add(self.tab_estados, text=" 📊 Por Estado ")
        self._construir_tab_estadistica(self.tab_estados, "estado", self._cargar_reporte_estado)

        # Pestaña D: Por Proyecto
        self.tab_proyectos = ttk.Frame(self.notebook)
        self.notebook.add(self.tab_proyectos, text=" 📁 Por Proyecto ")
        self._construir_tab_estadistica(self.tab_proyectos, "proyecto", self._cargar_reporte_proyecto)

        # Pestaña E: Por Prioridad
        self.tab_prioridad = ttk.Frame(self.notebook)
        self.notebook.add(self.tab_prioridad, text=" 🎯 Por Prioridad ")
        self._construir_tab_estadistica(self.tab_prioridad, "prioridad", self._cargar_reporte_prioridad)

        self.actualizar_todos_los_reportes()

    # -------------------------------------------------------------
    # TAB B: TICKETS VENCIDOS (OVERDUE)
    # -------------------------------------------------------------
    def _construir_tab_vencidos(self):
        f = tk.Frame(self.tab_vencidos, bg=COLOR_BLANCO, padx=15, pady=15)
        f.pack(fill="both", expand=True)

        tk.Label(
            f,
            text="Reporte B: Tickets cuya fecha límite ha expirado y no se han completado ni cancelado",
            font=FONT_SUBTITLE,
            bg=COLOR_BLANCO,
            fg=COLOR_PELIGRO
        ).pack(anchor="w", pady=(0, 10))

        cols = ("id", "titulo", "proyecto", "miembro", "prioridad", "fecha_limite", "estado")
        self.tree_vencidos = ttk.Treeview(f, columns=cols, show="headings")

        self.tree_vencidos.heading("id", text="#")
        self.tree_vencidos.heading("titulo", text="Título del Ticket")
        self.tree_vencidos.heading("proyecto", text="Proyecto Asociado (JOIN)")
        self.tree_vencidos.heading("miembro", text="Asignado a (JOIN)")
        self.tree_vencidos.heading("prioridad", text="Prioridad")
        self.tree_vencidos.heading("fecha_limite", text="Fecha Límite Vencida")
        self.tree_vencidos.heading("estado", text="Estado Actual")

        self.tree_vencidos.column("id", width=40, anchor="center")
        self.tree_vencidos.column("titulo", width=220)
        self.tree_vencidos.column("proyecto", width=180)
        self.tree_vencidos.column("miembro", width=150)
        self.tree_vencidos.column("prioridad", width=90, anchor="center")
        self.tree_vencidos.column("fecha_limite", width=120, anchor="center")
        self.tree_vencidos.column("estado", width=100, anchor="center")

        scroll = ttk.Scrollbar(f, orient="vertical", command=self.tree_vencidos.yview)
        self.tree_vencidos.configure(yscrollcommand=scroll.set)

        self.tree_vencidos.pack(side="left", fill="both", expand=True)
        scroll.pack(side="right", fill="y")

    # -------------------------------------------------------------
    # TAB A: TICKETS ABIERTOS
    # -------------------------------------------------------------
    def _construir_tab_abiertos(self):
        f = tk.Frame(self.tab_abiertos, bg=COLOR_BLANCO, padx=15, pady=15)
        f.pack(fill="both", expand=True)

        tk.Label(
            f,
            text="Reporte A: Todos los tickets en estado activo (Pendiente o En Progreso)",
            font=FONT_SUBTITLE,
            bg=COLOR_BLANCO,
            fg=COLOR_PRIMARIO
        ).pack(anchor="w", pady=(0, 10))

        cols = ("id", "titulo", "proyecto", "miembro", "prioridad", "estado", "fecha_limite")
        self.tree_abiertos = ttk.Treeview(f, columns=cols, show="headings")

        self.tree_abiertos.heading("id", text="#")
        self.tree_abiertos.heading("titulo", text="Título del Ticket")
        self.tree_abiertos.heading("proyecto", text="Proyecto Asociado (JOIN)")
        self.tree_abiertos.heading("miembro", text="Miembro Asignado (JOIN)")
        self.tree_abiertos.heading("prioridad", text="Prioridad")
        self.tree_abiertos.heading("estado", text="Estado")
        self.tree_abiertos.heading("fecha_limite", text="Fecha Límite")

        self.tree_abiertos.column("id", width=40, anchor="center")
        self.tree_abiertos.column("titulo", width=220)
        self.tree_abiertos.column("proyecto", width=180)
        self.tree_abiertos.column("miembro", width=150)
        self.tree_abiertos.column("prioridad", width=90, anchor="center")
        self.tree_abiertos.column("estado", width=100, anchor="center")
        self.tree_abiertos.column("fecha_limite", width=100, anchor="center")

        scroll = ttk.Scrollbar(f, orient="vertical", command=self.tree_abiertos.yview)
        self.tree_abiertos.configure(yscrollcommand=scroll.set)

        self.tree_abiertos.pack(side="left", fill="both", expand=True)
        scroll.pack(side="right", fill="y")

    # -------------------------------------------------------------
    # CONSTRUCTOR GENÉRICO PARA REPORTES CON GRÁFICO NATIVO
    # -------------------------------------------------------------
    def _construir_tab_estadistica(self, tab, nombre_columna: str, cargar_callback):
        f = tk.Frame(tab, bg=COLOR_BLANCO, padx=15, pady=15)
        f.pack(fill="both", expand=True)

        f_izq = tk.Frame(f, bg=COLOR_BLANCO, width=300)
        f_izq.pack(side="left", fill="both", padx=(0, 10))

        cols = (nombre_columna, "total")
        tree = ttk.Treeview(f_izq, columns=cols, show="headings", height=10)
        tree.heading(nombre_columna, text=nombre_columna.capitalize())
        tree.heading("total", text="Total Tickets")
        tree.column(nombre_columna, width=180)
        tree.column("total", width=90, anchor="center")
        tree.pack(fill="both", expand=True)

        f_der = tk.Frame(f, bg=COLOR_BLANCO)
        f_der.pack(side="right", fill="both", expand=True)

        tk.Label(f_der, text=f"Distribución Visual de Tickets por {nombre_columna.capitalize()}", font=FONT_BOLD, bg=COLOR_BLANCO).pack(anchor="w", pady=(0, 5))
        canvas = tk.Canvas(f_der, bg="#fafafa", bd=1, relief="solid")
        canvas.pack(fill="both", expand=True)

        tab._tree = tree
        tab._canvas = canvas
        tab._cargar = cargar_callback

    def _dibujar_barras(self, canvas: tk.Canvas, datos: List[Dict[str, Any]], clave_etiqueta: str, color_barra: str):
        """Dibuja un gráfico de barras vectorial nativo en Canvas sin dependencias externas."""
        canvas.delete("all")
        ancho = canvas.winfo_width() or 400
        alto = canvas.winfo_height() or 250

        if not datos:
            canvas.create_text(ancho // 2, alto // 2, text="No hay datos para mostrar", font=FONT_REGULAR, fill=COLOR_TEXTO)
            return

        max_val = max((d["total"] for d in datos), default=1)
        if max_val == 0:
            max_val = 1

        n = len(datos)
        margen_izq = 50
        margen_der = 20
        margen_arriba = 20
        margen_abajo = 40

        ancho_disp = ancho - margen_izq - margen_der
        alto_disp = alto - margen_arriba - margen_abajo

        ancho_barra = max(15, min(45, (ancho_disp // (n * 2))))
        espacio = (ancho_disp - (n * ancho_barra)) // (n + 1)

        # Eje base horizontal
        y_base = alto - margen_abajo
        canvas.create_line(margen_izq, y_base, ancho - margen_der, y_base, fill=COLOR_BORDE, width=2)

        x_actual = margen_izq + espacio

        colores = [COLOR_PRIMARIO, COLOR_EXITO, COLOR_ADVERTENCIA, COLOR_PELIGRO, "#8E24AA", "#00897B"]

        for i, item in enumerate(datos):
            val = item["total"]
            altura_barra = int((val / max_val) * (alto_disp - 20))
            y_top = y_base - altura_barra

            color = colores[i % len(colores)]

            # Rectángulo de la barra
            canvas.create_rectangle(
                x_actual, y_top, x_actual + ancho_barra, y_base,
                fill=color, outline="#ffffff", width=1
            )

            # Etiqueta de cantidad encima de la barra
            canvas.create_text(
                x_actual + (ancho_barra // 2), y_top - 10,
                text=str(val), font=FONT_BOLD, fill=COLOR_TEXTO
            )

            # Etiqueta de nombre abajo
            etiqueta = str(item[clave_etiqueta])
            if len(etiqueta) > 10:
                etiqueta = etiqueta[:9] + "…"

            canvas.create_text(
                x_actual + (ancho_barra // 2), y_base + 15,
                text=etiqueta, font=FONT_SMALL, fill=COLOR_TEXTO
            )

            x_actual += ancho_barra + espacio

    def _cargar_reporte_estado(self):
        tree = self.tab_estados._tree
        canvas = self.tab_estados._canvas
        for item in tree.get_children():
            tree.delete(item)

        datos = self.report_service.get_tickets_by_status()
        for d in datos:
            tree.insert("", "end", values=(d["estado"], d["total"]))

        self.after(50, lambda: self._dibujar_barras(canvas, datos, "estado", COLOR_PRIMARIO))

    def _cargar_reporte_proyecto(self):
        tree = self.tab_proyectos._tree
        canvas = self.tab_proyectos._canvas
        for item in tree.get_children():
            tree.delete(item)

        datos = self.report_service.get_tickets_by_project()
        for d in datos:
            tree.insert("", "end", values=(d["proyecto"], d["total"]))

        self.after(50, lambda: self._dibujar_barras(canvas, datos, "proyecto", COLOR_EXITO))

    def _cargar_reporte_prioridad(self):
        tree = self.tab_prioridad._tree
        canvas = self.tab_prioridad._canvas
        for item in tree.get_children():
            tree.delete(item)

        datos = self.report_service.get_tickets_by_priority()
        for d in datos:
            tree.insert("", "end", values=(d["prioridad"], d["total"]))

        self.after(50, lambda: self._dibujar_barras(canvas, datos, "prioridad", COLOR_ADVERTENCIA))

    def actualizar_todos_los_reportes(self):
        """Refresca todos los datos de los 5 reportes."""
        # 1. Vencidos
        for item in self.tree_vencidos.get_children():
            self.tree_vencidos.delete(item)
        for t in self.report_service.get_overdue_tickets():
            self.tree_vencidos.insert("", "end", values=(
                t.id,
                t.titulo,
                t.proyecto_nombre or f"#{t.proyecto_id}",
                t.miembro_nombre or f"#{t.miembro_id}",
                t.prioridad,
                t.fecha_limite,
                t.estado
            ))

        # 2. Abiertos
        for item in self.tree_abiertos.get_children():
            self.tree_abiertos.delete(item)
        for t in self.report_service.get_open_tickets():
            self.tree_abiertos.insert("", "end", values=(
                t.id,
                t.titulo,
                t.proyecto_nombre or f"#{t.proyecto_id}",
                t.miembro_nombre or f"#{t.miembro_id}",
                t.prioridad,
                t.estado,
                t.fecha_limite
            ))

        # 3. Gráficos y agrupaciones
        self._cargar_reporte_estado()
        self._cargar_reporte_proyecto()
        self._cargar_reporte_prioridad()
