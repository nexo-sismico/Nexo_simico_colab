// Presentación Nexo Sísmico — pptxgenjs, deck estructurado
const pptxgen = require("pptxgenjs");
const React = require("react");
const ReactDOMServer = require("react-dom/server");
const sharp = require("sharp");
const fa = require("react-icons/fa");
const path = require("path");
// Rutas relativas a este archivo: corre igual desde cualquier carpeta y sistema operativo.
const RAIZ = path.resolve(__dirname, "..", "..");
const SAL = path.join(RAIZ, "07 Outputs", "Prototipo NSR-10");
const FIG = (f) => path.join(SAL, "figuras", f);
// apply_theme.js solo existía en el entorno donde se generó el deck; sin él, el deck usa los colores definidos aquí.
let applyTheme = async () => {};
try { ({ applyTheme } = require(process.env.APPLY_THEME || "/mnt/skills/public/pptx/scripts/apply_theme.js")); } catch (e) {}
const N = require(path.join(SAL, "numeros.json"));
const OUT = path.join(RAIZ, "04 Entregables", "Presentacion", "Presentacion_Nexo_Sismico.pptx");

const THEME = {
  name: "Nexo Sismico",
  headFontFace: "Cambria",
  bodyFontFace: "Calibri",
  colors: {
    dk1: "1E2A33", lt1: "FFFFFF", dk2: "3A4A57", lt2: "EDF0F3",
    accent1: "E4572E", accent2: "5B7083", accent3: "2E8B57", accent4: "C0392B",
    accent5: "F2A541", accent6: "8FA3B5", hlink: "E4572E", folHlink: "5B7083",
  },
};
const HEX = THEME.colors;

const pres = new pptxgen();
pres.layout = "LAYOUT_16x9"; // 10 x 5.625
pres.title = "Nexo Sísmico — Estimación preliminar de derivas";
pres.author = "Equipo Nexo Sísmico";
pres.theme = { headFontFace: THEME.headFontFace, bodyFontFace: THEME.bodyFontFace };
const C = pres.SchemeColor;

async function icon(Comp, color = "#FFFFFF", size = 256) {
  const svg = ReactDOMServer.renderToStaticMarkup(React.createElement(Comp, { color, size: String(size) }));
  const buf = await sharp(Buffer.from(svg)).png().toBuffer();
  return "image/png;base64," + buf.toString("base64");
}

// ---------- Layouts ----------
const FOOT = { text: "Nexo Sísmico · Beca AI Talent (AECODE) · 2026", options: { x: 0.5, y: 5.25, w: 6, h: 0.25, fontSize: 9, color: C.accent2 } };
pres.defineSlideMaster({
  title: "TITULO", background: { color: HEX.dk1 },
  objects: [
    { placeholder: { options: { name: "title", type: "title", x: 0.6, y: 1.35, w: 8.8, h: 1.0, fontSize: 44, bold: true, color: C.background1, fontFace: THEME.headFontFace, valign: "bottom", align: "left", margin: 0 }, text: "" } },
    { placeholder: { options: { name: "body", type: "body", x: 0.6, y: 2.45, w: 8.0, h: 1.0, fontSize: 18, color: C.accent6, valign: "top", align: "left", margin: 0 }, text: "" } },
  ],
});
pres.defineSlideMaster({
  title: "CONTENIDO", background: { color: HEX.lt1 },
  objects: [
    { placeholder: { options: { name: "title", type: "title", x: 0.5, y: 0.3, w: 9.0, h: 0.75, fontSize: 28, bold: true, color: C.text1, fontFace: THEME.headFontFace, valign: "middle", align: "left", margin: 0 }, text: "" } },
    { text: FOOT },
  ],
  slideNumber: { x: 9.0, y: 5.22, w: 0.5, h: 0.3, fontSize: 9, color: C.accent2, align: "right" },
});
pres.defineSlideMaster({
  title: "OSCURO", background: { color: HEX.dk1 },
  objects: [
    { placeholder: { options: { name: "title", type: "title", x: 0.5, y: 0.3, w: 9.0, h: 0.75, fontSize: 28, bold: true, color: C.background1, fontFace: THEME.headFontFace, valign: "middle", align: "left", margin: 0 }, text: "" } },
  ],
  slideNumber: { x: 9.0, y: 5.22, w: 0.5, h: 0.3, fontSize: 9, color: C.accent6, align: "right" },
});

const T = (s, txt, o) => s.addText(txt, Object.assign({ isTextBox: true, fontSize: 14, color: C.text1, valign: "top", margin: 0 }, o));
function card(s, x, y, w, h, fill = C.background2, name = "card") {
  s.addShape(pres.shapes.ROUNDED_RECTANGLE, { x, y, w, h, rectRadius: 0.08, fill: { color: fill }, line: { color: fill }, objectName: name });
}
async function badge(s, x, y, Comp, d = 0.5, fill = C.accent1) {
  s.addShape(pres.shapes.OVAL, { x, y, w: d, h: d, fill: { color: fill }, line: { color: fill }, objectName: "badge" });
  s.addImage({ data: await icon(Comp), x: x + d * 0.22, y: y + d * 0.22, w: d * 0.56, h: d * 0.56, objectName: "icono" });
}
function num(s, x, y, n, d = 0.42, fill = C.accent1) {
  s.addShape(pres.shapes.OVAL, { x, y, w: d, h: d, fill: { color: fill }, line: { color: fill }, objectName: "numero" });
  T(s, String(n), { x, y, w: d, h: d, fontSize: 14, bold: true, color: C.background1, align: "center", valign: "middle" });
}
const f2 = (v, d = 2) => v.toFixed(d).replace(".", ",");
const f0 = (v) => String(Math.round(v)).replace(/\B(?=(\d{3})+(?!\d))/g, " ");

(async () => {
  // 1 ---------------------------------------------------------------- Portada
  pres.addSection({ title: "Apertura" });
  let s = pres.addSlide({ masterName: "TITULO", sectionTitle: "Apertura" });
  T(s, "INVESTIGACIÓN ACADÉMICA APLICADA · BECA AI TALENT (AECODE)", { x: 0.6, y: 0.7, w: 8.5, h: 0.35, fontSize: 12, bold: true, color: C.accent1, charSpacing: 2 });
  s.addText("Nexo Sísmico", { placeholder: "title" });
  s.addText("Estimación preliminar de derivas sísmicas en edificios aporticados de concreto armado: verificación NSR-10 automatizada y aprendizaje automático", { placeholder: "body" });
  T(s, "Lucero · Alexis · Nicolás Infante · Jean Piere · Joseph", { x: 0.6, y: 4.35, w: 8, h: 0.3, fontSize: 14, color: C.background1 });
  T(s, "Demo Day · 24 de octubre de 2026", { x: 0.6, y: 4.7, w: 8, h: 0.3, fontSize: 12, color: C.accent6 });
  await badge(s, 8.6, 4.3, fa.FaBuilding, 0.8);
  s.addNotes("Somos Nexo Sísmico. Nuestro proyecto es una investigación aplicada: estimar de forma preliminar las derivas sísmicas de edificios aporticados de concreto, para comparar alternativas de predimensionamiento sin rehacer un modelo completo cada vez.");

  // 2 ---------------------------------------------------------------- Problema
  pres.addSection({ title: "Problema y pregunta" });
  s = pres.addSlide({ masterName: "CONTENIDO", sectionTitle: "Problema y pregunta" });
  s.addText("Cada alternativa cuesta un modelo completo", { placeholder: "title" });
  T(s, [
    { text: "Para saber si una configuración de pórticos cumple la deriva, el ingeniero repite el ciclo completo:", options: { breakLine: true } },
    { text: "espectro, pesos, fuerzas, modelo en SAP2000, derivas y revisión normativa.", options: { breakLine: true } },
    { text: " ", options: { breakLine: true, fontSize: 8 } },
    { text: "Muchas alternativas no cumplen y se descartan después de todo ese trabajo.", options: { bold: true } },
  ], { x: 0.5, y: 1.35, w: 4.4, h: 2.4, fontSize: 16, paraSpaceAfter: 4 });
  const stats = [
    ["130", "modelos E.030 generados en 49 familias"],
    ["33 %", "superan el límite de deriva (43 de 130)"],
    ["1,0 %", "de hpi: límite de deriva NSR-10 (A.6.4)"],
  ];
  stats.forEach(([v, l], i) => {
    const y = 1.3 + i * 1.25;
    card(s, 5.3, y, 4.2, 1.05, C.background2, "stat");
    T(s, v, { x: 5.5, y: y + 0.12, w: 1.6, h: 0.8, fontSize: 36, bold: true, color: C.accent1, fontFace: THEME.headFontFace, valign: "middle" });
    T(s, l, { x: 7.15, y: y + 0.12, w: 2.2, h: 0.8, fontSize: 13, color: C.text2, valign: "middle" });
  });
  s.addNotes("El problema: en el predimensionamiento cada alternativa obliga a repetir espectro, pesos, fuerzas, modelo y revisión de derivas. En nuestra base paramétrica de 130 modelos, un tercio supera el límite de deriva: es trabajo que se pudo descartar antes.");

  // 3 ---------------------------------------------------------------- Pregunta
  s = pres.addSlide({ masterName: "CONTENIDO", sectionTitle: "Problema y pregunta" });
  s.addText("Pregunta de investigación", { placeholder: "title" });
  card(s, 0.5, 1.25, 9.0, 1.25, C.text1, "pregunta");
  T(s, "¿Con qué precisión puede Random Forest estimar las derivas máximas de familias de edificios aporticados no utilizadas en el entrenamiento, y qué ventaja ofrece al comparar alternativas de predimensionamiento?",
    { x: 0.8, y: 1.35, w: 8.4, h: 1.05, fontSize: 17, italic: true, color: C.background1, valign: "middle", fontFace: THEME.headFontFace });
  const objs = [
    [fa.FaCubes, "Generar", "familias paramétricas y analizarlas en OpenSees (E.030)"],
    [fa.FaCogs, "Automatizar", "la verificación NSR-10 con datos de SAP2000"],
    [fa.FaChartLine, "Evaluar", "Random Forest dejando plantas completas fuera"],
  ];
  for (let i = 0; i < 3; i++) {
    const x = 0.5 + i * 3.1;
    card(s, x, 2.85, 2.8, 2.05, C.background2, "objetivo");
    await badge(s, x + 0.25, 3.05, objs[i][0], 0.55);
    T(s, objs[i][1], { x: x + 0.95, y: 3.1, w: 1.7, h: 0.45, fontSize: 18, bold: true, color: C.text1, valign: "middle" });
    T(s, objs[i][2], { x: x + 0.25, y: 3.8, w: 2.35, h: 0.95, fontSize: 14, color: C.text2 });
  }
  s.addNotes("Nuestra pregunta es: ¿con qué precisión puede Random Forest estimar las derivas de edificios que no vio en el entrenamiento, y qué ventaja ofrece? Para responderla generamos familias paramétricas, automatizamos la verificación NSR-10 y evaluamos el modelo dejando plantas completas por fuera.");

  // 4 ---------------------------------------------------------------- Ejes
  pres.addSection({ title: "Solución" });
  s = pres.addSlide({ masterName: "CONTENIDO", sectionTitle: "Solución" });
  s.addText("Cuatro ejes de la beca en un mismo flujo", { placeholder: "title" });
  const ejes = [
    [fa.FaBrain, "Inteligencia artificial", "Random Forest con validación por planta; comparado con regresión lineal y referencias"],
    [fa.FaRobot, "Automatización", "Módulo NSR-10 en Python; bot de Telegram en n8n como interfaz propuesta"],
    [fa.FaProjectDiagram, "Simulación", "OpenSees para la base E.030; SAP2000 y algoritmo OpenSees del profesor para NSR-10"],
    [fa.FaDatabase, "Datos", "Base E.030 (130 modelos) y base NSR-10 (18 + 1 casos) con trazabilidad del origen"],
  ];
  for (let i = 0; i < 4; i++) {
    const x = 0.5 + (i % 2) * 4.6, y = 1.3 + Math.floor(i / 2) * 1.85;
    card(s, x, y, 4.4, 1.6, C.background2, "eje");
    await badge(s, x + 0.25, y + 0.3, ejes[i][0], 0.65);
    T(s, ejes[i][1], { x: x + 1.15, y: y + 0.22, w: 3.1, h: 0.4, fontSize: 17, bold: true });
    T(s, ejes[i][2], { x: x + 1.15, y: y + 0.65, w: 3.1, h: 0.85, fontSize: 13, color: C.text2 });
  }
  s.addNotes("El proyecto integra los cuatro ejes de la beca: inteligencia artificial con Random Forest, automatización con el módulo NSR-10 y el bot, simulación con OpenSees y SAP2000, y datos con dos bases trazables.");

  // 5 ---------------------------------------------------------------- Arquitectura
  s = pres.addSlide({ masterName: "CONTENIDO", sectionTitle: "Solución" });
  s.addText("Arquitectura: una pregunta, dos rutas de evidencia", { placeholder: "title" });
  s.addImage({ path: FIG("fig_flujo_integrado.png"), x: 0.5, y: 1.15, w: 9.0, h: 3.48, objectName: "flujo" });
  T(s, "Las rutas no se mezclan: E.030 (Perú) y NSR-10 (Colombia) difieren en espectro, límite de deriva e hipótesis. Comparten el método de aprendizaje y evaluación.",
    { x: 0.5, y: 4.68, w: 9.0, h: 0.45, fontSize: 12, color: C.text2, italic: true });
  s.addNotes("La arquitectura tiene dos rutas de evidencia que no se mezclan, porque las normas difieren: la ruta E.030 con 130 modelos paramétricos en OpenSees y la ruta NSR-10 con el módulo de verificación y los edificios del profesor Rojas Vallejo. Ambas alimentan el mismo método de Random Forest y la interfaz propuesta en Telegram.");

  // 6 ---------------------------------------------------------------- Módulo NSR-10
  pres.addSection({ title: "Prototipo" });
  s = pres.addSlide({ masterName: "CONTENIDO", sectionTitle: "Prototipo" });
  s.addText("Módulo NSR-10: del JSON al dictamen", { placeholder: "title" });
  const pasos = [
    ["Validar", "campos, rangos y 12 combinaciones"],
    ["Espectro", "Sa(T), Ta, Cu·Ta (A.2, A.4.2)"],
    ["FHE", "Vs, k, fuerzas por piso (A.4.3)"],
    ["Derivas", "12 combinaciones + torsión accidental 5 %"],
    ["Estabilidad", "Q (P-Δ), torsión 1aP, R (A.3.3)"],
    ["Registro", "reporte y fila para la base de datos"],
  ];
  pasos.forEach(([t, d], i) => {
    const x = 0.5 + i * 1.53;
    card(s, x, 1.55, 1.38, 2.3, i === 0 ? HEX.lt2 : C.background2, "paso");
    num(s, x + 0.48, 1.72, i + 1);
    T(s, t, { x: x + 0.08, y: 2.3, w: 1.22, h: 0.4, fontSize: 15, bold: true, align: "center" });
    T(s, d, { x: x + 0.1, y: 2.75, w: 1.18, h: 1.0, fontSize: 12, color: C.text2, align: "center" });
  });
  T(s, [
    { text: "Entrada: ", options: { bold: true } },
    { text: "sitio (Aa, Av, Fa, Fv, TL), grupo de uso, R0, geometría, pesos por piso, periodos de SAP2000 y desplazamientos en dos esquinas opuestas. Tiempo de cálculo: menos de 1 ms por caso.", options: {} },
  ], { x: 0.5, y: 4.15, w: 9.0, h: 0.6, fontSize: 13, color: C.text2 });
  s.addNotes("El prototipo es el módulo NSR-10 en Python. Recibe un JSON con el sitio, la geometría, los pesos y los resultados de SAP2000. Primero valida; luego calcula espectro, fuerza horizontal equivalente, derivas de doce combinaciones con torsión accidental, estabilidad P-Delta, irregularidad torsional y R. Al final escribe un reporte y una fila para la base de datos. Todo en menos de un milisegundo.");

  // 7 ---------------------------------------------------------------- 3 pruebas
  s = pres.addSlide({ masterName: "CONTENIDO", sectionTitle: "Prototipo" });
  s.addText("Tres pruebas: completa, incompleta y errónea", { placeholder: "title" });
  const casos = [
    [fa.FaCheck, C.accent3, "1 · Datos completos", "Edificio del curso, grupo 1, Piedemonte A (Bogotá)", `Vs = ${f0(N.vs)} kN\nDeriva máx. ${f2(N.dymax, 3)} % ≤ 1,0 %\nCUMPLE · ${String(N.ms[0]).replace(".", ",")} ms`],
    [fa.FaQuestion, C.accent5, "2 · Falta un dato", "Se eliminó el coeficiente Fv", "Se detiene antes de calcular\n«FALTA: sitio.Fv»"],
    [fa.FaTimes, C.accent4, "3 · Dato erróneo", "Altura libre del piso 1 = 350", "Rechazado: fuera de [1,8; 6,0] m\n«¿está en centímetros?»"],
  ];
  for (let i = 0; i < 3; i++) {
    const x = 0.5 + i * 3.1;
    card(s, x, 1.3, 2.8, 3.6, C.background2, "caso");
    await badge(s, x + 0.25, 1.5, casos[i][0], 0.6, casos[i][1]);
    T(s, casos[i][2], { x: x + 0.25, y: 2.25, w: 2.4, h: 0.4, fontSize: 17, bold: true });
    T(s, casos[i][3], { x: x + 0.25, y: 2.7, w: 2.4, h: 0.65, fontSize: 13, color: C.text2 });
    T(s, casos[i][4], { x: x + 0.25, y: 3.45, w: 2.4, h: 1.3, fontSize: 14, bold: true, color: C.text1 });
  }
  s.addNotes("Lo probamos con tres casos. Con datos completos, el edificio del curso en Piedemonte A da un cortante de 23 250 kilonewtons y una deriva máxima de 0,99 %: cumple. Si falta un dato, como Fv, se detiene y dice cuál falta. Si un dato está mal, como una altura escrita en centímetros, lo rechaza y explica el rango válido.");

  // 8 ---------------------------------------------------------------- Validación
  s = pres.addSlide({ masterName: "CONTENIDO", sectionTitle: "Prototipo" });
  s.addText("Reproduce el cálculo de referencia del curso", { placeholder: "title" });
  const hdr = { bold: true, color: HEX.lt1, fill: { color: HEX.dk1 }, fontSize: 13 };
  const cel = { fontSize: 13, color: HEX.dk1 };
  const filas = [
    ["Magnitud", "Excel + SAP2000", "Prototipo"],
    ["Cortante basal Vs (kN)", "23 250", f0(N.vs)],
    ["Fuerza en cubierta Fx (kN)", "7 361", "7 361"],
    ["Deriva máx. X / Y (% hpi)", "0,985 / 0,991", `${f2(N.dxmax, 3)} / ${f2(N.dymax, 3)}`],
    ["Índice de estabilidad Q", "0,0165", f2(N.Q, 4)],
    ["Relación torsional (1aP)", "1,193", f2(N.tor, 3)],
    ["Coeficiente R", "5,0", f2(N.R, 1)],
  ];
  s.addTable(filas.map((r, i) => r.map((c) => ({ text: c, options: i === 0 ? hdr : Object.assign({ fill: { color: i % 2 ? HEX.lt2 : HEX.lt1 } }, cel) }))),
    { x: 0.5, y: 1.3, w: 4.7, colW: [2.1, 1.3, 1.3], rowH: 0.42, border: { type: "solid", pt: 0.5, color: "C9D1D9" }, fontFace: "Calibri", objectName: "tabla_validacion" });
  s.addImage({ path: FIG("fig_derivas_caso_curso.png"), x: 5.45, y: 1.2, w: 4.05, h: 3.0, sizing: { type: "contain", w: 4.05, h: 3.0 }, objectName: "derivas" });
  T(s, "Envolvente de 12 combinaciones en las esquinas E5 y A1. La relación torsional (1,193) queda cerca del umbral 1,2 de irregularidad.",
    { x: 5.45, y: 4.3, w: 4.05, h: 0.7, fontSize: 11, color: C.text2, italic: true });
  s.addNotes("Validamos contra el cálculo de referencia del curso, hecho con Excel y SAP2000. El prototipo reproduce cortante, fuerzas, derivas, Q, relación torsional y R. La relación torsional de 1,19 queda muy cerca del límite de 1,2: un hallazgo útil para el diseñador.");

  // 9 ---------------------------------------------------------------- Base NSR-10
  pres.addSection({ title: "Resultados" });
  s = pres.addSlide({ masterName: "CONTENIDO", sectionTitle: "Resultados" });
  s.addText("Base NSR-10: 18 edificios teóricos + 1 verificado", { placeholder: "title" });
  const bst = [["18", "edificios del Prof. T. F. Rojas Vallejo (OpenSees)"], ["9", "plantas, 4 a 10 pisos, Bogotá, DES"], ["1", "caso del curso verificado con SAP2000"]];
  bst.forEach(([v, l], i) => {
    const x = 0.5 + i * 3.1;
    T(s, v, { x, y: 1.3, w: 2.8, h: 0.85, fontSize: 48, bold: true, color: C.accent1, fontFace: THEME.headFontFace });
    T(s, l, { x, y: 2.15, w: 2.8, h: 0.6, fontSize: 14, color: C.text2 });
  });
  card(s, 0.5, 3.05, 9.0, 1.85, HEX.lt2, "nota_profesor");
  await badge(s, 0.75, 3.3, fa.FaExclamationTriangle, 0.55, C.accent5);
  T(s, "Nota del profesor", { x: 1.5, y: 3.3, w: 7.8, h: 0.35, fontSize: 15, bold: true });
  T(s, "Varios resultados son teóricos: algunas plantas y luces no se resolverían con pórticos resistentes a momento en la práctica. Las plantas ausentes fallaron en el dimensionamiento del algoritmo de OpenSees. Por eso estos datos sirven para entrenar y comparar, no como diseños.",
    { x: 1.5, y: 3.7, w: 7.8, h: 1.1, fontSize: 13, color: C.text2 });
  s.addNotes("Para la ruta NSR-10 armamos una base con 18 edificios que diseñó el profesor Rojas Vallejo con su algoritmo en OpenSees, más el caso del curso. El profesor nos advirtió que varios son teóricos y que las plantas que faltan fallaron en el dimensionamiento. Los usamos para entrenar y comparar, no como diseños.");

  // 10 --------------------------------------------------------------- RF chart
  s = pres.addSlide({ masterName: "CONTENIDO", sectionTitle: "Resultados" });
  s.addText("Random Forest reduce 39 % el error de deriva", { placeholder: "title" });
  const get = (obj, mod) => N.met.find((m) => m.Objetivo === obj && m.Modelo === mod).MAE;
  const mods = ["Random Forest", "Regresión lineal", "Media (referencia)"];
  const dx = mods.map((m) => +get("Deriva máx. X (%)", m).toFixed(3));
  const dy = mods.map((m) => +get("Deriva máx. Y (%)", m).toFixed(3));
  s.addChart(pres.charts.BAR, [
    { name: "Deriva X", labels: ["Random Forest", "Regresión lineal", "Media"], values: dx },
    { name: "Deriva Y", labels: ["Random Forest", "Regresión lineal", "Media"], values: dy },
  ], {
    x: 0.5, y: 1.2, w: 5.6, h: 3.8, barDir: "col", barGapWidthPct: 60,
    chartColors: [HEX.accent1, HEX.accent2], showLegend: true, legendPos: "b", legendFontSize: 11, legendFontFace: "+mn-lt", legendColor: HEX.dk2,
    showTitle: true, title: "Error absoluto medio (puntos de % de hpi)", titleFontSize: 12, titleColor: HEX.dk2, titleFontFace: "+mn-lt",
    showValue: true, dataLabelPosition: "outEnd", dataLabelFontSize: 10, dataLabelColor: HEX.dk2, dataLabelFormatCode: "0.000", dataLabelFontFace: "+mn-lt",
    catAxisLabelColor: HEX.dk2, catAxisLabelFontSize: 11, catAxisLabelFontFace: "+mn-lt", valAxisHidden: true,
    valGridLine: { style: "none" }, catGridLine: { style: "none" }, objectName: "grafico_mae",
  });
  const red = Math.round((1 - dx[0] / dx[2]) * 100);
  card(s, 6.4, 1.3, 3.1, 1.6, C.background2, "stat");
  T(s, `−${red} %`, { x: 6.6, y: 1.4, w: 2.8, h: 0.8, fontSize: 40, bold: true, color: C.accent1, fontFace: THEME.headFontFace });
  T(s, "error de deriva frente a predecir la media", { x: 6.6, y: 2.2, w: 2.8, h: 0.6, fontSize: 13, color: C.text2 });
  card(s, 6.4, 3.2, 3.1, 1.6, C.background2, "stat");
  T(s, `${Math.round(N.ml.t_prediccion_ms)} ms`, { x: 6.6, y: 3.3, w: 2.8, h: 0.8, fontSize: 40, bold: true, color: C.accent1, fontFace: THEME.headFontFace });
  T(s, "por predicción; entrenar toma 0,4 s", { x: 6.6, y: 4.1, w: 2.8, h: 0.6, fontSize: 13, color: C.text2 });
  T(s, "Validación dejando una planta completa fuera (9 pliegues).", { x: 0.5, y: 4.95, w: 5.6, h: 0.25, fontSize: 10, color: C.accent2, italic: true });
  s.addNotes("Evaluamos Random Forest dejando cada planta completa por fuera. Con plantas que nunca vio, su error en la deriva fue de 0,086 puntos en X y 0,101 en Y: un 39 % menos que predecir la media y mejor que la regresión lineal. Cada predicción toma unos 32 milisegundos.");

  // 11 --------------------------------------------------------------- Calc vs pred
  s = pres.addSlide({ masterName: "CONTENIDO", sectionTitle: "Resultados" });
  s.addText("Útil para priorizar, aún no para certificar", { placeholder: "title" });
  s.addImage({ path: FIG("fig_calculado_vs_predicho.png"), x: 0.5, y: 1.2, w: 5.6, h: 3.0, sizing: { type: "contain", w: 5.6, h: 3.0 }, objectName: "calc_pred" });
  T(s, "Deriva calculada (OpenSees, profesor) frente a predicha por Random Forest en plantas no vistas.", { x: 0.5, y: 4.3, w: 5.6, h: 0.5, fontSize: 11, color: C.text2, italic: true });
  T(s, `${N.ml.detectados} de ${N.ml.cerca_limite_reales}`, { x: 6.4, y: 1.3, w: 3.1, h: 0.85, fontSize: 48, bold: true, color: C.accent1, fontFace: THEME.headFontFace });
  T(s, "edificios con deriva ≥ 0,90 % detectados por el modelo", { x: 6.4, y: 2.15, w: 3.1, h: 0.6, fontSize: 14, color: C.text2 });
  T(s, `${N.ml.falsas_alarmas}`, { x: 6.4, y: 2.95, w: 3.1, h: 0.85, fontSize: 48, bold: true, color: C.accent3, fontFace: THEME.headFontFace });
  T(s, "falsas alarmas; el modelo subestima los casos más cercanos al límite", { x: 6.4, y: 3.8, w: 3.1, h: 0.8, fontSize: 14, color: C.text2 });
  s.addNotes("Pero hay que ser honestos: de siete edificios cerca del límite, el modelo detectó tres y subestimó cuatro. No dio falsas alarmas. Por eso hoy sirve para ordenar alternativas, y la verificación final sigue en el módulo NSR-10 y SAP2000.");

  // 12 --------------------------------------------------------------- Limitaciones
  pres.addSection({ title: "Cierre" });
  s = pres.addSlide({ masterName: "CONTENIDO", sectionTitle: "Cierre" });
  s.addText("Limitaciones que condicionan los resultados", { placeholder: "title" });
  const lim = [
    [fa.FaFlask, "Base NSR-10 pequeña y teórica", "18 edificios; varias configuraciones no serían viables en pórticos reales"],
    [fa.FaHourglassHalf, "Ruta E.030 sin evaluar todavía", "Faltan las métricas del Random Forest en las familias reservadas"],
    [fa.FaStopwatch, "Ahorro de tiempo no cronometrado", "Se midió el cálculo (ms), no el flujo completo en SAP2000"],
    [fa.FaPlug, "Bot sin backend conectado", "Los flujos de n8n esperan el servicio Python con el predictor"],
  ];
  for (let i = 0; i < 4; i++) {
    const x = 0.5 + (i % 2) * 4.6, y = 1.3 + Math.floor(i / 2) * 1.8;
    await badge(s, x, y + 0.1, lim[i][0], 0.6, C.accent2);
    T(s, lim[i][1], { x: x + 0.8, y: y + 0.05, w: 3.5, h: 0.4, fontSize: 16, bold: true });
    T(s, lim[i][2], { x: x + 0.8, y: y + 0.5, w: 3.5, h: 0.9, fontSize: 14, color: C.text2 });
  }
  s.addNotes("Las limitaciones: la base NSR-10 es pequeña y teórica; las métricas del Random Forest en la ruta E.030 están pendientes; no cronometramos el flujo completo en SAP2000, así que no afirmamos un porcentaje de ahorro; y el bot todavía no está conectado al predictor.");

  // 13 --------------------------------------------------------------- Conclusiones
  s = pres.addSlide({ masterName: "OSCURO", sectionTitle: "Cierre" });
  s.addText("Conclusiones y siguientes pasos", { placeholder: "title" });
  const con = [
    "El módulo NSR-10 reproduce el cálculo de referencia y bloquea datos incompletos o erróneos antes de calcular.",
    "En plantas no vistas, Random Forest estimó la deriva con 0,086 % (X) y 0,101 % (Y) de error: 39 % menos que la referencia.",
    "Detecta 3 de 7 edificios cerca del límite: útil para priorizar, no para certificar.",
  ];
  con.forEach((c, i) => {
    num(s, 0.5, 1.3 + i * 0.95, i + 1);
    T(s, c, { x: 1.1, y: 1.27 + i * 0.95, w: 4.3, h: 0.85, fontSize: 14, color: C.background1 });
  });
  card(s, 5.8, 1.25, 3.7, 3.6, HEX.dk2, "siguientes");
  T(s, "Siguientes pasos", { x: 6.05, y: 1.4, w: 3.3, h: 0.4, fontSize: 17, bold: true, color: C.accent1 });
  T(s, [
    { text: "Evaluar el modelo en las familias E.030 reservadas", options: { bullet: true, breakLine: true } },
    { text: "Ampliar la base NSR-10 con casos verificados", options: { bullet: true, breakLine: true } },
    { text: "Conectar módulo y predictor al bot de Telegram", options: { bullet: true, breakLine: true } },
    { text: "Cronometrar el flujo completo para medir el ahorro", options: { bullet: true } },
  ], { x: 6.05, y: 1.9, w: 3.3, h: 2.8, fontSize: 14, color: C.background1, paraSpaceAfter: 6 });
  s.addNotes("En conclusión: el módulo NSR-10 reproduce el cálculo de referencia y filtra datos malos; el Random Forest reduce el error un 39 % en plantas que no vio, pero todavía no detecta todos los casos al límite. Los siguientes pasos son evaluar la ruta E.030, ampliar la base con casos verificados, conectar todo al bot y medir el ahorro de tiempo real.");

  // 14 --------------------------------------------------------------- Equipo
  s = pres.addSlide({ masterName: "CONTENIDO", sectionTitle: "Cierre" });
  s.addText("Equipo y herramientas", { placeholder: "title" });
  const eq = [
    ["Lucero", "Planteamiento académico"], ["Alexis", "Generación paramétrica y OpenSees"], ["Nicolás Infante", "Módulo NSR-10 y SAP2000"],
    ["Jean Piere", "Datos, Random Forest y bot n8n"], ["Joseph", "Validación y coordinación"],
  ];
  for (let i = 0; i < 5; i++) {
    const x = 0.5 + i * 1.84;
    card(s, x, 1.3, 1.68, 1.9, C.background2, "integrante");
    await badge(s, x + 0.54, 1.45, fa.FaUserAlt, 0.6, C.accent2);
    T(s, eq[i][0], { x: x + 0.08, y: 2.15, w: 1.52, h: 0.35, fontSize: 14, bold: true, align: "center" });
    T(s, eq[i][1], { x: x + 0.08, y: 2.5, w: 1.52, h: 0.65, fontSize: 11, color: C.text2, align: "center" });
  }
  T(s, "Herramientas", { x: 0.5, y: 3.5, w: 9, h: 0.35, fontSize: 15, bold: true });
  T(s, "Python · OpenSeesPy · SAP2000 · scikit-learn · n8n · Telegram · asistentes de IA generativa para programación · Obsidian · GitHub · Discord · Miro",
    { x: 0.5, y: 3.9, w: 9, h: 0.6, fontSize: 14, color: C.text2 });
  T(s, "Profesor de apoyo: Thomas Federico Rojas Vallejo (Universidad Nacional de Colombia), algoritmo de diseño NSR-10 en OpenSees.", { x: 0.5, y: 4.6, w: 9, h: 0.4, fontSize: 12, color: C.accent2, italic: true });
  s.addNotes("Somos cinco: Lucero en el planteamiento, Alexis en la generación y OpenSees, Nicolás en el módulo NSR-10, Jean Piere en datos, Random Forest y el bot, y Joseph en validación y coordinación. Agradecemos al profesor Thomas Rojas Vallejo por sus datos. Gracias.");

  await pres.writeFile({ fileName: OUT });
  await applyTheme(OUT, THEME);
  console.log("ok →", OUT);
})();
