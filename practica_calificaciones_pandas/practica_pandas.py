"""
================================================================================
PRÁCTICA: ANÁLISIS Y VISUALIZACIÓN DE CALIFICACIONES CON PANDAS Y MATPLOTLIB
Ingeniería en Sistemas Computacionales (ISC)
Estética Visual: Cyberpunk / Modern Dark (Fondo Negro #0b0b0b, Neón Rojo #ff1e42, Texto Blanco #ffffff)
================================================================================
"""

import sys
from pathlib import Path
import numpy as np
import pandas as pd
import matplotlib
# Configurar backend no interactivo para asegurar generación limpia y portable de gráficos
matplotlib.use("Agg")
import matplotlib.pyplot as plt

# Reconfigurar salida estándar a UTF-8 para evitar problemas de codificación en Windows (cp1252)
if sys.stdout.encoding != "utf-8":
    try:
        sys.stdout.reconfigure(encoding="utf-8")
    except Exception:
        pass


def aplicar_estilo_cyberpunk():
    """
    Aplica la paleta Cyberpunk Dark / Red Neon a Matplotlib:
    - Fondo profundo: #0b0b0b (figura) y #111115 (ejes)
    - Acentos y bordes: Rojo Neón (#ff1e42 / #ff0055)
    - Textos y etiquetas: Blanco Puro (#ffffff)
    - Rejilla: Tenue carmesí neón con baja opacidad (#ff1e42 con alpha)
    """
    plt.style.use("dark_background")
    plt.rcParams.update({
        "figure.facecolor": "#0b0b0b",
        "axes.facecolor": "#111116",
        "axes.edgecolor": "#ff1e42",
        "axes.linewidth": 1.4,
        "axes.labelcolor": "#ffffff",
        "xtick.color": "#ffffff",
        "ytick.color": "#ffffff",
        "text.color": "#ffffff",
        "grid.color": "#ff1e42",
        "grid.alpha": 0.18,
        "grid.linestyle": "--",
        "font.family": "sans-serif",
        "font.sans-serif": ["Segoe UI", "DejaVu Sans", "Helvetica", "Arial"],
        "figure.titlesize": 14,
        "axes.titlesize": 13,
        "axes.labelsize": 11,
    })


def guardar_grafico(fig, nombre_archivo: str, directorio_base: Path):
    """
    Guarda la figura en la raíz del proyecto y en static/plots/ para el dashboard web.
    IMPORTANTE: Siempre se ejecuta antes de plt.close().
    """
    ruta_raiz = directorio_base / nombre_archivo
    ruta_static = directorio_base / "static" / "plots" / nombre_archivo
    ruta_static.parent.mkdir(parents=True, exist_ok=True)

    fig.savefig(ruta_raiz, dpi=300, bbox_inches="tight", facecolor=fig.get_facecolor())
    fig.savefig(ruta_static, dpi=300, bbox_inches="tight", facecolor=fig.get_facecolor())
    print(f"  [GRÁFICO GUARDADO] -> {nombre_archivo} (DPI 300)")
    plt.close(fig)


def main():
    directorio_base = Path(__file__).resolve().parent
    ruta_csv = directorio_base / "calificaciones_isc.csv"

    print("=" * 80)
    print(" SISTEMA DE ANÁLISIS DE CALIFICACIONES ISC - PANDAS & MATPLOTLIB [CYBERPUNK]")
    print("=" * 80)

    # =========================================================================
    # EJERCICIO 1: Carga y Exploración Inicial del Dataset
    # =========================================================================
    print("\n" + "#" * 60)
    print(" EJERCICIO 1: CARGA Y REVISIÓN INICIAL")
    print("#" * 60)

    if not ruta_csv.exists():
        raise FileNotFoundError(
            f"No se encontró el archivo {ruta_csv}. Ejecute primero 'generate_dataset.py'."
        )

    # Cargar el dataset en un DataFrame
    df = pd.read_csv(ruta_csv)

    print("\n--> Primeras 5 filas del DataFrame (df.head()):")
    print(df.head().to_string(index=False))

    print(f"\n--> Dimensiones del DataFrame (df.shape): {df.shape[0]} filas x {df.shape[1]} columnas")

    print("\n--> Tipos de datos de las columnas (df.dtypes):")
    print(df.dtypes)

    print("\n--> Estadísticas descriptivas de 'calificacion' y 'asistencias' (df.describe()):")
    print(df[["calificacion", "asistencias"]].describe().round(2))

    # -------------------------------------------------------------------------
    # EXPLICACIÓN TEÓRICA DE LA ESTRUCTURA DEL DATASET:
    # ¿Por qué el archivo tiene exactamente 288 filas en lugar de 24?
    #
    # En este diseño de datos relacional/tabular en formato largo ("tidy data"):
    # Cada fila representa una observación unitaria: la calificación obtenida por
    # UN alumno específico en UNA unidad específica de UNA materia determinada.
    # El cálculo matemático exacto es:
    #   24 estudiantes (12 Grupo A + 12 Grupo B)
    #   × 4 materias ("Programacion", "Bases de datos", "Redes", "Matematicas discretas")
    #   × 3 unidades evaluativas por materia
    #   = 24 × 4 × 3 = 288 registros.
    # Si tuviera 24 filas, tendría que estar en formato ancho ("wide format") con
    # 12 columnas de calificaciones (4 materias × 3 unidades), lo cual dificulta
    # agregaciones, filtros vectorizados y análisis temporal por unidad.
    # -------------------------------------------------------------------------
    print("\n[NOTA DE ANÁLISIS - EXPLICACIÓN DE DIMENSIONES]")
    print("  El dataset contiene 288 registros y no 24 porque está estructurado en formato")
    print("  largo ('tidy/long format'): 24 estudiantes x 4 materias x 3 unidades = 288 observaciones.")

    # =========================================================================
    # EJERCICIO 2: Filtros Vectorizados (Sin bucles for)
    # =========================================================================
    print("\n" + "#" * 60)
    print(" EJERCICIO 2: FILTROS VECTORIZADOS (SIN BUCLES)")
    print("#" * 60)

    # Filtro A: Todas las filas correspondientes al Grupo A
    filtro_grupo_a = df[df["grupo"] == "A"]
    total_grupo_a = len(filtro_grupo_a)
    print(f"\n--> A) Registros del Grupo A: {total_grupo_a} filas (esperadas: 144 = 12 alumnos x 12 unidades)")
    print("    Muestra de los primeros 3 registros:")
    print(filtro_grupo_a.head(3).to_string(index=False))

    # Filtro B: Registros con calificación menor a 70 (estudiantes no aprobados en esa unidad)
    filtro_reprobados = df[df["calificacion"] < 70]
    total_reprobados = len(filtro_reprobados)
    print(f"\n--> B) Registros con calificación menor a 70 (< 70): {total_reprobados} filas")
    print("    Muestra de los primeros 4 registros reprobados:")
    print(filtro_reprobados.head(4).to_string(index=False))

    # Filtro C: Registros de la materia "Bases de datos" del Grupo B con calificación >= 80
    filtro_bd_b_80 = df[
        (df["materia"] == "Bases de datos") &
        (df["grupo"] == "B") &
        (df["calificacion"] >= 80)
    ]
    total_bd_b_80 = len(filtro_bd_b_80)
    print(f"\n--> C) Registros de 'Bases de datos' en Grupo B con calificacion >= 80: {total_bd_b_80} filas")
    print("    Detalle de registros encontrados:")
    print(filtro_bd_b_80[["matricula", "nombre", "unidad", "calificacion"]].to_string(index=False))

    # =========================================================================
    # EJERCICIO 3: Creación de Columna Calculada con np.where (Vectorizado)
    # =========================================================================
    print("\n" + "#" * 60)
    print(" EJERCICIO 3: COLUMNA CALCULADA 'situacion' (np.where)")
    print("#" * 60)

    # Vectorización pura con numpy.where: evita bucles for y optimiza el rendimiento
    df["situacion"] = np.where(df["calificacion"] >= 70, "Aprobado", "Reprobado")

    print("\n--> Columna 'situacion' agregada exitosamente:")
    print(df[["matricula", "nombre", "materia", "unidad", "calificacion", "situacion"]].head(8).to_string(index=False))

    distribucion_situacion = df["situacion"].value_counts()
    print("\n--> Distribución general de la situación académica:")
    for sit, cuenta in distribucion_situacion.items():
        porcentaje = (cuenta / len(df)) * 100
        print(f"    * {sit}: {cuenta} registros ({porcentaje:.2f}%)")

    # =========================================================================
    # EJERCICIO 4: Agrupaciones, Resúmenes y Exportación a CSV
    # =========================================================================
    print("\n" + "#" * 60)
    print(" EJERCICIO 4: RESÚMENES ESTADÍSTICOS Y EXPORTACIÓN")
    print("#" * 60)

    # 4.1 Promedio por materia
    prom_materia = df.groupby("materia")["calificacion"].mean().round(2)
    print("\n--> 4.1 Promedio de calificación por Materia:")
    print(prom_materia.to_string())

    # 4.2 Promedio por grupo y por materia
    prom_grupo_materia = df.groupby(["grupo", "materia"])["calificacion"].mean().round(2).unstack()
    print("\n--> 4.2 Promedio por Grupo y Materia:")
    print(prom_grupo_materia.to_string())

    # 4.3 Promedio general por alumno ordenado de mayor a menor
    # Preservando matrícula y nombre
    prom_alumnos = (
        df.groupby(["matricula", "nombre", "grupo"])
        .agg(
            promedio_calificacion=("calificacion", "mean"),
            promedio_asistencias=("asistencias", "mean"),
            unidades_aprobadas=("situacion", lambda s: (s == "Aprobado").sum()),
            unidades_reprobadas=("situacion", lambda s: (s == "Reprobado").sum()),
        )
        .round(2)
        .sort_values(by="promedio_calificacion", ascending=False)
        .reset_index()
    )

    print("\n--> 4.3 Top 5 Alumnos con Mayor Promedio General:")
    print(prom_alumnos.head(5).to_string(index=False))

    print("\n--> 4.3 Alumnos con Menor Promedio General (Últimos 5):")
    print(prom_alumnos.tail(5).to_string(index=False))

    # 4.4 Promedio por unidad evaluativa (1, 2 y 3)
    prom_unidad = df.groupby("unidad")["calificacion"].mean().round(2)
    print("\n--> 4.4 Promedio general por Unidad evaluativa:")
    print(prom_unidad.to_string())

    # 4.5 Conteo global de Aprobados vs Reprobados
    conteo_situacion = df["situacion"].value_counts()
    print("\n--> 4.5 Conteo de unidades Aprobadas vs Reprobadas:")
    print(conteo_situacion.to_string())

    # 4.6 Exportar promedios_alumnos.csv con reset_index() e index=False
    ruta_promedios_csv = directorio_base / "promedios_alumnos.csv"
    prom_alumnos.to_csv(ruta_promedios_csv, index=False, encoding="utf-8")
    print(f"\n--> Archivo exportado exitosamente: {ruta_promedios_csv}")
    print("    Columnas incluidas:", list(prom_alumnos.columns))

    # =========================================================================
    # EJERCICIO 5: Visualización de Datos con Estética Cyberpunk Dark / Neon Red
    # =========================================================================
    print("\n" + "#" * 60)
    print(" EJERCICIO 5: GENERACIÓN DE GRÁFICOS (CYBERPUNK THEME)")
    print("#" * 60)

    aplicar_estilo_cyberpunk()

    # -------------------------------------------------------------------------
    # Gráfico 1: promedio_materias.png (Gráfico de barras del promedio por materia)
    # -------------------------------------------------------------------------
    fig1, ax1 = plt.subplots(figsize=(9, 5.5), dpi=300)
    materias_nombres = prom_materia.index.tolist()
    materias_valores = prom_materia.values.tolist()

    # Barras en rojo neón (#ff1e42) con bordes iluminados
    barras = ax1.bar(
        materias_nombres,
        materias_valores,
        color="#ff1e42",
        edgecolor="#ffffff",
        linewidth=1.2,
        width=0.55,
        alpha=0.92,
        zorder=3
    )

    # Añadir resplandor o sombra tenue en las barras
    ax1.set_ylim(0, 100)
    ax1.set_ylabel("Calificación Promedio (0 - 100)", color="#ffffff", fontweight="bold")
    ax1.set_title("PROMEDIO GENERAL POR MATERIA // ISC", color="#ffffff", fontweight="bold", pad=15)
    ax1.grid(axis="y", linestyle="--", alpha=0.3, color="#ff1e42", zorder=0)

    # Etiquetas de valor sobre cada barra
    for barra in barras:
        altura = barra.get_height()
        ax1.text(
            barra.get_x() + barra.get_width() / 2.0,
            altura + 2.0,
            f"{altura:.1f}",
            ha="center",
            va="bottom",
            color="#ffffff",
            fontweight="bold",
            fontsize=11
        )

    # Línea de referencia de aprobación mínima (70)
    ax1.axhline(70, color="#ffffff", linestyle=":", linewidth=1.5, alpha=0.75, label="Mínimo Aprobatorio (70)")
    ax1.legend(loc="lower right", facecolor="#111116", edgecolor="#ff1e42", labelcolor="#ffffff")

    guardar_grafico(fig1, "promedio_materias.png", directorio_base)

    # -------------------------------------------------------------------------
    # Gráfico 2: histograma.png (Distribución de todas las calificaciones)
    # -------------------------------------------------------------------------
    fig2, ax2 = plt.subplots(figsize=(9, 5.5), dpi=300)

    # Bins de tamaño 5 para ver la distribución clara
    n, bins, patches = ax2.hist(
        df["calificacion"],
        bins=12,
        range=(40, 100),
        color="#ff1e42",
        edgecolor="#ffffff",
        linewidth=1.2,
        alpha=0.88,
        zorder=3
    )

    # Resaltar en tono más oscuro o carmesí las calificaciones reprobatorias
    for patch, bin_izq in zip(patches, bins[:-1]):
        if bin_izq < 70:
            patch.set_facecolor("#8a0f24")  # Rojo oscuro para reprobados
            patch.set_edgecolor("#ff1e42")
        else:
            patch.set_facecolor("#ff1e42")  # Neón brillante para aprobados
            patch.set_edgecolor("#ffffff")

    # Línea vertical punteada roja/blanca en 70 (corte de aprobación)
    ax2.axvline(
        70,
        color="#ffffff",
        linestyle="--",
        linewidth=2.2,
        zorder=4,
        label="Corte de Aprobación (70 pts)"
    )

    ax2.set_xlabel("Rango de Calificación", color="#ffffff", fontweight="bold")
    ax2.set_ylabel("Frecuencia (Cantidad de Registros)", color="#ffffff", fontweight="bold")
    ax2.set_title("DISTRIBUCIÓN DE CALIFICACIONES // CORTE DE APROBACIÓN", color="#ffffff", fontweight="bold", pad=15)
    ax2.grid(axis="y", linestyle="--", alpha=0.3, color="#ff1e42", zorder=0)
    ax2.legend(loc="upper left", facecolor="#111116", edgecolor="#ff1e42", labelcolor="#ffffff")

    guardar_grafico(fig2, "histograma.png", directorio_base)

    # -------------------------------------------------------------------------
    # Gráfico 3: tendencia_unidades.png (Líneas de evolución por unidad y materia)
    # -------------------------------------------------------------------------
    fig3, ax3 = plt.subplots(figsize=(9.5, 5.5), dpi=300)

    # Agrupar por materia y unidad
    evolucion_materias = df.groupby(["materia", "unidad"])["calificacion"].mean().unstack(level=0)

    # Paleta de colores neón complementaria manteniendo protagonismo de rojo neón
    colores_materias = {
        "Programacion": "#ff1e42",          # Neón Red primario
        "Bases de datos": "#ff6b8b",        # Coral Rosado Neón
        "Redes": "#ffffff",                 # Blanco Neón Puro
        "Matematicas discretas": "#c40030"  # Carmesí Profundo Neón
    }

    marcadores = {
        "Programacion": "o",
        "Bases de datos": "s",
        "Redes": "^",
        "Matematicas discretas": "D"
    }

    for materia in evolucion_materias.columns:
        color_linea = colores_materias.get(materia, "#ff1e42")
        marcador = marcadores.get(materia, "o")
        ax3.plot(
            evolucion_materias.index,
            evolucion_materias[materia],
            marker=marcador,
            markersize=8,
            linewidth=2.5,
            color=color_linea,
            label=materia,
            zorder=3
        )

        # Mostrar valores numéricos en los puntos
        for u in evolucion_materias.index:
            val = evolucion_materias.loc[u, materia]
            ax3.annotate(
                f"{val:.1f}",
                (u, val),
                textcoords="offset points",
                xytext=(0, 8),
                ha="center",
                fontsize=9,
                color=color_linea,
                fontweight="bold"
            )

    ax3.set_xticks([1, 2, 3])
    ax3.set_xticklabels(["Unidad 1", "Unidad 2", "Unidad 3"])
    ax3.set_ylim(60, 95)
    ax3.set_xlabel("Unidad Académica", color="#ffffff", fontweight="bold")
    ax3.set_ylabel("Calificación Promedio", color="#ffffff", fontweight="bold")
    ax3.set_title("TENDENCIA DE RENDIMIENTO POR UNIDAD // MATERIAS ISC", color="#ffffff", fontweight="bold", pad=15)
    ax3.grid(True, linestyle="--", alpha=0.3, color="#ff1e42", zorder=0)
    ax3.legend(loc="lower left", facecolor="#111116", edgecolor="#ff1e42", labelcolor="#ffffff")

    guardar_grafico(fig3, "tendencia_unidades.png", directorio_base)

    # =========================================================================
    # EJERCICIO 6: Interpretación y Preguntas de Análisis
    # =========================================================================
    print("\n" + "#" * 60)
    print(" EJERCICIO 6: INTERPRETACIÓN DE RESULTADOS")
    print("#" * 60)

    # Pregunta 1: Materia con menor promedio
    materia_menor_prom = prom_materia.idxmin()
    valor_menor_prom = prom_materia.min()
    print(f"\n1) ¿Cuál materia tuvo el menor promedio general?")
    print(f"   -> Respuesta: '{materia_menor_prom}' con un promedio de {valor_menor_prom:.2f} puntos.")
    print("      Justificación: Presenta mayor grado de dificultad conceptual y abstracción matemática,")
    print("      reflejando la mayor dispersión y calificaciones más bajas del periodo.")

    # Pregunta 2: Tendencia en la unidad 3 respecto a las unidades 1 y 2
    u1_prom = prom_unidad.loc[1]
    u2_prom = prom_unidad.loc[2]
    u3_prom = prom_unidad.loc[3]
    print(f"\n2) ¿Qué tendencia se observa en la Unidad 3 respecto a las Unidades 1 y 2?")
    print(f"   -> Respuesta: Unidad 1 = {u1_prom:.2f} pts | Unidad 2 = {u2_prom:.2f} pts | Unidad 3 = {u3_prom:.2f} pts.")
    if u3_prom < u2_prom:
        print(f"      Se observa una baja generalizada en la Unidad 3 (decremento de {u2_prom - u3_prom:.2f} puntos)")
        print("      respecto a la Unidad 2. Esto ocurre con frecuencia al final del semestre debido a la entrega")
        print("      de proyectos integradores y exámenes finales acumulativos en todas las materias simultáneamente.")
    else:
        print("      Se observa un incremento o estabilidad en el desempeño de la Unidad 3.")

    # Pregunta 3: Cuántos alumnos tienen un promedio general menor a 70
    alumnos_en_riesgo = prom_alumnos[prom_alumnos["promedio_calificacion"] < 70]
    total_en_riesgo = len(alumnos_en_riesgo)
    print(f"\n3) ¿Cuántos alumnos tienen un promedio general menor a 70 (en riesgo de reprobación)?")
    print(f"   -> Respuesta: {total_en_riesgo} alumno(s) de 24 estudiantes totales ({(total_en_riesgo / 24) * 100:.1f}%).")
    print("      Lista detallada de estudiantes en riesgo:")
    for _, fila in alumnos_en_riesgo.iterrows():
        print(f"      - Matrícula: {fila['matricula']} | {fila['nombre']} (Grupo {fila['grupo']}): {fila['promedio_calificacion']:.2f} pts")

    print("\n" + "=" * 80)
    print(" [OK] EJECUCIÓN COMPLETA Y EXITOSA DE TODOS LOS EJERCICIOS (1 AL 6)")
    print("=" * 80)


if __name__ == "__main__":
    main()
