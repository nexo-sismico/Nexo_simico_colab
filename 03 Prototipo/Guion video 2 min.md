# Guion — video del prototipo (≤ 2 min)

> ✅ **Video para entregar: `08 Multimedia/Video_prototipo_en_vivo.mp4` (1:20)**, grabación real de la consola corriendo `python demo_en_vivo.py` con las 3 pruebas (la demo narra cada paso en pantalla). Capturas en `04 Entregables/Prototipo/capturas/`. El video animado de abajo queda como respaldo.

> ✅ Generado: `08 Multimedia/Video_prototipo_NSR10.mp4` (1:58, sin voz, subtítulos con esta narración; tiempos en `04 Entregables/Videos/Video_prototipo_NSR10.srt`). Muestra las salidas reales de los 3 casos. Subir por enlace (no a Git).

| Tiempo | Pantalla | Narración |
|---|---|---|
| 0:00–0:15 | Diagrama de [[Flujo integrado de herramientas]] | "Nexo Sísmico estima derivas para comparar alternativas. Este es el módulo NSR-10 que produce respuestas de referencia verificables." |
| 0:15–0:50 | `caso1_completo.json` → `python correr_pruebas.py` → salida caso 1 | "Con los datos del edificio del curso, el prototipo calcula Sa, cortante, fuerzas, derivas de 12 combinaciones y estabilidad: Vs 23 250 kN, deriva 0.99 %, cumple." |
| 0:50–1:05 | Tabla Excel vs prototipo | "Reproduce exactamente el cálculo de referencia hecho con SAP2000." |
| 1:05–1:25 | Caso 2 | "Si falta un dato, por ejemplo Fv, se detiene y dice cuál falta." |
| 1:25–1:45 | Caso 3 | "Si un dato está mal, como una altura en centímetros, lo rechaza y explica el rango." |
| 1:45–2:00 | `base_datos_NSR10.csv` | "Cada caso válido se convierte en un registro de la base de datos que alimentará al predictor." |

Antes de grabar: cerrar pestañas con claves, tokens o correos; no mostrar rutas personales.
