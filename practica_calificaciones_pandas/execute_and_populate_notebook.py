"""
Script para ejecutar cada celda de 'practica_pandas.ipynb' en un entorno Python,
capturar salidas de consola (stdout) e imágenes generadas por Matplotlib (base64 PNG),
e inyectarlas en el notebook para que aparezcan renderizadas inmediatamente.
"""

import json
import io
import base64
import sys
import contextlib
from pathlib import Path

def run_notebook(nb_path: Path):
    with open(nb_path, "r", encoding="utf-8") as f:
        nb = json.load(f)

    # Contexto compartido de ejecución (variables globales)
    exec_globals = {
        "__name__": "__main__",
        "__file__": str(nb_path.resolve()),
    }

    execution_count = 1

    for cell in nb.get("cells", []):
        if cell["cell_type"] != "code":
            continue

        source_code = "".join(cell["source"])
        outputs = []

        # Buffer para capturar stdout
        stdout_buf = io.StringIO()
        
        import matplotlib
        matplotlib.use("Agg")
        import matplotlib.pyplot as plt

        # Limpiar figuras previas
        plt.close("all")

        try:
            with contextlib.redirect_stdout(stdout_buf):
                exec(source_code, exec_globals)
        except Exception as e:
            stdout_buf.write(f"\n[Error durante ejecución]: {e}\n")

        # Capturar texto de consola
        stdout_text = stdout_buf.getvalue()
        if stdout_text:
            outputs.append({
                "name": "stdout",
                "output_type": "stream",
                "text": [line + "\n" for line in stdout_text.rstrip("\n").split("\n")]
            })

        # Capturar figuras de Matplotlib generadas durante la celda
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

    with open(nb_path, "w", encoding="utf-8") as f:
        json.dump(nb, f, indent=2, ensure_ascii=False)

    print(f"[OK] Notebook ejecutado y poblado con salidas en: {nb_path}")

if __name__ == "__main__":
    p1 = Path("C:/Users/CASA/Downloads/proyectosPython/practica_calificaciones_pandas/practica_pandas.ipynb")
    p2 = Path("C:/Users/CASA/.gemini/antigravity/scratch/practica_calificaciones_pandas/practica_pandas.ipynb")
    run_notebook(p1)
    run_notebook(p2)
