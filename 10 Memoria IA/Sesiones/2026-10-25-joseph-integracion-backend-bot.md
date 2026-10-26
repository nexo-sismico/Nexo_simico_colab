---
tipo: sesion
fecha: 2026-10-25
autor: Joseph Leonardo Ccana Ayuque
tema: Validación local del backend y preparación del despliegue del bot
---

# Backend del bot E.030: validación local y bloqueo de despliegue

## Hecho
- Preparé un entorno virtual local (ignorado por Git) e instalé las dependencias del backend.
- Cargué `modelo_final.joblib` y confirmé 107 entradas y ocho objetivos de predicción.
- Corregí `normalize_unit()` para quitar diacríticos Unicode; valores como `adimensional / categoría` se rechazaban al compararse con la forma sin tilde.
- Ejecuté una prueba local con entradas sintéticas dentro de rangos: validación aceptada, ocho predicciones y repetición idempotente de la consulta.
- Revisé los tres workflows n8n: `BACKEND_URL` aún apunta a un marcador; el informe conserva `PDF_SERVICE_URL` provisional para Gotenberg.

## No hecho / limitaciones
- No se desplegó Railway ni se autorizó la app GitHub. Joseph confirmó la autorización OAuth solicitada, pero GitHub muestra el botón «Autorizar» deshabilitado; no se ha concedido acceso a la cuenta/repositorio.
- No hubo llamada real desde Telegram, y el caso sintético no valida precisión estructural ni reemplaza datos reales.
- No se configuró Gotenberg ni se generó PDF/archivo 3D.
- Los workflows siguen sin estar listos para activar: necesitan backend HTTPS, secreto Bearer sincronizado con n8n, configuración PDF y prueba punta a punta.

## Próximos pasos
1. Resolver el estado del botón OAuth de Railway y revisar el alcance de la app GitHub antes de darle acceso al repositorio privado.
2. Desplegar el contenedor con `BOT_API_TOKEN`, `BOT_DB_PATH` en volumen persistente y health check `/health`.
3. Configurar en n8n la misma credencial Bearer y URL en los tres workflows.
4. Configurar generación de PDF, probar datos reales del dominio por Telegram y validar la entrega del informe antes de publicar.
