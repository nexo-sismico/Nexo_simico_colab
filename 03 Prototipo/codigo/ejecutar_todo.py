"""Corre toda la cadena del módulo NSR-10 en orden, desde cualquier carpeta:
    python "03 Prototipo/codigo/ejecutar_todo.py"            # pruebas → base → ML → cifras → figuras → ficha
    python "03 Prototipo/codigo/ejecutar_todo.py" --informe  # además informe (DOCX) y presentación (PPTX) con Node
    python "03 Prototipo/codigo/ejecutar_todo.py" --videos   # además los dos videos (requiere ffmpeg)
Requisitos: pip install -r requirements.txt  ·  para --informe: npm install (en esta carpeta)."""
import os, subprocess, sys, time
from pathlib import Path

COD = Path(__file__).resolve().parent
PASOS = ["correr_pruebas.py", "base_datos_nsr10.py", "experimento_ml.py", "numeros.py", "figuras.py", "ficha.py"]
env = dict(os.environ, PYTHONUTF8="1", PYTHONIOENCODING="utf-8")   # Windows: tildes y símbolos sin errores
sys.stdout.reconfigure(encoding="utf-8", errors="replace")


def correr(cmd):
    t0 = time.perf_counter()
    print(f"\n▶ {' '.join(map(str, cmd))}")
    r = subprocess.run(cmd, cwd=COD, env=env)
    if r.returncode:
        sys.exit(f"✗ Falló: {cmd[-1]} (código {r.returncode})")
    print(f"✓ {Path(str(cmd[-1])).name} ({time.perf_counter() - t0:.1f} s)")


for p in PASOS:
    correr([sys.executable, p])
if "--informe" in sys.argv:
    correr(["node", "informe.js"])
    correr(["node", "deck.js"])
if "--videos" in sys.argv:
    correr([sys.executable, "videos.py"])
print("\nListo. Salidas en 07 Outputs/Prototipo NSR-10 y 04 Entregables.")
