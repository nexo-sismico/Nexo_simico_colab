---
tipo: decision
proyecto: Nexo Sísmico
fecha: 2026-10-24
estado: aceptada
reemplaza:
tags: [decision, equipo, ia]
---
# La memoria del proyecto vive en el repositorio, no en vaults personales

## Contexto
La memoria de trabajo con IA (contexto, decisiones, sesiones) estaba en el vault personal de Nicolás ("Mi cerebro"). Los compañeros y sus IAs no la veían, así que cada uno empezaba sin contexto.

## Decisión
La memoria compartida está en `10 Memoria IA/` de este repositorio. Las IAs la leen por `AGENTS.md` (Codex, Cursor y otras), `CLAUDE.md` (Claude Code), `GEMINI.md` y `.github/copilot-instructions.md`, que apuntan a lo mismo. Cada quien sincroniza automáticamente con `09 Cowork/instalar_sincronizacion.ps1`.

## Alternativas descartadas
- **Seguir en vaults personales** — nadie más ve el contexto.
- **Ponerlo todo en la descripción del repositorio de GitHub** — GitHub la limita a 350 caracteres; la portada completa es el `README.md`.

## Consecuencias
- Toda IA que trabaje aquí debe leer `AGENTS.md` y `10 Memoria IA/Contexto.md` antes de actuar, y registrar decisiones y sesiones en esta carpeta.
- Riesgo: conflictos si dos personas editan la misma nota a la vez → cada quien edita sobre todo sus notas; las compartidas, con cambios pequeños.

## Relacionado
[[Contexto]] · [[_Indice]]
