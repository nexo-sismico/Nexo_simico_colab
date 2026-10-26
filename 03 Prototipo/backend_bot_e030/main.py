"""API privada para los tres workflows RC Bot y el modelo E.030 del proyectoGH."""
from __future__ import annotations

import hashlib
import json
import math
import os
import sqlite3
import sys
import unicodedata
import uuid
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

import joblib
import numpy as np
import pandas as pd
from fastapi import Depends, FastAPI, Header, HTTPException
from fastapi.responses import Response
from pydantic import BaseModel, Field

ROOT = Path(__file__).resolve().parent
COLUMNS = json.loads((ROOT / "diccionario_columnas.json").read_text(encoding="utf-8"))
sys.path.insert(0, str(ROOT))  # joblib guarda estimadores definidos en modelos_mejorados.py
PACKAGE = joblib.load(ROOT / "modelo_final.joblib")
INPUTS: list[str] = PACKAGE["entradas"]
DOMAIN: dict[str, dict[str, Any]] = PACKAGE["dominio"]
TARGETS: list[str] = PACKAGE["objetivos"]
MODEL_SHA256 = hashlib.sha256((ROOT / "modelo_final.joblib").read_bytes()).hexdigest()
DB_PATH = Path(os.getenv("BOT_DB_PATH", str(ROOT / "consultas.sqlite3")))
API_TOKEN = os.getenv("BOT_API_TOKEN", "")

app = FastAPI(title="Nexo Sísmico · Backend RC Bot", version="0.1.0")


class ValidationRequest(BaseModel):
    session_id: str = Field(min_length=1, max_length=160)
    parametros: dict[str, Any]
    unidades: dict[str, str] = Field(default_factory=dict)
    supuestos_aceptados: list[Any] = Field(default_factory=list)


class QueryRequest(ValidationRequest):
    chat_id: str = Field(default="", max_length=80)
    user_id: str = Field(default="", max_length=80)
    idempotency_key: str = Field(min_length=1, max_length=240)


def require_api_key(authorization: str | None = Header(default=None)) -> None:
    if not API_TOKEN:
        raise HTTPException(503, "El backend no tiene BOT_API_TOKEN configurado.")
    if authorization != f"Bearer {API_TOKEN}":
        raise HTTPException(401, "Credencial no válida.")


def connect_db() -> sqlite3.Connection:
    DB_PATH.parent.mkdir(parents=True, exist_ok=True)
    db = sqlite3.connect(DB_PATH, timeout=15)
    db.execute("PRAGMA journal_mode=WAL")
    db.execute("""CREATE TABLE IF NOT EXISTS consultas (
        consulta_id TEXT PRIMARY KEY,
        idempotency_key TEXT NOT NULL UNIQUE,
        resultado_json TEXT NOT NULL,
        creada_en TEXT NOT NULL
    )""")
    retention_days = max(1, int(os.getenv("BOT_RETENTION_DAYS", "7")))
    cutoff = datetime.now(timezone.utc).timestamp() - retention_days * 86400
    cutoff_iso = datetime.fromtimestamp(cutoff, timezone.utc).isoformat()
    db.execute("DELETE FROM consultas WHERE creada_en < ?", (cutoff_iso,))
    return db


def metadata_for(name: str) -> dict[str, Any]:
    d = DOMAIN.get(name, {})
    c = COLUMNS.get(name, {})
    return {
        "descripcion": c.get("descripcion", name),
        "unidad": c.get("unidad", ""),
        "minimo": d.get("min"),
        "maximo": d.get("max"),
        "valores_permitidos": d.get("valores"),
        "admite_ausencia": bool(d.get("admite_ausencia", False)),
    }


def normalize_unit(value: str) -> str:
    text = unicodedata.normalize("NFKD", value.lower())
    text = "".join(ch for ch in text if not unicodedata.combining(ch))
    text = text.replace("²", "2").replace("³", "3")
    return "".join(ch for ch in text if ch.isalnum())


def unit_matches(supplied: str, expected: str) -> bool:
    if "adimensional" in expected.lower():
        return normalize_unit(supplied) in {"adimensional", "1", "categoria", "adimensionalcategoria"}
    return normalize_unit(supplied) == normalize_unit(expected)


def validate(req: ValidationRequest) -> tuple[pd.DataFrame | None, list[str], list[str]]:
    p = req.parametros
    unknown = sorted(set(p) - set(INPUTS))
    missing = [k for k in INPUTS if k not in p and not DOMAIN[k].get("admite_ausencia", False)]
    errors: list[str] = []
    if unknown:
        errors.append("Parámetros desconocidos: " + ", ".join(unknown[:15]))
    if missing:
        errors.append("Faltan entradas del modelo: " + ", ".join(missing[:20]))
    if errors:
        return None, errors, []

    row: dict[str, float] = {}
    out_of_domain: list[str] = []
    for name in INPUTS:
        value = p.get(name)
        if value is None or value == "":
            row[name] = np.nan
            if not DOMAIN[name].get("admite_ausencia", False):
                errors.append(f"Falta {name}.")
            continue
        if isinstance(value, bool):
            errors.append(f"{name} debe ser numérico, no booleano.")
            continue
        try:
            number = float(value)
        except (TypeError, ValueError):
            errors.append(f"{name} debe ser numérico.")
            continue
        if not math.isfinite(number):
            errors.append(f"{name} debe ser finito.")
            continue
        row[name] = number
        expected_unit = metadata_for(name)["unidad"]
        supplied_unit = req.unidades.get(name, "")
        if not supplied_unit:
            errors.append(f"Indique la unidad de {name} ({expected_unit}).")
        elif not unit_matches(supplied_unit, expected_unit):
            errors.append(f"Unidad incorrecta para {name}: use {expected_unit}; se recibió {supplied_unit}.")
        d = DOMAIN[name]
        if number < d["min"] or number > d["max"]:
            out_of_domain.append(f"{name}={number:g} fuera del rango entrenado [{d['min']:g}, {d['max']:g}].")
        allowed = d.get("valores")
        if allowed is not None and number not in allowed:
            out_of_domain.append(f"{name}={number:g} no está entre los valores de entrenamiento: {allowed}.")

    if out_of_domain:
        errors.extend(out_of_domain)
    if errors:
        return None, errors, out_of_domain

    frame = pd.DataFrame([{k: row.get(k, np.nan) for k in INPUTS}], columns=INPUTS)
    for axis in ("X", "Y"):
        count = int(frame.at[0, f"vanos_{axis}"])
        spans = [frame.at[0, f"luz_{axis}_{i}_cm"] for i in range(1, 6)]
        active = spans[:count]
        inactive = spans[count:]
        if any(pd.isna(x) or x <= 0 for x in active):
            errors.append(f"Complete las luces de los {count} vanos {axis}.")
        if any(not pd.isna(x) for x in inactive):
            errors.append(f"Deje vacíos los vanos {axis} inexistentes.")
        total = frame.at[0, f"L{axis.lower()}_cm"]
        if not errors and not np.isclose(sum(active), total, rtol=1e-8, atol=1e-6):
            errors.append(f"La suma de luces {axis} no coincide con la dimensión total.")
    return (None if errors else frame), errors, out_of_domain


def make_result(req: QueryRequest, frame: pd.DataFrame, query_id: str) -> dict[str, Any]:
    predictions = []
    per_model: dict[str, str] = {}
    for target in TARGETS:
        estimator = PACKAGE["modelos"][target]
        value = float(estimator.predict(frame)[0])
        config = getattr(estimator, "configuracion", None)
        if config is None and getattr(estimator, "modelos", None):
            config = "+".join(getattr(m, "configuracion", "modelo") for m in estimator.modelos)
        per_model[target] = config or type(estimator).__name__
        unit = "s" if target in ("Tx_s", "Ty_s") else (
            "kgf" if target.startswith("V_modal") else (
                "cm" if target.startswith("desplazamiento") else "adimensional"))
        predictions.append({"nombre": target, "valor": value, "unidad": unit})

    now = datetime.now(timezone.utc).isoformat()
    input_rows = [{
        "nombre": key,
        "valor": None if pd.isna(frame.iloc[0][key]) else float(frame.iloc[0][key]),
        "unidad": metadata_for(key)["unidad"],
    } for key in INPUTS]
    normalized = {k: input_rows[i]["valor"] for i, k in enumerate(INPUTS)}
    return {
        "consulta_id": query_id,
        "estado": "completada",
        "creada_en": now,
        "parametros_confirmados": normalized,
        "unidades": {k: metadata_for(k)["unidad"] for k in INPUTS},
        "supuestos_aceptados": req.supuestos_aceptados,
        "propiedades_calculadas": {},
        "unidades_propiedades": {},
        "predicciones": predictions,
        "modelo": {
            "id": "modelo_final.joblib · modelos seleccionados por respuesta",
            "version": MODEL_SHA256[:12],
            "archivo": "modelo_final.joblib",
            "configuracion_por_respuesta": per_model,
        },
        "metodologia": "Predicción del modelo final E.030 entrenado con estructuras generadas y familias separadas. Las respuestas pueden usar configuraciones distintas por objetivo. No es análisis estructural ni verificación normativa.",
        "referencias_verificadas": [{
            "texto": "Repositorio ProyectoGH de Jean Piere Velásquez Quispe; artefacto modelo_final.joblib.",
            "url": "https://github.com/PieroVQ/ProyectoGH",
        }],
        "entradas_107": input_rows,
        "archivos": [],
        "metricas_originales": {},
    }


@app.get("/health")
def health() -> dict[str, str]:
    return {"estado": "ok", "servicio": "Nexo Sísmico RC Bot"}


@app.get("/schema", dependencies=[Depends(require_api_key)])
def schema() -> dict[str, Any]:
    return {
        "nombre": "Modelo E.030 para pórticos de concreto",
        "unidades_generales": "cm, kgf, s; esfuerzos kgf/cm²",
        "nota": "Se requieren las entradas técnicas indicadas. No complete valores ausentes por inferencia. No es diseño ni verificación normativa.",
        "entradas": INPUTS,
        "campos": {
            k: {
                "descripcion": metadata_for(k)["descripcion"],
                "unidad": metadata_for(k)["unidad"],
                "min": DOMAIN[k]["min"],
                "max": DOMAIN[k]["max"],
                "valores": DOMAIN[k].get("valores"),
                "opcional": bool(DOMAIN[k].get("admite_ausencia", False)),
            }
            for k in INPUTS
        },
        "objetivos": TARGETS,
        "modelo_sha256_prefijo": MODEL_SHA256[:12],
    }


@app.post("/consultas/validar", dependencies=[Depends(require_api_key)])
def validate_endpoint(req: ValidationRequest) -> dict[str, Any]:
    frame, errors, out_domain = validate(req)
    if errors:
        return {
            "valido": False,
            "fuera_de_dominio": bool(out_domain),
            "errores": errors,
            "aclaraciones": [],
            "supuestos_propuestos": [],
            "secciones_propuestas": [],
        }
    return {
        "valido": True,
        "fuera_de_dominio": False,
        "errores": [],
        "aclaraciones": [],
        "supuestos_propuestos": [],
        "secciones_propuestas": [],
        "resumen_legible": f"Estructura dentro del dominio de entrenamiento. Se verificaron {len(INPUTS)} entradas y coherencia de luces. Modelo E.030, unidades cm, kgf y s. La predicción no constituye diseño ni verificación normativa.",
        "parametros_confirmados": req.parametros,
        "unidades": req.unidades,
        "supuestos_aceptados": req.supuestos_aceptados,
    }


@app.post("/consultas", dependencies=[Depends(require_api_key)])
def create_query(req: QueryRequest) -> dict[str, Any]:
    frame, errors, out_domain = validate(req)
    if errors or frame is None:
        raise HTTPException(422, detail={"errores": errors, "fuera_de_dominio": bool(out_domain)})
    # session_id/idempotency_key are derived from Telegram identifiers upstream;
    # retain only a one-way digest, never their raw values.
    idempotency_digest = hashlib.sha256(req.idempotency_key.encode("utf-8")).hexdigest()
    with connect_db() as db:
        existing = db.execute(
            "SELECT consulta_id, resultado_json FROM consultas WHERE idempotency_key=?",
            (idempotency_digest,),
        ).fetchone()
        if existing:
            return {"consulta_id": existing[0], "estado": "completada"}
        query_id = str(uuid.uuid4())
        try:
            result = make_result(req, frame, query_id)
        except Exception as exc:
            raise HTTPException(500, "No se pudo ejecutar el modelo de predicción.") from exc
        db.execute(
            "INSERT INTO consultas(consulta_id,idempotency_key,resultado_json,creada_en) VALUES(?,?,?,?)",
            (query_id, idempotency_digest, json.dumps(result, ensure_ascii=False, allow_nan=False), result["creada_en"]),
        )
    return {"consulta_id": query_id, "estado": "completada"}


@app.get("/consultas/{consulta_id}", dependencies=[Depends(require_api_key)])
def get_query(consulta_id: str) -> dict[str, Any]:
    with connect_db() as db:
        row = db.execute("SELECT resultado_json FROM consultas WHERE consulta_id=?", (consulta_id,)).fetchone()
    if not row:
        raise HTTPException(404, "Consulta no encontrada.")
    return json.loads(row[0])


@app.get("/consultas/{consulta_id}/archivos/{archivo_id}", dependencies=[Depends(require_api_key)])
def get_file(consulta_id: str, archivo_id: str) -> Response:
    raise HTTPException(404, "Esta consulta no contiene el archivo solicitado.")
