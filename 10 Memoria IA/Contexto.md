---
tipo: contexto
proyecto: Nexo Sísmico
actualizado: 2026-10-24
---
# Contexto actual (memoria compartida para personas e IAs)

> Estado **actual** del proyecto. No es un historial: el historial está en `Sesiones/` y las decisiones en `Decisiones/`. Quien termine una tarea importante actualiza esta nota.

## Objetivo
Proyecto Nexo Sísmico (Beca AI Talent, AECODE; modalidad C, investigación académica aplicada).
**Pregunta:** ¿con qué precisión **Random Forest** estima las derivas máximas de familias de edificios aporticados no usadas en el entrenamiento, y qué ventaja ofrece al comparar alternativas de predimensionamiento?
Dos líneas de evidencia que **no se mezclan**: E.030 Perú (generador + OpenSees, 1 500 estructuras) y NSR-10 Colombia (prototipo de verificación + 18 edificios del Prof. Rojas Vallejo).

## Repositorios y herramientas
- Este repositorio (vault de Obsidian + código + entregables): https://github.com/FrailM7/nexo-sismico (privado).
- Ruta E.030 (generador, OpenSees, modelos): https://github.com/PieroVQ/ProyectoGH.
- Prototipo NSR-10: Python en `03 Prototipo/codigo/` (`ejecutar_todo.py`, `rutas.py`). Informe y PPT con Node (`informe.js`, `deck.js`). Videos con `videos.py` (ffmpeg).
- Sincronización automática con GitHub cada 15 min: `09 Cowork/sincronizar.ps1` (instalar con `09 Cowork/instalar_sincronizacion.ps1`).

## Restricciones y convenciones
- E.030 y NSR-10 no se mezclan para entrenar (normas, unidades, rangos y rigidez distintos).
- Toda cifra lleva su procedencia; marcar lo provisional o teórico (datos del profesor = teóricos).
- Nunca claves, tokens, chat IDs ni URLs privadas. Videos fuera de Git (`08 Multimedia/`, compartir por enlace).
- Resultados en `07 Outputs/`, entregables en `04 Entregables/`. Decisiones en `01 Proyecto/Decisiones.md` y aquí en `Decisiones/`.
- Escribir en español.

## Estado actual (24 oct 2026)
- ✅ Prototipo NSR-10 con 3 pruebas y ficha de 1 página (con enlace al repositorio).
- ✅ Ruta E.030: Random Forest en 300 familias reservadas → deriva R² 0,990, MAE 0,040 %, 137 de 146 excedencias detectadas. Gradient Boosting como comparación: R² 0,995, 139 de 146.
- ✅ Ruta NSR-10: Random Forest con 18 edificios → MAE 0,086 % / 0,101 %, −39 % frente a la referencia, 3 de 7 casos al límite.
- ✅ Informe v2 (5 págs.), presentación v2 (15 diap.), video del prototipo (1:58) y video ejecutivo v2 (4:36, sin voz, con subtítulos).
- ✅ Código portable (Windows/macOS/Linux) y sincronización automática.

## Pendientes
- Revisión del equipo del informe y la PPT v2; Jean Piere confirma la versión E.030 citada (RM 183-2026-VIVIENDA).
- Subir los videos a Drive o YouTube y pegar los enlaces en `04 Entregables/Video ejecutivo 5 min.md`.
- Cronometrar el flujo manual en SAP2000 (Joseph) para hablar de ahorro de tiempo.
- Completar habilidades en `REGISTRO_EQUIPO.md`; Miro y Discord.
- Invitar como colaboradores a Lucero, Alexis y Joseph (faltan sus usuarios de GitHub).
- Opcional: backend del bot de Telegram con el modelo E.030; ampliar la base NSR-10 con casos verificados.

## Decisiones vigentes clave
- [[ADR-2026-10-24-repo-privado-y-sync-automatico]]
- [[ADR-2026-10-24-integrar-ruta-e030-de-piero]]
- [[ADR-2026-10-24-codigo-portable-rutas-comunes]]
- [[ADR-2026-10-24-random-forest-en-la-pregunta]]
- [[ADR-2026-10-24-memoria-compartida-en-el-repo]]
