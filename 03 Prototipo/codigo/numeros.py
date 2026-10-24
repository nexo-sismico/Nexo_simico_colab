"""Reúne en numeros.json las cifras que usan el informe (informe.js) y la presentación (deck.js).
Orden: correr_pruebas.py → base_datos_nsr10.py → experimento_ml.py → numeros.py → figuras.py → informe.js / deck.js."""
import json
import pandas as pd

r = json.load(open("resultados/caso1_completo.json", encoding="utf-8"))
pr = json.load(open("resultados/resumen_pruebas.json", encoding="utf-8"))
ml = json.load(open("resultados/resumen_ml_NSR10.json", encoding="utf-8"))
met = pd.read_csv("resultados/metricas_ml_NSR10.csv")
fx = r["fhe"]["X"]
numeros = {
    "vs": fx["Vs"], "dxmax": r["deriva_max_pct"]["X"], "dymax": r["deriva_max_pct"]["Y"],
    "Q": r["Q_max"], "tor": r["torsion_ratio"], "R": r["R"], "Sa": fx["Sa"],
    "Ta": r["parametros"]["Ta"], "CuTa": r["parametros"]["CuTa"], "Wt": r["parametros"]["Wt"],
    "ms": [c["ms"] for c in pr],
    "met": met.to_dict(orient="records"),
    "ml": ml,
}
json.dump(numeros, open("numeros.json", "w", encoding="utf-8"), ensure_ascii=False, indent=1)
print("numeros.json actualizado")
