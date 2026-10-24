# 🔴 PRÁCTICA: ANÁLISIS Y VISUALIZACIÓN DE CALIFICACIONES CON PANDAS Y MATPLOTLIB
### Ingeniería en Sistemas Computacionales (ISC) — Tópicos Avanzados de Programación
> **Estética Visual:** Cyberpunk / Modern Dark  
> **Paleta Cromática:** Fondo Negro Profundo (`#070709` / `#0b0b0b`), Acentos Neón Rojo (`#ff1e42` / `#ff0055`) y Textos Blanco Puro (`#ffffff`).

---

## 📋 Descripción del Proyecto

Este proyecto implementa una solución integral para el análisis exploratorio, agregación cuantitativa y visualización estadística de un dataset de calificaciones académicas de la carrera de Ingeniería en Sistemas Computacionales.

El sistema está desarrollado con **Python**, **Pandas**, **NumPy**, **Matplotlib** y una interfaz web interactiva en **Flask**, cumpliendo estrictamente con el formato tabular ordenado (*tidy data*) y técnicas vectorizadas que evitan bucles tradicionales `for`.

---

## 📁 Estructura del Repositorio

```text
practica_calificaciones_pandas/
│
├── calificaciones_isc.csv         # Dataset principal con exactamente 288 observaciones
├── promedios_alumnos.csv          # Archivo CSV exportado con promedios por alumno
├── generate_dataset.py            # Generador determinista del dataset académico
├── practica_pandas.py             # Script principal con los 6 Ejercicios resueltos
├── app.py                         # Servidor Flask con Dashboard Web interactivo
├── requirements.txt               # Lista de dependencias del entorno Python
├── README.md                      # Documentación completa y guía académica
│
├── promedio_materias.png          # Gráfica 1: Promedio por materia (Bar Chart)
├── histograma.png                 # Gráfica 2: Distribución de notas (Histogram)
├── tendencia_unidades.png         # Gráfica 3: Trayectoria por unidad (Line Plot)
│
├── static/
│   └── plots/                     # Copia de los gráficos para la plataforma web
│       ├── promedio_materias.png
│       ├── histograma.png
│       └── tendencia_unidades.png
└── templates/
    └── index.html                 # Interfaz visual del Dashboard en estética Cyberpunk
```

---

## ⚡ Instalación y Requisitos

### 1. Requisitos Previos
- Python 3.9 o superior instalado.
- Terminal / Consola de comandos (PowerShell, CMD o Bash).

### 2. Instalación de Dependencias
Ejecute en la raíz del proyecto:

```bash
pip install -r requirements.txt
```

*Contenido de dependencias:*
- `pandas>=2.0.0` (Estructuras DataFrame y operaciones de agregación)
- `numpy>=1.24.0` (Condicionales vectorizados con `np.where`)
- `matplotlib>=3.7.0` (Generación de gráficos con personalización Cyberpunk)
- `flask>=3.0.0` (Servidor web y API REST para el dashboard interactivo)

---

## 🚀 Guía de Ejecución

### Opción A: Ejecutar el Script de Análisis (Consola)
Para ejecutar los 6 ejercicios de la práctica y generar los reportes y gráficas:

```bash
python practica_pandas.py
```

Al terminar, se imprimirán en consola las tablas y respuestas de análisis, y se generarán los archivos:
- `promedios_alumnos.csv`
- `promedio_materias.png`
- `histograma.png`
- `tendencia_unidades.png`

---

### Opción B: Iniciar el Dashboard Web Interactivo (Flask)
Para explorar las calificaciones con filtros dinámicos, visualizador de gráficos y descargas:

```bash
python app.py
```

Abra su navegador web en la dirección:
👉 **`http://127.0.0.1:5000/`**

---

## 🔬 Desglose Técnico de los 6 Ejercicios

### 🔹 Ejercicio 1: Carga y Exploración Inicial
- Se lee el archivo `calificaciones_isc.csv` mediante `pd.read_csv()`.
- Se inspeccionan las primeras 5 filas (`df.head()`), las dimensiones del dataset (`df.shape` = `(288, 7)`), los tipos de datos de las columnas (`df.dtypes`) y los estadísticos descriptivos con `df[['calificacion', 'asistencias']].describe()`.

> **¿Por qué el archivo tiene 288 filas en lugar de 24?**  
> El dataset está diseñado en **formato largo (*tidy data*)**, donde cada fila representa una observación unitaria: la calificación obtenida por **un estudiante** en **una unidad evaluativa** de **una materia**.  
> El cálculo matemático es:  
> $$\text{Total Filas} = 24 \text{ alumnos} \times 4 \text{ materias} \times 3 \text{ unidades} = 288 \text{ registros}$$  
> Si tuviera 24 filas, tendría que estar en formato ancho (*wide format*) con 12 columnas de calificaciones diferentes, lo que imposibilitaría realizar agrupaciones directas por unidad o materia.

---

### 🔹 Ejercicio 2: Filtros Vectorizados (Sin bucles)
Se aplican máscaras booleanas vectorizadas directas de Pandas:
1. **Grupo A:** `df[df['grupo'] == 'A']` (144 filas).
2. **Reprobados:** `df[df['calificacion'] < 70]` (59 filas).
3. **Bases de Datos en Grupo B con nota $\ge 80$:**
   ```python
   filtro = df[(df['materia'] == 'Bases de datos') & (df['grupo'] == 'B') & (df['calificacion'] >= 80)]
   ```
   (26 registros coincidentes).

---

### 🔹 Ejercicio 3: Columna Calculada con `np.where`
Se agrega la columna `situacion` de forma 100% vectorizada:
```python
df['situacion'] = np.where(df['calificacion'] >= 70, 'Aprobado', 'Reprobado')
```
- **Aprobados:** 229 registros (79.51%)
- **Reprobados:** 59 registros (20.49%)

---

### 🔹 Ejercicio 4: Resúmenes y Exportación a CSV
Se calculan métricas agrupadas (`groupby`):
- **Promedio por Materia:**
  - *Programación:* 84.76 pts
  - *Bases de datos:* 82.21 pts
  - *Redes:* 79.35 pts
  - *Matemáticas discretas:* 74.90 pts
- **Promedio por Grupo y Materia:** Tabla cruzada con `.unstack()`.
- **Promedio General por Alumno:** Ordenado de mayor a menor con `.sort_values(ascending=False)`.
- **Promedio por Unidad:**
  - Unidad 1: 80.73 pts
  - Unidad 2: 83.10 pts
  - Unidad 3: 77.08 pts
- **Exportación:** Se genera `promedios_alumnos.csv` utilizando `.reset_index()` e `index=False` preservando `matricula`, `nombre`, `grupo`, `promedio_calificacion`, `promedio_asistencias`, `unidades_aprobadas` y `unidades_reprobadas`.

---

### 🔹 Ejercicio 5: Gráficas con Estética Cyberpunk Dark & Red Neon
Todas las figuras se configuraron bajo `plt.style.use('dark_background')` con los parámetros:
- Fondo de figura: `#0b0b0b`, fondo de ejes: `#111116`.
- Borde y acentos: Rojo neón (`#ff1e42`).
- Rejilla: Punteada (`--`) carmesí con baja opacidad (`alpha=0.18`).
- Textos y etiquetas: Blanco puro (`#ffffff`).
- Las figuras se guardan con `plt.savefig(..., dpi=300, bbox_inches='tight')` antes de cerrarlas.

1. `promedio_materias.png`: Gráfico de barras de promedios con eje Y de 0 a 100 y línea de referencia en 70.
2. `histograma.png`: Distribución de notas con línea vertical discontinua blanca en 70 ("Corte de Aprobación").
3. `tendencia_unidades.png`: Gráfico de líneas con marcadores personalizados que muestra la trayectoria de cada asignatura a través de las Unidades 1, 2 y 3.

---

### 🔹 Ejercicio 6: Interpretación y Respuestas Académicas

#### 1. ¿Cuál materia tuvo el menor promedio general?
> **Respuesta:** **Matemáticas discretas** con un promedio de **74.90 puntos**.  
> **Justificación:** Esta asignatura presenta mayor abstracción formal (lógica matemática, teoría de conjuntos, demostraciones y grafos), generando una mayor dispersión en las notas y mayor tasa de reprobación relativa en comparación con las materias de desarrollo práctico.

#### 2. ¿Qué tendencia se observa en la Unidad 3 respecto a las Unidades 1 y 2?
> **Respuesta:**
> - Unidad 1: **80.73 pts**
> - Unidad 2: **83.10 pts**
> - Unidad 3: **77.08 pts**  
> **Análisis:** Se observa una caída pronunciada de **6.02 puntos** en la Unidad 3 con respecto a la Unidad 2. Este fenómeno es característico del cierre de semestre, debido al agotamiento académico, la entrega simultánea de proyectos finales y la acumulación de exámenes departamentales.

#### 3. ¿Cuántos alumnos tienen un promedio general menor a 70?
> **Respuesta:** **4 alumnos** de un total de 24 estudiantes (un **16.7%** de la matrícula en condición de riesgo):
> 1. `ISC240109` — **Mateo Vargas** (Grupo A): **64.25 pts**
> 2. `ISC240119` — **Santiago Gomez** (Grupo B): **62.17 pts**
> 3. `ISC240105` — **Diego Ramirez** (Grupo A): **57.83 pts**
> 4. `ISC240123` — **Nicolas Paredes** (Grupo B): **57.58 pts**

---

## 🌐 Características del Dashboard Web (Flask)

- **Diseño Cyberpunk Responsivo:** Tipografías *Orbitron* e *Inter*, sombras de neón dinámicas y efectos hover de alto contraste.
- **KPI Metrics en Tiempo Real:** Total de registros, alumnos totales, promedio global, tasa de aprobación y alumnos en riesgo.
- **Visualizador Modal de Gráficos:** Inspección en alta resolución (DPI 300) al hacer clic en cualquiera de las 3 gráficas.
- **Motor de Filtrado Interactivo:** Filtrado instantáneo por grupo, materia y condición académica sin recargar la página.
- **Buscador en Vivo de Alumnos:** Búsqueda rápida por nombre o matrícula en la tabla de promedios.
- **Botón de Re-ejecución en Caliente:** Permite regenerar los cálculos y gráficas desde la interfaz web.

---

## 👨‍💻 Autor y Licencia
- **Materia:** Tópicos Avanzados de Programación // Ingeniería en Sistemas Computacionales
- **Entorno:** Python 3.14 / Pandas / Matplotlib / Flask
- **Licencia:** Material académico de libre uso educativo.
