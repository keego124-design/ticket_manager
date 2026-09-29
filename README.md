# 🎫 Ticket Management System (Sistema de Gestión de Tickets)

> **Proyecto Final Universitario:** Tópicos Avanzados de Programación  
> **Autor:** [@keego124-design](https://github.com/keego124-design)  
> **Tecnología:** Python 3.10+, Tkinter, ttk, SQLite3  
> **Arquitectura:** N-Capas Modular (Models, Repositories con SQL JOIN, Services con Reglas de Negocio, UI)

---

## 1. Título del Proyecto
**Ticket Management System (Sistema de Gestión y Control de Tickets, Proyectos y Equipos)**

---

## 2. Descripción General
Es una aplicación de escritorio robusta desarrollada en **Python** diseñada para gestionar el ciclo de vida de incidentes, tareas y requerimientos (tickets) dentro de proyectos de software. Permite coordinar equipos de desarrollo, asignando tickets a miembros específicos, monitoreando prioridades y estados, controlando vencimientos y generando reportes analíticos con métricas en tiempo real.

---

## 3. Objetivo
Proveer una solución integral de software de escritorio que demuestre el dominio de conceptos avanzados de programación:
- Arquitectura desacoplada en capas (Separation of Concerns).
- Persistencia de datos en base de datos relacional SQLite con integridad referencial (`PRAGMA foreign_keys = ON`).
- Consultas relacionales avanzadas mediante **SQL JOIN** explícitos.
- Validación estricta y cumplimiento de reglas de negocio en la capa de servicios.
- Seguridad en autenticación mediante hashing criptográfico **SHA-256** y control de acceso basado en roles (**RBAC**).
- Interfaces gráficas interactivas con **Tkinter** y **ttk**, incluyendo tablas dinámicas (`Treeview`), menús, modales y gráficos vectoriales nativos en `Canvas`.

---

## 4. Tecnologías Utilizadas
- **Lenguaje:** Python 3.10 o superior.
- **Interfaz Gráfica (GUI):** Tkinter y ttk (widgets estándar estilizados con tema *clam*).
- **Base de Datos:** SQLite 3 nativo mediante el módulo `sqlite3`.
- **Criptografía:** Módulo `hashlib` (SHA-256 para contraseñas).
- **Validaciones:** Módulos `datetime` (fechas ISO) y `re` (expresiones regulares para correos).
- **Dependencias Externas:** 0% (se utiliza 100% la biblioteca estándar de Python para máxima portabilidad).

---

## 5. Requisitos del Sistema
- Sistema Operativo: Windows 10/11, Linux o macOS.
- Python 3.10 o versión posterior instalado y agregado al PATH.

---

## 6. Instalación
1. Clonar el repositorio desde GitHub:
   ```bash
   git clone https://github.com/keego124-design/ticket_manager.git
   cd ticket_manager
   ```
2. No se requiere instalar librerías vía `pip` debido a que toda la pila tecnológica forma parte de la biblioteca estándar de Python.

---

## 7. Modo de Ejecución
Ejecutar el archivo principal desde la terminal:

- **En Windows:**
  ```powershell
  py main.py
  ```
  *(o `python main.py`)*

- **En Linux / macOS:**
  ```bash
  python3 main.py
  ```

Al iniciar por primera vez, el sistema creará automáticamente el archivo de base de datos `ticket_system.db` con todas las tablas e insertará los datos de prueba.

---

## 8. Credenciales por Defecto (Cuentas de Prueba)

El sistema implementa dos roles con niveles de acceso diferenciados:

| Rol | Usuario | Contraseña | Permisos y Alcance |
| :--- | :--- | :--- | :--- |
| **Administrador** | `admin` | `admin123` | Acceso total al sistema, eliminación y desactivación de entidades, reportes globales. |
| **Operador** | `operador` | `operador123` | Gestión operativa de tickets, proyectos y visualización de equipo. |

*(Las contraseñas no se almacenan en texto plano en la base de datos; se guardan bajo hash SHA-256).*

---

## 9. Estructura de la Base de Datos Relacional

El modelo entidad-relación cuenta con 4 tablas normalizadas e índices de rendimiento:

```text
+---------------------+       1:N       +-------------------+
|      proyectos      | <-------------- |      tickets      |
+---------------------+                 +-------------------+
| id (PK)             |                 | id (PK)           |
| nombre              |                 | proyecto_id (FK)  | ---> proyectos.id
| descripcion         |                 | miembro_id (FK)   | ---> miembros.id
| fecha_inicio        |                 | titulo            |
| fecha_fin           |                 | descripcion       |
| estado              |                 | prioridad         |
| activo              |                 | estado            |
+---------------------+                 | fecha_creacion    |
                                        | fecha_limite      |
+---------------------+       1:N       | fecha_cierre      |
|       miembros      | <-------------- | activo            |
+---------------------+                 +-------------------+
| id (PK)             |
| nombre              |
| correo (UNIQUE)     |
| telefono            |
| activo              |
+---------------------+

+---------------------+
|  usuarios_sistema   |
+---------------------+
| id (PK)             |
| username (UNIQUE)   |
| password_hash       |
| role                |
| active              |
+---------------------+
```

---

## 10. Arquitectura del Proyecto

El código fuente está estrictamente separado en 4 capas desacopladas:

```text
ticket_manager/
│
├── main.py                     # Punto de entrada y ciclo de vida de la aplicación
├── database.py                 # Conexión SQLite, DDL de tablas y seed de datos
├── config.py                   # Constantes del sistema, colores y configuraciones
├── requirements.txt            # Especificación de biblioteca estándar
├── .gitignore                  # Reglas de exclusión para control de versiones Git
├── README.md                   # Documentación técnica y académica completa
│
├── models/                     # Entidades de Dominio
│   ├── __init__.py
│   ├── usuario.py              # Clase Usuario (roles, active)
│   ├── proyecto.py             # Clase Proyecto (estados, validaciones)
│   ├── miembro.py              # Clase Miembro del Equipo
│   └── ticket.py               # Clase Ticket (prioridades, estados, campos JOIN)
│
├── repositories/               # Capa de Acceso a Datos (DAO / SQL)
│   ├── __init__.py
│   ├── usuario_repository.py   # Consultas parametrizadas de usuarios
│   ├── proyecto_repository.py  # CRUD y filtros de proyectos
│   ├── miembro_repository.py   # CRUD y validación de unicidad de miembros
│   └── ticket_repository.py   # CRUD, filtros y consulta explícita SQL JOIN
│
├── services/                   # Capa de Lógica de Negocio (Reglas de Negocio)
│   ├── __init__.py
│   ├── auth_service.py         # Login, hash SHA-256 y sesión de usuario
│   ├── proyecto_service.py     # Coherencia de fechas y regla de no eliminar con tickets
│   ├── miembro_service.py      # Validación regex de correos y miembros inactivos
│   ├── ticket_service.py       # Aplicación de las 12 reglas de negocio del ticket
│   └── report_service.py       # Consultas analíticas y cálculo de vencidos (Overdue)
│
└── ui/                         # Capa de Presentación (Tkinter / ttk)
    ├── __init__.py
    ├── styles.py               # Estilos centralizados ttk con tema clam
    ├── login_window.py         # Ventana modal de autenticación
    ├── main_window.py          # Ventana principal con Sidebar y contenedor dinámico
    ├── dashboard_view.py       # Panel de métricas KPI y tickets de atención urgente
    ├── proyecto_view.py        # Módulo CRUD de proyectos con Treeview y filtros
    ├── miembro_view.py         # Módulo CRUD de miembros de equipo
    ├── ticket_view.py          # Módulo central de tickets con SQL JOIN y multi-filtros
    └── report_view.py          # Centro de reportes con gráficos vectoriales en Canvas
```

---

## 11. Módulos Principales
1. **Módulo de Autenticación (`login_window.py`, `auth_service.py`):** Controla el acceso seguro al sistema.
2. **Dashboard (`dashboard_view.py`):** Visualización instantánea de 5 KPIs globales y tickets vencidos.
3. **Gestión de Proyectos (`proyecto_view.py`):** Alta, baja lógica, edición y seguimiento de estados de proyectos.
4. **Gestión de Miembros (`miembro_view.py`):** Control del personal asignable, validación de correos corporativos y estado activo/inactivo.
5. **Gestión de Tickets (`ticket_view.py`):** Núcleo operativo del sistema para registrar incidencias, asignar responsables, cambiar estados y aplicar filtros multicriterio.
6. **Módulo de Reportes (`report_view.py`):** Análisis cuantitativo por estado, proyecto, prioridad y detección de incumplimientos de fechas.

---

## 12. Reglas de Negocio Implementadas

El sistema valida de forma exhaustiva las siguientes 12 reglas en la capa de servicios:

1. **Regla 1 (Proyectos Cerrados):** No es posible crear un nuevo ticket dentro de un proyecto cuyo estado sea "Cerrado".
2. **Regla 2 (Miembros Inactivos):** Un miembro marcado como inactivo (`activo = 0`) no puede recibir la asignación de nuevos tickets.
3. **Regla 3 (Confirmación de Reapertura):** Si un ticket marcado previamente como "Completado" o "Cancelado" intenta cambiarse a "Pendiente", el sistema solicita una confirmación explícita mediante un cuadro de diálogo modal antes de autorizar el cambio.
4. **Regla 4 (Integridad en Eliminación de Proyectos):** Un proyecto no puede ser eliminado ni desactivado si aún contiene tickets abiertos (en estado "Pendiente" o "En Progreso").
5. **Regla 5 (Pertenencia Válida):** Todo ticket debe pertenecer obligatoriamente a un proyecto existente y activo.
6. **Regla 6 (Asignación Válida):** Todo ticket debe contar con un miembro responsable válido y activo.
7. **Regla 7 (Validación de Fechas Límite):** La fecha límite debe ser una fecha válida bajo el formato `YYYY-MM-DD`.
8. **Regla 8 (Registro Automático de Fecha de Cierre):** Al momento en que un ticket pasa a estado "Completado", el sistema estampa automáticamente la fecha actual (`fecha_cierre = hoy`).
9. **Regla 9 (Clasificación de Vencidos / Overdue):** Todo ticket no resuelto (que no esté Completado ni Cancelado) cuya fecha límite sea anterior a la fecha actual es clasificado automáticamente como vencido en reportes y dashboard.
10. **Regla 10 (Acciones Destructivas):** Toda acción de eliminación o desactivación solicita confirmación al usuario mediante `messagebox.askyesno`.
11. **Regla 11 (Campos Obligatorios):** Se valida que ningún campo mandatorio se guarde en blanco.
12. **Regla 12 (Mensajes Amigables):** Toda excepción o falla de validación muestra mensajes descriptivos en español sin provocar caídas del programa.

---

## 13. Pantallas y Vistas del Sistema

- **Pantalla de Login:** Tarjeta estilizada con campos de usuario y contraseña enmascarada, validación dinámica de credenciales y recordatorio de cuentas demo.
- **Sidebar de Navegación:** Acceso persistente con resaltado de la sección activa y botón de cierre de sesión seguro.
- **Barra de Estado / Header:** Indicador superior permanente con el usuario autenticado y su insignia de rol.
- **Vista Proyectos:** Formulario modal con selectores de fechas y validación de rango temporal (inicio $\le$ fin).
- **Vista Equipo:** Formulario con validación de correo mediante expresiones regulares (`r"^[\w\.-]+@[\w\.-]+\.\w+$"`).
- **Vista Tickets:** Formulario modal que auto-filtra miembros activos y proyectos abiertos.
- **Vista Reportes:** Pestañas organizadas con vistas de datos detalladas y representaciones visuales de barras.

---

## 14. Datos de Prueba Iniciales (Seed Data)

Si la base de datos se encuentra vacía, se cargan automáticamente:
- **2 Usuarios:** `admin` y `operador`.
- **8 Proyectos:** En estados *Planificación*, *En Progreso*, *Completado* y *Cerrado* (ej. "Sistema de Facturación 4.0", "Plataforma E-Commerce B2B", "App Móvil de Entregas").
- **5 Miembros:** 4 activos y 1 inactivo ("Tec. Miguel Angel Rios") para probar la regla de bloqueo de asignación.
- **12 Tickets:** Cubren casos de tickets abiertos, vencidos, completados con fecha de cierre registrada y cancelados.

---

## 15. Consulta con SQL JOIN Implementada

En cumplimiento de los requerimientos de la materia, la consulta relacional con **SQL JOIN** se implementa de manera explícita en `repositories/ticket_repository.py` dentro del método `list_all_with_join()` y `search_and_filter()`:

```sql
SELECT
    tickets.id,
    tickets.proyecto_id,
    tickets.miembro_id,
    tickets.titulo,
    tickets.descripcion,
    tickets.prioridad,
    tickets.estado,
    tickets.fecha_creacion,
    tickets.fecha_limite,
    tickets.fecha_cierre,
    tickets.activo,
    proyectos.nombre AS proyecto,
    miembros.nombre AS miembro
FROM tickets
JOIN proyectos ON tickets.proyecto_id = proyectos.id
JOIN miembros ON tickets.miembro_id = miembros.id
WHERE tickets.activo = 1
ORDER BY tickets.id DESC;
```

Esta consulta permite que el `ttk.Treeview` muestre directamente los nombres legibles del proyecto y del responsable en lugar de números de ID artificiales.

---

## 16. Reportes y Analíticas

El módulo de reportes (`report_view.py`) incluye 5 secciones clave:
- **A. Tickets Abiertos:** Listado detallado de todas las tareas pendientes de atención con sus fechas límite.
- **B. Tickets Vencidos (Overdue):** Identificación de tickets críticos cuya fecha límite ha expirado respecto al día de hoy.
- **C. Conteo por Estado:** Agrupación y gráfico de barras mostrando la distribución entre Pendiente, En Progreso, Completado y Cancelado.
- **D. Conteo por Proyecto:** Desglose del volumen de trabajo acumulado en cada iniciativa.
- **E. Conteo por Prioridad:** Identificación gráfica de tickets de prioridad Crítica, Alta, Media y Baja.

---

## 17. Instrucciones para GitHub

Para subir o sincronizar este proyecto en tu cuenta de GitHub:

1. Inicializar y confirmar los archivos:
   ```bash
   git init -b main
   git add .
   git commit -m "feat: entrega final del Ticket Management System con arquitectura modular y Tkinter"
   ```
2. Vincular el repositorio remoto:
   ```bash
   git remote add origin https://github.com/keego124-design/ticket_manager.git
   ```
3. Subir los cambios a la rama principal:
   ```bash
   git push -u origin main
   ```

---

## 18. Posibles Mejoras a Futuro
- Exportación de reportes a formatos **PDF** y **Excel (XLSX / CSV)**.
- Adjuntar archivos e imágenes a los tickets (evidencias de errores o capturas de pantalla).
- Sistema de notificaciones por correo electrónico al reasignar un ticket a un miembro.
- Historial de auditoría para registrar cada cambio de estado con marca de tiempo y usuario responsable.
