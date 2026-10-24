"""
================================================================================
DASHBOARD INTERACTIVO FLASK // ANÁLISIS DE CALIFICACIONES ISC
Estética: Cyberpunk / Modern Dark (Fondo Negro #070709, Neón Rojo #ff1e42, Blanco #ffffff)
================================================================================
"""

import os
import sys
from pathlib import Path
from flask import Flask, render_template, jsonify, send_file, request

# Reconfigurar salida estándar en Windows
if sys.stdout.encoding != "utf-8":
    try:
        sys.stdout.reconfigure(encoding="utf-8")
    except Exception:
        pass

import pandas as pd
import numpy as np
import time

# Importar lógica principal de la práctica
import practica_pandas

app = Flask(__name__, static_folder="static", template_folder="templates")
BASE_DIR = Path(__file__).resolve().parent


def asegurar_archivos_generados():
    """Verifica si los datos y gráficos existen; si no, ejecuta el análisis."""
    csv_calif = BASE_DIR / "calificaciones_isc.csv"
    csv_prom = BASE_DIR / "promedios_alumnos.csv"
    plot_1 = BASE_DIR / "static" / "plots" / "promedio_materias.png"

    if not csv_calif.exists():
        import generate_dataset
        generate_dataset.guardar_csv(csv_calif)

    if not csv_prom.exists() or not plot_1.exists():
        practica_pandas.main()


@app.route("/")
def index():
    asegurar_archivos_generados()

    df = pd.read_csv(BASE_DIR / "calificaciones_isc.csv")
    if "situacion" not in df.columns:
        df["situacion"] = np.where(df["calificacion"] >= 70, "Aprobado", "Reprobado")

    df_promedios = pd.read_csv(BASE_DIR / "promedios_alumnos.csv")

    # Métricas clave
    total_registros = len(df)
    promedio_general = round(df["calificacion"].mean(), 2)
    aprobados_count = int((df["calificacion"] >= 70).sum())
    tasa_aprobacion = round((aprobados_count / total_registros) * 100, 1)
    alumnos_riesgo_count = int((df_promedios["promedio_calificacion"] < 70).sum())

    alumnos_lista = df_promedios.to_dict(orient="records")

    return render_template(
        "index.html",
        total_registros=total_registros,
        promedio_general=promedio_general,
        aprobados_count=aprobados_count,
        tasa_aprobacion=tasa_aprobacion,
        alumnos_riesgo_count=alumnos_riesgo_count,
        alumnos=alumnos_lista,
        timestamp=int(time.time()),
    )


@app.route("/api/datos")
def api_datos():
    """Retorna todos los registros de calificaciones con su situación para filtrado dinámico."""
    asegurar_archivos_generados()
    df = pd.read_csv(BASE_DIR / "calificaciones_isc.csv")
    if "situacion" not in df.columns:
        df["situacion"] = np.where(df["calificacion"] >= 70, "Aprobado", "Reprobado")
    return jsonify(df.to_dict(orient="records"))


@app.route("/api/alumnos")
def api_alumnos():
    """Retorna la tabla de promedios de alumnos."""
    asegurar_archivos_generados()
    df_prom = pd.read_csv(BASE_DIR / "promedios_alumnos.csv")
    return jsonify(df_prom.to_dict(orient="records"))


@app.route("/descargar/promedios_alumnos.csv")
def descargar_promedios():
    """Permite descargar el archivo generado de promedios de alumnos."""
    ruta = BASE_DIR / "promedios_alumnos.csv"
    if not ruta.exists():
        practica_pandas.main()
    return send_file(ruta, as_attachment=True, download_name="promedios_alumnos.csv")


@app.route("/api/regenerar", methods=["POST"])
def api_regenerar():
    """Endpoint para re-ejecutar en caliente el script de análisis."""
    try:
        practica_pandas.main()
        return jsonify({"status": "ok", "message": "Análisis y gráficos regenerados exitosamente."})
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500


if __name__ == "__main__":
    puerto = int(os.environ.get("PORT", 5000))
    print(f"\n==================================================================")
    print(f" [DASHBOARD CYBERPUNK ACTIVO] Servidor Flask corriendo")
    print(f" Acceda localmente en: http://127.0.0.1:{puerto}/")
    print(f"==================================================================\n")
    app.run(host="0.0.0.0", port=puerto, debug=False)
