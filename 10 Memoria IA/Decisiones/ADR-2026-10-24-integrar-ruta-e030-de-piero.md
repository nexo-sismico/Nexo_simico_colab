---
tipo: decision
proyecto: AECODE Nexo Sismico
fecha: 2026-10-24
estado: aceptada
reemplaza:
tags: [decision, ml, e030]
---
# Integrar la ruta E.030 del repo de Piero como evidencia principal de R1

## Contexto
El vault decía "130 configuraciones, 49 familias, RF E.030 pendiente". El repo PieroVQ/ProyectoGH (commit 07fd4b2) ya tenía 1 500 estructuras/1 500 familias y modelos evaluados en 300 familias reservadas.

## Decisión
Enlazar el repo (no copiarlo) y documentarlo en `02 Modulos/Ruta E030 - repositorio de Piero.md`; actualizar notas. Métricas tomadas de sus CSV; excedencias calculadas en la revisión (139/146, 2 falsas alarmas).

## Alternativas descartadas
- **Copiar su base y modelos al vault** — duplica 8 MB y pierde trazabilidad.
- **Recargar `modelo_evaluacion.joblib` para reproducir métricas** — bloqueado (pickle = ejecución de código); sí se corrieron sus 11 pruebas unitarias (OK).

## Consecuencias
- El mejor modelo es Gradient Boosting, no RF: decisión pendiente del equipo sobre cómo nombrarlo en la pregunta.
- Falta llevar resultados al informe y a la PPT.

## Relacionado
[[Contexto]] · [[_Indice]]
