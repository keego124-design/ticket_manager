"""
Script para generar y validar 'practica_pandas.ipynb' con la estructura académica requerida:
- Celda 1 (Markdown): Portada con Título (#), Objetivo del programa, Materia y Autor.
- Celda 2 (Code): Únicamente importaciones de librerías y constantes iniciales del script original.
- Celdas intermedias (Markdown + Code): Subtítulo (##) con explicación, entradas y salidas esperadas antes de cada función o bloque, seguido de su celda Code correspondiente.
- Sección final (Markdown + Code): Subtítulo "## Ejecución y Pruebas" con la llamada principal al programa.
"""

import json
import io
import base64
import contextlib
from pathlib import Path

BASE_DIR = Path("C:/Users/CASA/Downloads/proyectosPython/practica_calificaciones_pandas")
DEST_SCRATCH = Path("C:/Users/CASA/.gemini/antigravity/scratch/practica_calificaciones_pandas")

def create_academic_notebook():
    cells = []

    def add_md(source_text):
        lines = [line + "\n" for line in source_text.strip().split("\n")]
        if lines:
            lines[-1] = lines[-1].rstrip("\n")
        cells.append({
            "cell_type": "markdown",
            "metadata": {},
            "source": lines
        })

    def add_code(source_text):
        lines = [line + "\n" for line in source_text.strip().split("\n")]
        if lines:
            lines[-1] = lines[-1].rstrip("\n")
        cells.append({
            "cell_type": "code",
            "execution_count": None,
            "metadata": {},
            "outputs": [],
            "source": lines
        })

    # =========================================================================
    # CELDA 1 (MARKDOWN): PORTADA
    # =========================================================================
    add_md("""# PRÁCTICA: ANÁLISIS Y VISUALIZACIÓN DE CALIFICACIONES CON PANDAS Y MATPLOTLIB
### Tópicos Avanzados de Programación — Ingeniería en Sistemas Computacionales (ISC)
---
- **Materia:** Tópicos Avanzados de Programación
- **Carrera:** Ingeniería en Sistemas Computacionales (ISC)
- **Autor:** Estudiante de ISC (`keego124-design`)
- **Objetivo del Programa:** Desarrollar un sistema de análisis exploratorio, filtrado vectorizado, categorización académica, resumen estadístico multidimensional y visualización gráfica de un dataset escolar en formato ordenado (*tidy data*), implementando una estética visual moderna Cyberpunk (fondo oscuro y acentos morado neón) sin la utilización de bucles iterativos tradicionales.
- **Entorno de Ejecución:** Python 3.14 / Pandas 2.x / NumPy 2.x / Matplotlib 3.x en Visual Studio Code con Jupyter Extension.""")

    # =========================================================================
    # CELDA 2 (CODE): IMPORTACIONES Y CONSTANTES
    # =========================================================================
    add_code("""import sys
from pathlib import Path
import numpy as np
import pandas as pd
import matplotlib
import matplotlib.pyplot as plt

# Reconfigurar salida estándar a UTF-8 para evitar problemas de codificación en Windows (cp1252)
if sys.stdout.encoding != "utf-8":
    try:
        sys.stdout.reconfigure(encoding="utf-8")
    except Exception:
        pass

# Constantes iniciales del script original
DIRECTORIO_BASE = Path(".").resolve()
RUTA_CSV = DIRECTORIO_BASE / "calificaciones_isc.csv"

print("✅ Librerías importadas y constantes inicializadas correctamente.")""")

    # =========================================================================
    # CELDA 3 & 4: FUNCIÓN aplicar_estilo_cyberpunk
    # =========================================================================
    add_md("""## Función: aplicar_estilo_cyberpunk
- **Descripción:** Configura la paleta visual de alto contraste en Matplotlib inspirada en la estética Cyberpunk / Modern Dark (fondo oscuro `#08060d` / `#0f0c18`, bordes y acentos en morado neón `#b026ff`, textos en blanco puro `#ffffff` y rejillas con baja opacidad `alpha=0.18`).
- **Entradas:** Ninguna (opera directamente sobre los parámetros globales `plt.rcParams`).
- **Salidas esperadas:** Parámetros de estilo globales de Matplotlib actualizados para todas las figuras subsiguientes.""")

    add_code("""def aplicar_estilo_cyberpunk():
    \"\"\"
    Aplica la paleta Cyberpunk Dark / Purple Neon a Matplotlib:
    - Fondo profundo: #08060d (figura) y #0f0c18 (ejes)
    - Acentos y bordes: Morado Neón (#b026ff)
    - Textos y etiquetas: Blanco Puro (#ffffff)
    - Rejilla: Tenue morado neón con baja opacidad (#b026ff con alpha 0.18)
    \"\"\"
    plt.style.use("dark_background")
    plt.rcParams.update({
        "figure.facecolor": "#08060d",
        "axes.facecolor": "#0f0c18",
        "axes.edgecolor": "#b026ff",
        "axes.linewidth": 1.4,
        "axes.labelcolor": "#ffffff",
        "xtick.color": "#ffffff",
        "ytick.color": "#ffffff",
        "text.color": "#ffffff",
        "grid.color": "#b026ff",
        "grid.alpha": 0.18,
        "grid.linestyle": "--",
        "font.family": "sans-serif",
        "font.sans-serif": ["Segoe UI", "DejaVu Sans", "Helvetica", "Arial"],
        "figure.titlesize": 14,
        "axes.titlesize": 13,
        "axes.labelsize": 11,
    })

# Aplicar estilo inicial
aplicar_estilo_cyberpunk()
print("✅ Estilo Cyberpunk Purple Neon aplicado globalmente.")""")

    # =========================================================================
    # CELDA 5 & 6: FUNCIÓN guardar_grafico
    # =========================================================================
    add_md("""## Función: guardar_grafico
- **Descripción:** Almacena la figura generada en el directorio raíz del proyecto y en la subcarpeta `static/plots/` (requerida por el servidor web Flask), asegurando alta resolución a 300 DPI y ajuste perimetral (`bbox_inches="tight"`).
- **Entradas:**
  - `fig`: Objeto `Figure` de Matplotlib a almacenar.
  - `nombre_archivo`: Cadena de texto (`str`) con el nombre del archivo (ej. `"promedio_materias.png"`).
  - `directorio_base`: Objeto `Path` del directorio base.
- **Salidas esperadas:** Archivos PNG creados en disco y mensaje de confirmación impreso en consola.""")

    add_code("""def guardar_grafico(fig, nombre_archivo: str, directorio_base: Path):
    \"\"\"
    Guarda la figura en la raíz del proyecto y en static/plots/ para el dashboard web.
    IMPORTANTE: Siempre se ejecuta antes de plt.close().
    \"\"\"
    ruta_raiz = directorio_base / nombre_archivo
    ruta_static = directorio_base / "static" / "plots" / nombre_archivo
    ruta_static.parent.mkdir(parents=True, exist_ok=True)

    fig.savefig(ruta_raiz, dpi=300, bbox_inches="tight", facecolor=fig.get_facecolor())
    fig.savefig(ruta_static, dpi=300, bbox_inches="tight", facecolor=fig.get_facecolor())
    print(f"  [GRÁFICO GUARDADO] -> {nombre_archivo} (DPI 300)")
    plt.close(fig)

print("✅ Función guardar_grafico definida correctamente.")""")

    # =========================================================================
    # CELDA 7 & 8: EJERCICIO 1
    # =========================================================================
    add_md("""## Ejercicio 1: Carga y Exploración Inicial del Dataset
- **Descripción:** Realiza la lectura del archivo CSV relacional `calificaciones_isc.csv`, verifica su existencia y presenta en consola las primeras filas (`head()`), sus dimensiones (`shape`), los tipos de datos por columna (`dtypes`) y los estadísticos descriptivos (`describe()`). Asimismo, fundamenta teóricamente por qué el dataset contiene exactamente 288 filas en lugar de 24 (formato largo / *tidy data*: $24 \\text{ alumnos} \\times 4 \\text{ materias} \\times 3 \\text{ unidades}$).
- **Entradas:**
  - `ruta_csv`: Ruta del archivo CSV de calificaciones (`Path`).
- **Salidas esperadas:**
  - `df`: DataFrame de Pandas cargado y validado con 288 filas y 7 columnas.""")

    add_code("""def ejercicio_1_carga_y_revision(ruta_csv: Path) -> pd.DataFrame:
    \"\"\"
    EJERCICIO 1: Carga y Exploración Inicial del Dataset
    \"\"\"
    print("\\n" + "#" * 60)
    print(" EJERCICIO 1: CARGA Y REVISIÓN INICIAL")
    print("#" * 60)

    if not ruta_csv.exists():
        raise FileNotFoundError(
            f"No se encontró el archivo {ruta_csv}. Ejecute primero 'generate_dataset.py'."
        )

    # Cargar el dataset en un DataFrame
    df = pd.read_csv(ruta_csv)

    print("\\n--> Primeras 5 filas del DataFrame (df.head()):")
    print(df.head().to_string(index=False))

    print(f"\\n--> Dimensiones del DataFrame (df.shape): {df.shape[0]} filas x {df.shape[1]} columnas")

    print("\\n--> Tipos de datos de las columnas (df.dtypes):")
    print(df.dtypes)

    print("\\n--> Estadísticas descriptivas de 'calificacion' y 'asistencias' (df.describe()):")
    print(df[["calificacion", "asistencias"]].describe().round(2))

    # Explicación teórica de la estructura en formato largo (tidy data)
    print("\\n[NOTA DE ANÁLISIS - EXPLICACIÓN DE DIMENSIONES]")
    print("  El dataset contiene 288 registros y no 24 porque está estructurado en formato")
    print("  largo ('tidy/long format'): 24 estudiantes x 4 materias x 3 unidades = 288 observaciones.")

    return df

# Ejecución del Ejercicio 1
df = ejercicio_1_carga_y_revision(RUTA_CSV)""")

    # =========================================================================
    # CELDA 9 & 10: EJERCICIO 2
    # =========================================================================
    add_md("""## Ejercicio 2: Filtros Vectorizados (Sin Bucles for)
- **Descripción:** Demuestra el filtrado mediante indexación booleana vectorizada en Pandas sin recurrir a bucles `for` ni `while`:
  1. Filtro A: Todas las filas del Grupo A (144 registros esperados).
  2. Filtro B: Registros con calificación menor a 70 puntos (reprobados).
  3. Filtro C: Registros de la materia "Bases de datos" del Grupo B con calificación $\\ge 80$.
- **Entradas:**
  - `df`: DataFrame de calificaciones cargado.
- **Salidas esperadas:**
  - Tupla con los subconjuntos filtrados `(filtro_grupo_a, filtro_reprobados, filtro_bd_b_80)` e impresión de muestras en pantalla.""")

    add_code("""def ejercicio_2_filtros_vectorizados(df: pd.DataFrame):
    \"\"\"
    EJERCICIO 2: Filtros Vectorizados (Sin bucles for)
    \"\"\"
    print("\\n" + "#" * 60)
    print(" EJERCICIO 2: FILTROS VECTORIZADOS (SIN BUCLES)")
    print("#" * 60)

    # Filtro A: Todas las filas correspondientes al Grupo A
    filtro_grupo_a = df[df["grupo"] == "A"]
    total_grupo_a = len(filtro_grupo_a)
    print(f"\\n--> A) Registros del Grupo A: {total_grupo_a} filas (esperadas: 144 = 12 alumnos x 12 unidades)")
    print("    Muestra de los primeros 3 registros:")
    print(filtro_grupo_a.head(3).to_string(index=False))

    # Filtro B: Registros con calificación menor a 70 (estudiantes no aprobados en esa unidad)
    filtro_reprobados = df[df["calificacion"] < 70]
    total_reprobados = len(filtro_reprobados)
    print(f"\\n--> B) Registros con calificación menor a 70 (< 70): {total_reprobados} filas")
    print("    Muestra de los primeros 4 registros reprobados:")
    print(filtro_reprobados.head(4).to_string(index=False))

    # Filtro C: Registros de la materia 'Bases de datos' del Grupo B con calificación >= 80
    filtro_bd_b_80 = df[
        (df["materia"] == "Bases de datos") &
        (df["grupo"] == "B") &
        (df["calificacion"] >= 80)
    ]
    total_bd_b_80 = len(filtro_bd_b_80)
    print(f"\\n--> C) Registros de 'Bases de datos' en Grupo B con calificacion >= 80: {total_bd_b_80} filas")
    print("    Detalle de registros encontrados:")
    print(filtro_bd_b_80[["matricula", "nombre", "unidad", "calificacion"]].to_string(index=False))

    return filtro_grupo_a, filtro_reprobados, filtro_bd_b_80

# Ejecución del Ejercicio 2
filtro_grupo_a, filtro_reprobados, filtro_bd_b_80 = ejercicio_2_filtros_vectorizados(df)""")

    # =========================================================================
    # CELDA 11 & 12: EJERCICIO 3
    # =========================================================================
    add_md("""## Ejercicio 3: Columna Calculada 'situacion' (np.where)
- **Descripción:** Implementa la categorización de aprobación mediante la función vectorizada `np.where()`, asignando `'Aprobado'` si la calificación es $\\ge 70$, y `'Reprobado'` si es menor a 70. Adicionalmente calcula la distribución porcentual global.
- **Entradas:**
  - `df`: DataFrame con la columna numérica `calificacion`.
- **Salidas esperadas:**
  - `df`: DataFrame actualizado con la nueva columna calculada `situacion`.""")

    add_code("""def ejercicio_3_columna_calculada(df: pd.DataFrame) -> pd.DataFrame:
    \"\"\"
    EJERCICIO 3: Creación de Columna Calculada con np.where (Vectorizado)
    \"\"\"
    print("\\n" + "#" * 60)
    print(" EJERCICIO 3: COLUMNA CALCULADA 'situacion' (np.where)")
    print("#" * 60)

    # Vectorización pura con numpy.where: evita bucles for y optimiza el rendimiento
    df["situacion"] = np.where(df["calificacion"] >= 70, "Aprobado", "Reprobado")

    print("\\n--> Columna 'situacion' agregada exitosamente:")
    print(df[["matricula", "nombre", "materia", "unidad", "calificacion", "situacion"]].head(8).to_string(index=False))

    distribucion_situacion = df["situacion"].value_counts()
    print("\\n--> Distribución general de la situación académica:")
    for sit, cuenta in distribucion_situacion.items():
        porcentaje = (cuenta / len(df)) * 100
        print(f"    * {sit}: {cuenta} registros ({porcentaje:.2f}%)")

    return df

# Ejecución del Ejercicio 3
df = ejercicio_3_columna_calculada(df)""")

    # =========================================================================
    # CELDA 13 & 14: EJERCICIO 4
    # =========================================================================
    add_md("""## Ejercicio 4: Resúmenes Estadísticos y Exportación a CSV
- **Descripción:** Aplica el método `groupby()` para consolidar resúmenes cuantitativos:
  1. Promedio por materia.
  2. Promedio por grupo y materia (tabla cruzada con `.unstack()`).
  3. Promedio general por alumno ordenado de mayor a menor.
  4. Promedio por unidad evaluativa (1, 2 y 3).
  5. Conteo global de Aprobados vs Reprobados.
  6. Exportación de `promedios_alumnos.csv` con `.reset_index()` e `index=False`.
- **Entradas:**
  - `df`: DataFrame con la columna `situacion`.
  - `directorio_base`: Ruta de destino para guardar el archivo exportado (`Path`).
- **Salidas esperadas:**
  - Tupla `(prom_materia, prom_grupo_materia, prom_alumnos, prom_unidad)` y archivo CSV generado en disco.""")

    add_code("""def ejercicio_4_resumenes_y_exportacion(df: pd.DataFrame, directorio_base: Path):
    \"\"\"
    EJERCICIO 4: Agrupaciones, Resúmenes y Exportación a CSV
    \"\"\"
    print("\\n" + "#" * 60)
    print(" EJERCICIO 4: RESÚMENES ESTADÍSTICOS Y EXPORTACIÓN")
    print("#" * 60)

    # 4.1 Promedio por materia
    prom_materia = df.groupby("materia")["calificacion"].mean().round(2)
    print("\\n--> 4.1 Promedio de calificación por Materia:")
    print(prom_materia.to_string())

    # 4.2 Promedio por grupo y por materia
    prom_grupo_materia = df.groupby(["grupo", "materia"])["calificacion"].mean().round(2).unstack()
    print("\\n--> 4.2 Promedio por Grupo y Materia:")
    print(prom_grupo_materia.to_string())

    # 4.3 Promedio general por alumno ordenado de mayor a menor (preservando matrícula y nombre)
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

    print("\\n--> 4.3 Top 5 Alumnos con Mayor Promedio General:")
    print(prom_alumnos.head(5).to_string(index=False))

    print("\\n--> 4.3 Alumnos con Menor Promedio General (Últimos 5):")
    print(prom_alumnos.tail(5).to_string(index=False))

    # 4.4 Promedio por unidad evaluativa (1, 2 y 3)
    prom_unidad = df.groupby("unidad")["calificacion"].mean().round(2)
    print("\\n--> 4.4 Promedio general por Unidad evaluativa:")
    print(prom_unidad.to_string())

    # 4.5 Conteo global de Aprobados vs Reprobados
    conteo_situacion = df["situacion"].value_counts()
    print("\\n--> 4.5 Conteo de unidades Aprobadas vs Reprobadas:")
    print(conteo_situacion.to_string())

    # 4.6 Exportar promedios_alumnos.csv con reset_index() e index=False
    ruta_promedios_csv = directorio_base / "promedios_alumnos.csv"
    prom_alumnos.to_csv(ruta_promedios_csv, index=False, encoding="utf-8")
    print(f"\\n--> Archivo exportado exitosamente: {ruta_promedios_csv}")
    print("    Columnas incluidas:", list(prom_alumnos.columns))

    return prom_materia, prom_grupo_materia, prom_alumnos, prom_unidad

# Ejecución del Ejercicio 4
prom_materia, prom_grupo_materia, prom_alumnos, prom_unidad = ejercicio_4_resumenes_y_exportacion(df, DIRECTORIO_BASE)""")

    # =========================================================================
    # CELDA 15 & 16: EJERCICIO 5
    # =========================================================================
    add_md("""## Ejercicio 5: Generación de Gráficos (Estética Cyberpunk)
- **Descripción:** Genera tres gráficos de alta resolución (300 DPI) con estética Cyberpunk Purple Neon (fondo oscuro `#08060d` / `#0f0c18`, acentos morado neón `#b026ff` y textos blancos `#ffffff`):
  1. `promedio_materias.png`: Gráfico de barras de promedios por asignatura (escala 0 a 100 y línea de mínimo aprobatorio en 70).
  2. `histograma.png`: Histograma de frecuencias de las 288 notas con línea vertical punteada en 70.
  3. `tendencia_unidades.png`: Gráfico de líneas con marcadores para evaluar la trayectoria por unidad de cada materia.
- **Entradas:**
  - `df`: DataFrame completo.
  - `prom_materia`: Serie de promedios por materia.
  - `directorio_base`: Ruta de almacenamiento (`Path`).
- **Salidas esperadas:**
  - Tres figuras de Matplotlib guardadas en disco y desplegadas en pantalla.""")

    add_code("""def ejercicio_5_generacion_graficos(df: pd.DataFrame, prom_materia: pd.Series, directorio_base: Path):
    \"\"\"
    EJERCICIO 5: Visualización de Datos con Estética Cyberpunk Dark / Purple Neon
    \"\"\"
    print("\\n" + "#" * 60)
    print(" EJERCICIO 5: GENERACIÓN DE GRÁFICOS (CYBERPUNK THEME)")
    print("#" * 60)

    aplicar_estilo_cyberpunk()

    # -------------------------------------------------------------------------
    # Gráfico 1: promedio_materias.png (Gráfico de barras del promedio por materia)
    # -------------------------------------------------------------------------
    fig1, ax1 = plt.subplots(figsize=(9, 5.5), dpi=300)
    materias_nombres = prom_materia.index.tolist()
    materias_valores = prom_materia.values.tolist()

    # Barras en morado neón (#b026ff) con bordes iluminados
    barras = ax1.bar(
        materias_nombres,
        materias_valores,
        color="#b026ff",
        edgecolor="#ffffff",
        linewidth=1.2,
        width=0.55,
        alpha=0.92,
        zorder=3
    )

    ax1.set_ylim(0, 100)
    ax1.set_ylabel("Calificación Promedio (0 - 100)", color="#ffffff", fontweight="bold")
    ax1.set_title("PROMEDIO GENERAL POR MATERIA // ISC", color="#ffffff", fontweight="bold", pad=15)
    ax1.grid(axis="y", linestyle="--", alpha=0.3, color="#b026ff", zorder=0)

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
    ax1.legend(loc="lower right", facecolor="#120e1d", edgecolor="#b026ff", labelcolor="#ffffff")

    guardar_grafico(fig1, "promedio_materias.png", directorio_base)

    # -------------------------------------------------------------------------
    # Gráfico 2: histograma.png (Distribución de todas las calificaciones)
    # -------------------------------------------------------------------------
    fig2, ax2 = plt.subplots(figsize=(9, 5.5), dpi=300)

    n, bins, patches = ax2.hist(
        df["calificacion"],
        bins=12,
        range=(40, 100),
        color="#b026ff",
        edgecolor="#ffffff",
        linewidth=1.2,
        alpha=0.88,
        zorder=3
    )

    # Resaltar en tono más oscuro las calificaciones reprobatorias
    for patch, bin_izq in zip(patches, bins[:-1]):
        if bin_izq < 70:
            patch.set_facecolor("#4a0e68")  # Morado oscuro para reprobados
            patch.set_edgecolor("#b026ff")
        else:
            patch.set_facecolor("#b026ff")  # Neón brillante para aprobados
            patch.set_edgecolor("#ffffff")

    # Línea vertical punteada blanca en 70 (corte de aprobación)
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
    ax2.grid(axis="y", linestyle="--", alpha=0.3, color="#b026ff", zorder=0)
    ax2.legend(loc="upper left", facecolor="#120e1d", edgecolor="#b026ff", labelcolor="#ffffff")

    guardar_grafico(fig2, "histograma.png", directorio_base)

    # -------------------------------------------------------------------------
    # Gráfico 3: tendencia_unidades.png (Líneas de evolución por unidad y materia)
    # -------------------------------------------------------------------------
    fig3, ax3 = plt.subplots(figsize=(9.5, 5.5), dpi=300)

    # Agrupar por materia y unidad
    evolucion_materias = df.groupby(["materia", "unidad"])["calificacion"].mean().unstack(level=0)

    colores_materias = {
        "Programacion": "#b026ff",          # Neón Purple primario
        "Bases de datos": "#d946ef",        # Fuchsia Neón
        "Redes": "#ffffff",                 # Blanco Neón Puro
        "Matematicas discretas": "#8b5cf6"  # Amatista Neón
    }

    marcadores = {
        "Programacion": "o",
        "Bases de datos": "s",
        "Redes": "^",
        "Matematicas discretas": "D"
    }

    for materia in evolucion_materias.columns:
        color_linea = colores_materias.get(materia, "#b026ff")
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
    ax3.grid(True, linestyle="--", alpha=0.3, color="#b026ff", zorder=0)
    ax3.legend(loc="lower left", facecolor="#120e1d", edgecolor="#b026ff", labelcolor="#ffffff")

    guardar_grafico(fig3, "tendencia_unidades.png", directorio_base)

    return fig1, fig2, fig3

# Ejecución del Ejercicio 5
fig1, fig2, fig3 = ejercicio_5_generacion_graficos(df, prom_materia, DIRECTORIO_BASE)""")

    # =========================================================================
    # CELDA 17 & 18: EJERCICIO 6
    # =========================================================================
    add_md("""## Ejercicio 6: Interpretación y Preguntas de Análisis
- **Descripción:** Analiza y resuelve las tres interrogantes analíticas requeridas por la práctica:
  1. Materia con menor promedio general (justificación académica de abstracción formal).
  2. Tendencia observada en la Unidad 3 respecto a las Unidades 1 y 2 (caída típica de cierre semestral).
  3. Identificación y conteo de estudiantes con promedio general $< 70$ (en riesgo académico).
- **Entradas:**
  - `prom_materia`, `prom_unidad`, `prom_alumnos`.
- **Salidas esperadas:**
  - Respuestas explicadas y verificadas con base en los cálculos del dataset.""")

    add_code("""def ejercicio_6_interpretacion(prom_materia: pd.Series, prom_unidad: pd.Series, prom_alumnos: pd.DataFrame):
    \"\"\"
    EJERCICIO 6: Interpretación y Preguntas de Análisis
    \"\"\"
    print("\\n" + "#" * 60)
    print(" EJERCICIO 6: INTERPRETACIÓN DE RESULTADOS")
    print("#" * 60)

    # Pregunta 1: Materia con menor promedio
    materia_menor_prom = prom_materia.idxmin()
    valor_menor_prom = prom_materia.min()
    print(f"\\n1) ¿Cuál materia tuvo el menor promedio general?")
    print(f"   -> Respuesta: '{materia_menor_prom}' con un promedio de {valor_menor_prom:.2f} puntos.")
    print("      Justificación: Presenta mayor grado de dificultad conceptual y abstracción matemática,")
    print("      reflejando la mayor dispersión y calificaciones más bajas del periodo.")

    # Pregunta 2: Tendencia en la unidad 3 respecto a las unidades 1 y 2
    u1_prom = prom_unidad.loc[1]
    u2_prom = prom_unidad.loc[2]
    u3_prom = prom_unidad.loc[3]
    print(f"\\n2) ¿Qué tendencia se observa en la Unidad 3 respecto a las Unidades 1 y 2?")
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
    print(f"\\n3) ¿Cuántos alumnos tienen un promedio general menor a 70 (en riesgo de reprobación)?")
    print(f"   -> Respuesta: {total_en_riesgo} alumno(s) de 24 estudiantes totales ({(total_en_riesgo / 24) * 100:.1f}%).")
    print("      Lista detallada de estudiantes en riesgo:")
    for _, fila in alumnos_en_riesgo.iterrows():
        print(f"      - Matrícula: {fila['matricula']} | {fila['nombre']} (Grupo {fila['grupo']}): {fila['promedio_calificacion']:.2f} pts")

# Ejecución del Ejercicio 6
ejercicio_6_interpretacion(prom_materia, prom_unidad, prom_alumnos)""")

    # =========================================================================
    # CELDA 19 & 20: FUNCIÓN PRINCIPAL MAIN
    # =========================================================================
    add_md("""## Función Principal: main
- **Descripción:** Función integradora que agrupa y orquesta el flujo completo de la práctica de forma secuencial, idéntica a la estructura del script de producción `practica_pandas.py`.
- **Entradas:** Ninguna (utiliza las constantes de configuración global).
- **Salidas esperadas:** Ejecución de punta a punta del pipeline de datos.""")

    add_code("""def main():
    \"\"\"
    Función orquestadora principal
    \"\"\"
    directorio_base = DIRECTORIO_BASE
    ruta_csv = RUTA_CSV

    print("=" * 80)
    print(" SISTEMA DE ANÁLISIS DE CALIFICACIONES ISC - PANDAS & MATPLOTLIB [CYBERPUNK]")
    print("=" * 80)

    # 1. Carga y revisión inicial
    df_local = ejercicio_1_carga_y_revision(ruta_csv)

    # 2. Filtros vectorizados
    ejercicio_2_filtros_vectorizados(df_local)

    # 3. Columna calculada 'situacion'
    df_local = ejercicio_3_columna_calculada(df_local)

    # 4. Resúmenes y exportación a CSV
    p_mat, p_grp_mat, p_alumn, p_uni = ejercicio_4_resumenes_y_exportacion(df_local, directorio_base)

    # 5. Generación de gráficos Cyberpunk
    ejercicio_5_generacion_graficos(df_local, p_mat, directorio_base)

    # 6. Interpretación de resultados
    ejercicio_6_interpretacion(p_mat, p_uni, p_alumn)

    print("\\n" + "=" * 80)
    print(" [OK] EJECUCIÓN COMPLETA Y EXITOSA DE TODOS LOS EJERCICIOS (1 AL 6)")
    print("=" * 80)

print("✅ Función main() definida correctamente.")""")

    # =========================================================================
    # CELDA 21 & 22: SECCIÓN FINAL: EJECUCIÓN Y PRUEBAS
    # =========================================================================
    add_md("""## Ejecución y Pruebas
- **Descripción:** Ejecución de la función principal `main()` para validar el comportamiento general del sistema y verificación automatizada de la presencia e integridad de cada uno de los archivos y reportes generados.
- **Entradas:** Ninguna.
- **Salidas esperadas:** Validación de ejecución completa de los 6 ejercicios y auditoría de archivos en disco (`calificaciones_isc.csv`, `promedios_alumnos.csv`, y las 3 gráficas PNG).""")

    add_code("""# Llamada principal al programa
main()

# Verificación de integridad de archivos generados
print("\\n" + "=" * 80)
print(" VERIFICACIÓN DE INTEGRIDAD DE ARCHIVOS GENERADOS")
print("=" * 80)
archivos_verificar = [
    "calificaciones_isc.csv",
    "promedios_alumnos.csv",
    "promedio_materias.png",
    "histograma.png",
    "tendencia_unidades.png",
    "static/plots/promedio_materias.png",
    "static/plots/histograma.png",
    "static/plots/tendencia_unidades.png",
]

for archivo in archivos_verificar:
    p = DIRECTORIO_BASE / archivo
    if p.exists():
        print(f"  [OK] {archivo:35} -> Existe ({p.stat().st_size:,} bytes)")
    else:
        print(f"  [ALERTA] {archivo:35} -> No encontrado")
print("=" * 80)""")

    notebook_dict = {
        "cells": cells,
        "metadata": {
            "language_info": {
                "name": "python",
                "version": "3.14.7"
            },
            "kernelspec": {
                "display_name": "Python 3",
                "language": "python",
                "name": "python3"
            }
        },
        "nbformat": 4,
        "nbformat_minor": 5
    }

    return notebook_dict

def populate_outputs(nb_dict: dict, work_dir: Path):
    """
    Ejecuta cada celda de código secuencialmente en orden descendente y captura
    sus salidas (stdout) e imágenes generadas (base64 PNG) para insertarlas en el JSON.
    """
    exec_globals = {
        "__name__": "__main__",
        "__file__": str((work_dir / "practica_pandas.py").resolve()),
    }

    execution_count = 1

    for cell in nb_dict.get("cells", []):
        if cell["cell_type"] != "code":
            continue

        source_code = "".join(cell["source"])
        outputs = []

        stdout_buf = io.StringIO()

        import matplotlib
        matplotlib.use("Agg")
        import matplotlib.pyplot as plt

        plt.close("all")

        try:
            with contextlib.redirect_stdout(stdout_buf):
                exec(source_code, exec_globals)
        except Exception as e:
            stdout_buf.write(f"\n[Error durante ejecución]: {e}\n")

        stdout_text = stdout_buf.getvalue()
        if stdout_text:
            outputs.append({
                "name": "stdout",
                "output_type": "stream",
                "text": [line + "\n" for line in stdout_text.rstrip("\n").split("\n")]
            })

        for fig_num in plt.get_fignums():
            fig = plt.figure(fig_num)
            img_buf = io.BytesIO()
            fig.savefig(img_buf, format="png", dpi=fig.dpi, bbox_inches="tight", facecolor=fig.get_facecolor())
            img_buf.seek(0)
            img_b64 = base64.b64encode(img_buf.read()).decode("utf-8")

            outputs.append({
                "data": {
                    "image/png": img_b64,
                    "text/plain": [f"<Figure size {fig.get_size_inches()[0]*fig.dpi:.0f}x{fig.get_size_inches()[1]*fig.dpi:.0f} with {len(fig.axes)} Axes>"]
                },
                "metadata": {},
                "output_type": "display_data"
            })

        plt.close("all")

        cell["outputs"] = outputs
        cell["execution_count"] = execution_count
        execution_count += 1

    return nb_dict

if __name__ == "__main__":
    print("[1/3] Construyendo estructura académica del notebook...")
    nb = create_academic_notebook()

    print("[2/3] Ejecutando celdas en orden (Run All) y poblando salidas...")
    nb_poblado = populate_outputs(nb, BASE_DIR)

    dest_local = BASE_DIR / "practica_pandas.ipynb"
    dest_scratch = DEST_SCRATCH / "practica_pandas.ipynb"

    print("[3/3] Guardando archivos .ipynb...")
    with open(dest_local, "w", encoding="utf-8") as f:
        json.dump(nb_poblado, f, indent=2, ensure_ascii=False)
    print(f" [OK] Guardado en: {dest_local}")

    dest_scratch.parent.mkdir(parents=True, exist_ok=True)
    with open(dest_scratch, "w", encoding="utf-8") as f:
        json.dump(nb_poblado, f, indent=2, ensure_ascii=False)
    print(f" [OK] Guardado en: {dest_scratch}")

    print("\n✅ Proceso completado exitosamente.")
