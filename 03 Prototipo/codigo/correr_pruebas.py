"""Ejecuta las 3 pruebas del prototipo y guarda reportes en 07 Outputs/Prototipo NSR-10/resultados/"""
import json, os, time
from nexo_nsr10 import analizar, reporte
from rutas import COD, RES

PRUEBAS = [(COD / "casos/caso1_completo.json", "CASO 1 · BIEN LLENADO"),
           (COD / "casos/caso2_falta_dato.json", "CASO 2 · FALTA UN DATO (Fv)"),
           (COD / "casos/caso3_dato_erroneo.json", "CASO 3 · DATO EQUIVOCADO (altura libre 350)")]
resumen = []
for ruta, titulo in PRUEBAS:
    t0 = time.perf_counter()
    r = analizar(json.load(open(ruta, encoding="utf-8")))
    ms = (time.perf_counter() - t0) * 1000
    txt = reporte(r, titulo) + f"\n(tiempo de ejecución: {ms:.1f} ms)"
    print(txt, "\n")
    base = os.path.splitext(os.path.basename(ruta))[0]
    open(RES / f"{base}.txt", "w", encoding="utf-8").write(txt)
    json.dump(r, open(RES / f"{base}.json", "w", encoding="utf-8"), ensure_ascii=False, indent=1, default=float)
    resumen.append({"caso": titulo, "estado": r["estado"], "ms": round(ms, 1),
                    "detalle": (r["faltan"] or r["errores"] or [f"Vs = {r['fhe']['X']['Vs']:,.0f} kN; deriva máx {max(r['deriva_max_pct'].values()):.3f} %"])})
json.dump(resumen, open(RES / "resumen_pruebas.json", "w", encoding="utf-8"), ensure_ascii=False, indent=1)
