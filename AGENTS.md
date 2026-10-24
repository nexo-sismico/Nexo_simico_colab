# AGENTS.md — instrucciones para cualquier IA que trabaje en Nexo Sísmico

> Lo leen automáticamente Codex, Cursor, Copilot, Gemini, Claude Code y otros agentes. Si usas una IA de chat sin acceso al repositorio, pégale este archivo y `10 Memoria IA/Contexto.md` al empezar.

## 1. Qué es este repositorio
Vault de Obsidian **y** repositorio Git del equipo **Nexo Sísmico** (Beca AI Talent, AECODE; modalidad C, investigación académica aplicada). Es la **única fuente de verdad**: lo que no está aquí no existe para la entrega.

**Pregunta de investigación:** ¿con qué precisión **Random Forest** estima las derivas máximas de familias de edificios aporticados de concreto no usadas en el entrenamiento, y qué ventaja ofrece al comparar alternativas de predimensionamiento?

**Dos líneas de evidencia que NO se mezclan:**
| Línea | Qué es | Dónde | Resultado clave |
|---|---|---|---|
| E.030 (Perú) | Generador paramétrico + OpenSees, 1 500 estructuras de 1 500 familias | https://github.com/PieroVQ/ProyectoGH · `02 Modulos/Ruta E030 - repositorio de Piero.md` | Random Forest en 300 familias reservadas: deriva R² 0,990, MAE 0,040 %, 137 de 146 excedencias. Gradient Boosting (comparación): R² 0,995 |
| NSR-10 (Colombia) | Prototipo que valida y calcula (FHE, derivas, Q, R) + 18 edificios teóricos del Prof. Rojas Vallejo | `03 Prototipo/codigo/` · `02 Modulos/Modulo NSR-10 y SAP2000.md` | Reproduce SAP2000 (Vs 23 250 kN, deriva 0,991 %); RF con 18 datos: −39 % de error, solo prioriza |

## 2. Lee esto antes de hacer nada (en orden)
1. `10 Memoria IA/Contexto.md` — estado actual y pendientes.
2. `01 Proyecto/Explicacion del proyecto.md` — el proyecto completo de principio a fin.
3. `10 Memoria IA/_Indice.md` — decisiones vigentes (no las contradigas sin proponer una nueva).
4. `01 Proyecto/Rubrica y checklist.md` — cómo se califica.
5. La nota del módulo en el que vas a trabajar (`02 Modulos/`, `03 Prototipo/`, `04 Entregables/`).

## 3. Reglas que no se rompen
- **E.030 y NSR-10 no se mezclan** para entrenar ni en una misma tabla de métricas (normas, unidades, rangos de altura e hipótesis distintas).
- **La pregunta dice Random Forest.** Gradient Boosting se reporta solo como comparación.
- **Toda cifra lleva su procedencia** (calculado, SAP2000, profesor, generador) y lo provisional se marca. Los 18 edificios del profesor son **teóricos**.
- **Nunca** escribas claves, tokens, chat IDs, URLs privadas ni datos personales. La sincronización bloquea patrones de claves, pero no confíes en eso.
- **No subas videos** (`08 Multimedia/` está fuera de Git): se comparten por enlace.
- No modifiques archivos originales de datos (`03 Prototipo/codigo/Resumen_resultados_profesor.xlsx`, la base E.030 del otro repositorio).
- Límites de entrega: informe ≤ 5 páginas, video del prototipo ≤ 2 min, video ejecutivo ≤ 5 min, ficha de 1 página.
- Escribe en **español**, frases cortas y claras.

## 4. Estructura
| Carpeta | Contenido |
|---|---|
| `00 Inicio.md` | Mapa del vault y tabla de estado |
| `01 Proyecto/` | Explicación, planteamiento, rúbrica, roles, decisiones, alcance |
| `02 Modulos/` | E.030, NSR-10 + SAP2000, Random Forest, bot n8n, datos del profesor |
| `03 Prototipo/` | Especificación, pruebas, **código** (`codigo/`) y **app web** (`app/`) |
| `04 Entregables/` | Informe, presentación, ficha, guiones y subtítulos |
| `05 Datos/` | Insumos (JSON del bot, etc.) |
| `07 Outputs/` | Resultados generados (NSR-10 y E.030) |
| `08 Multimedia/` | Videos (fuera de Git) |
| `09 Cowork/` | Sincronización y traspaso de contexto |
| `10 Memoria IA/` | **Memoria compartida**: contexto, decisiones (ADR) y sesiones |

## 5. Cómo correr el código
```
pip install -r "03 Prototipo/codigo/requirements.txt"
python "03 Prototipo/codigo/ejecutar_todo.py"             # pruebas → base → ML → cifras → figuras → ficha
python "03 Prototipo/codigo/ejecutar_todo.py" --informe   # + informe DOCX y presentación PPTX (npm install en codigo/)
python "03 Prototipo/codigo/ejecutar_todo.py" --videos    # + videos (requiere ffmpeg)
python "03 Prototipo/codigo/resumen_e030.py" RUTA/ProyectoGH   # resultados E.030 para informe y PPT
python "03 Prototipo/app/abrir_app.py"                  # app web del prototipo (usa el mismo nexo_nsr10.py)
```
Las métricas de Random Forest pueden variar en el cuarto decimal entre equipos; no subas resultados regenerados si solo cambia ese ruido.

## 6. Cómo registrar lo que haces (memoria compartida)
- **Decisión que cambia el rumbo** → `10 Memoria IA/Decisiones/ADR-AAAA-MM-DD-tema.md` + una fila en `01 Proyecto/Decisiones.md` + línea en `10 Memoria IA/_Indice.md`.
- **Al terminar una sesión** → `10 Memoria IA/Sesiones/AAAA-MM-DD-HHMM-<tu nombre>.md` (qué se hizo, qué no funcionó y por qué, próximos pasos) y actualiza `10 Memoria IA/Contexto.md` si cambió el estado.
- **Cambiaste una cifra** → actualízala en todas partes (informe, PPT, notas): mismo título, pregunta y números en todo.

## 7. Cómo trabajamos en conjunto (Git)
- Cada integrante tiene la **sincronización automática** instalada (`09 Cowork/instalar_sincronizacion.ps1`): cada 15 min trae los cambios del equipo, revisa que no haya claves y sube lo nuevo.
- Para evitar conflictos: **cada quien edita sobre todo las notas de su módulo**; en notas compartidas (`00 Inicio.md`, `Decisiones.md`, `Contexto.md`) haz cambios pequeños y agrega filas en lugar de reescribir.
- Si una IA hace muchos cambios, haz un commit con mensaje claro (`Alexis: tabla de la familia 9`) en lugar de esperar al automático.
- Si la sincronización reporta conflicto, resuélvelo en GitHub Desktop; no fuerces (`--force`) nunca.

## 8. Responsables
Nombres oficiales (para entregables): `03 Prototipo/codigo/equipo.json`.

| Persona | Rol | Notas que suele editar |
|---|---|---|
| Lucero Vivivana Vargas Silva | Planteamiento académico | `01 Proyecto/Planteamiento.md`, introducción del informe |
| Oswer Alexis Huamani | Generación paramétrica y OpenSees | `02 Modulos/Generador OpenSees E030.md` |
| Nicolás Infante Hernández | Módulo NSR-10 y SAP2000, repositorio | `02 Modulos/Modulo NSR-10 y SAP2000.md`, `03 Prototipo/` |
| Jean Piere Velásquez Quispe | Datos, modelos E.030 y bot n8n | `02 Modulos/Ruta E030 - repositorio de Piero.md`, `02 Modulos/Bot Telegram n8n.md` |
| Joseph Leonardo Ccana Ayuque | Validación, tiempos e integración | `04 Entregables/`, tiempos |
