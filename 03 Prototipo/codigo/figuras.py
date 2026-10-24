import json, pandas as pd, numpy as np, matplotlib
matplotlib.use("Agg"); import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch
from rutas import RES, FIG
plt.rcParams.update({"font.family": "DejaVu Sans", "font.size": 10})
NAVY, ORANGE, GREY, GREEN = "#1F3864", "#E07B39", "#8C8C8C", "#3A7D44"
pr = pd.read_csv(RES / "predicciones_ml_NSR10.csv"); met = pd.read_csv(RES / "metricas_ml_NSR10.csv")
# 1) calculado vs predicho
fig, axs = plt.subplots(1, 2, figsize=(9, 4))
for ax, c, t in zip(axs, ["dx_pct", "dy_pct"], ["Deriva máx. X (%)", "Deriva máx. Y (%)"]):
    ax.scatter(pr[f"{c}_real"], pr[f"{c}_RF"], color=NAVY, s=40, zorder=3)
    ax.plot([0.4, 1.05], [0.4, 1.05], color=GREY, ls="--", lw=1, label="predicción perfecta")
    ax.axvline(0.9, color=ORANGE, lw=1, ls=":"); ax.axhline(0.9, color=ORANGE, lw=1, ls=":", label="revisión 0.90 %")
    m = met[(met["Objetivo"] == t) & (met["Modelo"] == "Random Forest")].iloc[0]
    ax.set_title(f"{t}\nRandom Forest · MAE = {m.MAE:.3f} % · R² = {m.R2:.2f}", fontsize=10)
    ax.set_xlabel("Calculado (OpenSees, profesor)"); ax.set_ylabel("Predicho (validación por planta)")
    ax.set_xlim(0.4, 1.05); ax.set_ylim(0.4, 1.05); ax.grid(alpha=.3); ax.legend(fontsize=8, loc="upper left")
plt.tight_layout(); plt.savefig(FIG / "fig_calculado_vs_predicho.png", dpi=200); plt.close()
# 2) MAPE por modelo
fig, ax = plt.subplots(figsize=(9, 3.6))
objs = met["Objetivo"].unique(); w = 0.26
mods = ["Random Forest", "Regresión lineal", "Referencia"]
cols = [NAVY, "#5B8BD0", GREY]
for k, mo in enumerate(mods):
    vals = [met[(met["Objetivo"] == o) & ((met["Modelo"] == mo) | ((mo == "Referencia") & met["Modelo"].isin(["Ta NSR-10", "Media (referencia)"])))]["MAPE_%"].iloc[0] for o in objs]
    b = ax.bar(np.arange(len(objs)) + (k - 1) * w, vals, w, color=cols[k], label=mo if mo != "Referencia" else "Referencia (Ta NSR-10 / media)")
    ax.bar_label(b, fmt="%.0f", fontsize=8)
ax.set_xticks(np.arange(len(objs))); ax.set_xticklabels(objs); ax.set_ylabel("Error porcentual medio (%)")
ax.set_title("Error en edificios no vistos (18 edificios NSR-10, validación dejando una planta fuera)", fontsize=10)
ax.legend(fontsize=8); ax.grid(axis="y", alpha=.3); plt.tight_layout(); plt.savefig(FIG / "fig_errores_modelos.png", dpi=200); plt.close()
# 3) flujo integrado
fig, ax = plt.subplots(figsize=(11, 4.2)); ax.axis("off"); ax.set_xlim(0, 11); ax.set_ylim(0, 4.2)
def box(x, y, w, h, t, c=NAVY, fill="white"):
    ax.add_patch(FancyBboxPatch((x, y), w, h, boxstyle="round,pad=0.04,rounding_size=0.12", fc=fill, ec=c, lw=1.6))
    ax.text(x + w / 2, y + h / 2, t, ha="center", va="center", fontsize=8.6, color="#111")
def arr(x1, y1, x2, y2, ls="-"):
    ax.annotate("", (x2, y2), (x1, y1), arrowprops=dict(arrowstyle="->", color=GREY, lw=1.3, ls=ls))
ax.text(0.1, 3.95, "Ruta Perú · E.030", color=NAVY, fontsize=9, weight="bold")
box(0.1, 2.9, 1.8, 0.8, "Generador\nparamétrico"); box(2.2, 2.9, 1.8, 0.8, "OpenSees\nmodal espectral"); box(4.3, 2.9, 1.8, 0.8, "Base E.030\n1 500 estructuras")
ax.text(0.1, 1.85, "Ruta Colombia · NSR-10", color=GREEN, fontsize=9, weight="bold")
box(0.1, 0.8, 1.8, 0.8, "SAP2000 +\nMódulo NSR-10", GREEN, "#EEF6EF"); box(2.2, 0.8, 1.8, 0.8, "Edificios teóricos\ndel profesor (OpenSees)", GREEN); box(4.3, 0.8, 1.8, 0.8, "Base NSR-10\n18 + casos", GREEN)
box(6.6, 1.85, 1.8, 0.9, "Random Forest\nvalidación por\nfamilia / planta", ORANGE, "#FDF0E7"); box(8.9, 2.9, 1.9, 0.8, "Métricas · MAE, R²\nexcedencias · tiempos")
box(8.9, 0.8, 1.9, 0.8, "Servicio Python +\nBot Telegram (n8n)\n[interfaz propuesta]", GREY)
arr(1.9, 3.3, 2.2, 3.3); arr(4.0, 3.3, 4.3, 3.3); arr(6.1, 3.3, 6.6, 2.5); ax.plot([1.0, 1.0, 5.2], [0.8, 0.62, 0.62], color=GREY, lw=1.3); arr(5.2, 0.62, 5.2, 0.8); arr(4.0, 1.2, 4.3, 1.2); arr(6.1, 1.2, 6.6, 2.1)
arr(8.4, 2.5, 8.9, 3.2); arr(8.4, 2.1, 8.9, 1.3)
ax.text(5.5, 0.18, "El módulo NSR-10 valida entradas y produce respuestas de referencia; cada caso válido se suma a la base NSR-10.", ha="center", fontsize=8, color=GREY)
plt.savefig(FIG / "fig_flujo_integrado.png", dpi=200, bbox_inches="tight"); plt.close()
# 4) importancia
imp = pd.read_csv(RES / "importancia_variables_dx.csv", index_col=0)["importancia"].head(7)[::-1]
fig, ax = plt.subplots(figsize=(5.5, 3.2)); ax.barh(imp.index, imp.values, color=NAVY)
ax.set_title("Importancia de variables · deriva X (Random Forest)", fontsize=10); ax.grid(axis="x", alpha=.3)
plt.tight_layout(); plt.savefig(FIG / "fig_importancia.png", dpi=200); plt.close()
# 5) derivas del caso del curso
r = json.load(open(RES / "caso1_completo.json", encoding="utf-8"))
fig, ax = plt.subplots(figsize=(5.5, 3.4))
for dd, c in (("X", NAVY), ("Y", ORANGE)):
    v = [x["deriva_pct"] for x in r["derivas"] if x["dir"] == dd]
    ax.plot(v, range(1, len(v) + 1), marker="o", color=c, label=f"Dirección {dd}")
ax.axvline(1.0, color="#C00000", ls="--", lw=1, label="Límite NSR-10 (1.0 %)")
ax.set_xlabel("Deriva de piso (% hpi) · envolvente de 12 combinaciones"); ax.set_ylabel("Nivel"); ax.set_yticks(range(1, 6))
ax.set_title("Edificio del curso (grupo 1, Piedemonte A)", fontsize=10); ax.grid(alpha=.3); ax.legend(fontsize=8)
plt.tight_layout(); plt.savefig(FIG / "fig_derivas_caso_curso.png", dpi=200); plt.close()
print("ok")
