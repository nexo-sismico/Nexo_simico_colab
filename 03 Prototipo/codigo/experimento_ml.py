"""
Experimento de aprendizaje automático sobre la base NSR-10 (18 edificios teóricos del Prof. Rojas Vallejo).
Validación dejando una planta completa por fuera (las dos alturas de la planta nunca se reparten
entre entrenamiento y prueba). Se compara Random Forest con dos referencias:
  - Ta = 0.047·H^0.9 (NSR-10) para el periodo, y la media del entrenamiento para el resto
  - Regresión lineal sobre variables físicas
"""
import json, time, numpy as np, pandas as pd
from sklearn.ensemble import RandomForestRegressor
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score
from rutas import RES, SAL

d = pd.read_csv(SAL / "base_datos_NSR10.csv")
d = d[d["fuente"].str.contains("Rojas")].reset_index(drop=True)
d["planta"] = d["id"].str.split("-").str[0]
lx = d["luces_x_m"].apply(json.loads); ly = d["luces_y_m"].apply(json.loads)
X = pd.DataFrame({
    "H_m": d["hn_m"], "n_pisos": d["n_pisos"], "Lx_m": d["Lx_m"], "Ly_m": d["Ly_m"],
    "area_m2": d["area_m2"], "n_col": d["n_col"],
    "luz_max_m": [max(max(a), max(b)) for a, b in zip(lx, ly)],
    "luz_media_m": [np.mean(a + b) for a, b in zip(lx, ly)],
    "D_kNm2": d["D_entrepiso_kNm2"], "L_kNm2": d["L_entrepiso_kNm2"], "I": d["I"],
})
X["esbeltez"] = X["H_m"] / X[["Lx_m", "Ly_m"]].min(axis=1)
X["W_est_kN"] = X["area_m2"] * X["n_pisos"] * X["D_kNm2"]   # peso aproximado: entrada conocida de antemano
objetivos = {"Tx_s": "Periodo Tx (s)", "Vx_kN": "Cortante Vx (kN)", "dx_pct": "Deriva máx. X (%)", "dy_pct": "Deriva máx. Y (%)"}
grupos = d["planta"].values
filas, pred_tab = [], {"id": d["id"]}
tiempos = {}
for y_col, nombre in objetivos.items():
    y = d[y_col].values
    p_rf, p_lin, p_ref = np.zeros(len(y)), np.zeros(len(y)), np.zeros(len(y))
    t_fit = []
    for g in np.unique(grupos):
        tr, te = grupos != g, grupos == g
        rf = RandomForestRegressor(n_estimators=500, min_samples_leaf=2, random_state=42)
        t0 = time.perf_counter(); rf.fit(X[tr], y[tr]); t_fit.append(time.perf_counter() - t0)
        p_rf[te] = rf.predict(X[te])
        cols = ["H_m", "luz_max_m", "W_est_kN", "esbeltez"]
        p_lin[te] = LinearRegression().fit(X.loc[tr, cols], y[tr]).predict(X.loc[te, cols])
        p_ref[te] = (0.047 * X.loc[te, "H_m"] ** 0.9) if y_col == "Tx_s" else y[tr].mean()
    for met, p in (("Random Forest", p_rf), ("Regresión lineal", p_lin),
                   ("Ta NSR-10" if y_col == "Tx_s" else "Media (referencia)", p_ref)):
        filas.append({"Objetivo": nombre, "Modelo": met, "MAE": mean_absolute_error(y, p),
                      "RMSE": mean_squared_error(y, p) ** 0.5, "R2": r2_score(y, p),
                      "MAPE_%": float(np.mean(np.abs(p - y) / np.abs(y)) * 100)})
    pred_tab[f"{y_col}_real"] = y; pred_tab[f"{y_col}_RF"] = p_rf
    tiempos[y_col] = float(np.mean(t_fit))

# Detección de excedencias: con el umbral de diseño (1.0 %) ninguno excede; se evalúa el criterio
# práctico "cerca del límite" (deriva ≥ 0.90 %) que obliga a revisar la alternativa.
umbral = 0.90
real = np.maximum(d["dx_pct"], d["dy_pct"]) >= umbral
pred = np.maximum(pred_tab["dx_pct_RF"], pred_tab["dy_pct_RF"]) >= umbral
tp, fn, fp = int((real & pred).sum()), int((real & ~pred).sum()), int((~real & pred).sum())

# Tiempo de predicción de un edificio (modelo final entrenado con los 18)
rf_final = RandomForestRegressor(n_estimators=500, min_samples_leaf=2, random_state=42).fit(X, d["dx_pct"])
t0 = time.perf_counter()
for _ in range(100): rf_final.predict(X.iloc[[0]])
t_pred_ms = (time.perf_counter() - t0) / 100 * 1000
imp = pd.Series(rf_final.feature_importances_, index=X.columns).sort_values(ascending=False)

met = pd.DataFrame(filas)
met.round(4).to_csv(RES / "metricas_ml_NSR10.csv", index=False)
pd.DataFrame(pred_tab).round(4).to_csv(RES / "predicciones_ml_NSR10.csv", index=False)
imp.round(4).to_csv(RES / "importancia_variables_dx.csv", header=["importancia"])
json.dump({"n_registros": len(d), "n_plantas": int(len(np.unique(grupos))), "validacion": "dejando una planta fuera (9 pliegues)",
           "umbral_revision_pct": umbral, "cerca_limite_reales": int(real.sum()), "detectados": tp, "no_detectados": fn,
           "falsas_alarmas": fp, "t_entrenamiento_s": tiempos, "t_prediccion_ms": t_pred_ms},
          open(RES / "resumen_ml_NSR10.json", "w", encoding="utf-8"), indent=1)
print(met.round(3).to_string(index=False))
print(f"\nCerca del límite (≥{umbral}%): reales {int(real.sum())}, detectados {tp}, no detectados {fn}, falsas alarmas {fp}")
print(f"Predicción de un edificio: {t_pred_ms:.2f} ms")
print(imp.round(3).head(6).to_string())
