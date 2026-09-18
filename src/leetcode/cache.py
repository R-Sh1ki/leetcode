# File:  cache.py
# Author:  R-Sh1ki
# E-mail:  ryougi.shiki.kong@outlook.com
# Created Time: 2026-09-16 13:11:37
# ---------------------------------------------------
# Modified By: R-Sh1ki
# Modified Time: 2026-09-17 14:05:05


from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from .paths import problemsDir


def problem_path(slug: str) -> Path:
    return problemsDir / f"{slug}.json"


def exists(slug: str) -> bool:
    return problem_path(slug).exists()


def load(slug: str) -> dict[str, Any]:
    path = problem_path(slug)

    if not path.exists():
        raise FileNotFoundError(f"Problem cache does not exist: {path}")

    return json.loads(path.read_text(encoding="utf-8"))


def save(slug: str, data: dict[str, Any]) -> Path:
    problemsDir.mkdir(parents=True, exist_ok=True)

    path = problem_path(slug)

    path.write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8")

    return path
