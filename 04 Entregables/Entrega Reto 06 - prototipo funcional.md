---
tags: [entrega, prototipo, reto06]
actualizado: 2026-10-24
---
# Entrega Reto 06 — Prototipo funcional (checklist)

Orden de trabajo: `06 Referencias/Orden de trabajo Reto 06.md` · Fecha límite: **sábado 24 oct 2026, 11:59 p. m.**
Equipo: Lucero Vivivana Vargas Silva · Oswer Alexis Huamani · Nicolás Infante Hernández · Jean Piere Velásquez Quispe · Joseph Leonardo Ccana Ayuque

## Qué subir a la plataforma
| # | Pide la orden | Archivo listo | Estado |
|---|---|---|---|
| 1 | **Ficha técnica (1 página)**: problema, tecnología, resultados de las 3 pruebas, qué falta mejorar | `04 Entregables/Prototipo/Ficha_pruebas_prototipo_NSR10.pdf` | ✅ |
| 2 | **Video ≤ 2 min** con el prototipo corriendo en vivo con el caso real | `08 Multimedia/Video_prototipo_en_vivo.mp4` (1:20, grabación real de la consola) | ✅ falta subir a Drive/YouTube y pegar el enlace aquí: _(enlace)_ |
| 3 | **Enlace o capturas** | Repositorio https://github.com/FrailM7/nexo-sismico · capturas en `04 Entregables/Prototipo/capturas/` | ✅ |
| 4 | Definición del prototipo y esquema (Miro) | `04 Entregables/Prototipo/Definicion_prototipo.pdf` · `Esquema_prototipo.png` | ✅ falta pegar el esquema en el tablero de Miro |
| + | Interfaz interactiva para ingenieros | App web `03 Prototipo/app/` (`python "03 Prototipo/app/abrir_app.py"`) · captura `capturas/app_web_verificar.png` | ✅ local; falta hospedarla |
| 5 | Plus: medición antes vs. después (5 casos) | Plantilla en `Definicion_prototipo.pdf`, sección 6 | ⏳ falta cronometrar el cálculo manual |

## Cómo cumple cada parte de la orden
- **Pieza tecnológica:** módulo de verificación sísmica NSR-10 (`03 Prototipo/codigo/nexo_nsr10.py`).
- **Problema AEC:** el ingeniero que predimensiona edificios aporticados rehace a mano espectro, FHE, derivas y estabilidad por cada alternativa; datos faltantes o en otras unidades pasan sin aviso.
- **Esquema:** entra JSON (sitio, geometría, pesos, SAP2000) → valida → calcula NSR-10 → sale reporte con dictamen + registro para la base. La tecnología valida y calcula; la persona modela en SAP2000 y decide el diseño.
- **Tecnología:** Python (automatización), SAP2000 (datos del caso real), scikit-learn (base del predictor), GitHub.
- **Pruebas (ejecución real):** 1) datos completos → OK, Vs = 23 250 kN, deriva 0,991 % ≤ 1,0 %, igual a Excel + SAP2000 · 2) sin Fv → se detiene y dice qué falta, no lo inventa · 3) altura de 350 → error, explica el rango y rechaza.
- **Reglas:** sin claves ni tokens; sin datos personales (edificio académico); resultados reales, no inventados.

## Cómo regenerar (si cambia algo)
```
python "03 Prototipo/codigo/correr_pruebas.py"     # resultados de las 3 pruebas
python "03 Prototipo/codigo/demo_en_vivo.py"       # demo para grabar (≈ 1:20); --rapido para revisar
python "03 Prototipo/codigo/prototipo_docs.py"     # esquema y definición
python "03 Prototipo/codigo/ficha.py"              # ficha de 1 página
```
Los nombres de los integrantes se editan solo en `03 Prototipo/codigo/equipo.json`.
