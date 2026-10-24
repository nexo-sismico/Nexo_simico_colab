# Random Forest

## A. Ruta NSR-10 (hecho, Nicolás) — `03 Prototipo/codigo/experimento_ml.py`
- Datos: 18 edificios teóricos del profesor (9 plantas × 2 alturas). Ver [[Datos del profesor NSR-10]].
- 13 variables conocidas antes del análisis: altura, pisos, Lx, Ly, área, nº columnas, luz máx. y media, cargas D y L, I, esbeltez y peso estimado (área·pisos·D).
- RandomForestRegressor (scikit-learn 1.9.1): 500 árboles, hoja mínima 2, semilla 42.
- Validación: **dejando una planta completa fuera** (9 pliegues; las dos alturas de la planta salen juntas).
- Comparación con regresión lineal (altura, luz máx., peso estimado, esbeltez), fórmula Ta (periodo) y la media (referencia).

| Respuesta | Random Forest MAE · R² | Regresión lineal | Referencia |
|---|---|---|---|
| Periodo Tx (s) | 0.070 · 0.79 | 0.062 · 0.85 | Ta: 0.104 · 0.63 |
| Cortante Vx (kN) | 2601 · 0.65 | 2399 · 0.66 | Media: 4766 · −0.08 |
| Deriva máx. X (%) | **0.086 · 0.59** | 0.094 · 0.53 | Media: 0.142 · −0.13 |
| Deriva máx. Y (%) | **0.101 · 0.42** | 0.130 · 0.11 | Media: 0.166 · −0.15 |

- Deriva: −39 % de error frente a la referencia. Edificios con deriva ≥ 0.90 %: detecta **3 de 7**, 0 falsas alarmas (subestima los más cercanos al límite).
- Tiempos: entrenar ≈ 0.4 s; predecir ≈ 32 ms.
- Salidas: `07 Outputs/Prototipo NSR-10/resultados/` (métricas, predicciones, importancia) y `figuras/`.
- Lectura: sirve para **priorizar** alternativas, no para certificar.

## B. Ruta E.030 (✅ hecho, Jean Piere) — https://github.com/PieroVQ/ProyectoGH
Detalle y revisión: [[Ruta E030 - repositorio de Piero]].
- 1 500 estructuras / 1 500 familias; prueba con **300 familias nunca vistas**; selección solo por validación cruzada por familia.
- 7 configuraciones comparadas (Random Forest ×3, Extra Trees ×2, Gradient Boosting ×2) con variables físicas auxiliares (periodo aproximado por rigidez de piso y espectro E.030).

| Respuesta (prueba) | Mejor modelo · MAE · R² | Random Forest normalizado (CV) R² | Referencia (media) R² |
|---|---|---|---|
| Periodo Tx | Gradient Boosting · 0,0043 s · 0,999 | — | −0,005 |
| Deriva máx. X | Gradient Boosting · **0,026 %** · **0,995** | 0,989 | −0,004 |
| Deriva máx. Y | Gradient Boosting · **0,026 %** · **0,995** | 0,990 | −0,005 |

- Excedencias (deriva > 0,007, X o Y): **139 de 146 detectadas (95 %)**, 7 no detectadas, 2 falsas alarmas.
- Checklist de trazabilidad: ✅ diccionario de variables · ✅ sin IDs ni salidas como entradas · ✅ partición por familias (`division.csv`) · ✅ semillas y versiones · ✅ comparación con predictor sencillo · ✅ predicciones de prueba · ✅ MAE, RMSE, R² · ✅ excedencias (calculadas en la revisión).
- ⚠️ El mejor modelo es Gradient Boosting; la pregunta nombra Random Forest → reportar ambos (decisión del equipo, ver [[Decisiones]]).

## Lectura conjunta
Con 18 edificios (NSR-10) el Random Forest solo prioriza (R² 0,42–0,59); con 1 500 estructuras generadas y variables físicas, los modelos de árboles alcanzan R² 0,995 en familias nuevas. La diferencia la explican la cantidad de datos y las variables físicas, no el algoritmo.
