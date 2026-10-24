# Módulo NSR-10 y SAP2000 (Nicolás)

Notebook: `Plantilla_Analisis_Estructural_AEA_NSR10_completa.ipynb` (en el proyecto de Claude).

| Bloque | Hace | Norma |
|---|---|---|
| 1 | Aa, Av, Fa, Fv, I por ciudad, suelo y uso | A.2 |
| 2 | Espesor de losa, viguetas, aligeramiento | C.9.5, C.8.13 |
| 3–3B | Planta (AutoCAD LIST), avalúo de cargas | Título B |
| 4 | Pesos por nivel, Wt, hn | — |
| 5 | FHE: Ta, Cu·Ta, Sa(T), Vs, Fx/Fy, torsión 5 % | A.4, A.3.6.7 |
| 6 | Espectro para SAP2000 | A.2.6 |
| 7 | Derivas con torsión y P-Delta | A.6 |
| 8 | Irregularidades y R | A.3.3 |
| 9 | 34 combinaciones con E/R | B.2.4, A.3.6.3 |
| 10 | Masa participativa y ajuste de cortante dinámico | A.5 |
| 11 | Resumen y registro JSON para ML | — |

**Caso V7 (Cúcuta, suelo D, 5 pisos):** Sa = 1.006 g · Ta = 0.634 s · Cu·Ta = 0.760 s · Wt ≈ 64 600 kN · Vs ≈ 65 000 kN · R = 6.3 (retroceso 2P).
⚠️ Derivas (~0.8 %) y ajuste dinámico = **datos de ejemplo** hasta pegar resultados SAP.

Alcance para la entrega académica: análisis estructural **hasta antes del ítem 4** del ejercicio (grupo 1). Excluir hoja VTA-1 (diseño). Ver `05 Datos/Nicolas`.

## Caso de prueba: ejercicio del curso, grupo 1
Edificio de oficinas en concreto reforzado, 5 pisos, Bogotá, suelo **Piedemonte A** (microzonificación). Altura libre 3.50 m (piso 1) y 2.50 m (pisos superiores). Losa aligerada en una dirección. f'c = 21 MPa, acero A706 Gr 60. Cubierta tipo A (Tabla B.4.2.1-2). Luces grupo 1: X1 = 6.35, X2 = 7.05, X3 = 8.40, Y1 = 6.75, Y2 = 7.25 m.
Alcance para AECODE: ítems 1 a 3 de la memoria (descripción, cargas, fuerza sísmica, derivas e índice de estabilidad). **Sin diseño.**
Excel de soporte: `PROYECTO DISEÑO_personal1.xlsx` — hojas 00 Memoria, 01 Geometría, 02 Losa, Reacciones y cargas, Escaleras, 05 Espectro, FHE, derivas (Der-…), Análisis de R. **Omitir "Diseño VTA-1".**
