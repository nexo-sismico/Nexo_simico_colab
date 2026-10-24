---
tipo: indice
proyecto: Nexo Sísmico
---
# Memoria del proyecto (compartida)

Aquí guarda el equipo, y sus IAs, lo que no debe perderse entre sesiones: **el estado actual, las decisiones con su porqué y lo que se intentó y no funcionó**.

- [[Contexto]] — estado actual: léelo antes de trabajar.
- Reglas para las IAs: `AGENTS.md` en la raíz del repositorio.

## Cómo usar esta carpeta
| Cuándo | Qué hacer |
|---|---|
| Al empezar | Leer [[Contexto]], las decisiones `aceptada` más recientes y la última sesión |
| Al decidir algo que cambia el rumbo | Crear `Decisiones/ADR-AAAA-MM-DD-tema.md` (plantilla abajo) y una fila en `01 Proyecto/Decisiones.md` |
| Al terminar una sesión de trabajo | Crear `Sesiones/AAAA-MM-DD-HHMM-nombre.md` y actualizar [[Contexto]] si cambió el estado |

Plantilla de decisión: título · Contexto · Decisión · Alternativas descartadas · Consecuencias · Relacionado.
Plantilla de sesión: Objetivo · Qué se hizo · Decisiones · Lo que NO funcionó y por qué · Próximos pasos.
Nunca guardar claves, tokens ni datos personales.

## Decisiones
- [[ADR-2026-10-24-repo-privado-y-sync-automatico]] — repositorio privado y sincronización cada 15 min con chequeo de claves
- [[ADR-2026-10-24-integrar-ruta-e030-de-piero]] — la ruta E.030 de Jean Piere responde la pregunta central
- [[ADR-2026-10-24-codigo-portable-rutas-comunes]] — `rutas.py` + `ejecutar_todo.py`: el código corre en cualquier PC
- [[ADR-2026-10-24-random-forest-en-la-pregunta]] — se mantiene Random Forest; Gradient Boosting como comparación
- [[ADR-2026-10-24-memoria-compartida-en-el-repo]] — la memoria vive aquí, no en vaults personales

## Sesiones
- [[2026-10-24-1302]] — publicación en GitHub, código portable, revisión E.030, explicación y sincronización
- [[2026-10-24-1330-nicolas]] — videos v2 y memoria compartida para el equipo y sus IAs
