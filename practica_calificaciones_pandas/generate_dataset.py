"""
Script para generar el dataset inicial calificaciones_isc.csv
Cumple con exactamente 288 filas (24 estudiantes x 4 materias x 3 unidades).
"""
import random
import csv
from pathlib import Path

# Fijar semilla determinista para reproducibilidad académica
random.seed(42)

ALUMNOS = [
    # Grupo A (12 alumnos)
    ("ISC240101", "Alejandro Navarro", "A", 88),
    ("ISC240102", "Sofia Morales", "A", 92),
    ("ISC240103", "Carlos Espinoza", "A", 74),
    ("ISC240104", "Valeria Hernandez", "A", 85),
    ("ISC240105", "Diego Ramirez", "A", 58),     # Estudiante en riesgo (< 70)
    ("ISC240106", "Mariana Torres", "A", 95),
    ("ISC240107", "Gabriel Castro", "A", 78),
    ("ISC240108", "Camila Ortiz", "A", 82),
    ("ISC240109", "Mateo Vargas", "A", 64),      # Estudiante en riesgo (< 70)
    ("ISC240110", "Daniela Reyes", "A", 90),
    ("ISC240111", "Rodrigo Ramos", "A", 76),
    ("ISC240112", "Valentina Cruz", "A", 84),
    # Grupo B (12 alumnos)
    ("ISC240113", "Javier Mendez", "B", 86),
    ("ISC240114", "Natalia Salazar", "B", 91),
    ("ISC240115", "Emilio Guzman", "B", 79),
    ("ISC240116", "Andrea Flores", "B", 87),
    ("ISC240117", "Leonardo Silva", "B", 73),
    ("ISC240118", "Luciana Delgado", "B", 94),
    ("ISC240119", "Santiago Gomez", "B", 62),    # Estudiante en riesgo (< 70)
    ("ISC240120", "Paula Herrera", "B", 89),
    ("ISC240121", "Sebastian Rios", "B", 80),
    ("ISC240122", "Regina Aguilar", "B", 85),
    ("ISC240123", "Nicolas Paredes", "B", 56),   # Estudiante en riesgo (< 70)
    ("ISC240124", "Renata Castillo", "B", 88),
]

MATERIAS = [
    # (Nombre, mod_promedio)
    ("Programacion", 4),
    ("Bases de datos", 2),
    ("Redes", 0),
    ("Matematicas discretas", -5),  # Materia con menor promedio
]

UNIDADES = [1, 2, 3]


def generar_datos():
    filas = []
    for matricula, nombre, grupo, base_nivel in ALUMNOS:
        for materia, mod_mat in MATERIAS:
            for unidad in UNIDADES:
                # Modificador de unidad: Unidad 3 tiene un ligero decremento en promedio
                mod_u = 0 if unidad == 1 else (2 if unidad == 2 else -4)
                
                # Ruido aleatorio controlado
                ruido = random.randint(-6, 6)
                
                # Calificación final ajustada
                calif = base_nivel + mod_mat + mod_u + ruido
                calif = max(42, min(100, calif))  # Rango 0-100
                
                # Asistencias correlacionadas con el nivel del alumno (de 30 sesiones)
                asist_base = int(22 + (base_nivel / 100.0) * 8)
                asist = max(18, min(30, asist_base + random.randint(-2, 2)))
                
                filas.append({
                    "matricula": matricula,
                    "nombre": nombre,
                    "grupo": grupo,
                    "materia": materia,
                    "unidad": unidad,
                    "calificacion": calif,
                    "asistencias": asist
                })
    return filas


def guardar_csv(ruta: Path):
    filas = generar_datos()
    ruta.parent.mkdir(parents=True, exist_ok=True)
    with open(ruta, mode="w", newline="", encoding="utf-8") as f:
        escritor = csv.DictWriter(f, fieldnames=[
            "matricula", "nombre", "grupo", "materia", "unidad", "calificacion", "asistencias"
        ])
        escritor.writeheader()
        escritor.writerows(filas)
    print(f"[OK] Archivo generado exitosamente en: {ruta} (Total filas: {len(filas)})")


if __name__ == "__main__":
    base1 = Path("C:/Users/CASA/.gemini/antigravity/scratch/practica_calificaciones_pandas/calificaciones_isc.csv")
    base2 = Path("C:/Users/CASA/Downloads/proyectosPython/practica_calificaciones_pandas/calificaciones_isc.csv")
    guardar_csv(base1)
    guardar_csv(base2)
