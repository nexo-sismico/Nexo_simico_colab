"""Resultados de la ruta E.030 (repositorio de Jean Piere) para el informe y la presentación.
Usa la misma base (1 500 estructuras), la misma partición por familias (1 200 desarrollo / 300 prueba) y la
configuración "RF_normalizado" de su repositorio. Entrena el Random Forest con las 1 200 de desarrollo y lo evalúa
una sola vez en las 300 familias reservadas; Gradient Boosting (modelo seleccionado por Piero) se toma de sus
predicciones de prueba guardadas. No carga ningún .joblib.
    python resumen_e030.py RUTA/A/ProyectoGH        (o variable de entorno E030_REPO)
Salidas: 07 Outputs/E030/ (resumen_E030.json, predicciones_prueba_RF_GB.csv, fig_e030_calculado_vs_predicho.png)"""
import json, os, sys, time
from pathlib import Path
import numpy as np, pandas as pd
import matplotlib
matplotlib.use("Agg"); import matplotlib.pyplot as plt
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score
from rutas import RAIZ

REPO = Path(sys.argv[1] if len(sys.argv) > 1 else os.environ.get("E030_REPO", RAIZ.parent / "ProyectoGH")).resolve()
OUT = RAIZ / "07 Outputs" / "E030"; OUT.mkdir(parents=True, exist_ok=True)
sys.path.insert(0, str(REPO / "ml_porticos"))
from modelos_mejorados import RespuestaRegressor   # clases del repositorio de Piero

LIM = 0.007
base = pd.read_excel(REPO / "base_ml_ampliada" / "estructuras.xlsx")
div = pd.read_csv(REPO / "resultados_ml_optimizado" / "division.csv")
var = json.load(open(REPO / "resultados_ml_optimizado" / "variables_utilizadas.json", encoding="utf-8"))["entradas"]
gb = pd.read_csv(REPO / "resultados_ml_optimizado" / "predicciones_prueba.csv")
met_repo = pd.read_csv(REPO / "resultados_ml_optimizado" / "metricas.csv")
ids_prueba = set(div.loc[div.conjunto == "prueba", "ID_estructura"])
des = base[~base.ID_estructura.isin(ids_prueba)].reset_index(drop=True)
pru = base[base.ID_estructura.isin(ids_prueba)].set_index("ID_estructura").loc[gb.ID_estructura].reset_index()


def metricas(y, p):
    return {"MAE": float(mean_absolute_error(y, p)), "RMSE": float(np.sqrt(mean_squared_error(y, p))), "R2": float(r2_score(y, p)),
            "err_rel_mediano_pct": float(np.median(np.abs(p - y) / y) * 100)}


def excedencias(y, p):
    r, q = y > LIM, p > LIM
    return {"reales": int(r.sum()), "detectadas": int((r & q).sum()), "no_detectadas": int((r & ~q).sum()), "falsas_alarmas": int((~r & q).sum())}


res = {"fuente": "https://github.com/PieroVQ/ProyectoGH", "n_desarrollo": len(des), "n_prueba": len(pru), "limite_deriva": LIM,
       "base_estructuras": len(base), "base_exceden": int(((base.deriva_max_X > LIM) | (base.deriva_max_Y > LIM)).sum()), "objetivos": {}}
tabla = {"ID_estructura": gb.ID_estructura}
for obj in ["Tx_s", "deriva_max_X", "deriva_max_Y"]:
    t0 = time.perf_counter()
    rf = RespuestaRegressor(obj, "RF_normalizado", semilla=48371).fit(des[var], des[obj])
    t_ent = time.perf_counter() - t0
    y = pru[obj].to_numpy(); p_rf = rf.predict(pru[var]); p_gb = gb[f"{obj}_predicho"].to_numpy()
    assert np.allclose(y, gb[f"{obj}_real"]), "la base no coincide con las predicciones guardadas"
    t0 = time.perf_counter(); [rf.predict(pru[var].iloc[[0]]) for _ in range(20)]; t_pred = (time.perf_counter() - t0) / 20 * 1000
    media = met_repo[(met_repo.objetivo == obj) & (met_repo.conjunto == "baseline_media_entrenamiento")].iloc[0]
    res["objetivos"][obj] = {"RF": metricas(y, p_rf), "GB": metricas(y, p_gb), "media_R2": float(media.R2), "media_MAE": float(media.MAE),
                             "t_entrenamiento_RF_s": t_ent, "t_prediccion_RF_ms": t_pred}
    if obj.startswith("deriva"):
        res["objetivos"][obj]["exced_RF"] = excedencias(y, p_rf); res["objetivos"][obj]["exced_GB"] = excedencias(y, p_gb)
    tabla[f"{obj}_real"] = y; tabla[f"{obj}_RF"] = p_rf; tabla[f"{obj}_GB"] = p_gb
    print(obj, "RF R2 =", round(res["objetivos"][obj]["RF"]["R2"], 4), "· GB R2 =", round(res["objetivos"][obj]["GB"]["R2"], 4))

t = pd.DataFrame(tabla)
for k in ("RF", "GB"):
    y = (t.deriva_max_X_real > LIM) | (t.deriva_max_Y_real > LIM); q = (t[f"deriva_max_X_{k}"] > LIM) | (t[f"deriva_max_Y_{k}"] > LIM)
    res[f"exced_XoY_{k}"] = {"reales": int(y.sum()), "detectadas": int((y & q).sum()), "no_detectadas": int((y & ~q).sum()), "falsas_alarmas": int((~y & q).sum())}
t.to_csv(OUT / "predicciones_prueba_RF_GB.csv", index=False)
with open(OUT / "resumen_E030.json", "w", encoding="utf-8") as fh:
    json.dump(res, fh, ensure_ascii=False, indent=1)

# Figura: calculado (OpenSees) vs predicho (Random Forest) en las 300 familias reservadas
plt.rcParams.update({"font.family": "DejaVu Sans", "font.size": 10})
fig, axs = plt.subplots(1, 2, figsize=(9, 4))
for ax, e in zip(axs, "XY"):
    o = res["objetivos"][f"deriva_max_{e}"]; y = t[f"deriva_max_{e}_real"] * 100; p = t[f"deriva_max_{e}_RF"] * 100
    ax.scatter(y, p, s=12, color="#1F3864", alpha=.7, zorder=3)
    m = max(y.max(), p.max()) * 1.05
    ax.plot([0, m], [0, m], color="#8C8C8C", ls="--", lw=1, label="predicción perfecta")
    ax.axvline(LIM * 100, color="#E07B39", lw=1, ls=":"); ax.axhline(LIM * 100, color="#E07B39", lw=1, ls=":", label="límite E.030 (0,7 %)")
    ax.set_title(f"Deriva máx. {e} · Random Forest\nMAE = {o['RF']['MAE'] * 100:.3f} % · R² = {o['RF']['R2']:.3f}", fontsize=10)
    ax.set_xlabel("Calculado (OpenSees, %)"); ax.set_ylabel("Predicho (300 familias reservadas, %)")
    ax.set_xlim(0, m); ax.set_ylim(0, m); ax.grid(alpha=.3); ax.legend(fontsize=8, loc="upper left")
plt.tight_layout(); plt.savefig(OUT / "fig_e030_calculado_vs_predicho.png", dpi=200); plt.close()
print("→", OUT)
