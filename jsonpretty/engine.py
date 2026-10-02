"""Parse / pretty / minify JSON."""

from __future__ import annotations

import json
from dataclasses import dataclass


@dataclass
class Result:
    ok: bool
    text: str
    error: str = ""


def _parse(raw: str) -> tuple[object | None, str]:
    text = raw.strip()
    if not text:
        return None, "пусто"
    try:
        return json.loads(text), ""
    except json.JSONDecodeError as exc:
        return None, f"ошибка JSON: строка {exc.lineno}, кол. {exc.colno} — {exc.msg}"


def pretty(raw: str, indent: int = 2) -> Result:
    data, err = _parse(raw)
    if err:
        return Result(False, raw, err)
    out = json.dumps(data, ensure_ascii=False, indent=indent)
    return Result(True, out)


def minify(raw: str) -> Result:
    data, err = _parse(raw)
    if err:
        return Result(False, raw, err)
    out = json.dumps(data, ensure_ascii=False, separators=(",", ":"))
    return Result(True, out)
