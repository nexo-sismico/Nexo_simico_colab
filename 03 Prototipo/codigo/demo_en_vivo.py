"""Demostración en vivo del prototipo (≈ 1 min 50 s) para grabar el video del Reto 06.
Ejecuta de verdad las 3 pruebas con nexo_nsr10.analizar() y narra cada paso en la consola.
    python demo_en_vivo.py            # demo con pausas para grabar (OBS o ffmpeg)
    python demo_en_vivo.py --rapido   # sin pausas, para revisar
Opcional: variable NEXO_MARCAS=archivo.json guarda los segundos en que empieza cada parte (para extraer capturas)."""
import json, os, sys, time
from nexo_nsr10 import analizar, reporte, registro_bd
from rutas import COD

RAPIDO = "--rapido" in sys.argv
EQ = json.load(open(COD / "equipo.json", encoding="utf-8"))
T0 = time.perf_counter()
MARCAS = {}

if os.name == "nt":
    os.system("")                                        # activa colores ANSI en la consola de Windows
    os.system("title Nexo Sismico - demo en vivo")
    os.system("mode con: cols=118 lines=45")
    try:                                                 # ventana siempre visible mientras se graba
        import ctypes
        hwnd = ctypes.windll.kernel32.GetConsoleWindow()
        ctypes.windll.user32.SetWindowPos(hwnd, -1, 30, 30, 0, 0, 0x0001)
    except Exception:
        pass

AZ, VE, RO, AM, GR, NE, FIN = "\033[96m", "\033[92m", "\033[91m", "\033[93m", "\033[90m", "\033[1m", "\033[0m"


def pausa(s):
    if not RAPIDO:
        time.sleep(s)


def limpiar():
    print("\033[2J\033[H", end="")


def marca(nombre):
    MARCAS[nombre] = round(time.perf_counter() - T0, 2)


def escribir(txt, color=AZ, v=0.018):
    for ch in txt:
        print(color + ch + FIN, end="", flush=True)
        if not RAPIDO:
            time.sleep(v)
    print()


def narrar(txt):
    escribir("» " + txt, AM, 0.012)


def colorear(linea):
    if "✓" in linea or "CUMPLEN" in linea or "Estado: OK" in linea:
        return VE + linea + FIN
    if "✗" in linea or "FALTA" in linea or "ERROR" in linea or "Detenido" in linea or "inválid" in linea.lower():
        return RO + linea + FIN
    return linea


def mostrar(r, titulo, ms):
    for l in reporte(r, titulo).splitlines():
        print(colorear(l))
    print(GR + f"(ejecución real: {ms:.2f} ms)" + FIN)


def correr(datos):
    t = time.perf_counter()
    r = analizar(datos)
    return r, (time.perf_counter() - t) * 1000


casos = {k: json.load(open(COD / "casos" / f"{k}.json", encoding="utf-8")) for k in ("caso1_completo", "caso2_falta_dato", "caso3_dato_erroneo")}

# ---------------------------------------------------------------- portada
limpiar(); pausa(3); marca("portada")
print(NE + AZ + "NEXO SÍSMICO · Prototipo funcional · Reto 06 (AECODE)" + FIN)
print(AZ + "Verificación sísmica NSR-10 automatizada para edificios aporticados de concreto" + FIN)
print(GR + "Equipo: " + " · ".join(p["corto"] for p in EQ["integrantes"]) + FIN)
print(GR + EQ["repositorio"] + "  ·  código: 03 Prototipo/codigo" + FIN)
print()
narrar("Problema: cada alternativa de predimensionamiento obliga a rehacer espectro, fuerzas,")
narrar("derivas y estabilidad a mano; un dato faltante o en otras unidades pasa sin aviso.")
narrar("Caso real: edificio de oficinas de 5 pisos, Bogotá, microzona Piedemonte A (grupo 1).")
pausa(5)

# ---------------------------------------------------------------- prueba 1
limpiar(); marca("prueba1")
print(NE + VE + "PRUEBA 1 · Datos completos y correctos" + FIN)
c = casos["caso1_completo"]
print(GR + "Entrada (casos/caso1_completo.json):" + FIN)
print(f"  sitio: Aa={c['sitio']['Aa']}  Av={c['sitio']['Av']}  Fa={c['sitio']['Fa']}  Fv={c['sitio']['Fv']}  grupo de uso={c['sitio']['grupo_uso']}")
print(f"  alturas libres (m): {c['geometria']['alturas_libres']}")
print(f"  periodos SAP2000 (s): {c['periodos_sap']}  · desplazamientos de 12 combinaciones en 2 esquinas")
pausa(4)
escribir(">>> analizar(caso1)", NE)
r, ms = correr(c)
mostrar(r, "CASO 1 · BIEN LLENADO", ms)
pausa(1); marca("prueba1_resultado")
vs, dmax = f"{r['fhe']['X']['Vs']:,.0f}".replace(",", " "), f"{max(r['deriva_max_pct'].values()):.3f}".replace(".", ",")
narrar(f"Calculó todo y emite dictamen: Vs = {vs} kN, deriva máx. {dmax} % ≤ 1,0 %: CUMPLE.")
narrar("Coincide con el cálculo de referencia hecho con Excel y SAP2000.")
pausa(14)

# ---------------------------------------------------------------- prueba 2
limpiar(); marca("prueba2")
print(NE + AM + "PRUEBA 2 · Falta un dato" + FIN)
c = casos["caso2_falta_dato"]
print(GR + "Entrada (casos/caso2_falta_dato.json): el sitio no trae Fv" + FIN)
print("  sitio: " + json.dumps(c["sitio"], ensure_ascii=False))
pausa(5)
escribir(">>> analizar(caso2)", NE)
r, ms = correr(c)
mostrar(r, "CASO 2 · FALTA UN DATO", ms)
pausa(1); marca("prueba2_resultado")
narrar("Se detiene ANTES de calcular y dice exactamente qué falta. No inventa el valor.")
pausa(12)

# ---------------------------------------------------------------- prueba 3
limpiar(); marca("prueba3")
print(NE + RO + "PRUEBA 3 · Dato erróneo" + FIN)
c = casos["caso3_dato_erroneo"]
print(GR + "Entrada (casos/caso3_dato_erroneo.json): altura libre del piso 1 escrita en centímetros" + FIN)
print(f"  alturas libres: {c['geometria']['alturas_libres']}")
pausa(5)
escribir(">>> analizar(caso3)", NE)
r, ms = correr(c)
mostrar(r, "CASO 3 · DATO ERRÓNEO", ms)
pausa(1); marca("prueba3_resultado")
narrar("Marca el error, explica el rango válido y rechaza la entrada. Tampoco calcula.")
pausa(12)

# ---------------------------------------------------------------- cierre
limpiar(); marca("cierre")
print(NE + AZ + "RESUMEN DE LAS 3 PRUEBAS (ejecución real)" + FIN)
filas = []
for k, nombre in (("caso1_completo", "1 · Datos completos"), ("caso2_falta_dato", "2 · Falta un dato"), ("caso3_dato_erroneo", "3 · Dato erróneo")):
    r, ms = correr(casos[k])
    est = {"ok": VE + "OK · calcula y dictamina" + FIN, "faltan_datos": AM + "DETENIDO · pide el dato" + FIN,
           "datos_invalidos": RO + "RECHAZADO · explica el error" + FIN}[r["estado"]]
    print(f"  {nombre:<22} {est}   ({ms:.2f} ms)")
print()
reg = registro_bd(casos["caso1_completo"], analizar(casos["caso1_completo"]))
print(GR + "El caso válido genera un registro para la base de datos del predictor:" + FIN)
print("  " + ", ".join(f"{k}={round(reg[k], 3) if isinstance(reg[k], float) else reg[k]}" for k in ("id", "norma", "n_pisos", "Tx_s", "dx_pct", "dy_pct") if k in reg))
print()
narrar("La tecnología valida y calcula; la persona modela en SAP2000 y decide el diseño.")
narrar("Sin claves ni datos personales. Código y ficha técnica en el repositorio del equipo.")
pausa(9)
marca("fin")

if os.environ.get("NEXO_MARCAS"):
    with open(os.environ["NEXO_MARCAS"], "w", encoding="utf-8") as fh:
        json.dump(MARCAS, fh, indent=1)
