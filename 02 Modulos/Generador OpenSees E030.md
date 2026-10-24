# Generador OpenSees (ruta Perú, E.030)

Responsable: Alexis (documentación) · código y base: Jean Piere — **https://github.com/PieroVQ/ProyectoGH** (ver [[Ruta E030 - repositorio de Piero]]).
- **Versión vigente: 1 500 estructuras de 1 500 familias** (una alternativa por familia; 2 368 intentos, semilla 20261119). La versión anterior tenía 130 configuraciones y 49 familias.
- Dominio: 2–5 pisos, 2–5 vanos, luces 3–6 m, alturas 2,7–3,3 m, f'c 210/280 kgf/cm², Z 0,10–0,45, suelos S0–S3, U 1,0/1,3.
- Respuestas: periodos, cortante modal ajustado, desplazamiento de techo y deriva en X e Y (8 salidas).
- Partición: 1 200 desarrollo / 300 prueba, **por familias**.
- ✅ La deriva exportada es la **normativa** (elástica × 0,75·R, R = 8), comparada con 0,007. Unidades: cm, kgf, s.

Pendiente: caso de comprobación independiente (una familia calculada a mano o en SAP2000) y una figura 3D para el informe (`porticos_rc/main.py ver`).
JSON del bot de Piero: ver `05 Datos/Piero JSON`.
