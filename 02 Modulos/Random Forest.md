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

## B. Ruta E.030 (pendiente, Jean Piere)
Checklist de trazabilidad:
- [ ] Diccionario de variables (significado, unidades, origen, disponibilidad)
- [ ] Excluir IDs, familia y salidas que revelen la deriva
- [ ] Partición por familias; lista de IDs por conjunto
- [ ] Hiperparámetros, semillas, versiones
- [ ] Comparación con predictor sencillo (misma partición)
- [ ] Tabla de predicciones reservadas: ID, familia, deriva ref., predicción X/Y
- [ ] MAE, RMSE, R² por dirección; excedencias no detectadas (umbral 0.007)

Cuando estén, se agregan al informe (sección 3.2) y a la diapositiva 10 con el mismo formato de la tabla A.
