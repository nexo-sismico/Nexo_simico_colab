---
tags: [modulo, e030, ml, revision]
actualizado: 2026-10-24
fuente: https://github.com/PieroVQ/ProyectoGH (commit 07fd4b2)
---
# Ruta E.030 — repositorio de Jean Piere (revisión)

Repositorio: **https://github.com/PieroVQ/ProyectoGH** · revisado el 2026-10-24 sobre el commit `07fd4b2` ("Prediccion modelo").
Es la pieza que en el vault figuraba como **pendiente**: generador paramétrico + OpenSees (E.030, Perú) + modelos de aprendizaje con familias reservadas. Ya está hecha y es la evidencia principal para la pregunta de investigación.

## Qué contiene
| Carpeta | Qué hace |
|---|---|
| `porticos_rc/` | Generador de pórticos de concreto (2–5 pisos, 2–5 vanos, luces 3–6 m, f'c 210/280 kgf/cm²), predimensionamiento (E.060), cargas (E.020), análisis modal espectral E.030 en OpenSeesPy, visualización 3D (Plotly) y pruebas |
| `ml_porticos/` | Creación de la base, optimización y comparación de 7 configuraciones (Random Forest, Extra Trees, Gradient Boosting), predicción e informes HTML |
| `base_ml_ampliada/` | **1 500 estructuras de 1 500 familias** (una alternativa por familia), 107 entradas, diccionario de variables |
| `resultados_ml_optimizado/` | Modelos (`modelo_evaluacion.joblib`, `modelo_final.joblib`), métricas, predicciones de prueba, división, importancias |

Metodología completa: `porticos_rc/METODOLOGIA.md` del repositorio (secciones brutas, diafragma rígido, CQC 5 %, SRSS 100/30, excentricidad ±5 %, deriva normativa = elástica × 0,75·R con R = 8, límite 0,007, sin P-Delta).

## Resultados (prueba con 300 familias nunca vistas)
Partición: 1 200 estructuras de desarrollo / 300 de prueba, **por familia**. Selección del modelo solo con validación cruzada (3 pliegues por familia); la prueba se usó una sola vez.

| Respuesta | Modelo elegido | MAE | R² | Error relativo mediano | Referencia (media) R² |
|---|---|---|---|---|---|
| Periodo Tx (s) | Gradient Boosting | 0,0043 s | 0,999 | 0,5 % | −0,005 |
| Cortante modal ajustado X (kgf) | Gradient Boosting | 223 kgf | 0,9998 | 0,04 % | −0,002 |
| Desplazamiento de techo X (cm) | Gradient Boosting | 0,117 cm | 0,999 | 1,2 % | −0,007 |
| **Deriva máx. X** | Gradient Boosting | **0,00026** (0,026 %) | **0,995** | 2,6 % | −0,004 |
| **Deriva máx. Y** | Gradient Boosting | **0,00026** (0,026 %) | **0,995** | 2,5 % | −0,005 |

**Detección de excedencias (deriva > 0,007)** — calculada en esta revisión a partir de `predicciones_prueba.csv`:

| Dirección | Exceden de verdad | Detectadas | No detectadas | Falsas alarmas |
|---|---|---|---|---|
| X | 140 | 134 | 6 | 3 |
| Y | 136 | 132 | 4 | 3 |
| Cualquiera (X o Y) | 146 | **139 (95 %)** | **7** | 2 |

Comparación de configuraciones en validación cruzada (deriva X, R²): RF original 0,889 · RF con variables físicas 0,976 · **RF normalizado 0,989** · Extra Trees 0,990 · **Gradient Boosting 0,994**. La referencia "RF directo, misma base" de `metricas.csv` (sin variables físicas) da R² = 0,921.
Tiempos registrados en el repositorio: generar y analizar las 1 500 estructuras (2 368 intentos) ≈ 250 s en total (≈ 0,17 s por estructura aceptada; el resumen no indica cuántos procesos en paralelo); optimización completa ≈ 317 s.

## Hallazgos de la revisión
| # | Hallazgo | Impacto | Qué se hizo / propuesta |
|---|---|---|---|
| 1 | El modelo seleccionado es **Gradient Boosting**, no Random Forest. La pregunta de investigación nombra a Random Forest. | Coherencia del informe | ✅ Decidido: la pregunta mantiene Random Forest. Se entrenó `RF_normalizado` con su misma partición (`resumen_e030.py`): deriva R² 0,990, MAE 0,040 %, 137 de 146 excedencias en prueba. Gradient Boosting se reporta como comparación. |
| 2 | La clave del desempeño son las **variables físicas auxiliares** (periodo aproximado por rigidez de piso, espectro E.030) y predecir el cociente respecto a esa estimación. | Aporte metodológico fuerte | Destacarlo en el informe: el ML corrige una estimación física, no adivina desde cero. |
| 3 | El vault decía "130 configuraciones, 49 familias" | Cifras desactualizadas | Actualizado a 1 500 estructuras / 1 500 familias en todas las notas. |
| 4 | Unidades kgf-cm y deriva adimensional (0,007) frente a kN-m y % en NSR-10 (límite 1,0 %) | Riesgo de mezclar | Se mantiene la regla: **no se mezclan** las bases; se comparan solo como dos líneas de evidencia. |
| 5 | Rangos distintos: E.030 2–5 pisos; profesor NSR-10 4–10 pisos | Dominio | Cada modelo solo se usa dentro de su dominio (el predictor E.030 rechaza entradas fuera de rango). |
| 6 | Norma citada: E.030 RM 183-2026-VIVIENDA | Trazabilidad | Confirmar con Jean Piere que es la versión vigente usada en el curso. |
| 7 | El repositorio no reporta excedencias no detectadas (lo pide la rúbrica/objetivos) | Métrica faltante | Calculada aquí (tabla de arriba); sugerir agregarla a `informe.html`. |
| 8 | README con ruta fija `D:\AECODE\ProyectoGH` y Python 3.12 exacto | Menor | Sugerencia: indicar "la carpeta donde clonaste el repositorio". |
| 9 | El bot n8n necesita un backend que hoy no existe | Prototipo A | `modelo_final.joblib` + `modelos_mejorados.py` son exactamente lo que ese backend debe cargar (`POST /consultas`). |

Verificación hecha: las **11 pruebas unitarias de `ml_porticos` pasan** (Python 3.13, scikit-learn 1.9.1, numpy 2.5.4, pandas 3.1.0 — mismas versiones de sus modelos). No se ejecutaron las pruebas de `porticos_rc` (requieren OpenSeesPy) ni se volvió a cargar el `.joblib`.

## Cómo encaja con lo nuestro
- **R1 de la pregunta de investigación (precisión en familias nuevas) queda respondida con E.030**: Random Forest, deriva con R² 0,990 y 137 de 146 excedencias detectadas (Gradient Boosting, como comparación: R² 0,995 y 139 de 146).
- La ruta NSR-10 (18 edificios del profesor) sigue siendo la **validación en Colombia** con pocos datos (R² 0,59 / 0,42): muestra que con 18 edificios el RF solo sirve para priorizar; con 1 500 generados, la precisión es alta. Ese contraste es un resultado en sí mismo: **la cantidad y trazabilidad de los datos manda**.
- Ahorro de tiempo (R4): el generador automatiza la modelación (≈ 0,17 s por estructura aceptada); la predicción NSR-10 medida es ≈ 32 ms por edificio. Falta cronometrar la predicción E.030 y el flujo manual en SAP2000 (Joseph).

Ver también: [[Random Forest]] · [[Generador OpenSees E030]] · [[Flujo integrado de herramientas]] · [[Decisiones]]
