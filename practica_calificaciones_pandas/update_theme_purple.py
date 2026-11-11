"""
Script para actualizar la estética a Cyberpunk Neon Purple (#b026ff)
en practica_pandas.py y build_notebook.py
"""

from pathlib import Path

BASE_DIR = Path("C:/Users/CASA/Downloads/proyectosPython/practica_calificaciones_pandas")

# 1. Actualizar practica_pandas.py
p_pandas = BASE_DIR / "practica_pandas.py"
with open(p_pandas, "r", encoding="utf-8") as f:
    code = f.read()

replacements_pandas = [
    ("Fondo Negro #0b0b0b, Neón Rojo #ff1e42", "Fondo Negro #08060d, Neón Morado #b026ff"),
    ("Cyberpunk Dark / Red Neon", "Cyberpunk Dark / Purple Neon"),
    ('"figure.facecolor": "#0b0b0b"', '"figure.facecolor": "#08060d"'),
    ('"axes.facecolor": "#111116"', '"axes.facecolor": "#0f0c18"'),
    ('"axes.edgecolor": "#ff1e42"', '"axes.edgecolor": "#b026ff"'),
    ('"grid.color": "#ff1e42"', '"grid.color": "#b026ff"'),
    ('color="#ff1e42"', 'color="#b026ff"'),
    ('edgecolor="#ff1e42"', 'edgecolor="#b026ff"'),
    ('#8a0f24', '#4a0e68'),
    ('#ff1e42', '#b026ff'),
    ('#111116', '#120e1d'),
    ('#ff6b8b', '#d946ef'),
    ('#c40030', '#8b5cf6'),
]

for old, new in replacements_pandas:
    code = code.replace(old, new)

with open(p_pandas, "w", encoding="utf-8") as f:
    f.write(code)
print(f"[OK] {p_pandas.name} actualizado.")

# 2. Actualizar build_notebook.py
p_nb = BASE_DIR / "build_notebook.py"
with open(p_nb, "r", encoding="utf-8") as f:
    nb_code = f.read()

replacements_nb = [
    ("Fondo Negro Profundo (`#070709` / `#0b0b0b`), Acentos Neón Rojo (`#ff1e42` / `#ff0055`)",
     "Fondo Negro Profundo (`#07060a` / `#08060d`), Acentos Neón Morado (`#b026ff` / `#d946ef`)"),
    ("Cyberpunk Red Neon", "Cyberpunk Purple Neon"),
    ("Dark & Red Neon", "Dark & Purple Neon"),
    ('"figure.facecolor": "#0b0b0b"', '"figure.facecolor": "#08060d"'),
    ('"axes.facecolor": "#111116"', '"axes.facecolor": "#0f0c18"'),
    ('"axes.edgecolor": "#ff1e42"', '"axes.edgecolor": "#b026ff"'),
    ('"grid.color": "#ff1e42"', '"grid.color": "#b026ff"'),
    ('color="#ff1e42"', 'color="#b026ff"'),
    ('edgecolor="#ff1e42"', 'edgecolor="#b026ff"'),
    ('#8a0f24', '#4a0e68'),
    ('#ff1e42', '#b026ff'),
    ('#111116', '#120e1d'),
    ('#ff6b8b', '#d946ef'),
    ('#c40030', '#8b5cf6'),
]

for old, new in replacements_nb:
    nb_code = nb_code.replace(old, new)

with open(p_nb, "w", encoding="utf-8") as f:
    f.write(nb_code)
print(f"[OK] {p_nb.name} actualizado.")
