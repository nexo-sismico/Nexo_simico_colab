# Prototipo — especificación (entrega de hoy)

**Qué es.** Módulo de análisis sísmico NSR-10 automatizado que recibe los datos de un edificio en un formulario/JSON, **valida** las entradas y entrega parámetros sísmicos, pesos, FHE y verificaciones, con un mensaje claro cuando falta o está mal un dato.

**Flujo:** Entrada (JSON/panel) → Validación (faltantes, rangos, tipos) → Cálculo NSR-10 → Reporte.

**Reglas de validación (borrador, ajustar con el ejercicio del grupo 1)**
| Campo | Regla |
|---|---|
| ciudad | Debe existir en la tabla de capitales o usar PERSONALIZADO con Aa y Av |
| tipo_suelo | A, B, C, D o E |
| grupo_uso | 1–4 |
| alturas de entrepiso | > 0 y ≤ 6 m |
| luces | > 0 |
| columnas dx, dy | ≥ 0.30 m en DES (C.21) |
| periodos Tx, Ty | > 0 |

**Tres pruebas:** ver [[Pruebas 3 casos]].
