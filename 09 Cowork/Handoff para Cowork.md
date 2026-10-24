---
tags: [cowork, handoff]
---
# Handoff para Cowork (pasar el contexto a una sesión nueva)

## Cómo usarlo
1. En Claude (Cowork), conecta la carpeta `C:\Users\nicoi\Documents\AECODE Nexo Sismico`.
2. Pega el prompt de abajo como primer mensaje.

## Prompt para pegar
```
Trabajas en el proyecto académico "Nexo Sísmico" (Beca AI Talent, AECODE), modalidad C:
investigación académica aplicada. La carpeta conectada es un vault de Obsidian y repositorio
Git del grupo: es la única fuente de verdad.

Lee en este orden antes de hacer nada:
1. 00 Inicio.md
2. 01 Proyecto/Ruta de trabajo y coordinacion.md   ← qué se entrega, quién y cuándo
3. 01 Proyecto/Rubrica y checklist.md              ← criterios de calificación
4. 01 Proyecto/Inventario de insumos.md            ← dónde está cada archivo
5. 01 Proyecto/Decisiones.md y Alcance y limitaciones.md
6. 02 Modulos/ (los cuatro módulos) y 03 Prototipo/

Reglas:
- No mezclar con el proyecto "Oficinas Piedemonte A Bogotá" (otro vault) ni tocar
  Documentos\Claude outputs. Aquí el edificio del grupo 1 solo se usa como caso de prueba
  del análisis NSR-10 hasta antes del ítem 4 (sin diseño; omitir hoja "Diseño VTA-1").
- Las rutas Perú (E.030, 130 modelos) y Colombia (NSR-10) no se mezclan para entrenar.
- Marcar siempre lo provisional: V7 con datos SAP de ejemplo; datos ficticios del bot n8n.
- Nunca escribir claves, tokens, chat IDs ni URLs privadas en el vault.
- Guardar resultados en 07 Outputs/ y actualizar la nota correspondiente y Decisiones.md.
- Videos en 08 Multimedia/ (fuera de Git): compartir por enlace.

Tarea actual: [escribir aquí la tarea, por ejemplo "preparar los 3 casos del prototipo B y la ficha"].
```

## Estado al 2026-10-24
- Vault creado y ordenado. Falta publicarlo en GitHub (ver [[GitHub - configurar repositorio]]).
- Prototipo de hoy pendiente de decisión A/B (ver [[Ruta de trabajo y coordinacion]]).


## Estado 24 oct (cierre)
Entregables v1 listos en `04 Entregables/` (informe, presentación, ficha, guiones). Videos en `08 Multimedia/` (por enlace). Para publicar el repositorio usa el prompt de [[GitHub - configurar repositorio]].
