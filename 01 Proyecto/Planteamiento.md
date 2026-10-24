# Planteamiento

**Problema.** Comparar alternativas de predimensionamiento obliga a repetir geometría, cargas, parámetros normativos y análisis. Falta demostrar con qué precisión un predictor aproxima las derivas de familias nuevas y qué tiempo ahorra.

**Solución.** Flujo reproducible: generar familias de estructuras → analizarlas (OpenSees, E.030) → documentar el módulo NSR-10 vinculado a SAP2000 → entrenar Random Forest con resultados verificados → herramienta que recibe una alternativa y estima derivas en X e Y.

**Objetivo general.** Desarrollar y validar una herramienta predictiva de derivas sustentada en simulaciones documentadas, evaluada con errores, detección de excedencias y tiempos.

**Objetivos específicos (propuesta)**
1. Generar y analizar familias paramétricas con supuestos documentados.
2. Documentar la ruta colombiana NSR-10 + SAP2000 y su intercambio de datos.
3. Entrenar Random Forest separando por familias y compararlo con un predictor sencillo.
4. Medir MAE, RMSE, R², excedencias no detectadas y tiempos.
5. Demostrar el prototipo con casos correctos, incompletos y erróneos.

**Hipótesis.** El predictor reduce el error frente a una referencia sencilla y el tiempo de evaluación de alternativas dentro del dominio estudiado. Se acepta o rechaza con familias reservadas.

**Ejes temáticos propuestos** (confirmar nombres oficiales del temario)
| Eje | Evidencia |
|---|---|
| IA y aprendizaje automático | Random Forest, evaluación sobre familias reservadas |
| Programación y automatización AEC | Generador paramétrico, notebook NSR-10, exportaciones |
| Simulación estructural | OpenSees, SAP2000, modelo 3D |
| Análisis y visualización de datos | Depuración, calculado vs predicho, métricas |

Ejemplo del problema (Excel, familia 9): ID 17 columnas 30×30 → derivas 0.0092 / 0.0099; ID 18 35×35 → 0.0056 / 0.0060 (≈39 % menos, dentro de 0.007). Son datos del Excel, no predicciones.
