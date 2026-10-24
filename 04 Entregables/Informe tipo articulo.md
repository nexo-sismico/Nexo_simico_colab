# Informe tipo artículo (≤ 5 páginas) — ✅ versión 2 (con resultados E.030)

Archivos: `04 Entregables/Informe/Informe_tecnico_Nexo_Sismico.pdf` (5 págs.) y `.docx` (editable). Se regenera con `python "03 Prototipo/codigo/ejecutar_todo.py" --informe` y el PDF con Word (Guardar como PDF).

Estructura: Resumen · 1 Introducción (problema, pregunta, objetivos, ejes) · 2 Metodología (2.1 generación E.030, 2.2 módulo NSR-10, 2.3 aprendizaje E.030, 2.4 base NSR-10 y aprendizaje) · 3 Resultados (3.1 prototipo, 3.2 Random Forest en 300 familias E.030 con Gradient Boosting como comparación, 3.3 Random Forest NSR-10) · 4 Discusión · 5 Conclusiones · 11 referencias.

Decisión (24 oct): la pregunta mantiene **Random Forest**; Gradient Boosting se reporta como comparación. Cifras E.030 de `07 Outputs/E030/resumen_E030.json` (`resumen_e030.py`).

## Revisión del equipo antes de enviar
- [ ] Lucero: coherencia pregunta–objetivos–conclusiones y redacción del resumen
- [ ] Alexis: párrafo 2.1 (generador E.030) — supuestos y cifras
- [x] Métricas E.030 en 3.2 (Random Forest entrenado con la partición de Jean Piere; Gradient Boosting de su repositorio)
- [ ] Jean Piere: revisar 2.1, 2.3 y 3.2 y confirmar la versión de la E.030 citada en [2] (RM 183-2026-VIVIENDA, tomada de su METODOLOGIA.md)
- [ ] Joseph: tiempos medidos, si se cronometra el flujo SAP2000
- [ ] Todos: nada de claves, tokens ni rutas personales
