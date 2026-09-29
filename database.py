"""
database.py
-----------
Manejo centralizado de la base de datos SQLite3:
- Apertura de conexiones con integridad referencial activa (PRAGMA foreign_keys = ON).
- Creación de tablas, restricciones e índices.
- Precarga automática de datos de prueba si la base de datos está vacía.
"""

import sqlite3
import hashlib
from datetime import datetime, timedelta
from config import DB_PATH, ROLE_ADMIN, ROLE_OPERATOR


def get_connection():
    """Retorna una conexión a SQLite con soporte de llaves foráneas y row_factory."""
    conn = sqlite3.connect(DB_PATH)
    conn.execute("PRAGMA foreign_keys = ON;")
    conn.row_factory = sqlite3.Row
    return conn


def hash_password(password: str) -> str:
    """Calcula el hash SHA-256 de una contraseña en texto plano."""
    return hashlib.sha256(password.encode("utf-8")).hexdigest()


def init_database():
    """Crea las tablas necesarias si no existen e inserta datos iniciales si está vacía."""
    conn = get_connection()
    cursor = conn.cursor()

    # 1. Tabla de Usuarios del Sistema
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS usuarios_sistema (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            password_hash TEXT NOT NULL,
            role TEXT NOT NULL CHECK(role IN ('admin', 'operator')),
            active INTEGER NOT NULL DEFAULT 1
        );
    """)

    # 2. Tabla de Proyectos
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS proyectos (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nombre TEXT NOT NULL,
            descripcion TEXT,
            fecha_inicio TEXT NOT NULL,
            fecha_fin TEXT NOT NULL,
            estado TEXT NOT NULL,
            activo INTEGER NOT NULL DEFAULT 1
        );
    """)

    # 3. Tabla de Miembros del Equipo
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS miembros (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nombre TEXT NOT NULL,
            correo TEXT UNIQUE NOT NULL,
            telefono TEXT,
            activo INTEGER NOT NULL DEFAULT 1
        );
    """)

    # 4. Tabla de Tickets
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS tickets (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            proyecto_id INTEGER NOT NULL,
            miembro_id INTEGER NOT NULL,
            titulo TEXT NOT NULL,
            descripcion TEXT,
            prioridad TEXT NOT NULL,
            estado TEXT NOT NULL,
            fecha_creacion TEXT NOT NULL,
            fecha_limite TEXT NOT NULL,
            fecha_cierre TEXT,
            activo INTEGER NOT NULL DEFAULT 1,
            FOREIGN KEY (proyecto_id) REFERENCES proyectos (id) ON DELETE RESTRICT,
            FOREIGN KEY (miembro_id) REFERENCES miembros (id) ON DELETE RESTRICT
        );
    """)

    # Índices útiles para acelerar búsquedas y filtros
    cursor.execute("CREATE INDEX IF NOT EXISTS idx_tickets_proyecto ON tickets(proyecto_id);")
    cursor.execute("CREATE INDEX IF NOT EXISTS idx_tickets_miembro ON tickets(miembro_id);")
    cursor.execute("CREATE INDEX IF NOT EXISTS idx_tickets_estado ON tickets(estado);")
    cursor.execute("CREATE INDEX IF NOT EXISTS idx_proyectos_estado ON proyectos(estado);")

    conn.commit()

    # Comprobar si se requieren datos de prueba
    cursor.execute("SELECT COUNT(*) AS total FROM usuarios_sistema;")
    total_usuarios = cursor.fetchone()["total"]

    if total_usuarios == 0:
        _insertar_datos_semilla(cursor)
        conn.commit()

    conn.close()


def _insertar_datos_semilla(cursor):
    """Inserta datos de prueba completos cumpliendo todas las reglas de negocio."""
    print("[+] Inicializando base de datos con datos de prueba...")

    # A. Usuarios iniciales (admin y operator)
    usuarios = [
        ("admin", hash_password("admin123"), ROLE_ADMIN, 1),
        ("operador", hash_password("operador123"), ROLE_OPERATOR, 1),
    ]
    cursor.executemany("""
        INSERT INTO usuarios_sistema (username, password_hash, role, active)
        VALUES (?, ?, ?, ?);
    """, usuarios)

    # B. Proyectos iniciales (8 proyectos con estados variados)
    hoy = datetime.now()
    fecha_hace_60d = (hoy - timedelta(days=60)).strftime("%Y-%m-%d")
    fecha_hace_30d = (hoy - timedelta(days=30)).strftime("%Y-%m-%d")
    fecha_hoy = hoy.strftime("%Y-%m-%d")
    fecha_en_15d = (hoy + timedelta(days=15)).strftime("%Y-%m-%d")
    fecha_en_30d = (hoy + timedelta(days=30)).strftime("%Y-%m-%d")
    fecha_en_60d = (hoy + timedelta(days=60)).strftime("%Y-%m-%d")

    proyectos = [
        ("Plataforma E-Commerce B2B", "Desarrollo de marketplace institucional con pasarela de pagos.", fecha_hace_60d, fecha_en_30d, "En Progreso", 1),
        ("App Móvil de Entregas", "Aplicación móvil en Flutter para seguimiento de paquetes en tiempo real.", fecha_hace_30d, fecha_en_60d, "En Progreso", 1),
        ("Migración Cloud AWS", "Pase de infraestructura física local a contenedores ECS y base RDS.", fecha_hace_60d, fecha_hace_30d, "Completado", 1),
        ("Portal de Recursos Humanos", "Módulo de gestión de vacaciones, nóminas y expedientes.", fecha_hoy, fecha_en_60d, "Planificación", 1),
        ("Sistema de Facturación 4.0", "Emisión electrónica de CFDI y reportes fiscales automáticos.", fecha_hace_60d, fecha_hace_30d, "Cerrado", 1),
        ("Integración API Bancaria", "Conexión directa vía webhooks con servicios financieros.", fecha_hace_30d, fecha_en_15d, "En Progreso", 1),
        ("Panel Analítico de Ventas", "Dashboard de métricas con exportación a Excel y PDF.", fecha_hoy, fecha_en_30d, "Planificación", 1),
        ("Auditoría de Seguridad y Pentesting", "Revisión integral de vulnerabilidades en servicios web.", fecha_hace_60d, fecha_hace_30d, "Completado", 1),
    ]
    cursor.executemany("""
        INSERT INTO proyectos (nombre, descripcion, fecha_inicio, fecha_fin, estado, activo)
        VALUES (?, ?, ?, ?, ?, ?);
    """, proyectos)

    # C. Miembros del equipo (5 miembros, al menos 1 inactivo)
    miembros = [
        ("Ing. Roberto Morales", "roberto.morales@empresa.com", "555-102-9901", 1),
        ("Lic. Carolina Herrera", "carolina.herrera@empresa.com", "555-204-8812", 1),
        ("Mtro. Daniel Espinoza", "daniel.espinoza@empresa.com", "555-306-7723", 1),
        ("Ing. Sofia Valenzuela", "sofia.valenzuela@empresa.com", "555-408-6634", 1),
        ("Tec. Miguel Angel Rios", "miguel.rios@empresa.com", "555-510-5545", 0),  # Miembro Inactivo
    ]
    cursor.executemany("""
        INSERT INTO miembros (nombre, correo, telefono, activo)
        VALUES (?, ?, ?, ?);
    """, miembros)

    # D. Tickets de prueba (12 tickets con estados variados, vencidos, completados, cancelados)
    fecha_limite_vencida = (hoy - timedelta(days=5)).strftime("%Y-%m-%d")
    fecha_limite_futura_corta = (hoy + timedelta(days=3)).strftime("%Y-%m-%d")
    fecha_limite_futura_larga = (hoy + timedelta(days=20)).strftime("%Y-%m-%d")

    tickets = [
        # (proyecto_id, miembro_id, titulo, descripcion, prioridad, estado, fecha_creacion, fecha_limite, fecha_cierre, activo)
        # Ticket 1: Abierto / En Progreso - Alta prioridad
        (1, 1, "Implementar autenticación OAuth2", "Integrar login social con Google y GitHub en la tienda.", "Alta", "En Progreso", fecha_hace_30d, fecha_limite_futura_corta, None, 1),
        # Ticket 2: Vencido (Overdue) - Crítica
        (1, 2, "Corregir fallo en cálculo de impuestos", "El carrito calcula 15% en vez de 16% en zona centro.", "Crítica", "Pendiente", fecha_hace_30d, fecha_limite_vencida, None, 1),
        # Ticket 3: Completado con fecha de cierre
        (3, 3, "Provisionar base de datos PostgreSQL en AWS RDS", "Configurar réplicas de lectura y backups automáticos.", "Alta", "Completado", fecha_hace_60d, fecha_hace_30d, fecha_hace_30d, 1),
        # Ticket 4: Cancelado
        (2, 4, "Soporte para Windows Phone 8", "El cliente decidió descontinuar compatibilidad con versiones obsoletas.", "Baja", "Cancelado", fecha_hace_30d, fecha_hace_30d, fecha_hace_30d, 1),
        # Ticket 5: En Progreso
        (2, 1, "Configuración de notificaciones Push Firebase", "Permitir envío de alertas de reparto en segundo plano.", "Media", "En Progreso", fecha_hace_30d, fecha_limite_futura_larga, None, 1),
        # Ticket 6: Pendiente
        (4, 2, "Diseño de wireframes para portal de vacaciones", "Presentar maquetas a la gerencia de RH.", "Media", "Pendiente", fecha_hoy, fecha_limite_futura_larga, None, 1),
        # Ticket 7: Completado
        (1, 3, "Optimizar velocidad de carga de catálogo", "Implementar compresión WebP y paginado del lado servidor.", "Media", "Completado", fecha_hace_30d, fecha_hace_15d := (hoy - timedelta(days=15)).strftime("%Y-%m-%d"), fecha_hace_15d, 1),
        # Ticket 8: Vencido (Overdue) - Alta
        (6, 4, "Revisar compatibilidad de firmas HMAC-SHA256", "La pasarela bancaria está rechazando solicitudes mal firmadas.", "Alta", "En Progreso", fecha_hace_30d, fecha_limite_vencida, None, 1),
        # Ticket 9: Pendiente - Baja prioridad
        (7, 1, "Definir paleta de colores para gráficos", "Alinear gráficos analíticos con el manual corporativo.", "Baja", "Pendiente", fecha_hoy, fecha_limite_futura_larga, None, 1),
        # Ticket 10: Completado en auditoría
        (8, 3, "Auditar inyecciones SQL y Cross-Site Scripting", "Ejecutar pruebas con escáner OWASP ZAP.", "Crítica", "Completado", fecha_hace_60d, fecha_hace_30d, fecha_hace_30d, 1),
        # Ticket 11: En Progreso - Crítica
        (6, 2, "Manejo de reintentos en desconexión bancaria", "Implementar cola con exponencial backoff para cobros.", "Crítica", "En Progreso", fecha_hace_30d, fecha_limite_futura_corta, None, 1),
        # Ticket 12: Pendiente
        (4, 4, "Estructuración de base de datos de empleados", "Normalizar tablas de departamentos y puestos.", "Media", "Pendiente", fecha_hoy, fecha_en_15d, None, 1),
    ]

    cursor.executemany("""
        INSERT INTO tickets (
            proyecto_id, miembro_id, titulo, descripcion, prioridad,
            estado, fecha_creacion, fecha_limite, fecha_cierre, activo
        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?);
    """, tickets)

    print("[OK] Datos semilla cargados con exito (2 usuarios, 8 proyectos, 5 miembros, 12 tickets).")
