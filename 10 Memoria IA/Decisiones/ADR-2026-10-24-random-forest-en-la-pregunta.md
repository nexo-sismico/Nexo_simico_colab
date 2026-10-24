---
tipo: decision
proyecto: AECODE Nexo Sismico
fecha: 2026-10-24
estado: aceptada
reemplaza:
tags: [decision, ml, informe]
---
# La pregunta mantiene Random Forest; Gradient Boosting como comparación

## Contexto
En el repo E.030 de Piero el modelo seleccionado es Gradient Boosting; la pregunta de investigación nombra Random Forest y no había métricas de RF en la prueba.

## Decisión
Nicolás eligió mantener "Random Forest". Se entrenó `RF_normalizado` (su código, sin cargar .joblib) con la misma partición 1 200/300 por familia: deriva R² 0,990, MAE 0,040 %, 137/146 excedencias, 2 falsas alarmas. GB (R² 0,995, 139/146) se reporta como comparación. Script: `03 Prototipo/codigo/resumen_e030.py` → `07 Outputs/E030/`.

## Alternativas descartadas
- **"Modelos de ensamble de árboles"** en la pregunta — el usuario prefirió no cambiar la pregunta.
- **Usar métricas de CV del RF** — la prueba única en familias reservadas es más fuerte.

## Consecuencias
- Informe v2 (5 págs., límite 5) y PPT v2 (15 diap.) actualizados y exportados con Word/PowerPoint.
- Video ejecutivo quedó en v1 (sin diapositiva E.030; falta ffmpeg).
- Cita [2] usa E.030 RM 183-2026-VIVIENDA (tomada del repo de Piero): pedir confirmación.

## Relacionado
[[Contexto]] · [[_Indice]] · [[ADR-2026-10-24-integrar-ruta-e030-de-piero]]
