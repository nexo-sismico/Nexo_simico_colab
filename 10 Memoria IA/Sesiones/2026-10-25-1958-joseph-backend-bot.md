---
tipo: sesion
fecha: 2026-10-25
autor: Joseph Leonardo Ccana Ayuque
tema: Preparación del backend del bot de Telegram en n8n
---
# Sesión — backend del bot (2026-10-25)

## Hecho
- Revisé el vault, los tres JSON de n8n y el código del modelo en `PieroVQ/ProyectoGH`.
- Confirmé en la cuenta n8n de Joseph que la credencial de Telegram está probada y asignada a los nodos. El disparador recibió un mensaje real; el flujo sigue inactivo.
- Añadí `03 Prototipo/backend_bot_e030/` con un servicio FastAPI inicial, Dockerfile, dependencias, artefacto de modelo y manifiestos de dominio. El servicio define `/schema`, `/consultas/validar`, `/consultas` y `/consultas/{id}`.
- Registré que el modelo requiere 107 entradas y que no deben inferirse datos de ingeniería ausentes.

## Pendiente / sin verificar
- La API nueva aún no se ha ejecutado contra el artefacto en el entorno; la instalación local de dependencias no terminó.
- No hay backend HTTPS, secreto Bearer, credencial IA ni servicio PDF conectado a n8n.
- El backend todavía no produce PDF ni archivos 3D. Falta acordar la captura de las 107 entradas.
- No se publicaron ni activaron los workflows; la prueba real hecha fue únicamente recepción del trigger.

## Próximo paso
Preparar una prueba local del servicio y decidir el alojamiento HTTPS y proveedor de IA con Joseph. Después conectar credenciales en n8n y ejecutar casos reales antes de activar.
