# File:  testcase.py
# Author:  R-Sh1ki
# E-mail:  ryougi.shiki.kong@outlook.com
# Created Time: 2026-09-16 20:46:03
# ---------------------------------------------------
# Modified By: R-Sh1ki
# Modified Time: 2026-09-16 21:56:01


from __future__ import annotations

import ast
import json
from dataclasses import dataclass
from typing import Any


@dataclass
class TestCase:
    args: list[Any]
    expected: Any
    source: str = "manual"

    @classmethod
    def from_dict(cls, data: dict) -> TestCase:
        return cls(
            args=data["args"],
            expected=data["expected"],
            source=data.get("source", "manual"),
        )

    def to_dict(self) -> dict:
        return {
            "source": self.source,
            "args": self.args,
            "expected": self.expected,
        }


def parse_value(value: str) -> Any:
    value = value.strip()

    try:
        return json.loads(value)
    except json.JSONDecodeError:
        pass

    try:
        return ast.literal_eval(value)
    except (ValueError, SyntaxError):
        return value
