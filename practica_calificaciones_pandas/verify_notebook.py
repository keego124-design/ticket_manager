import sys
import json
from pathlib import Path

if sys.stdout.encoding != "utf-8":
    try:
        sys.stdout.reconfigure(encoding="utf-8")
    except Exception:
        pass

p = Path("practica_pandas.ipynb")
with open(p, "r", encoding="utf-8") as f:
    nb = json.load(f)

print("=" * 80)
print(" VALIDACIÓN ESTRUCTURAL DE PRACTICA_PANDAS.IPYNB")
print("=" * 80)
print(f"Total de celdas: {len(nb['cells'])}")
print("-" * 80)

for idx, cell in enumerate(nb['cells']):
    ctype = cell['cell_type']
    first_line = cell['source'][0].strip() if cell['source'] else '<vacía>'
    outputs = len(cell.get('outputs', []))
    exec_num = cell.get('execution_count')
    print(f"Celda {idx:02d} [{ctype.upper():8}] (Exec #{str(exec_num):4}, Outs: {outputs}) -> {first_line[:65]}")

print("=" * 80)
