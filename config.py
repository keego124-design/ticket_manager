"""
config.py
---------
Configuraciones globales del sistema de gestión de tickets:
- Rutas de base de datos
- Constantes de negocio
- Paleta de colores y estilos visuales
"""

import os
from pathlib import Path

# Directorio raíz del proyecto
BASE_DIR = Path(__file__).resolve().parent

# Ruta de la base de datos SQLite
DB_NAME = "ticket_system.db"
DB_PATH = BASE_DIR / DB_NAME

# Roles de usuario permitidos
ROLE_ADMIN = "admin"
ROLE_OPERATOR = "operator"
ROLES_DISPONIBLES = [ROLE_ADMIN, ROLE_OPERATOR]

# Estados de Proyectos
ESTADO_PROY_PLANIFICACION = "Planificación"
ESTADO_PROY_EN_PROGRESO = "En Progreso"
ESTADO_PROY_COMPLETADO = "Completado"
ESTADO_PROY_CERRADO = "Cerrado"
ESTADOS_PROYECTO = [
    ESTADO_PROY_PLANIFICACION,
    ESTADO_PROY_EN_PROGRESO,
    ESTADO_PROY_COMPLETADO,
    ESTADO_PROY_CERRADO,
]

# Prioridades de Tickets
PRIORIDAD_BAJA = "Baja"
PRIORIDAD_MEDIA = "Media"
PRIORIDAD_ALTA = "Alta"
PRIORIDAD_CRITICA = "Crítica"
PRIORIDADES_TICKET = [
    PRIORIDAD_BAJA,
    PRIORIDAD_MEDIA,
    PRIORIDAD_ALTA,
    PRIORIDAD_CRITICA,
]

# Estados de Tickets
ESTADO_TICKET_PENDIENTE = "Pendiente"
ESTADO_TICKET_EN_PROGRESO = "En Progreso"
ESTADO_TICKET_COMPLETADO = "Completado"
ESTADO_TICKET_CANCELADO = "Cancelado"
ESTADOS_TICKET = [
    ESTADO_TICKET_PENDIENTE,
    ESTADO_TICKET_EN_PROGRESO,
    ESTADO_TICKET_COMPLETADO,
    ESTADO_TICKET_CANCELADO,
]

# Paleta de Colores Corporativa (Diseño limpio y moderno)
COLOR_PRIMARIO = "#1565C0"       # Azul institucional
COLOR_PRIMARIO_OSCURO = "#0D47A1"
COLOR_SECUNDARIO = "#37474F"     # Gris pizarra para sidebar
COLOR_SECUNDARIO_HOVER = "#455A64"
COLOR_FONDO = "#ECEFF1"          # Gris muy claro para ventanas
COLOR_BLANCO = "#FFFFFF"
COLOR_TEXTO = "#263238"          # Gris oscuro legible
COLOR_TEXTO_SECUNDARIO = "#607D8B"
COLOR_EXITO = "#2E7D32"          # Verde
COLOR_PELIGRO = "#C62828"        # Rojo
COLOR_ADVERTENCIA = "#EF6C00"    # Naranja
COLOR_BORDE = "#CFD8DC"
