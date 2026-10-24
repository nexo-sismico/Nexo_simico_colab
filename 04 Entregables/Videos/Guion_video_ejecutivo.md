# Guion del video ejecutivo (duración 4:48)

Narración por diapositiva. Para grabar la voz: reproducir el MP4 y leer cada subtítulo cuando aparece, o grabar el audio aparte y montarlo sobre el MP4 (el .srt tiene los tiempos).

## 1. Nexo Sísmico  ·  0:00 (15 s)

Somos Nexo Sísmico. Nuestro proyecto es una investigación aplicada: estimar de forma preliminar las derivas sísmicas de edificios aporticados de concreto, para comparar alternativas de predimensionamiento sin rehacer un modelo completo cada vez.

## 2. Cada alternativa cuesta un modelo completo  ·  0:14 (17 s)

El problema: en el predimensionamiento cada alternativa obliga a repetir espectro, pesos, fuerzas, modelo y revisión de derivas. En nuestra base paramétrica de 130 modelos, un tercio supera el límite de deriva: es trabajo que se pudo descartar antes.

## 3. Pregunta de investigación  ·  0:31 (18 s)

Nuestra pregunta es: ¿con qué precisión puede Random Forest estimar las derivas de edificios que no vio en el entrenamiento, y qué ventaja ofrece? Para responderla generamos familias paramétricas, automatizamos la verificación NSR-10 y evaluamos el modelo dejando plantas completas por fuera.

## 4. Cuatro ejes de la beca en un mismo flujo  ·  0:50 (15 s)

El proyecto integra los cuatro ejes de la beca: inteligencia artificial con Random Forest, automatización con el módulo NSR-10 y el bot, simulación con OpenSees y SAP2000, y datos con dos bases trazables.

## 5. Arquitectura: una pregunta, dos rutas de evidencia  ·  1:04 (24 s)

La arquitectura tiene dos rutas de evidencia que no se mezclan, porque las normas difieren: la ruta E.030 con 130 modelos paramétricos en OpenSees y la ruta NSR-10 con el módulo de verificación y los edificios del profesor Rojas Vallejo. Ambas alimentan el mismo método de Random Forest y la interfaz propuesta en Telegram.

## 6. Módulo NSR-10: del JSON al dictamen  ·  1:28 (28 s)

El prototipo es el módulo NSR-10 en Python. Recibe un JSON con el sitio, la geometría, los pesos y los resultados de SAP2000. Primero valida; luego calcula espectro, fuerza horizontal equivalente, derivas de doce combinaciones con torsión accidental, estabilidad P-Delta, irregularidad torsional y R. Al final escribe un reporte y una fila para la base de datos. Todo en menos de un milisegundo.

## 7. Tres pruebas: completa, incompleta y errónea  ·  1:56 (26 s)

Lo probamos con tres casos. Con datos completos, el edificio del curso en Piedemonte A da un cortante de 23 250 kilonewtons y una deriva máxima de 0,99 %: cumple. Si falta un dato, como Fv, se detiene y dice cuál falta. Si un dato está mal, como una altura escrita en centímetros, lo rechaza y explica el rango válido.

## 8. Reproduce el cálculo de referencia del curso  ·  2:21 (18 s)

Validamos contra el cálculo de referencia del curso, hecho con Excel y SAP2000. El prototipo reproduce cortante, fuerzas, derivas, Q, relación torsional y R. La relación torsional de 1,19 queda muy cerca del límite de 1,2: un hallazgo útil para el diseñador.

## 9. Base NSR-10: 18 edificios teóricos + 1 verificado  ·  2:40 (23 s)

Para la ruta NSR-10 armamos una base con 18 edificios que diseñó el profesor Rojas Vallejo con su algoritmo en OpenSees, más el caso del curso. El profesor nos advirtió que varios son teóricos y que las plantas que faltan fallaron en el dimensionamiento. Los usamos para entrenar y comparar, no como diseños.

## 10. Random Forest reduce 39 % el error de deriva  ·  3:03 (21 s)

Evaluamos Random Forest dejando cada planta completa por fuera. Con plantas que nunca vio, su error en la deriva fue de 0,086 puntos en X y 0,101 en Y: un 39 % menos que predecir la media y mejor que la regresión lineal. Cada predicción toma unos 32 milisegundos.

## 11. Útil para priorizar, aún no para certificar  ·  3:24 (18 s)

Pero hay que ser honestos: de siete edificios cerca del límite, el modelo detectó tres y subestimó cuatro. No dio falsas alarmas. Por eso hoy sirve para ordenar alternativas, y la verificación final sigue en el módulo NSR-10 y SAP2000.

## 12. Limitaciones que condicionan los resultados  ·  3:41 (19 s)

Las limitaciones: la base NSR-10 es pequeña y teórica; las métricas del Random Forest en la ruta E.030 están pendientes; no cronometramos el flujo completo en SAP2000, así que no afirmamos un porcentaje de ahorro; y el bot todavía no está conectado al predictor.

## 13. Conclusiones y siguientes pasos  ·  4:00 (27 s)

En conclusión: el módulo NSR-10 reproduce el cálculo de referencia y filtra datos malos; el Random Forest reduce el error un 39 % en plantas que no vio, pero todavía no detecta todos los casos al límite. Los siguientes pasos son evaluar la ruta E.030, ampliar la base con casos verificados, conectar todo al bot y medir el ahorro de tiempo real.

## 14. Equipo y herramientas  ·  4:28 (21 s)

Somos cinco: Lucero en el planteamiento, Alexis en la generación y OpenSees, Nicolás en el módulo NSR-10, Jean Piere en datos, Random Forest y el bot, y Joseph en validación y coordinación. Agradecemos al profesor Thomas Rojas Vallejo por sus datos. Gracias.

