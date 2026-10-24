# Pruebas con 3 casos — RESULTADOS (2026-10-24)

Prototipo: `03 Prototipo/codigo/nexo_nsr10.py` · Ejecutar `python correr_pruebas.py` · Salidas: `07 Outputs/Prototipo NSR-10/`

| # | Caso | Entrada | Esperado | Obtenido | Tiempo |
|---|---|---|---|---|---|
| 1 | Bien llenado | Edificio del curso, grupo 1 (Piedemonte A), 12 combinaciones en esquinas E5 y A1 | Cálculo completo | **OK** · Vs = 23 250 kN · deriva máx 0.985 % (X) / 0.991 % (Y) ≤ 1.0 % · Q = 0.0165 · R = 5.0 | < 1 ms |
| 2 | Falta un dato | Sin `sitio.Fv` | Detener y pedir el dato | **Detenido**: "FALTA: sitio.Fv — coeficiente de amplificación Fv" | < 1 ms |
| 3 | Dato equivocado | Altura libre piso 1 = 350 | Rechazar e indicar rango | **Rechazado**: "350 m fuera de [1.8, 6.0] m — ¿está en centímetros?" | < 1 ms |

## Validación contra el Excel (SAP2000)
| Magnitud | Excel | Prototipo |
|---|---|---|
| Vs (kN) | 23 250 | 23 250 |
| Fx cubierta (kN) | 7 361 | 7 361 |
| Deriva máx X / Y (%) | 0.985 / 0.991 | 0.985 / 0.991 |
| Q máx | 0.0165 | 0.0165 |
| Torsión Δmax/Δprom | 1.148 (X2, piso 2) | 1.193 (máximo de las 12 combinaciones) → regular, pero cerca de 1.2 |

Ficha: `07 Outputs/Prototipo NSR-10/Ficha_pruebas_prototipo_NSR10.pdf`
