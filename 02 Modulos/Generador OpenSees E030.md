# Generador OpenSees (ruta Perú, E.030)

Responsable: Alexis (con el autor del generador).
- 130 configuraciones, 49 familias; cada familia mantiene pisos y vanos y varía secciones/cargas.
- Respuestas: periodos, cortante basal, desplazamiento de techo y deriva en X e Y.
- Partición: 100 desarrollo / 30 prueba, **por familias completas**.
- 43 de 130 configuraciones con etiqueta de incumplimiento de deriva (umbral 0.007).

Pendiente: confirmar si la deriva exportada es elástica o inelástica (E.030: 0.75·R para regulares), unidades, y caso de comprobación independiente.
JSON de Piero: ver `05 Datos/Piero JSON`.
