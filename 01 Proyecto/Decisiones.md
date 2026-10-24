# Registro de decisiones (evidencia de iteración)

| Fecha | Decisión | Motivo |
|---|---|---|
| 2026-10-03 | Problema y solución definidos (entrega parcial) | Hito de la rúbrica |
| 2026-10-10 | Acotar a pórticos de concreto regulares, columnas cuadradas | Conversación con el profesor |
| 2026-10-13 | 10 plantas, relación de aspecto ≤ 1.5, cargas con tablas NSR-10 | Evitar irregularidad torsional; trazabilidad normativa |
| 2026-10-13 | 20 edificios (pisos 4–10 en parejas) enviados al profesor | Tiempo de cómputo del profesor |
| 2026-10-22 | Se reciben 18 resultados del profesor (falta P9) | — |
| 2026-10-22 | Dos líneas de datos no mezclables: E.030 (130 modelos) y NSR-10 (profesor) | Norma, rango de pisos y rigidez distintos |
| 2026-10-23 | Notebook NSR-10 completado (bloques 6–11) con flujo SAP2000 | Análisis aplicado hasta derivas y fuerzas de diseño |
| 2026-10-24 | **Cambio de modalidad: startup → investigación académica aplicada** | Tiempo disponible |
| 2026-10-24 | Prototipo con 3 pruebas (correcto, faltante, erróneo) | Requisito de la entrega |
| 2026-10-24 | Prototipo de hoy = ruta B (módulo NSR-10) calibrado con el edificio del curso (grupo 1) y 12 combinaciones de deriva | Ya funciona y es verificable contra SAP2000 |
| 2026-10-24 | Informe con dos líneas de evidencia (E.030 + RF; NSR-10 + base de datos) y el bot como interfaz propuesta | Coherencia con la pregunta de investigación |
| 2026-10-24 | Base NSR-10 unificada: 18 edificios del profesor + casos del módulo | Ampliar el predictor a Colombia sin mezclar con E.030 |
| 2026-10-24 | Los 18 resultados del profesor se marcan como **teóricos**; P9 no está porque falló el dimensionamiento en su algoritmo OpenSees | Aclaración del profesor: algunas plantas y luces no se resolverían con pórticos resistentes a momento en la práctica |
| 2026-10-24 | Random Forest NSR-10 evaluado dejando una planta completa fuera (9 pliegues) y comparado con regresión lineal, Ta y la media | Probar generalización a plantas no vistas, que es la pregunta de investigación |
| 2026-10-24 | No se afirma un porcentaje de ahorro de tiempo: solo se reportan tiempos medidos (cálculo < 1 ms, predicción 32 ms) | El flujo completo en SAP2000 no se cronometró |
| 2026-10-24 | Videos generados sin voz y con subtítulos; el equipo puede grabar la narración sobre ellos | No hay herramienta de voz en el entorno; el guion queda listo |
