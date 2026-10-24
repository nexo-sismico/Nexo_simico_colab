# Datos del profesor (NSR-10, Bogotá)

Algoritmo: Prof. Thomas Federico Rojas Vallejo (UNAL), OpenSees; DES, suelo lacustre 200 de Bogotá, regulares (R = R0).

> [!warning] Aclaración del profesor (24 oct)
> "Varios de estos resultados son de carácter únicamente teórico, dado que las configuraciones en planta y la magnitud de las luces de algunas configuraciones no se resolverían en pórticos resistentes a momento en la práctica. Además las plantas que no están es porque tuvieron un error en el dimensionamiento para el algoritmo de OpenSees."
> → En la base de datos su `estado_dato` es *teórico (profesor)*; se usan para entrenar y comparar, **no como diseños**. P9 no se pide de nuevo: falló el dimensionamiento.
- 20 edificios propuestos (10 plantas × 2 alturas), **18 con resultados** (falta P9-4P y P9-10P).
- Salidas: Tx, Ty, Tz, Sa (0.45 constante), Vx, Vy, dx, dy, Cu·Ta; secciones de columnas y vigas en imágenes.
- **No se mezcla** con la base E.030.

## Cómo se agregan a la base de datos
`03 Prototipo/codigo/base_datos_nsr10.py` une:
1. Entradas que definió el equipo (`config_plantas_profesor.py`: luces, pisos, uso, cargas).
2. Resultados del profesor (`Resumen_resultados_profesor.xlsx`).
3. Casos validados por el módulo NSR-10 (hoy: edificio del curso, grupo 1).

Salida: `07 Outputs/Prototipo NSR-10/base_datos_NSR10.csv` — **19 registros**, esquema común con fuente, norma, programa y estado del dato.

## Pendientes
- [ ] Transcribir secciones de columnas y vigas de las 34 imágenes (columna `columnas`).
- [x] ~~Pedir P9-4P y P9-10P~~ → fallaron en el dimensionamiento del algoritmo; no se incluyen.
- [ ] Confirmar con el profesor que usó la versión final de las plantas (P2, P5 y P6 cambiaron el 13 de oct).
- [ ] Confirmar si sus derivas usan inercias agrietadas.

Resultados del aprendizaje con esta base: ver [[Random Forest]] (sección NSR-10).

Cita: Rojas Vallejo, T. F. (2026). *Algoritmo de diseño sísmico de pórticos de concreto reforzado en OpenSees* [Código no publicado]. Universidad Nacional de Colombia.
