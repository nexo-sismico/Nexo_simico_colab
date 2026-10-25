"""Arma la carpeta que se publica en internet (Netlify u otro hosting estático) con SOLO lo que la app necesita:
la interfaz, el motor nexo_nsr10.py, el caso de ejemplo y los nombres del equipo. El resto del vault no se publica.
    python "03 Prototipo/app/construir_sitio.py"      → 03 Prototipo/app/dist/
Netlify lo ejecuta solo (ver netlify.toml en la raíz del repositorio)."""
import shutil
from pathlib import Path

APP = Path(__file__).resolve().parent
COD = APP.parent / "codigo"
DIST = APP / "dist"

ARCHIVOS = {                                   # destino en el sitio: origen en el repositorio
    "index.html": APP / "index.html",
    "app.js": APP / "app.js",
    "estilos.css": APP / "estilos.css",
    "nexo_nsr10.py": COD / "nexo_nsr10.py",
    "casos/caso1_completo.json": COD / "casos" / "caso1_completo.json",
    "equipo.json": COD / "equipo.json",
}

shutil.rmtree(DIST, ignore_errors=True)
for destino, origen in ARCHIVOS.items():
    p = DIST / destino
    p.parent.mkdir(parents=True, exist_ok=True)
    shutil.copy2(origen, p)

# En el sitio los datos están junto a index.html (en el repositorio están en ../codigo)
html = (DIST / "index.html").read_text(encoding="utf-8")
html = html.replace('<meta name="nexo-datos" content="../codigo/">', '<meta name="nexo-datos" content="./">')
(DIST / "index.html").write_text(html, encoding="utf-8")
(DIST / "_headers").write_text("/*\n  X-Content-Type-Options: nosniff\n  Referrer-Policy: strict-origin-when-cross-origin\n/nexo_nsr10.py\n  Content-Type: text/plain; charset=utf-8\n", encoding="utf-8")
print(f"Sitio listo en {DIST} ({len(ARCHIVOS)} archivos)")
