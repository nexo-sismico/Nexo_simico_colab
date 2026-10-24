# Nexo Sísmico — Beca AI Talent (AECODE)

**Estimación preliminar de derivas sísmicas en edificios aporticados de concreto armado mediante generación paramétrica, verificación normativa automatizada y aprendizaje automático.**
Investigación académica aplicada · Equipo: Lucero · Alexis · Nicolás Infante · Jean Piere · Joseph · Profesor de apoyo: Thomas F. Rojas Vallejo (UNAL).

> Este repositorio es **a la vez el vault de Obsidian del equipo y la memoria compartida para nuestras IAs**. Todo el contexto, las decisiones y el estado del proyecto están aquí, y cada computador del equipo se sincroniza solo con GitHub.

---

## 🧭 Si eres nuevo (persona o IA), lee en este orden
1. **[`10 Memoria IA/Contexto.md`](10%20Memoria%20IA/Contexto.md)** — estado actual y pendientes.
2. **[`01 Proyecto/Explicacion del proyecto.md`](01%20Proyecto/Explicacion%20del%20proyecto.md)** — el proyecto completo de principio a fin.
3. **[`AGENTS.md`](AGENTS.md)** — reglas de trabajo (las IAs lo leen solas).
4. **[`00 Inicio.md`](00%20Inicio.md)** — mapa del vault.

## 🎯 La pregunta y lo que encontramos
> ¿Con qué precisión **Random Forest** estima las derivas máximas de familias de edificios aporticados no usadas en el entrenamiento, y qué ventaja ofrece al comparar alternativas de predimensionamiento?

| Línea de evidencia | Datos | Resultado de Random Forest |
|---|---|---|
| **E.030 (Perú)** — generador + OpenSees ([repositorio de Jean Piere](https://github.com/PieroVQ/ProyectoGH)) | 1 500 estructuras de 1 500 familias; prueba con 300 familias nunca vistas | Deriva **R² 0,990**, error medio **0,040 %**, detecta **137 de 146** edificios que exceden el límite. Gradient Boosting (comparación): R² 0,995 |
| **NSR-10 (Colombia)** — prototipo de verificación + edificios del profesor | 18 edificios teóricos + caso del curso | Error de deriva 0,086 % / 0,101 % (−39 % frente a la referencia); detecta 3 de 7 casos al límite: solo sirve para priorizar |

**Conclusión:** dentro del dominio entrenado, Random Forest con variables físicas sirve para **descartar alternativas en fracciones de segundo**; la precisión depende más de la cantidad y trazabilidad de los datos que del algoritmo. No sustituye la verificación normativa.

El prototipo NSR-10 reproduce exactamente el cálculo de referencia con SAP2000 (Vs = 23 250 kN, deriva 0,991 %) y bloquea entradas incompletas o erróneas.

## 📦 Entregables
| Entregable | Archivo | Estado |
|---|---|---|
| Informe tipo artículo (5 págs.) | [`04 Entregables/Informe/`](04%20Entregables/Informe) | ✅ v2 |
| Presentación (15 diapositivas) | [`04 Entregables/Presentacion/`](04%20Entregables/Presentacion) | ✅ v2 |
| Ficha de pruebas (1 página) | [`04 Entregables/Prototipo/`](04%20Entregables/Prototipo) | ✅ |
| Video del prototipo (1:58) y ejecutivo (4:36) | `08 Multimedia/` (fuera de Git) · guiones y subtítulos en [`04 Entregables/Videos/`](04%20Entregables/Videos) | ✅ falta subir por enlace |

---

## 👥 Cómo trabajamos en conjunto (todos con lo mismo, siempre)

### Una sola vez, en tu computador
1. **Acepta la invitación** al repositorio (llega a tu correo de GitHub).
2. Instala **[GitHub Desktop](https://desktop.github.com)**, **Git para Windows** (`winget install Git.Git`) y **[Obsidian](https://obsidian.md)**.
3. GitHub Desktop → *File → Clone repository* → `FrailM7/nexo-sismico` → elige una carpeta.
4. Obsidian → *Open folder as vault* → esa carpeta.
5. **Activa la sincronización automática** (PowerShell, dentro de la carpeta clonada):
   ```powershell
   powershell -ExecutionPolicy Bypass -File "09 Cowork\instalar_sincronizacion.ps1"
   ```
   Desde ahí, **cada 15 minutos** tu PC trae los cambios del equipo, revisa que no haya claves ni archivos de más de 50 MB y sube lo tuyo. En macOS o Linux: plugin **Obsidian Git** con *auto commit-and-sync* cada 10 min.

### Día a día
- Trabaja en Obsidian (o con tu IA) normalmente: los cambios suben solos.
- **Edita sobre todo las notas de tu módulo** (tabla de responsables en [`AGENTS.md`](AGENTS.md)); en notas compartidas haz cambios pequeños y agrega filas en vez de reescribir. Así no hay conflictos.
- Si haces un cambio grande, haz tú mismo *Commit + Push* en GitHub Desktop con un mensaje claro (`Alexis: tabla de la familia 9`).
- Decisiones → `01 Proyecto/Decisiones.md` y `10 Memoria IA/Decisiones/`. Al cerrar una sesión de trabajo → `10 Memoria IA/Sesiones/`.
- Si la sincronización avisa conflicto (registro en `%LOCALAPPDATA%\NexoSismico\sincronizar.log`), resuélvelo en GitHub Desktop. Nunca uses *force push*.

### Con tu IA (Claude, ChatGPT/Codex, Gemini, Copilot, Cursor)
- **IAs que abren la carpeta** (Claude Code, Codex, Cursor, Gemini CLI, Copilot) leen solas `AGENTS.md`, `CLAUDE.md`, `GEMINI.md` o `.github/copilot-instructions.md`: ya saben las reglas, dónde está todo y cómo registrar lo que hacen.
- **IAs de chat** (ChatGPT, Claude.ai, Gemini web): al empezar, pégales `AGENTS.md` y `10 Memoria IA/Contexto.md`, y pídeles que al final te den la nota de sesión para guardarla en `10 Memoria IA/Sesiones/`.

---

## 🗂️ Estructura
| Carpeta | Contenido |
|---|---|
| `00 Inicio.md` | Mapa del vault y estado |
| `01 Proyecto/` | Explicación, planteamiento, rúbrica, roles, decisiones, alcance |
| `02 Modulos/` | E.030 (repositorio de Jean Piere), NSR-10 + SAP2000, Random Forest, bot n8n, datos del profesor |
| `03 Prototipo/` | Especificación, pruebas y código (`codigo/`) |
| `04 Entregables/` | Informe, presentación, ficha, guiones y subtítulos |
| `05 Datos/` · `06 Referencias/` | Insumos · normas y fuentes |
| `07 Outputs/` | Resultados generados (NSR-10 y E.030) |
| `08 Multimedia/` | Videos (fuera de Git; compartir por enlace) |
| `09 Cowork/` | Sincronización automática y traspaso de contexto |
| `10 Memoria IA/` | **Memoria compartida**: contexto, decisiones (ADR) y sesiones |

## ⚙️ Correr el código
```bash
pip install -r "03 Prototipo/codigo/requirements.txt"
python "03 Prototipo/codigo/ejecutar_todo.py"     # --informe para DOCX/PPTX, --videos para los MP4
```
Detalles en [`03 Prototipo/codigo/README.md`](03%20Prototipo/codigo/README.md).

**Reglas de oro:** E.030 y NSR-10 no se mezclan · toda cifra con su procedencia · nunca claves, tokens ni datos personales · los videos van por enlace.
