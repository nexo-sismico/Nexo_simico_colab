/* Nexo Sísmico · interfaz del verificador NSR-10.
   El cálculo lo hace el mismo nexo_nsr10.py del prototipo, ejecutado en el navegador con Pyodide:
   la interfaz solo arma el JSON de entrada, muestra la validación y dibuja los resultados. */
"use strict";

const $ = (s) => document.querySelector(s);
const $$ = (s) => [...document.querySelectorAll(s)];
const COMBOS = [1, 2, 3, 4, 5, 6].map((i) => `DER-X${i}`).concat([1, 2, 3, 4, 5, 6].map((i) => `DER-Y${i}`));
const CANDIDATOS = (f) => [`../codigo/${f}`, f];          // la app vive en 03 Prototipo/app y el motor en ../codigo (o copia junto a la app)
const CLAVE_ALT = "nexo-sismico-alternativas";

const estado = {
  py: null,                 // funciones Python
  extra: {},                // campos del JSON que el formulario no edita (luces, columnas, cargas por m², etc.)
  derivas: null,            // derivas_sap del caso
  ultimo: null,             // { datos, r, ms }
  alternativas: [],
  graficas: {},
};

/* ------------------------------------------------------------------ utilidades */
function fmt(v, d = 2) {
  if (v === null || v === undefined || Number.isNaN(v)) return "—";
  const [e, f] = Math.abs(v).toFixed(d).split(".");
  const miles = e.replace(/\B(?=(\d{3})+(?!\d))/g, " ");
  return (v < 0 ? "−" : "") + miles + (f ? "," + f : "");
}
function num(txt) {
  const t = String(txt ?? "").trim().replace(/\s/g, "").replace(",", ".");
  if (t === "") return undefined;
  const n = Number(t);
  return Number.isFinite(n) ? n : String(txt).trim();      // texto no numérico: el motor lo marca como error
}
function setPath(obj, ruta, v) {
  const k = ruta.split(".");
  let o = obj;
  k.slice(0, -1).forEach((p) => { o[p] = o[p] && typeof o[p] === "object" ? o[p] : {}; o = o[p]; });
  if (v === undefined) delete o[k[k.length - 1]]; else o[k[k.length - 1]] = v;
}
function getPath(obj, ruta) { return ruta.split(".").reduce((o, p) => (o && typeof o === "object" ? o[p] : undefined), obj); }
function aviso(txt, ms = 3200) {
  const t = $("#aviso"); t.textContent = txt; t.hidden = false;
  clearTimeout(aviso.t); aviso.t = setTimeout(() => (t.hidden = true), ms);
}
function descargar(nombre, contenido, tipo) {
  const a = document.createElement("a");
  a.href = URL.createObjectURL(new Blob([contenido], { type: tipo }));
  a.download = nombre; document.body.appendChild(a); a.click();
  setTimeout(() => { URL.revokeObjectURL(a.href); a.remove(); }, 500);
}
async function primero(rutas, como = "text") {
  for (const r of rutas) {
    try { const res = await fetch(r, { cache: "no-cache" }); if (res.ok) return como === "json" ? res.json() : res.text(); } catch (e) { /* siguiente */ }
  }
  throw new Error(`No se encontró ${rutas[0]}`);
}
const css = (n) => getComputedStyle(document.documentElement).getPropertyValue(n).trim();
const guardarLocal = (k, v) => { try { localStorage.setItem(k, JSON.stringify(v)); } catch (e) { /* almacenamiento no disponible */ } };
const leerLocal = (k, def) => { try { return JSON.parse(localStorage.getItem(k)) ?? def; } catch (e) { return def; } };

/* ------------------------------------------------------------------ motor Python */
async function iniciarMotor() {
  const pill = $("#motor");
  try {
    const pyodide = await loadPyodide();
    const fuente = await primero(CANDIDATOS("nexo_nsr10.py"));
    pyodide.FS.writeFile("nexo_nsr10.py", fuente);
    pyodide.runPython(`
import json, nexo_nsr10 as nx
def _validar(s):
    e, f, er, a = nx.validar(json.loads(s))
    return json.dumps({"estado": e, "faltan": f, "errores": er, "avisos": a}, ensure_ascii=False)
def _analizar(s):
    return json.dumps(nx.analizar(json.loads(s)), ensure_ascii=False, default=float)
def _reporte(s, t):
    return nx.reporte(json.loads(s), t)
def _registro(sd, sr):
    return json.dumps(nx.registro_bd(json.loads(sd), json.loads(sr)), ensure_ascii=False, default=float)
def _espectro(sp, sT):
    p, Ts = json.loads(sp), json.loads(sT)
    return json.dumps([nx.espectro(T, p["Aa"], p["Av"], p["Fa"], p["Fv"], p["I"], p["TL"])[0] for T in Ts])
`);
    const f = (n) => pyodide.globals.get(n);
    estado.py = {
      version: pyodide.runPython("nx.VERSION"),
      validar: (d) => JSON.parse(f("_validar")(JSON.stringify(d))),
      analizar: (d) => JSON.parse(f("_analizar")(JSON.stringify(d))),
      reporte: (r, t) => f("_reporte")(JSON.stringify(r), t),
      registro: (d, r) => JSON.parse(f("_registro")(JSON.stringify(d), JSON.stringify(r))),
      espectro: (p, Ts) => JSON.parse(f("_espectro")(JSON.stringify(p), JSON.stringify(Ts))),
    };
    pill.className = "pill pill-listo";
    pill.textContent = `Motor NSR-10 v${estado.py.version} listo`;
    pill.title = "nexo_nsr10.py ejecutándose en este navegador (Pyodide)";
    $("#btn-verificar").disabled = false;
    revisar();
    return true;
  } catch (e) {
    pill.className = "pill pill-error";
    pill.textContent = "No se pudo cargar el motor";
    $("#revision").className = "revision error";
    $("#revision").innerHTML = `<h3>No se pudo cargar el motor de cálculo</h3><p>${e.message}. Abra la app con <code>python "03 Prototipo/app/abrir_app.py"</code> (necesita conexión a internet la primera vez).</p>`;
    console.error(e);
    return false;
  }
}

/* ------------------------------------------------------------------ formulario */
function filasPisos(n, valores = {}) {
  const tb = $("#pisos");
  const prev = leerPisos();
  tb.innerHTML = "";
  for (let i = n; i >= 1; i--) {                       // de arriba hacia abajo, como el edificio
    const v = (k) => valores[k]?.[i - 1] ?? prev[k]?.[i - 1] ?? "";
    const tr = document.createElement("tr");
    tr.innerHTML = `<td>${i}</td>
      <td><input id="hl-${i}" type="text" inputmode="decimal" aria-label="Altura libre nivel ${i}" value="${v("hl")}"></td>
      <td><input id="w-${i}" type="text" inputmode="decimal" aria-label="Peso sísmico nivel ${i}" value="${v("w")}"></td>
      <td><input id="l-${i}" type="text" inputmode="decimal" aria-label="Carga viva nivel ${i}" value="${v("l")}"></td>`;
    tb.appendChild(tr);
  }
}
function leerPisos() {
  const out = { hl: [], w: [], l: [] };
  const n = $$("#pisos tr").length;
  for (let i = 1; i <= n; i++) ["hl", "w", "l"].forEach((k) => out[k].push($(`#${k}-${i}`)?.value ?? ""));
  return out;
}
function nPisos() { return Math.max(1, Math.min(30, parseInt($("#n-pisos").value, 10) || 1)); }

function leerFormulario() {
  const d = structuredClone(estado.extra);
  $$("#form [data-ruta]").forEach((el) => {
    const ruta = el.dataset.ruta;
    let v = el.tagName === "SELECT" ? el.value : el.value;
    if (["id", "fuente", "sitio.ciudad", "sitio.microzona"].includes(ruta)) v = v.trim() || undefined;
    else if (el.dataset.tipo === "int") v = parseInt(v, 10);
    else v = num(v);
    setPath(d, ruta, v);
  });
  const ret = d.geometria?.retroceso;
  if (ret && ["A", "B", "C", "D"].some((k) => ret[k] === undefined)) delete d.geometria.retroceso;   // incompleto: no se usa
  const p = leerPisos();
  const lista = (arr) => (arr.every((x) => String(x).trim() === "") ? undefined : arr.map((x) => (String(x).trim() === "" ? null : num(x))));
  setPath(d, "geometria.alturas_libres", lista(p.hl));
  setPath(d, "pesos.W_kN", lista(p.w));
  setPath(d, "pesos.L_kN", lista(p.l));
  if (estado.derivas) d.derivas_sap = structuredClone(estado.derivas); else delete d.derivas_sap;
  d.limite_deriva = d.limite_deriva ?? 0.01;
  return d;
}

function llenarFormulario(d) {
  estado.extra = structuredClone(d);
  ["sitio", "sistema", "geometria", "pesos", "periodos_sap"].forEach((k) => { if (estado.extra[k]) estado.extra[k] = { ...estado.extra[k] }; });
  // lo que edita el formulario sale de "extra" para que el formulario mande
  $$("#form [data-ruta]").forEach((el) => {
    const v = getPath(d, el.dataset.ruta);
    el.value = v === undefined || v === null ? (el.tagName === "SELECT" ? el.options[0].value : "") : String(v).replace(".", el.dataset.ruta.match(/^(id|fuente|sitio\.ciudad|sitio\.microzona)$/) ? "." : ",");
    setPath(estado.extra, el.dataset.ruta, undefined);
  });
  const g = d.geometria || {}, p = d.pesos || {};
  const n = (g.alturas_libres || p.W_kN || [1, 1, 1]).length;
  $("#n-pisos").value = n;
  $("#pisos").innerHTML = "";
  const dec = (a) => (a || []).map((x) => (x === null || x === undefined ? "" : String(x).replace(".", ",")));
  filasPisos(n, { hl: dec(g.alturas_libres), w: dec(p.W_kN), l: dec(p.L_kN) });
  ["alturas_libres"].forEach((k) => { if (estado.extra.geometria) delete estado.extra.geometria[k]; });
  if (estado.extra.pesos) { delete estado.extra.pesos.W_kN; delete estado.extra.pesos.L_kN; }
  estado.derivas = d.derivas_sap ? structuredClone(d.derivas_sap) : null;
  delete estado.extra.derivas_sap;
  const r0 = String(getPath(d, "sistema.R0") ?? "");
  $("#sistema-preset").value = ["7", "5", "2.5"].includes(r0) ? r0 : "otro";
  pintarDesplazamientos();
}

/* ------------------------------------------------------------------ validación en vivo */
function marcarCampos(res) {
  $$(".con-error, .con-falta").forEach((el) => el.classList.remove("con-error", "con-falta"));
  const marcar = (msg, clase) => {
    const m = msg.match(/^([A-Za-z_]+(?:\.[A-Za-z_0-9-]+)*)(?:\[nivel (\d+)\])?/);
    if (!m) return null;
    const [, ruta, nivel] = m;
    const lista = { "geometria.alturas_libres": "hl", "pesos.W_kN": "w", "pesos.L_kN": "l" }[ruta];
    let els = [];
    if (lista) els = nivel ? [$(`#${lista}-${nivel}`)] : $$(`[id^="${lista}-"]`);
    else if (ruta.startsWith("derivas_sap") || ruta.startsWith("esquina")) els = [$("#desp-estado")];
    else els = [$(`#form [data-ruta="${ruta}"]`)];
    els.filter(Boolean).forEach((el) => el.classList.add(clase));
    return els[0] || null;
  };
  const items = [];
  res.faltan.forEach((m) => items.push({ m: `Falta ${m}`, el: marcar(m, "con-falta"), tipo: "falta" }));
  res.errores.forEach((m) => items.push({ m: m.replace(/ = None: debe ser numérico/, ": falta el valor"), el: marcar(m, "con-error"), tipo: "error" }));
  return items;
}
function mostrarRevision(res, detenido = false) {
  const box = $("#revision");
  const items = marcarCampos(res);
  if (res.estado === "ok") {
    box.className = "revision ok";
    box.innerHTML = detenido ? "" : `<h3>Entrada completa y en rango</h3><p>Pulse <strong>Verificar edificio</strong> para calcular.</p>`;
    if (detenido) box.innerHTML = "";
    return;
  }
  const falta = res.estado === "faltan_datos";
  box.className = "revision " + (falta ? "falta" : "error");
  const tit = detenido
    ? (falta ? "Cálculo detenido: faltan datos" : "Cálculo detenido: hay datos fuera de rango")
    : (falta ? (res.faltan.length > 1 ? `Faltan ${res.faltan.length} datos para poder calcular` : "Falta 1 dato para poder calcular") : "Hay datos que revisar antes de calcular");
  const lis = items.slice(0, 14).map((it, i) => `<li>${it.el ? `<a href="#" data-i="${i}">${escapar(it.m)}</a>` : escapar(it.m)}</li>`).join("");
  box.innerHTML = `<h3>${tit}</h3>${detenido ? "<p>La herramienta no inventa ni supone valores: corrija lo marcado y vuelva a verificar. No se generó ningún resultado.</p>" : ""}<ul>${lis}</ul>${items.length > 14 ? `<p class="nota">… y ${items.length - 14} más.</p>` : ""}`;
  box.querySelectorAll("a[data-i]").forEach((a) => a.addEventListener("click", (e) => {
    e.preventDefault(); const el = items[+a.dataset.i].el; el.scrollIntoView({ block: "center", behavior: "smooth" }); el.focus?.();
  }));
}
function escapar(t) { return String(t).replace(/[&<>"]/g, (c) => ({ "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;" }[c])); }

let tRevisar;
function revisar() {
  clearTimeout(tRevisar);
  tRevisar = setTimeout(() => {
    if (!estado.py) return;
    const res = estado.py.validar(leerFormulario());
    if (!$("#resultados").hidden && res.estado === "ok") { marcarCampos(res); return; }
    mostrarRevision(res);
  }, 250);
}

/* ------------------------------------------------------------------ desplazamientos */
function pintarDesplazamientos() {
  const box = $("#desp-estado");
  box.classList.remove("con-falta", "con-error");
  if (!estado.derivas?.esquinas || !Object.keys(estado.derivas.esquinas).length) {
    box.innerHTML = `<div class="esq"><div class="esq-titulo"><span>Sin desplazamientos</span></div><p class="nota">Pegue la tabla de SAP2000 o abra un JSON del caso.</p></div>`;
    return;
  }
  box.innerHTML = Object.entries(estado.derivas.esquinas).map(([nom, e]) => {
    const c = e.combinaciones || {};
    const niveles = Object.values(c)[0]?.length ?? 0;
    const ok = COMBOS.filter((k) => c[k]).length;
    return `<div class="esq"><div class="esq-titulo"><span>Esquina ${escapar(nom)}</span><span class="nota">${ok}/12 combinaciones · ${niveles} niveles</span></div>
      <div class="combos">${COMBOS.map((k) => `<span class="combo ${c[k] ? "" : "falta"}" title="${k}${c[k] ? "" : " falta"}">${k.slice(4)}</span>`).join("")}</div></div>`;
  }).join("");
}

function partirFilas(texto) {
  const lineas = texto.split(/\r?\n/).map((l) => l.trim()).filter(Boolean);
  if (!lineas.length) return [];
  const sep = lineas[0].includes("\t") ? "\t" : lineas[0].includes(";") ? ";" : ",";
  return lineas.map((l) => l.split(sep).map((c) => c.trim().replace(/^"|"$/g, "")));
}
function interpretarTabla(texto) {
  const filas = partirFilas(texto);
  const norm = (s) => s.toLowerCase().normalize("NFD").replace(/[̀-ͯ]/g, "").replace(/\s/g, "");
  for (let h = 0; h < Math.min(filas.length, 6); h++) {
    const cab = filas[h].map(norm);
    const ix = (n) => cab.indexOf(n);
    const u1 = ix("u1"), u2 = ix("u2");
    if (u1 < 0 || u2 < 0) continue;
    const datos = filas.slice(h + 1).filter((f) => Number.isFinite(Number(String(f[u1]).replace(",", "."))));
    if (ix("joint") >= 0 && ix("outputcase") >= 0) return { tipo: "sap", cab: { joint: ix("joint"), caso: ix("outputcase"), u1, u2 }, filas: datos };
    if (ix("esquina") >= 0 && ix("combinacion") >= 0 && ix("nivel") >= 0) return { tipo: "nexo", cab: { esq: ix("esquina"), caso: ix("combinacion"), nivel: ix("nivel"), u1, u2 }, filas: datos };
  }
  return { tipo: null };
}
function importarTabla() {
  const msg = $("#imp-msg");
  const t = interpretarTabla($("#imp-texto").value);
  const k = parseFloat($("#imp-unidad").value);
  const val = (x) => Number(String(x).replace(",", ".")) * k;
  const esquinas = {};
  let duplicados = 0;
  if (t.tipo === "sap") {
    const n = nPisos();
    const mapas = [[$("#imp-e1").value.trim() || "E1", $("#imp-n1").value], [$("#imp-e2").value.trim() || "E2", $("#imp-n2").value]]
      .map(([nom, s]) => [nom, s.split(/[,;\s]+/).map((x) => x.trim()).filter(Boolean)]);
    for (const [nom, nudos] of mapas) {
      if (nudos.length !== n) { msg.className = "imp-msg mal"; msg.textContent = `La esquina ${nom} tiene ${nudos.length} nudos y el edificio tiene ${n} pisos: indique un nudo por nivel, de abajo hacia arriba.`; return false; }
    }
    for (const [nom, nudos] of mapas) {
      const combos = {};
      for (const c of COMBOS) {
        const filas = nudos.map((j) => t.filas.filter((f) => f[t.cab.joint] === j && f[t.cab.caso].toUpperCase() === c));
        if (filas.every((f) => f.length)) {
          duplicados += filas.filter((f) => f.length > 1).length;
          combos[c] = filas.map((f) => [val(f[0][t.cab.u1]), val(f[0][t.cab.u2])]);
        }
      }
      esquinas[nom] = { combinaciones: combos };
    }
  } else if (t.tipo === "nexo") {
    for (const f of t.filas) {
      const nom = f[t.cab.esq], c = f[t.cab.caso].toUpperCase(), i = parseInt(f[t.cab.nivel], 10) - 1;
      if (!COMBOS.includes(c) || !(i >= 0)) continue;
      esquinas[nom] = esquinas[nom] || { combinaciones: {} };
      (esquinas[nom].combinaciones[c] = esquinas[nom].combinaciones[c] || [])[i] = [val(f[t.cab.u1]), val(f[t.cab.u2])];
    }
  } else {
    msg.className = "imp-msg mal";
    msg.textContent = "No reconozco la tabla. Debe tener encabezados Joint, OutputCase, U1 y U2 (SAP2000) o Esquina, Combinacion, Nivel, U1 y U2.";
    return false;
  }
  const nEsq = Object.keys(esquinas).length;
  const nCombos = Object.values(esquinas).reduce((s, e) => s + Object.keys(e.combinaciones).length, 0);
  if (!nCombos) { msg.className = "imp-msg mal"; msg.textContent = "No encontré las combinaciones DER-X1…DER-Y6 para esos nudos. Revise los nombres de las combinaciones y de los nudos."; return false; }
  estado.derivas = { esquinas };
  pintarDesplazamientos();
  revisar();
  aviso(`Importadas ${nCombos} combinaciones en ${nEsq} esquina${nEsq > 1 ? "s" : ""}${duplicados ? ` (había ${duplicados} filas repetidas por nudo: se tomó la primera)` : ""}.`, 4500);
  return true;
}

/* ------------------------------------------------------------------ verificar y resultados */
function verificar() {
  if (!estado.py) return;
  clearTimeout(tRevisar);                 // el resultado oficial manda sobre la revisión en vivo pendiente
  const datos = leerFormulario();
  const t0 = performance.now();
  const r = estado.py.analizar(datos);
  const ms = performance.now() - t0;
  if (r.estado !== "ok") {
    $("#resultados").hidden = true;
    estado.ultimo = null;
    mostrarRevision({ estado: r.estado, faltan: r.faltan, errores: r.errores }, true);
    $("#revision").scrollIntoView({ block: "start", behavior: "smooth" });
    return;
  }
  estado.ultimo = { datos, r, ms };
  marcarCampos({ faltan: [], errores: [] });
  $("#revision").className = "revision"; $("#revision").innerHTML = "";
  $("#resultados").hidden = false;
  pintarResultados();
}

function pintarResultados() {
  const { r, ms } = estado.ultimo;
  const lim = 100 * (estado.ultimo.datos.limite_deriva ?? 0.01);
  const cumple = r.dictamen.derivas && r.dictamen.estabilidad;
  const p = r.parametros;
  const tor = r.torsion_ratio;
  const torClase = tor > 1.4 ? "mal" : tor > 1.2 ? "aviso" : "ok";
  const torTxt = tor > 1.4 ? "extrema (1bP)" : tor > 1.2 ? "irregular (1aP)" : "regular";
  $("#dictamen").className = "dictamen" + (cumple ? "" : " no");
  $("#dictamen").innerHTML = `
    <div class="sello">${cumple ? "Cumple" : "No cumple"}</div>
    <p>Deriva máxima <strong>${fmt(r.deriva_max_pct.X, 3)} %</strong> en X y <strong>${fmt(r.deriva_max_pct.Y, 3)} %</strong> en Y, frente al límite de ${fmt(lim, 1)} % de la altura de piso (A.6.4). ${cumple ? "Las derivas y la estabilidad cumplen." : r.dictamen.derivas ? "Las derivas cumplen, pero la estabilidad no (Q > 0,30)." : "Hay pisos que superan el límite: rigidice la estructura o cambie la alternativa."}</p>
    <div class="chips">
      <span class="chip ${r.dictamen.derivas ? "ok" : "mal"}">Derivas ${r.dictamen.derivas ? "✓" : "✗"}</span>
      <span class="chip ${r.dictamen.estabilidad ? (r.dictamen.p_delta_requerido ? "aviso" : "ok") : "mal"}">Q máx ${fmt(r.Q_max, 4)} · ${r.dictamen.p_delta_requerido ? "considerar P-Delta" : "P-Delta no requerido"}</span>
      <span class="chip ${torClase}">Torsión Δmáx/Δprom ${fmt(tor, 3)} · ${torTxt}</span>
      <span class="chip">R = ${fmt(r.R, 2)} (φa ${fmt(r.phi_a, 1)} · φp ${fmt(r.phi_p, 1)} · φr ${fmt(r.phi_r, 1)})</span>
      <span class="chip">Calculado en ${fmt(ms, 1)} ms</span>
    </div>`;
  const fx = r.fhe.X, fy = r.fhe.Y;
  const kpi = (et, val, nota = "") => `<div class="kpi"><span class="kpi-et">${et}</span><span class="kpi-val">${val}</span>${nota ? `<span class="kpi-nota">${nota}</span>` : ""}</div>`;
  $("#kpis").innerHTML = [
    kpi("Cortante basal Vs", `${fmt(fx.Vs, 0)} <small>kN</small>`, fx.Vs === fy.Vs ? "igual en X e Y" : `Y: ${fmt(fy.Vs, 0)} kN`),
    kpi("Periodo de diseño", `${fmt(fx.T_diseno, 3)} <small>s</small>`, `X · Y: ${fmt(fy.T_diseno, 3)} s · Cu·Ta ${fmt(p.CuTa, 3)} s`),
    kpi("Sa", `${fmt(fx.Sa, 4)} <small>g</small>`, `${fx.tramo}${fy.Sa !== fx.Sa ? ` · Y: ${fmt(fy.Sa, 4)} g` : ""}`),
    kpi("Peso sísmico Wt", `${fmt(p.Wt, 0)} <small>kN</small>`, `hn = ${fmt(p.hn, 2)} m · ${r.niveles.length} pisos`),
    kpi("Índice Q máx", `${fmt(r.Q_max, 4)}`, "A.6.2.3 · límite 0,30"),
    kpi("Coeficiente R", `${fmt(r.R, 2)}`, `I = ${fmt(p.I, 2)} · Tc = ${fmt(p.Tc, 3)} s`),
  ].join("");
  pintarTablas(r, lim);
  $("#avisos").innerHTML = r.advertencias.length ? `<strong>Advertencias</strong><ul>${r.advertencias.map((a) => `<li>${escapar(a)}</li>`).join("")}</ul>` : "";
  pintarGraficas();
}

function pintarTablas(r, lim) {
  const n = r.niveles.length;
  const filasN = [...r.niveles].reverse().map((nv) => {
    const i = nv.nivel - 1;
    return `<tr><td>${nv.nivel}</td><td>${fmt(nv.Z, 2)}</td><td>${fmt(nv.hpi, 2)}</td><td>${fmt(nv.W, 0)}</td><td>${fmt(r.fhe.X.F[i], 0)}</td><td>${fmt(r.fhe.Y.F[i], 0)}</td><td>${fmt(r.fhe.X.V[i], 0)}</td><td>${fmt(r.fhe.Y.V[i], 0)}</td></tr>`;
  }).join("");
  $("#t-niveles").innerHTML = `<caption>Fuerza horizontal equivalente</caption><thead><tr><th>Nivel</th><th>Z (m)</th><th>hpi (m)</th><th>W (kN)</th><th>Fx (kN)</th><th>Fy (kN)</th><th>Vx (kN)</th><th>Vy (kN)</th></tr></thead><tbody>${filasN}</tbody>`;
  const der = (d, nivel) => r.derivas.find((x) => x.dir === d && x.nivel === nivel);
  const filasD = [];
  for (let nivel = n; nivel >= 1; nivel--) {
    const x = der("X", nivel), y = der("Y", nivel);
    const c = (v) => `<td class="${v.cumple ? "ok" : "mal"}">${fmt(v.deriva_pct, 3)}</td>`;
    filasD.push(`<tr><td>${nivel}</td>${c(x)}<td class="txt">${escapar(x.combinacion)}</td>${c(y)}<td class="txt">${escapar(y.combinacion)}</td></tr>`);
  }
  $("#t-derivas").innerHTML = `<caption>Derivas por nivel (% hpi, límite ${fmt(lim, 1)} %)</caption><thead><tr><th>Nivel</th><th>X</th><th>Combinación</th><th>Y</th><th>Combinación</th></tr></thead><tbody>${filasD.join("")}</tbody>`;
}

/* ------------------------------------------------------------------ gráficas */
function baseGrafica() {
  const tinta = css("--tinta-2"), linea = css("--linea"), f = css("--f-texto");
  Chart.defaults.font.family = f; Chart.defaults.font.size = 12; Chart.defaults.color = tinta;
  return {
    responsive: true, maintainAspectRatio: false, animation: false,
    interaction: { mode: "nearest", intersect: false },
    plugins: { legend: { position: "bottom", labels: { boxWidth: 12, boxHeight: 12, usePointStyle: true } },
      tooltip: { backgroundColor: css("--tinta"), titleColor: css("--hoja"), bodyColor: css("--hoja"), padding: 9, cornerRadius: 4 } },
    scales: { x: { grid: { color: linea }, border: { color: linea } }, y: { grid: { color: linea }, border: { color: linea } } },
  };
}
function nueva(id, cfg) {
  estado.graficas[id]?.destroy();
  estado.graficas[id] = new Chart(document.getElementById(id), cfg);
}
function pintarGraficas() {
  if (!estado.ultimo || typeof Chart === "undefined") return;
  const { r, datos } = estado.ultimo;
  const n = r.niveles.length, lim = 100 * (datos.limite_deriva ?? 0.01);
  const X = css("--serie-x"), Y = css("--serie-y"), malo = css("--mal"), tinta3 = css("--tinta-3");
  const puntos = (d) => [{ x: 0, y: 0 }].concat(r.derivas.filter((v) => v.dir === d).map((v) => ({ x: v.deriva_pct, y: v.nivel, c: v.combinacion })));
  const maxD = Math.max(lim, r.deriva_max_pct.X, r.deriva_max_pct.Y) * 1.15;

  let b = baseGrafica();
  nueva("g-derivas", { type: "scatter", data: { datasets: [
      { label: "Dirección X", data: puntos("X"), borderColor: X, backgroundColor: X, showLine: true, borderWidth: 2, pointRadius: (c) => (c.dataIndex ? 4.5 : 0), pointHoverRadius: 7 },
      { label: "Dirección Y", data: puntos("Y"), borderColor: Y, backgroundColor: Y, showLine: true, borderWidth: 2, pointStyle: "rectRot", pointRadius: (c) => (c.dataIndex ? 5 : 0), pointHoverRadius: 7 },
      { label: `Límite NSR-10 (${fmt(lim, 1)} %)`, data: [{ x: lim, y: 0 }, { x: lim, y: n + 0.4 }], borderColor: malo, borderDash: [6, 4], borderWidth: 1.5, showLine: true, pointRadius: 0, pointHoverRadius: 0 },
    ] },
    options: { ...b, scales: {
      x: { ...b.scales.x, min: 0, max: Math.ceil(maxD * 10) / 10, title: { display: true, text: "Deriva (% de la altura de piso)" }, ticks: { callback: (v) => fmt(v, 1) } },
      y: { ...b.scales.y, min: 0, max: n + 0.4, title: { display: true, text: "Nivel" }, ticks: { stepSize: 1, callback: (v) => (Number.isInteger(v) ? (v === 0 ? "Base" : v) : "") } } },
      plugins: { ...b.plugins, tooltip: { ...b.plugins.tooltip, filter: (it) => it.datasetIndex < 2 && it.dataIndex > 0,
        callbacks: { title: (it) => `Nivel ${it[0].raw.y}`, label: (it) => `${it.dataset.label}: ${fmt(it.raw.x, 3)} % · ${it.raw.c}` } } } },
  });

  const p = r.parametros;
  const Tmax = Math.max(3, p.TL + 0.5, r.fhe.X.T_diseno * 2);
  const Ts = Array.from({ length: 241 }, (_, i) => 0.02 + (Tmax - 0.02) * i / 240);
  const sp = { Aa: datos.sitio.Aa, Av: datos.sitio.Av, Fa: datos.sitio.Fa, Fv: datos.sitio.Fv, I: p.I, TL: p.TL };
  const Sa = estado.py.espectro(sp, Ts);
  b = baseGrafica();
  nueva("g-espectro", { type: "scatter", data: { datasets: [
      { label: "Espectro de diseño", data: Ts.map((t, i) => ({ x: t, y: Sa[i] })), showLine: true, borderColor: css("--marino"), borderWidth: 2, pointRadius: 0, pointHoverRadius: 0, fill: { target: "origin", above: "rgba(31,56,100,.07)" } },
      { label: `Tx = ${fmt(r.fhe.X.T_diseno, 3)} s`, data: [{ x: r.fhe.X.T_diseno, y: r.fhe.X.Sa }], backgroundColor: X, borderColor: css("--hoja"), borderWidth: 2, pointRadius: 7, pointHoverRadius: 9 },
      { label: `Ty = ${fmt(r.fhe.Y.T_diseno, 3)} s`, data: [{ x: r.fhe.Y.T_diseno, y: r.fhe.Y.Sa }], backgroundColor: Y, borderColor: css("--hoja"), borderWidth: 2, pointStyle: "rectRot", pointRadius: 8, pointHoverRadius: 10 },
      { label: `Cu·Ta = ${fmt(p.CuTa, 3)} s`, data: [{ x: p.CuTa, y: 0 }, { x: p.CuTa, y: Math.max(...Sa) * 1.08 }], borderColor: tinta3, borderDash: [4, 4], borderWidth: 1, showLine: true, pointRadius: 0, pointHoverRadius: 0 },
    ] },
    options: { ...b, scales: {
      x: { ...b.scales.x, min: 0, max: Math.ceil(Tmax), title: { display: true, text: "Periodo T (s)" }, ticks: { callback: (v) => fmt(v, 1) } },
      y: { ...b.scales.y, min: 0, title: { display: true, text: "Sa (g)" }, ticks: { callback: (v) => fmt(v, 2) } } },
      plugins: { ...b.plugins, tooltip: { ...b.plugins.tooltip, filter: (it) => it.datasetIndex === 1 || it.datasetIndex === 2 || (it.datasetIndex === 0 && it.dataIndex % 4 === 0),
        callbacks: { label: (it) => `T = ${fmt(it.raw.x, 3)} s · Sa = ${fmt(it.raw.y, 4)} g` } } } },
  });

  const etiquetas = [...r.niveles].reverse().map((nv) => `Nivel ${nv.nivel}`);
  const inv = (a) => [...a].reverse();
  b = baseGrafica();
  nueva("g-fuerzas", { type: "bar", data: { labels: etiquetas, datasets: [
      { label: "Fx", data: inv(r.fhe.X.F), backgroundColor: X, borderRadius: 4, borderSkipped: "start", barPercentage: 0.8, categoryPercentage: 0.75 },
      { label: "Fy", data: inv(r.fhe.Y.F), backgroundColor: Y, borderRadius: 4, borderSkipped: "start", barPercentage: 0.8, categoryPercentage: 0.75 },
    ] },
    options: { ...b, indexAxis: "y", interaction: { mode: "index", intersect: false },
      scales: { x: { ...b.scales.x, min: 0, title: { display: true, text: "kN" }, ticks: { callback: (v) => fmt(v, 0) } }, y: { ...b.scales.y, grid: { display: false } } },
      plugins: { ...b.plugins, tooltip: { ...b.plugins.tooltip, callbacks: { label: (it) => `${it.dataset.label}: ${fmt(it.raw, 0)} kN` } } } },
  });
}

/* ------------------------------------------------------------------ alternativas */
function resumen(datos, r) {
  return { pisos: r.niveles.length, Wt: r.parametros.Wt, VsX: r.fhe.X.Vs, VsY: r.fhe.Y.Vs, Tx: r.fhe.X.T_diseno, Ty: r.fhe.Y.T_diseno,
    dX: r.deriva_max_pct.X, dY: r.deriva_max_pct.Y, Q: r.Q_max, R: r.R, tor: r.torsion_ratio,
    cumple: r.dictamen.derivas && r.dictamen.estabilidad, lim: 100 * (datos.limite_deriva ?? 0.01) };
}
function guardarAlternativa() {
  if (!estado.ultimo) return;
  const { datos, r } = estado.ultimo;
  let nombre = (datos.id || `Alternativa ${estado.alternativas.length + 1}`).trim();
  let k = 2; const base = nombre;
  while (estado.alternativas.some((a) => a.nombre === nombre)) nombre = `${base} (${k++})`;
  estado.alternativas.push({ nombre, fecha: new Date().toISOString(), datos, s: resumen(datos, r) });
  guardarLocal(CLAVE_ALT, estado.alternativas);
  pintarComparar();
  aviso(`«${nombre}» guardada. Cambie los datos y verifique otra versión para compararlas.`);
}
function pintarComparar() {
  const alts = estado.alternativas;
  $("#n-alt").textContent = alts.length;
  $("#comparar-vacio").hidden = alts.length > 0;
  $("#comparar-lleno").hidden = alts.length === 0;
  if (!alts.length) return;
  $("#t-comparar").innerHTML = `<thead><tr><th>Alternativa</th><th>Pisos</th><th>Wt (kN)</th><th>Vs X (kN)</th><th>Tx (s)</th><th>Deriva X (%)</th><th>Deriva Y (%)</th><th>Q máx</th><th>R</th><th>Dictamen</th><th></th></tr></thead><tbody>${
    alts.map((a, i) => `<tr><td class="txt"><strong>${escapar(a.nombre)}</strong></td><td>${a.s.pisos}</td><td>${fmt(a.s.Wt, 0)}</td><td>${fmt(a.s.VsX, 0)}</td><td>${fmt(a.s.Tx, 3)}</td>
      <td class="${a.s.dX <= a.s.lim ? "ok" : "mal"}">${fmt(a.s.dX, 3)}</td><td class="${a.s.dY <= a.s.lim ? "ok" : "mal"}">${fmt(a.s.dY, 3)}</td>
      <td>${fmt(a.s.Q, 4)}</td><td>${fmt(a.s.R, 2)}</td><td class="txt ${a.s.cumple ? "ok" : "mal"}">${a.s.cumple ? "Cumple" : "No cumple"}</td>
      <td class="txt"><button class="btn btn-mini" data-cargar="${i}" type="button">Abrir</button> <button class="btn-x" data-borrar="${i}" type="button" aria-label="Borrar ${escapar(a.nombre)}">✕</button></td></tr>`).join("")}</tbody>`;
  $$("[data-cargar]").forEach((b) => b.addEventListener("click", () => { llenarFormulario(alts[+b.dataset.cargar].datos); verVista("verificar"); verificar(); }));
  $$("[data-borrar]").forEach((b) => b.addEventListener("click", () => { alts.splice(+b.dataset.borrar, 1); guardarLocal(CLAVE_ALT, alts); pintarComparar(); }));
  if (typeof Chart === "undefined" || $("#vista-comparar").hidden) return;
  const b = baseGrafica();
  const lim = alts[0].s.lim;
  nueva("g-comparar", { data: { labels: alts.map((a) => a.nombre), datasets: [
      { type: "bar", label: "Deriva máx. X", data: alts.map((a) => a.s.dX), backgroundColor: css("--serie-x"), borderRadius: 4, borderSkipped: "start", categoryPercentage: 0.7, barPercentage: 0.85 },
      { type: "bar", label: "Deriva máx. Y", data: alts.map((a) => a.s.dY), backgroundColor: css("--serie-y"), borderRadius: 4, borderSkipped: "start", categoryPercentage: 0.7, barPercentage: 0.85 },
      { type: "line", label: `Límite (${fmt(lim, 1)} %)`, data: alts.map(() => lim), borderColor: css("--mal"), borderDash: [6, 4], borderWidth: 1.5, pointRadius: 0 },
    ] },
    options: { ...b, interaction: { mode: "index", intersect: false },
      scales: { x: { ...b.scales.x, grid: { display: false } }, y: { ...b.scales.y, min: 0, suggestedMax: lim * 1.2, title: { display: true, text: "% de la altura de piso" }, ticks: { callback: (v) => fmt(v, 1) } } },
      plugins: { ...b.plugins, tooltip: { ...b.plugins.tooltip, callbacks: { label: (it) => `${it.dataset.label}: ${fmt(it.raw, 3)} %` } } } },
  });
}

/* ------------------------------------------------------------------ vistas y eventos */
function verVista(v) {
  ["verificar", "comparar", "ayuda"].forEach((k) => {
    $(`#vista-${k}`).hidden = k !== v;
    $(`#tab-${k}`).classList.toggle("activa", k === v);
  });
  if (v === "comparar") pintarComparar();
  if (location.hash.slice(1) !== v) history.replaceState(null, "", `#${v}`);
}

async function cargarEjemplo(verificarAlTerminar = true, avisar = true) {
  try {
    const d = await primero(CANDIDATOS("casos/caso1_completo.json"), "json");
    llenarFormulario(d);
    if (verificarAlTerminar && estado.py) verificar(); else revisar();
    if (avisar) aviso("Ejemplo cargado: edificio de oficinas de 5 pisos del curso (grupo 1, Bogotá, Piedemonte A), con datos de SAP2000.");
  } catch (e) { aviso("No se encontró el caso de ejemplo."); }
}

function conectar() {
  $$(".pestana").forEach((t) => t.addEventListener("click", () => verVista(t.dataset.vista)));
  $("#form").addEventListener("input", revisar);
  $("#form").addEventListener("change", revisar);
  $("#form").addEventListener("submit", (e) => { e.preventDefault(); verificar(); });
  $("#n-pisos").addEventListener("change", () => { filasPisos(nPisos()); revisar(); });
  $("#sistema-preset").addEventListener("change", (e) => { if (e.target.value !== "otro") { $("#sistema-R0").value = e.target.value.replace(".", ","); revisar(); } else $("#sistema-R0").focus(); });
  $("#btn-ejemplo").addEventListener("click", () => cargarEjemplo(true));
  $("#archivo-json").addEventListener("change", async (e) => {
    const f = e.target.files[0]; if (!f) return;
    try { llenarFormulario(JSON.parse(await f.text())); verificar(); aviso(`Abierto ${f.name}`); }
    catch (err) { aviso(`${f.name} no es un JSON válido.`); }
    e.target.value = "";
  });
  $("#btn-guardar-json").addEventListener("click", () => {
    const d = leerFormulario();
    descargar(`${(d.id || "edificio").replace(/[^\w-]+/g, "_")}.json`, JSON.stringify(d, null, 1), "application/json");
  });
  // pruebas del prototipo: parten del ejemplo completo y le introducen un solo defecto
  $("#prueba-fv").addEventListener("click", async () => {
    await cargarEjemplo(false, false);
    $("#sitio-Fv").value = ""; verificar();
    aviso("Prueba 2: ejemplo sin Fv. La herramienta se detiene y no inventa el valor.", 4500);
  });
  $("#prueba-cm").addEventListener("click", async () => {
    await cargarEjemplo(false, false);
    $("#hl-1").value = "350"; verificar();
    aviso("Prueba 3: altura libre del nivel 1 = 350 (escrita en centímetros). La herramienta la rechaza.", 4500);
  });
  // importador
  const dlg = $("#dlg-importar");
  $("#btn-importar").addEventListener("click", () => { $("#imp-msg").textContent = ""; dlg.showModal(); $("#imp-texto").focus(); });
  $("#imp-texto").addEventListener("input", () => {
    const t = interpretarTabla($("#imp-texto").value);
    $("#imp-mapa").hidden = t.tipo !== "sap";
    const msg = $("#imp-msg");
    if (t.tipo === "sap") {
      const nudos = [...new Set(t.filas.map((f) => f[t.cab.joint]))];
      msg.className = "imp-msg ok"; msg.textContent = `Tabla de SAP2000: ${t.filas.length} filas, ${nudos.length} nudos (${nudos.slice(0, 12).join(", ")}${nudos.length > 12 ? "…" : ""}).`;
    } else if (t.tipo === "nexo") { msg.className = "imp-msg ok"; msg.textContent = `Formato Nexo: ${t.filas.length} filas.`; }
    else { msg.className = "imp-msg"; msg.textContent = ""; }
  });
  $("#imp-aplicar").addEventListener("click", () => { if (importarTabla()) dlg.close(); });
  // exportar
  $("#btn-alternativa").addEventListener("click", guardarAlternativa);
  const reporteTxt = () => estado.py.reporte(estado.ultimo.r, estado.ultimo.datos.id || "Verificación NSR-10");
  $("#btn-copiar").addEventListener("click", async () => {
    try { await navigator.clipboard.writeText(reporteTxt()); aviso("Reporte copiado al portapapeles."); }
    catch (e) { aviso("No se pudo copiar; use Descargar reporte."); }
  });
  $("#btn-txt").addEventListener("click", () => descargar(`reporte_${(estado.ultimo.datos.id || "edificio").replace(/[^\w-]+/g, "_")}.txt`, reporteTxt(), "text/plain;charset=utf-8"));
  $("#btn-csv").addEventListener("click", () => {
    const fila = estado.py.registro(estado.ultimo.datos, estado.ultimo.r);
    const celda = (v) => { const s = typeof v === "object" && v !== null ? JSON.stringify(v) : String(v ?? ""); return /[",\n]/.test(s) ? `"${s.replace(/"/g, '""')}"` : s; };
    descargar("registro_base_NSR10.csv", "﻿" + Object.keys(fila).join(",") + "\n" + Object.values(fila).map(celda).join(",") + "\n", "text/csv;charset=utf-8");
  });
  $("#btn-imprimir").addEventListener("click", () => window.print());
  $("#btn-borrar-alt").addEventListener("click", () => { estado.alternativas = []; guardarLocal(CLAVE_ALT, []); pintarComparar(); });
  matchMedia("(prefers-color-scheme: dark)").addEventListener("change", () => { pintarGraficas(); pintarComparar(); });
  addEventListener("hashchange", () => { const v = location.hash.slice(1); if (["verificar", "comparar", "ayuda"].includes(v)) verVista(v); });
}

(async function inicio() {
  conectar();
  estado.alternativas = leerLocal(CLAVE_ALT, []);
  $("#n-alt").textContent = estado.alternativas.length;
  filasPisos(5);
  pintarDesplazamientos();
  const v = location.hash.slice(1);
  verVista(["verificar", "comparar", "ayuda"].includes(v) ? v : "verificar");
  primero(CANDIDATOS("equipo.json"), "json").then((e) => { $("#equipo-nombres").textContent = e.integrantes.map((p) => p.nombre).join(" · "); }).catch(() => {});
  const ejemplo = cargarEjemplo(false);
  const listo = await iniciarMotor();
  await ejemplo;
  if (listo) verificar();
})();
