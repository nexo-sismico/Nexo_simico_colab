const fs = require("fs");
const path = require("path");
// Rutas relativas a este archivo: corre igual desde cualquier carpeta y sistema operativo.
const RAIZ = path.resolve(__dirname, "..", "..");
const SAL = path.join(RAIZ, "07 Outputs", "Prototipo NSR-10");
const FIG = (f) => path.join(SAL, "figuras", f);
const {
  Document, Packer, Paragraph, TextRun, Table, TableRow, TableCell, ImageRun, AlignmentType,
  WidthType, ShadingType, BorderStyle, HeadingLevel, Footer, PageNumber, LevelFormat,
} = require("docx");

const N = JSON.parse(fs.readFileSync(path.join(SAL, "numeros.json"), "utf8"));
const f = (x, d = 3) => Number(x).toFixed(d).replace(".", ",");
const met = (o, m, k) => N.met.find((r) => r.Objetivo === o && r.Modelo === m)[k];
// Ruta E.030 (repositorio de Jean Piere): generado por resumen_e030.py
const E = JSON.parse(fs.readFileSync(path.join(RAIZ, "07 Outputs", "E030", "resumen_E030.json"), "utf8"));
const eo = (o, m, k) => E.objetivos[o][m][k];
const pc = (x, d = 3) => f(x * 100, d);   // deriva adimensional → % de la altura de piso
const exRF = E.exced_XoY_RF, exGB = E.exced_XoY_GB;
const FONT = "Arial", SZ = 19; // 9.5 pt
const NAVY = "1F3864";
const EQ = JSON.parse(fs.readFileSync(path.join(__dirname, "equipo.json"), "utf8")).integrantes;   // nombres oficiales

const P = (runs, opt = {}) => new Paragraph({
  spacing: { after: 70, line: 252 }, alignment: AlignmentType.JUSTIFIED, ...opt,
  children: (Array.isArray(runs) ? runs : [runs]).map((r) => typeof r === "string" ? new TextRun({ text: r, font: FONT, size: SZ }) : r),
});
const B = (t) => new TextRun({ text: t, font: FONT, size: SZ, bold: true });
const I = (t) => new TextRun({ text: t, font: FONT, size: SZ, italics: true });
const H = (t) => new Paragraph({ keepNext: true, heading: HeadingLevel.HEADING_1, spacing: { before: 140, after: 60 },
  children: [new TextRun({ text: t, font: FONT, size: 22, bold: true, color: NAVY })] });
const H2 = (t) => new Paragraph({ keepNext: true, heading: HeadingLevel.HEADING_2, spacing: { before: 90, after: 40 },
  children: [new TextRun({ text: t, font: FONT, size: 20, bold: true, color: NAVY })] });
const bullet = (runs) => new Paragraph({ numbering: { reference: "b", level: 0 }, spacing: { after: 30, line: 245 },
  children: (Array.isArray(runs) ? runs : [runs]).map((r) => typeof r === "string" ? new TextRun({ text: r, font: FONT, size: SZ }) : r) });
const cap = (t) => new Paragraph({ alignment: AlignmentType.CENTER, spacing: { after: 90 },
  children: [new TextRun({ text: t, font: FONT, size: 16, italics: true, color: "555555" })] });
const img = (file, w, h) => new Paragraph({ alignment: AlignmentType.CENTER, keepNext: true, spacing: { after: 30 },
  children: [new ImageRun({ type: "png", data: fs.readFileSync(file), transformation: { width: w, height: h } })] });

const border = { style: BorderStyle.SINGLE, size: 4, color: "BFBFBF" };
const borders = { top: border, bottom: border, left: border, right: border };
function table(rows, widths) {
  const total = widths.reduce((a, b) => a + b, 0);
  return new Table({
    width: { size: total, type: WidthType.DXA }, columnWidths: widths,
    rows: rows.map((r, i) => new TableRow({
      children: r.map((c, j) => new TableCell({
        borders, width: { size: widths[j], type: WidthType.DXA },
        shading: i === 0 ? { fill: NAVY, type: ShadingType.CLEAR, color: "auto" } : undefined,
        margins: { top: 40, bottom: 40, left: 80, right: 80 },
        children: [new Paragraph({ alignment: j === 0 ? AlignmentType.LEFT : AlignmentType.CENTER,
          children: [new TextRun({ text: String(c), font: FONT, size: 16, bold: i === 0, color: i === 0 ? "FFFFFF" : "000000" })] })],
      })),
    })),
  });
}

const e030Rows = [["Respuesta (300 familias reservadas)", "Random Forest MAE · R²", "Gradient Boosting MAE · R²", "Media (referencia) MAE · R²"],
  ["Periodo Tx (s)", `${f(eo("Tx_s", "RF", "MAE"))} · ${f(eo("Tx_s", "RF", "R2"))}`, `${f(eo("Tx_s", "GB", "MAE"))} · ${f(eo("Tx_s", "GB", "R2"))}`, `${f(E.objetivos.Tx_s.media_MAE)} · ${f(E.objetivos.Tx_s.media_R2)}`],
  ...["X", "Y"].map((e) => { const o = `deriva_max_${e}`; return [`Deriva máx. ${e} (%)`, `${pc(eo(o, "RF", "MAE"))} · ${f(eo(o, "RF", "R2"))}`, `${pc(eo(o, "GB", "MAE"))} · ${f(eo(o, "GB", "R2"))}`, `${pc(E.objetivos[o].media_MAE)} · ${f(E.objetivos[o].media_R2)}`]; }),
  ["Excedencias detectadas (X o Y)", `${exRF.detectadas} de ${exRF.reales} · ${exRF.falsas_alarmas} falsas alarmas`, `${exGB.detectadas} de ${exGB.reales} · ${exGB.falsas_alarmas} falsas alarmas`, "—"]];

const objs = ["Periodo Tx (s)", "Cortante Vx (kN)", "Deriva máx. X (%)", "Deriva máx. Y (%)"];
const refName = (o) => (o === "Periodo Tx (s)" ? "Ta NSR-10" : "Media (referencia)");
const mlRows = [["Respuesta", "Random Forest MAE · R²", "Regresión lineal MAE · R²", "Referencia MAE · R²"]];
for (const o of objs) {
  const d = o.includes("Vx") ? 0 : 3;
  mlRows.push([o, ...["Random Forest", "Regresión lineal", refName(o)].map((m) => `${f(met(o, m, "MAE"), d)} · ${f(met(o, m, "R2"), 2)}`)]);
}

const children = [
  new Paragraph({ alignment: AlignmentType.CENTER, spacing: { after: 60 }, children: [new TextRun({
    text: "Estimación preliminar de derivas sísmicas en edificios aporticados de concreto reforzado mediante generación paramétrica, verificación normativa automatizada y aprendizaje automático",
    font: FONT, size: 28, bold: true, color: NAVY })] }),
  new Paragraph({ alignment: AlignmentType.CENTER, spacing: { after: 30 }, children: [new TextRun({
    text: EQ.map((p) => p.nombre).join(" · "), font: FONT, size: 19 })] }),
  new Paragraph({ alignment: AlignmentType.CENTER, spacing: { after: 120 }, children: [new TextRun({
    text: "Equipo Nexo Sísmico · Beca AI Talent, 2.ª generación (AECODE) · Modalidad C: investigación académica aplicada · Octubre de 2026",
    font: FONT, size: 16, color: "555555" })] }),
  P([B("Resumen. "), `Comparar alternativas de predimensionamiento sísmico obliga a repetir la preparación de cargas, parámetros normativos y análisis estructurales. Este trabajo plantea un flujo reproducible con dos líneas de evidencia que no se mezclan: ${f(E.base_estructuras, 0).replace(/\B(?=(\d{3})+(?!\d))/g, " ")} edificios de otras tantas familias generados y analizados en OpenSees bajo la norma peruana E.030, y una ruta colombiana NSR-10 formada por un módulo automatizado de verificación y 18 edificios teóricos diseñados con el algoritmo del Prof. T. F. Rojas Vallejo. En ${E.n_prueba} familias E.030 reservadas, Random Forest estimó la deriva máxima con un error absoluto medio de ${pc(eo("deriva_max_X", "RF", "MAE"))} % (X) y ${pc(eo("deriva_max_Y", "RF", "MAE"))} % (Y) de la altura de piso y R² de ${f(eo("deriva_max_X", "RF", "R2"), 2)}, y detectó ${exRF.detectadas} de los ${exRF.reales} edificios que superan el límite de 0,7 %; Gradient Boosting, usado como comparación, alcanzó R² de ${f(eo("deriva_max_X", "GB", "R2"))}. El módulo NSR-10, probado con un caso correcto, uno incompleto y uno erróneo, reproduce exactamente el cálculo de referencia del edificio del curso (cortante basal de ${f(N.vs / 1000, 2)} MN y derivas de ${f(N.dxmax)} % y ${f(N.dymax)} %) y bloquea las entradas defectuosas. Con solo 18 edificios NSR-10 y validación por planta, el error de Random Forest fue de ${f(met("Deriva máx. X (%)", "Random Forest", "MAE"))} % y ${f(met("Deriva máx. Y (%)", "Random Forest", "MAE"))} %, 39 % menor que la referencia, pero detectó solo 3 de 7 edificios cercanos al límite. La precisión depende sobre todo de la cantidad de datos trazables y de las variables físicas: la herramienta sirve para filtrar alternativas dentro del dominio entrenado, no para sustituir la verificación.`]),
  P([B("Palabras clave: "), "deriva sísmica, Random Forest, Gradient Boosting, NSR-10, E.030, OpenSees, automatización, predimensionamiento."]),

  H("1. Introducción"),
  P("En el predimensionamiento de edificios aporticados el ingeniero prueba varias combinaciones de luces, secciones y alturas antes de fijar un modelo definitivo. Cada alternativa exige recalcular cargas, espectro, fuerzas sísmicas y derivas, aunque la decisión que se busca sea solo descartar opciones que no cumplirán. El aprendizaje automático se ha propuesto para estimar respuestas estructurales a partir de variables de diseño y reducir esas iteraciones [5, 6], pero su utilidad depende de que los datos de entrenamiento sean trazables y de que la evaluación se haga sobre configuraciones no vistas."),
  P([B("Pregunta de investigación. "), I("¿Con qué precisión Random Forest puede estimar las derivas máximas de familias de edificios aporticados no utilizadas durante el entrenamiento, y qué ventaja ofrece al comparar alternativas de predimensionamiento?")]),
  P([B("Objetivo general: "), "desarrollar y validar una herramienta predictiva de derivas sustentada en simulaciones documentadas. ", B("Objetivos específicos: "), "(i) generar y analizar familias paramétricas; (ii) automatizar y validar la verificación NSR-10 con datos de SAP2000; (iii) consolidar una base de datos con procedencia explícita; (iv) evaluar Random Forest frente a referencias sencillas con partición por familias; (v) demostrar el prototipo con entradas correctas, incompletas y erróneas."]),
  P([B("Ejes temáticos. "), "Inteligencia artificial y aprendizaje automático (Random Forest y su validación); programación y automatización para AEC (generador, módulo NSR-10, exportaciones); simulación estructural (OpenSees y SAP2000); análisis y visualización de datos (base de datos, métricas y gráficos)."]),

  H("2. Metodología"),
  P("El enfoque es cuantitativo y aplicado, basado en experimentación computacional. La Figura 1 resume la arquitectura: las dos rutas normativas se mantienen separadas porque difieren en espectro, rango de alturas e hipótesis de rigidez, y convergen en un mismo procedimiento de aprendizaje y evaluación."),
  img(FIG("fig_flujo_integrado.png"), 560, 217),
  cap("Figura 1. Flujo integrado de herramientas del proyecto."),
  H2("2.1 Ruta E.030: generación paramétrica"),
  P(`Un generador en Python [11] crea edificios regulares de concreto armado de dos a cinco pisos, dos a cinco vanos por dirección y luces de 3 a 6 m, con f'c de 210 o 280 kgf/cm², zonas sísmicas Z = 0,10 a 0,45, suelos S0 a S3 y usos comunes o importantes. Predimensiona columnas, vigas y losas con criterios de la E.060, metra cargas según la E.020 y construye en OpenSeesPy [3] un pórtico espacial con secciones brutas y diafragma rígido por piso. El análisis modal espectral sigue la E.030 [2]: combinación CQC, regla direccional 100/30, excentricidad accidental de ±5 %, ajuste al cortante mínimo y deriva normativa igual a la elástica por 0,75·R (R = 8), comparada con 0,007. Se generaron ${f(E.base_estructuras, 0).replace(/\B(?=(\d{3})+(?!\d))/g, " ")} estructuras, una por familia y con semilla fija; ${E.base_exceden} (${f(E.base_exceden / E.base_estructuras * 100, 0)} %) superan el límite en alguna dirección. No se reduce la rigidez por agrietamiento ni se incluye P-Delta, simplificaciones que tienden a subestimar periodos y derivas.`),
  H2("2.2 Ruta NSR-10: módulo automatizado de verificación"),
  P([`El módulo ${""}`, I("nexo_nsr10"), ` (Python) recibe un archivo JSON con el sitio, el sistema, la geometría, los pesos por nivel, los periodos de SAP2000 y los desplazamientos de dos esquinas opuestas para 12 combinaciones de deriva (±Fx y ±Fy, sin torsión y con ±Mz accidental). Primero valida que existan todos los campos y que estén en rango; luego aplica la NSR-10 [1]: espectro de la Figura A.2.6-1 con coeficientes de microzonificación de Bogotá [7], periodo aproximado y límite Cu·Ta (A.4.2), cortante basal y distribución vertical (A.4.3), torsión accidental del 5 % (A.3.6.7), derivas Δ = √(Δx² + Δy²) frente al 1,0 % de la altura de piso (A.6), índice de estabilidad Q (A.6.2.3) y coeficiente R con la revisión de irregularidad torsional (A.3.3). El caso de calibración es el edificio de oficinas de cinco pisos del curso de Diseño Estructural, grupo 1 (Bogotá, microzona Piedemonte A, Aa = 0,15, Av = 0,20, Fa = 1,65, Fv = 2,0).`]),
  H2("2.3 Aprendizaje en la ruta E.030"),
  P(`Las estructuras se dividieron por familia en ${E.n_desarrollo} de desarrollo y ${E.n_prueba} reservadas para una prueba final usada una sola vez. Las 107 entradas describen geometría, secciones, cargas, masas y sitio, todas conocidas antes del análisis. Random Forest [4] (scikit-learn [9], 250 árboles, hoja mínima de 1) recibe además variables físicas auxiliares —un periodo aproximado a partir de la rigidez lateral de los pisos y la ordenada espectral de la E.030— y aprende el cociente entre la respuesta de OpenSees y esa estimación. Como comparación se usaron Gradient Boosting [10], el modelo que el repositorio del equipo selecciona por validación cruzada por familias, y la media del entrenamiento. Se reportan MAE, RMSE, R² y la detección de edificios que superan 0,007.`),
  H2("2.4 Base de datos NSR-10 y aprendizaje"),
  P("La base une, con un esquema común que registra fuente, norma, programa y estado del dato, 18 edificios diseñados con el algoritmo en OpenSees del Prof. T. F. Rojas Vallejo [8] (DES, suelo lacustre 200 de Bogotá, estructuras regulares) y los casos validados por el módulo. Las entradas de esos edificios (10 plantas regulares con relación de aspecto ≤ 1,5, dos alturas por planta entre 4 y 10 pisos, cargas del Título B y grupo de uso) fueron definidas por el equipo. Según el profesor, estos resultados son de carácter teórico: algunas plantas y luces no se resolverían con pórticos resistentes a momento en la práctica, y las dos configuraciones de la planta P9 se excluyeron por un error de dimensionamiento en el algoritmo."),
  P(`Se entrenó Random Forest [4] (scikit-learn [9], 500 árboles, hoja mínima de 2, semilla 42) con 13 variables conocidas antes del análisis: altura, pisos, dimensiones y área de planta, número de columnas, luces máxima y media, cargas, coeficiente de importancia, esbeltez y un peso aproximado (área × pisos × carga muerta). Se comparó con una regresión lineal y con una referencia sencilla (Ta = 0,047·H^0,9 para el periodo y la media del entrenamiento para las demás respuestas). La validación dejó fuera una planta completa en cada uno de los 9 pliegues, de modo que las dos alturas de una planta nunca se reparten entre entrenamiento y prueba. Se reportan MAE, RMSE, R², el error porcentual medio y la detección de edificios con deriva ≥ 0,90 %, umbral práctico de revisión.`),

  H("3. Resultados"),
  H2("3.1 Prototipo NSR-10: tres pruebas"),
  P(`Con la entrada completa, el módulo entregó Ta = ${f(N.Ta)} s, Cu·Ta = ${f(N.CuTa)} s, Sa = ${f(N.Sa, 4)} g en la meseta del espectro, peso sísmico de ${f(N.Wt / 1000, 2)} MN, cortante basal de ${f(N.vs / 1000, 2)} MN y derivas máximas de ${f(N.dxmax)} % (X) y ${f(N.dymax)} % (Y), todas dentro del 1,0 % (Figura 2). Q máximo fue ${f(N.Q, 4)} (no requiere P-Delta) y la relación Δmáx/Δprom = ${f(N.tor)} quedó por debajo del 1,2 de irregularidad torsional, por lo que R = ${f(N.R, 1)}. Estos valores coinciden con el cálculo de referencia hecho con SAP2000 y hoja de cálculo. Al eliminar Fv, el módulo se detuvo e identificó el campo faltante; al introducir una altura libre de 350 (en centímetros), rechazó el valor e indicó el rango válido. Ninguna de las dos entradas defectuosas produjo resultados. Cada ejecución tardó menos de 1 ms.`),
  img(FIG("fig_derivas_caso_curso.png"), 330, 204),
  cap("Figura 2. Derivas por nivel del edificio del curso: envolvente de 12 combinaciones en las esquinas E5 y A1."),
  H2("3.2 Random Forest en familias E.030 reservadas"),
  P(`La Tabla 1 resume la prueba en las ${E.n_prueba} familias reservadas. Random Forest estimó la deriva máxima con un MAE de ${pc(eo("deriva_max_X", "RF", "MAE"))} % (X) y ${pc(eo("deriva_max_Y", "RF", "MAE"))} % (Y) y R² de ${f(eo("deriva_max_X", "RF", "R2"))} y ${f(eo("deriva_max_Y", "RF", "R2"))}, frente a un R² nulo al predecir la media, y el periodo con R² de ${f(eo("Tx_s", "RF", "R2"))}. De los ${exRF.reales} edificios de prueba que superan 0,007 en alguna dirección, detectó ${exRF.detectadas} con ${exRF.falsas_alarmas} falsas alarmas; los ${exRF.no_detectadas} no detectados tienen derivas reales entre 0,70 % y 0,76 %, justo por encima del límite (Figura 3). Gradient Boosting redujo el MAE de la deriva a ${pc(eo("deriva_max_X", "GB", "MAE"))} % y detectó ${exGB.detectadas} casos: una mejora modesta que indica que el aporte principal proviene de los datos y de las variables físicas más que del algoritmo. Entrenar cada modelo tomó unos ${f(E.objetivos.deriva_max_X.t_entrenamiento_RF_s, 0)} s y predecir un edificio, menos de 0,1 s.`),
  table(e030Rows, [2900, 2100, 2100, 2100]),
  cap("Tabla 1. Prueba única en 300 familias E.030 no vistas (1 200 de desarrollo). Derivas en % de la altura de piso."),
  img(path.join(RAIZ, "07 Outputs", "E030", "fig_e030_calculado_vs_predicho.png"), 520, 231),
  cap("Figura 3. Deriva calculada (OpenSees) frente a predicha por Random Forest en 300 familias E.030 reservadas."),
  H2("3.3 Random Forest sobre la base NSR-10"),
  P("La Tabla 2 resume el desempeño en plantas no vistas. Para las derivas, Random Forest redujo el error absoluto medio en 39 % (X) y 39 % (Y) respecto de la referencia y superó a la regresión lineal. Para el periodo y el cortante basal, la regresión lineal sobre variables físicas fue igual o ligeramente mejor, lo que es esperable con 18 casos y relaciones casi proporcionales a la altura y al peso. Ambos modelos mejoraron la fórmula Ta de la norma (error medio de 13,2 % frente a 9,2 % y 7,2 %). Las variables más influyentes en la deriva fueron el número de pisos, la altura y la esbeltez."),
  table(mlRows, [2300, 2300, 2300, 2300]),
  cap("Tabla 2. Error absoluto medio (MAE) y R² con validación dejando una planta fuera (18 edificios, 9 plantas). Derivas en % de la altura de piso."),
  img(FIG("fig_calculado_vs_predicho.png"), 560, 248),
  cap("Figura 4. Deriva calculada (OpenSees, profesor) frente a predicha por Random Forest en plantas NSR-10 no vistas."),
  P(`De los 7 edificios con deriva ≥ 0,90 %, el modelo identificó 3 y no generó falsas alarmas; los 4 restantes fueron subestimados (Figura 4). La predicción de un edificio tomó ${f(N.ml.t_prediccion_ms, 0)} ms y el entrenamiento de cada modelo unos 0,4 s.`),

  H("4. Discusión"),
  P(`Los resultados responden la pregunta en dos escalas. Con una base amplia y trazable (E.030), Random Forest estima la deriva de familias no vistas con un error de unas cuatro centésimas de punto porcentual y detecta el ${f(exRF.detectadas / exRF.reales * 100, 0)} % de las excedencias, precisión suficiente para descartar alternativas antes de modelarlas; los casos no detectados están a menos de 0,06 puntos del límite, por lo que la verificación final sigue siendo necesaria en esa franja. Con 18 edificios teóricos (NSR-10), el mismo método solo ordena alternativas: el error es de una décima de punto y la mayoría de los casos exigentes se subestiman. La diferencia se explica por el tamaño de la muestra, el carácter teórico de varios diseños del profesor y las variables físicas usadas en la ruta E.030. Que Gradient Boosting mejore poco a Random Forest indica que la elección del algoritmo es secundaria frente a la calidad y cantidad de los datos.`),
  P("El módulo NSR-10 aporta lo que el predictor no puede dar por sí solo: respuestas de referencia trazables, validación de entradas y registros para ampliar la base colombiana hacia un tamaño comparable al de la E.030. Las dos rutas no se mezclan porque responden a normas, unidades, rangos de altura e hipótesis distintas; el modelo E.030 solo es válido dentro de su dominio (dos a cinco pisos) y rechaza entradas fuera de él. El ahorro de tiempo se manifiesta en la predicción (fracciones de segundo por alternativa frente a un análisis completo), pero no se cronometró el procedimiento manual de modelación en SAP2000, por lo que no se reporta un porcentaje de ahorro."),
  P("El trabajo se organizó en cinco frentes con responsables definidos (planteamiento, generación y OpenSees, módulo NSR-10, datos y Random Forest, validación y coordinación), con un repositorio común y un registro de decisiones que documenta las iteraciones, entre ellas el cambio de modalidad a investigación aplicada y la separación de las dos rutas normativas."),

  H("5. Conclusiones"),
  bullet(["El módulo NSR-10 reproduce el cálculo de referencia del edificio del curso (Vs, fuerzas, derivas de 12 combinaciones, Q y R) y rechaza entradas incompletas o erróneas antes de calcular."]),
  bullet([`En ${E.n_prueba} familias E.030 no vistas, Random Forest estimó la deriva máxima con MAE de ${pc(eo("deriva_max_X", "RF", "MAE"))} % y R² de ${f(eo("deriva_max_X", "RF", "R2"), 2)}, y detectó ${exRF.detectadas} de ${exRF.reales} excedencias; Gradient Boosting, como comparación, llegó a R² de ${f(eo("deriva_max_X", "GB", "R2"))}.`]),
  bullet([`Con 18 casos NSR-10 teóricos y validación por planta, Random Forest redujo el error de deriva un 39 % frente a la referencia (MAE de ${f(met("Deriva máx. X (%)", "Random Forest", "MAE"))} % y ${f(met("Deriva máx. Y (%)", "Random Forest", "MAE"))} %), pero detectó 3 de 7 edificios cercanos al límite: sirve para priorizar, no para certificar.`]),
  bullet(["La precisión depende más de la cantidad y trazabilidad de los datos que del algoritmo. Siguientes pasos: ampliar la base NSR-10 con casos verificados por el módulo, conectar módulo y predictor al bot de Telegram y cronometrar el flujo completo para cuantificar el ahorro."]),

  H("Referencias"),
  ...[
    "[1] Asociación Colombiana de Ingeniería Sísmica. (2010). Reglamento Colombiano de Construcción Sismo Resistente NSR-10, Títulos A, B y C. Bogotá.",
    "[2] Ministerio de Vivienda, Construcción y Saneamiento. (2026). Norma Técnica E.030 Diseño Sismorresistente (RM 183-2026-VIVIENDA). Lima.",
    "[3] McKenna, F., Scott, M. H., & Fenves, G. L. (2010). Nonlinear finite-element analysis software architecture using object composition. Journal of Computing in Civil Engineering, 24(1), 95–107.",
    "[4] Breiman, L. (2001). Random forests. Machine Learning, 45, 5–32.",
    "[5] Sun, H., Burton, H. V., & Huang, H. (2021). Machine learning applications for building structural design and performance assessment: State-of-the-art review. Journal of Building Engineering, 33, 101816.",
    "[6] Xie, Y., Ebad Sichani, M., Padgett, J. E., & DesRoches, R. (2020). The promises and challenges of machine learning in earthquake engineering. Earthquake Spectra, 36(4), 1769–1801.",
    "[7] Alcaldía Mayor de Bogotá. (2010). Decreto 523 de 2010: microzonificación sísmica de Bogotá D.C.",
    "[8] Rojas Vallejo, T. F. (2026). Algoritmo de diseño sísmico de pórticos de concreto reforzado en OpenSees [Código no publicado]. Universidad Nacional de Colombia.",
    "[9] Pedregosa, F., et al. (2011). Scikit-learn: Machine learning in Python. Journal of Machine Learning Research, 12, 2825–2830.",
    "[10] Friedman, J. H. (2001). Greedy function approximation: A gradient boosting machine. The Annals of Statistics, 29(5), 1189–1232.",
    "[11] Equipo Nexo Sísmico. (2026). Pórticos de concreto armado: generador, análisis E.030 y modelos de aprendizaje [Repositorio de código]. https://github.com/PieroVQ/ProyectoGH",
  ].map((t) => new Paragraph({ spacing: { after: 30 }, children: [new TextRun({ text: t, font: FONT, size: 16 })] })),
];

const doc = new Document({
  creator: "Equipo Nexo Sísmico", title: "Informe técnico Nexo Sísmico",
  numbering: { config: [{ reference: "b", levels: [{ level: 0, format: LevelFormat.BULLET, text: "•", alignment: AlignmentType.LEFT,
    style: { paragraph: { indent: { left: 360, hanging: 200 } } } }] }] },
  sections: [{
    properties: { page: { size: { width: 12240, height: 15840 }, margin: { top: 900, bottom: 900, left: 1000, right: 1000 } } },
    footers: { default: new Footer({ children: [new Paragraph({ alignment: AlignmentType.CENTER, children: [
      new TextRun({ text: "Nexo Sísmico · Informe técnico · pág. ", font: FONT, size: 14, color: "777777" }),
      new TextRun({ children: [PageNumber.CURRENT], font: FONT, size: 14, color: "777777" })] })] }) },
    children,
  }],
});
Packer.toBuffer(doc).then((b) => { const out = path.join(RAIZ, "04 Entregables", "Informe", "Informe_tecnico_Nexo_Sismico.docx");
  fs.writeFileSync(out, b); console.log("ok →", out, "(PDF: abrir en Word → Guardar como PDF)"); });
