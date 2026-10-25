---
tags: [moc, aecode]
actualizado: 2026-10-24
---
# Nexo Sísmico — Inicio

> **Modalidad C: Investigación académica aplicada** (ya no startup).
> Demo Day: **24 oct 2026**. Entrega de hoy: **prototipo probado con 3 casos + video ≤ 2 min + ficha de 1 página**.

## Título de trabajo
Estimación preliminar de derivas sísmicas en edificios aporticados de concreto armado mediante generación paramétrica y aprendizaje automático.

## Pregunta de investigación
¿Con qué precisión Random Forest estima las derivas máximas de familias de edificios aporticados no usadas en el entrenamiento, y qué reducción de tiempo ofrece al comparar alternativas de predimensionamiento?

## 👉 Empieza aquí
- **[[Ruta de trabajo y coordinacion]]** — qué se entrega hoy, quién y en qué orden
- **[[Explicacion del proyecto]]** — el proyecto completo explicado de principio a fin (léelo primero)
- **[[Entrega Reto 06 - prototipo funcional]]** — qué subir hoy y dónde está cada archivo
- **[[Contexto]]** (`10 Memoria IA/`) — memoria compartida del equipo y sus IAs: estado, decisiones y sesiones · reglas para IAs en `AGENTS.md`
- **[[Flujo integrado de herramientas]]** — cómo encajan todas las herramientas y la historia del informe
- [[Inventario de insumos]] — dónde está cada archivo
- [[Handoff para Cowork]] · [[GitHub - configurar repositorio]] · `REGISTRO_EQUIPO.md`

## Mapa
- Proyecto: [[Planteamiento]] · [[Rubrica y checklist]] · [[Equipo y roles]] · [[Decisiones]] · [[Alcance y limitaciones]]
- Módulos: [[Generador OpenSees E030]] · [[Ruta E030 - repositorio de Piero]] · [[Modulo NSR-10 y SAP2000]] · [[Random Forest]] · [[Bot Telegram n8n]] · [[Datos del profesor NSR-10]]
- Repositorios: equipo https://github.com/FrailM7/nexo-sismico · E.030 (Piero) https://github.com/PieroVQ/ProyectoGH
- Prototipo (entrega de hoy): [[Prototipo - especificacion]] · [[Pruebas 3 casos]] · [[Guion video 2 min]] · [[Ficha 1 pagina]]
- Entregables finales: [[Informe tipo articulo]] · [[Presentacion PPT]] · [[Video ejecutivo 5 min]]
- Datos: carpeta `05 Datos` · Referencias: [[Normas y fuentes]]

## Estado rápido
| Pieza | Estado |
|---|---|
| Base OpenSees E.030 (1 500 estructuras, 1 500 familias) | ✅ En el repositorio de Piero · [[Ruta E030 - repositorio de Piero]] |
| Notebook NSR-10 (bloques 1–11) | Funciona; datos SAP de ejemplo en bloques 7, 8 y 10 |
| Bot Telegram n8n (Jean Piere) | Flujos listos; backend Python no implementado |
| Prototipo con 3 casos | ✅ Ruta B lista: [[Pruebas 3 casos]] · ficha en `07 Outputs` |
| Base de datos NSR-10 | ✅ 19 registros (18 profesor + caso del curso) |
| Informe tipo artículo (5 págs., v2 con E.030) | ✅ `04 Entregables/Informe/` · [[Informe tipo articulo]] |
| Presentación (15 diapositivas, v2 con E.030) | ✅ `04 Entregables/Presentacion/` · [[Presentacion PPT]] |
| Video prototipo (1:58) y ejecutivo v2 (4:36, con E.030) | ✅ MP4 en `08 Multimedia` (fuera de Git) · guion y .srt en `04 Entregables/Videos/` · falta subir por enlace |
| Random Forest NSR-10 (validación por planta) | ✅ MAE deriva 0.086 % (X) / 0.101 % (Y), −39 % vs referencia · [[Random Forest]] |
| Random Forest E.030 (300 familias reservadas) | ✅ Deriva R² 0,990 · MAE 0,040 % · 137 de 146 excedencias (Gradient Boosting como comparación: 0,995) · en informe y PPT v2 |
| Código del prototipo | ✅ Corre en Windows: `python "03 Prototipo/codigo/ejecutar_todo.py"` |
| App web del prototipo | ✅ En línea: https://nexo-sismico-nsr10.netlify.app (se publica sola al cambiar la app o el motor) · local: `python "03 Prototipo/app/abrir_app.py"` |
| Repositorio GitHub | ✅ https://github.com/FrailM7/nexo-sismico · sincronización automática cada 15 min en el PC de Nicolás |
