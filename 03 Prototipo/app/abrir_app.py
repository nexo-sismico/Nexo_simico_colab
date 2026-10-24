"""Abre la app Nexo Sísmico NSR-10 en el navegador.
    python "03 Prototipo/app/abrir_app.py"                 # sirve el repositorio en http://127.0.0.1:8765 y abre la app
    python "03 Prototipo/app/abrir_app.py" --puerto 9000 --sin-navegador
Solo usa la biblioteca estándar. La primera vez necesita internet (descarga Pyodide y Chart.js desde la CDN);
los datos del edificio no salen del computador: el cálculo corre en el navegador."""
import argparse, functools, http.server, socket, sys, threading, webbrowser
from pathlib import Path
from urllib.parse import quote

APP = Path(__file__).resolve().parent
RAIZ = APP.parents[1]                       # raíz del repositorio: la app lee ../codigo/nexo_nsr10.py


def puerto_libre(p):
    for q in range(p, p + 30):
        with socket.socket() as s:
            if s.connect_ex(("127.0.0.1", q)):
                return q
    raise SystemExit("No hay puertos libres entre %d y %d" % (p, p + 29))


def main():
    for s in (sys.stdout, sys.stderr):        # consolas de Windows en cp1252
        try:
            s.reconfigure(encoding="utf-8", errors="replace")
        except (AttributeError, ValueError):
            pass
    ap = argparse.ArgumentParser()
    ap.add_argument("--puerto", type=int, default=8765)
    ap.add_argument("--sin-navegador", action="store_true")
    a = ap.parse_args()
    puerto = puerto_libre(a.puerto)
    Manejador = functools.partial(http.server.SimpleHTTPRequestHandler, directory=str(RAIZ))
    Manejador.log_message = lambda *args: None
    srv = http.server.ThreadingHTTPServer(("127.0.0.1", puerto), Manejador)
    url = f"http://127.0.0.1:{puerto}/{quote(APP.relative_to(RAIZ).as_posix())}/index.html"
    print(f"Nexo Sísmico NSR-10 → {url}\nCtrl+C para cerrar.", flush=True)
    if not a.sin_navegador:
        threading.Timer(0.6, webbrowser.open, [url]).start()
    try:
        srv.serve_forever()
    except KeyboardInterrupt:
        print("Servidor cerrado.")
        sys.exit(0)


if __name__ == "__main__":
    main()
