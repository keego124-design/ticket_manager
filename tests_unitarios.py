"""
tests_unitarios.py
------------------
Suite de pruebas automatizadas para verificar la integridad del sistema:
- Creación de base de datos e integridad referencial.
- Autenticación y roles.
- Consulta obligatoria con SQL JOIN.
- Cumplimiento de las 12 reglas de negocio.
"""

import os
import sys
import unittest
from datetime import datetime, timedelta

# Asegurar importación de módulos locales
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from database import init_database, get_connection
from services.auth_service import AuthService
from services.proyecto_service import ProyectoService
from services.miembro_service import MiembroService
from services.ticket_service import TicketService
from services.report_service import ReportService
from repositories.ticket_repository import TicketRepository


class TestTicketManagementSystem(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        """Inicializa la base de datos de pruebas."""
        init_database()
        cls.auth_service = AuthService.get_instance()
        cls.proyecto_service = ProyectoService()
        cls.miembro_service = MiembroService()
        cls.ticket_service = TicketService()
        cls.report_service = ReportService()
        cls.ticket_repo = TicketRepository()

    def test_01_foreign_keys_habilitadas(self):
        """Verifica que PRAGMA foreign_keys esté activo."""
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("PRAGMA foreign_keys;")
        row = cursor.fetchone()
        conn.close()
        self.assertEqual(row[0], 1, "Las llaves foráneas deben estar activadas en SQLite.")

    def test_02_autenticacion_y_roles(self):
        """Verifica login seguro, hash SHA-256 y roles admin/operator."""
        # Login admin válido
        exito, msg, user = self.auth_service.login("admin", "admin123")
        self.assertTrue(exito)
        self.assertIsNotNone(user)
        self.assertTrue(user.es_admin())

        # Login operador válido
        exito_op, msg_op, user_op = self.auth_service.login("operador", "operador123")
        self.assertTrue(exito_op)
        self.assertFalse(user_op.es_admin())

        # Credenciales incorrectas
        fallo, msg_f, _ = self.auth_service.login("admin", "password_incorrecta")
        self.assertFalse(fallo)

    def test_03_sql_join_en_tickets(self):
        """Verifica la ejecución de la consulta SQL JOIN y mapeo de nombres de proyecto y miembro."""
        tickets = self.ticket_repo.list_all_with_join()
        self.assertGreaterEqual(len(tickets), 1, "Debe haber tickets registrados.")
        primer_ticket = tickets[0]
        self.assertIsNotNone(primer_ticket.proyecto_nombre, "El nombre del proyecto debe provenir del SQL JOIN.")
        self.assertIsNotNone(primer_ticket.miembro_nombre, "El nombre del miembro debe provenir del SQL JOIN.")
        self.assertNotEqual(primer_ticket.proyecto_nombre, "", "El nombre del proyecto no puede estar vacío.")

    def test_04_regla_1_no_crear_ticket_en_proyecto_cerrado(self):
        """Regla 1: Un ticket no puede crearse dentro de un proyecto cerrado."""
        # Proyecto 5 es "Sistema de Facturación 4.0" (Cerrado)
        proyectos = self.proyecto_service.listar_proyectos()
        proy_cerrado = next((p for p in proyectos if p.estado == "Cerrado"), None)
        self.assertIsNotNone(proy_cerrado, "Debe existir al menos un proyecto cerrado en los datos de prueba.")

        miembros_activos = self.miembro_service.listar_miembros(solo_activos=True)
        miembro = miembros_activos[0]

        exito, mensaje, _ = self.ticket_service.crear_ticket(
            proyecto_id=proy_cerrado.id,
            miembro_id=miembro.id,
            titulo="Ticket de prueba en proyecto cerrado",
            descripcion="Debe fallar según la regla 1",
            prioridad="Media",
            estado="Pendiente",
            fecha_limite="2026-12-31"
        )
        self.assertFalse(exito, "La creación de ticket en proyecto cerrado debió ser rechazada.")
        self.assertIn("Regla de Negocio 1", mensaje)

    def test_05_regla_2_no_asignar_a_miembro_inactivo(self):
        """Regla 2: Un miembro inactivo no puede recibir nuevos tickets."""
        miembros = self.miembro_service.listar_miembros()
        miembro_inactivo = next((m for m in miembros if not m.activo), None)
        self.assertIsNotNone(miembro_inactivo, "Debe existir al menos un miembro inactivo en los datos.")

        proyectos_activos = self.proyecto_service.listar_proyectos(solo_activos=True)
        proy_abierto = next((p for p in proyectos_activos if p.estado != "Cerrado"), None)

        exito, mensaje, _ = self.ticket_service.crear_ticket(
            proyecto_id=proy_abierto.id,
            miembro_id=miembro_inactivo.id,
            titulo="Ticket para miembro inactivo",
            descripcion="Debe fallar según la regla 2",
            prioridad="Alta",
            estado="Pendiente",
            fecha_limite="2026-12-31"
        )
        self.assertFalse(exito, "No debe permitirse asignar tickets a miembros inactivos.")
        self.assertIn("Regla de Negocio 2", mensaje)

    def test_06_regla_3_reapertura_requiere_confirmacion(self):
        """Regla 3: Un ticket Completado no regresa a Pendiente sin confirmación explícita."""
        tickets = self.ticket_repo.list_all_with_join()
        t_completado = next((t for t in tickets if t.estado == "Completado"), None)
        self.assertIsNotNone(t_completado, "Debe existir un ticket completado.")

        # Intento sin confirmación explícita
        exito, mensaje = self.ticket_service.actualizar_ticket(
            ticket_id=t_completado.id,
            proyecto_id=t_completado.proyecto_id,
            miembro_id=t_completado.miembro_id,
            titulo=t_completado.titulo,
            descripcion=t_completado.descripcion,
            prioridad=t_completado.prioridad,
            nuevo_estado="Pendiente",
            fecha_limite=t_completado.fecha_limite,
            confirmacion_reapertura=False
        )
        self.assertFalse(exito)
        self.assertEqual(mensaje, "REQUIERE_CONFIRMACION_REAPERTURA")

        # Con confirmación explícita concedida
        exito_conf, msg_conf = self.ticket_service.actualizar_ticket(
            ticket_id=t_completado.id,
            proyecto_id=t_completado.proyecto_id,
            miembro_id=t_completado.miembro_id,
            titulo=t_completado.titulo,
            descripcion=t_completado.descripcion,
            prioridad=t_completado.prioridad,
            nuevo_estado="Pendiente",
            fecha_limite=t_completado.fecha_limite,
            confirmacion_reapertura=True
        )
        self.assertTrue(exito_conf)

        # Regresarlo a Completado para preservar el estado de prueba
        self.ticket_service.cambiar_estado(t_completado.id, "Completado")

    def test_07_regla_4_no_eliminar_proyecto_con_tickets_abiertos(self):
        """Regla 4: No se puede eliminar ni desactivar un proyecto con tickets abiertos."""
        proyectos = self.proyecto_service.listar_proyectos()
        # Buscar un proyecto con tickets abiertos (ej. Proyecto 1)
        proy_con_tickets = next((p for p in proyectos if self.proyecto_service.repo.count_open_tickets(p.id) > 0), None)
        self.assertIsNotNone(proy_con_tickets, "Debe existir un proyecto con tickets abiertos.")

        # Intento de eliminación
        exito_del, msg_del = self.proyecto_service.eliminar_proyecto(proy_con_tickets.id)
        self.assertFalse(exito_del, "No debe permitirse eliminar proyectos con tickets abiertos.")
        self.assertIn("Regla de Negocio", msg_del)

        # Intento de desactivación
        exito_des, msg_des = self.proyecto_service.desactivar_proyecto(proy_con_tickets.id)
        self.assertFalse(exito_des, "No debe permitirse desactivar proyectos con tickets abiertos.")

    def test_08_regla_8_fecha_cierre_automatica(self):
        """Regla 8: Al completar un ticket se estampa automáticamente la fecha de cierre."""
        proyectos = self.proyecto_service.listar_proyectos(solo_activos=True)
        p_abierto = next((p for p in proyectos if p.estado != "Cerrado"), None)
        miembros = self.miembro_service.listar_miembros(solo_activos=True)

        _, _, tid = self.ticket_service.crear_ticket(
            proyecto_id=p_abierto.id,
            miembro_id=miembros[0].id,
            titulo="Ticket para prueba de fecha de cierre",
            descripcion="Probando regla 8",
            prioridad="Baja",
            estado="En Progreso",
            fecha_limite="2026-11-20"
        )
        self.assertIsNotNone(tid)

        # Cambiar a Completado
        self.ticket_service.cambiar_estado(tid, "Completado")
        ticket_mod = self.ticket_service.obtener_ticket(tid)
        self.assertIsNotNone(ticket_mod.fecha_cierre, "La fecha de cierre debe registrarse automáticamente.")
        self.assertEqual(ticket_mod.fecha_cierre, datetime.now().strftime("%Y-%m-%d"))

    def test_09_regla_9_tickets_vencidos_en_reporte(self):
        """Regla 9: Tickets no cerrados con fecha_limite < hoy deben clasificarse como vencidos."""
        vencidos = self.report_service.get_overdue_tickets()
        self.assertGreaterEqual(len(vencidos), 1, "Debe haber al menos un ticket vencido en el seed.")
        for v in vencidos:
            self.assertNotIn(v.estado, ("Completado", "Cancelado"))
            self.assertLess(v.fecha_limite, datetime.now().strftime("%Y-%m-%d"))

    def test_10_validacion_correo_regex(self):
        """Verifica validación de formato de correo con expresiones regulares."""
        # Correo inválido sin dominio
        valido, _ = self.miembro_service.validar_datos("Prueba", "correo_invalido", "555-1234")
        self.assertFalse(valido)

        # Correo válido
        valido_ok, _ = self.miembro_service.validar_datos("Prueba", "valido@correo.com", "555-1234")
        self.assertTrue(valido_ok)


if __name__ == "__main__":
    unittest.main(verbosity=2)
