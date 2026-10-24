# Guion del video ejecutivo (duración 4:36)

Narración por diapositiva. Para grabar la voz: reproducir el MP4 y leer cada subtítulo cuando aparece, o grabar el audio aparte y montarlo sobre el MP4 (el .srt tiene los tiempos).

## 1. Nexo Sísmico  ·  0:00 (15 s)

Somos Nexo Sísmico. Nuestro proyecto es una investigación aplicada: estimar de forma preliminar las derivas sísmicas de edificios aporticados de concreto, para comparar alternativas de predimensionamiento sin rehacer un modelo completo cada vez.

## 2. Cada alternativa cuesta un modelo completo  ·  0:14 (18 s)

El problema: en el predimensionamiento cada alternativa obliga a repetir espectro, pesos, fuerzas, modelo y revisión de derivas. En nuestra base paramétrica de 1 500 edificios, el 45 % supera el límite de deriva: es trabajo que se pudo descartar antes.

## 3. Pregunta de investigación  ·  0:32 (16 s)

Nuestra pregunta: ¿con qué precisión puede Random Forest estimar las derivas de edificios que no vio al entrenar, y qué ventaja ofrece? Para responderla generamos familias paramétricas, automatizamos la verificación NSR-10 y evaluamos solo con edificios nuevos.

## 4. Cuatro ejes de la beca en un mismo flujo  ·  0:48 (15 s)

El proyecto integra los cuatro ejes de la beca: inteligencia artificial con Random Forest, automatización con el módulo NSR-10 y el bot, simulación con OpenSees y SAP2000, y datos con dos bases trazables.

## 5. Arquitectura: una pregunta, dos rutas de evidencia  ·  1:03 (21 s)

La arquitectura tiene dos rutas que no se mezclan porque las normas difieren: la ruta E.030, con 1 500 edificios paramétricos en OpenSees, y la ruta NSR-10, con el módulo de verificación y los edificios del profesor Rojas Vallejo. Ambas alimentan el mismo método de evaluación.

## 6. Módulo NSR-10: del JSON al dictamen  ·  1:24 (21 s)

El prototipo es el módulo NSR-10 en Python. Recibe un JSON con el sitio, la geometría, los pesos y los resultados de SAP2000; primero valida y luego calcula espectro, fuerza horizontal equivalente, derivas de doce combinaciones con torsión accidental, estabilidad y R. Todo en menos de un milisegundo.

## 7. Tres pruebas: completa, incompleta y errónea  ·  1:44 (21 s)

Lo probamos con tres casos. Con datos completos, el edificio del curso da 23 250 kilonewtons de cortante y 0,99 % de deriva: cumple. Si falta un dato, como Fv, se detiene y dice cuál falta. Si un dato está mal, como una altura en centímetros, lo rechaza.

## 8. Reproduce el cálculo de referencia del curso  ·  2:05 (18 s)

Validamos contra el cálculo de referencia del curso, hecho con Excel y SAP2000. El prototipo reproduce cortante, fuerzas, derivas, Q, relación torsional y R. La relación torsional de 1,19 queda muy cerca del límite de 1,2: un hallazgo útil para el diseñador.

## 9. E.030: Random Forest acierta la deriva con R² 0,99  ·  2:24 (33 s)

Esta es la respuesta principal. Generamos y analizamos 1 500 edificios en OpenSees, entrenamos Random Forest con 1 200 y lo probamos una sola vez con 300 familias que nunca vio. Su error medio en la deriva fue de 0,04 puntos, con R² de 0,99, y detectó 137 de 146 excedencias; las que se le escapan están justo en el límite. Gradient Boosting, como comparación, mejora poco: lo que manda son los datos.

## 10. Base NSR-10: 18 edificios teóricos + 1 verificado  ·  2:56 (16 s)

Para la ruta colombiana usamos 18 edificios que diseñó el profesor Rojas Vallejo con su algoritmo en OpenSees, más el caso del curso. Varios son teóricos, así que sirven para entrenar y comparar, no como diseños.

## 11. NSR-10: con 18 edificios, −39 % de error de deriva  ·  3:12 (14 s)

Con plantas NSR-10 que nunca vio, el error de deriva de Random Forest fue de 0,086 puntos en X y 0,101 en Y: un 39 % menos que predecir la media.

## 12. NSR-10: con pocos datos, útil solo para priorizar  ·  3:26 (18 s)

Con 18 edificios, el modelo detectó tres de siete casos cerca del límite y no dio falsas alarmas. Con tan pocos datos solo sirve para ordenar alternativas; por eso el siguiente paso es ampliar la base colombiana con casos verificados.

## 13. Limitaciones que condicionan los resultados  ·  3:43 (21 s)

Las limitaciones: la base NSR-10 es pequeña y teórica; el modelo E.030 solo vale de 2 a 5 pisos y con sus hipótesis de rigidez; no cronometramos el flujo completo en SAP2000, así que no afirmamos un porcentaje de ahorro; y el bot todavía no está conectado al predictor.

## 14. Conclusiones y siguientes pasos  ·  4:05 (23 s)

En conclusión: el módulo NSR-10 reproduce el cálculo de referencia y filtra datos malos; con 1 500 edificios, Random Forest estima la deriva de familias nuevas con R² de 0,99, y con 18 solo sirve para priorizar. Siguientes pasos: ampliar la base NSR-10, conectar el bot y medir el ahorro de tiempo.

## 15. Equipo y herramientas  ·  4:28 (8 s)

Somos Lucero, Alexis, Nicolás, Jean Piere y Joseph. Agradecemos al profesor Thomas Rojas Vallejo por sus datos. Gracias.

