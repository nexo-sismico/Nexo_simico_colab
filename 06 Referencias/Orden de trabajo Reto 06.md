# ORDEN DE TRABAJO: RETO 06 - PROTOTIPO FUNCIONAL
**Programa:** AECODE - AI Talent 2 Generación
**Objetivo:** Construir y probar un prototipo funcional de la implementación tecnológica del proyecto final utilizando un caso real del sector AEC.

---

## 🛠️ 1. DEFINICIÓN DEL PROTOTIPO (Parte 1 y 2)
*Acciones iniciales antes de empezar a codificar o configurar.*

- [ ] **Seleccionar la pieza tecnológica:** Elegir una funcionalidad específica del proyecto final que se pueda convertir en un prototipo funcional (no tiene que ser todo el proyecto, solo una parte que funcione).
- [ ] **Definir el problema AEC:**
  - ¿Quién vive el problema?
  - ¿Con qué datos se trabaja?
  - ¿Qué demoras o errores genera actualmente?
- [ ] **Diseñar el esquema de funcionamiento (ej. en Miro):**
  - Mapear el flujo de datos: ¿Qué entra? $\rightarrow$ ¿Qué hace el prototipo? $\rightarrow$ ¿Qué sale?
  - Definir herramientas a usar (n8n, Make, Python, Claude, APIs, etc.).
  - Aclarar límites: ¿Qué decide la tecnología y qué requiere decisión humana?

## 💻 2. CONSTRUCCIÓN DEL PROTOTIPO
*Opciones de tecnologías permitidas (usar las que apliquen a tu proyecto).*

- [ ] **Automatización:** n8n, Make, Google Sheets + Apps Script, o Python.
- [ ] **Agentes IA:** Claude, ChatGPT, Gemini o el agente de n8n.
- [ ] **Análisis / Datos:** Python, Power BI, RAG, OCR.
- [ ] **Específicas del sector:** Implementación BIM, geoespacial, IFC, modelos 3D/4D.

## 🧪 3. PROTOCOLO DE PRUEBAS (Parte 3 - OBLIGATORIO)
*El prototipo DEBE ser sometido a estos tres escenarios de prueba. No se aceptan simulaciones.*

- [ ] **Prueba 1 (Camino Feliz):** Ingresar datos correctos y completos.
  - *Resultado esperado:* El sistema procesa la información y da la respuesta correcta.
- [ ] **Prueba 2 (Datos Faltantes):** Ingresar un registro con un dato omitido (ej. campo en blanco).
  - *Resultado esperado:* El sistema debe avisar que falta el dato; **NO** debe inventarlo (evitar alucinaciones).
- [ ] **Prueba 3 (Datos Erróneos):** Ingresar un dato imposible (ej. avance del 150%, fecha incoherente).
  - *Resultado esperado:* El sistema debe marcarlo como error y rechazarlo.

## 📦 4. PREPARACIÓN DE ENTREGABLES
*Materiales que se deben generar una vez el prototipo funciona.*

- [ ] **Enlace / Capturas:** Link al prototipo funcional o capturas de pantalla de la configuración.
- [ ] **Video de Demostración:**
  - Duración máxima: 2 minutos.
  - Mostrar el prototipo corriendo en vivo con el caso real.
- [ ] **Ficha Técnica (1 página):**
  - Problema que ataca.
  - Tecnología utilizada.
  - Resultados de las 3 pruebas ejecutadas.
  - Qué falta por mejorar en el futuro.

## 🌟 5. PLUS RECOMENDADO (Actividad Complementaria)
- [ ] **Medición del impacto (Antes vs. Después):** Medir cuánto tarda la tarea manualmente versus con el prototipo (se puede hacer con una muestra de 5 casos).

---

## ⚠️ REGLAS CRÍTICAS Y ADVERTENCIAS
1. **SEGURIDAD:** PROHIBIDO incluir claves, tokens, API keys o contraseñas en el código, capturas o videos.
2. **PRIVACIDAD:** PROHIBIDO usar datos personales reales en las pruebas.
3. **VERACIDAD:** No se evalúan ideas ni presentaciones de diapositivas, se evalúa tecnología funcionando. NO inventar resultados.

**⏳ FECHA LÍMITE DE ENTREGA:** Sábado 24 de octubre de 2026, 11:59 p.m.