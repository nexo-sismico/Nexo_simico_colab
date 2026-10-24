"""Rutas y fuentes comunes para que los scripts corran igual en Windows, macOS, Linux o Colab.
Entradas (casos, Excel del profesor): esta carpeta. Salidas: 07 Outputs/Prototipo NSR-10. Entregables: 04 Entregables."""
import glob, os, sys
from pathlib import Path

for _s in (sys.stdout, sys.stderr):   # Windows: imprimir ✓ → á sin UnicodeEncodeError
    try:
        _s.reconfigure(encoding="utf-8", errors="replace")
    except (AttributeError, ValueError):
        pass

COD = Path(__file__).resolve().parent                 # 03 Prototipo/codigo
RAIZ = COD.parents[1]                                 # raíz del vault / repositorio
SAL = RAIZ / "07 Outputs" / "Prototipo NSR-10"        # base de datos, numeros.json, ficha
RES = SAL / "resultados"
FIG = SAL / "figuras"
ENT = RAIZ / "04 Entregables"
for d in (RES, FIG):
    d.mkdir(parents=True, exist_ok=True)

_DIRS = ["/usr/share/fonts", "/usr/local/share/fonts", "/Library/Fonts", "/System/Library/Fonts",
         os.path.expanduser("~/Library/Fonts"), os.path.expanduser("~/.fonts"),
         os.path.join(os.environ.get("WINDIR", r"C:\Windows"), "Fonts"),
         os.path.join(os.environ.get("LOCALAPPDATA", ""), "Microsoft", "Windows", "Fonts")]
try:  # matplotlib siempre trae DejaVu: respaldo garantizado
    import matplotlib
    _DIRS.append(os.path.join(os.path.dirname(matplotlib.__file__), "mpl-data", "fonts", "ttf"))
except ImportError:
    pass


def fuente(*nombres):
    """Primera fuente .ttf encontrada entre los nombres dados (en orden de preferencia)."""
    for n in nombres:
        for d in _DIRS:
            if d and os.path.isdir(d):
                hit = glob.glob(os.path.join(d, "**", n), recursive=True)
                if hit:
                    return hit[0]
    raise FileNotFoundError(f"No se encontró ninguna de las fuentes {nombres}; instala matplotlib (trae DejaVu).")


# Liberation Sans y Arial tienen las mismas métricas: el PDF queda igual en Linux y en Windows.
SANS = lambda: fuente("LiberationSans-Regular.ttf", "arial.ttf", "Arial.ttf", "DejaVuSans.ttf")
SANS_B = lambda: fuente("LiberationSans-Bold.ttf", "arialbd.ttf", "Arial Bold.ttf", "DejaVuSans-Bold.ttf")
MONO = lambda: fuente("DejaVuSansMono.ttf")
MONO_B = lambda: fuente("DejaVuSansMono-Bold.ttf")
