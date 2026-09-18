# File:  cell.py
# Author:  R-Sh1ki
# E-mail:  ryougi.shiki.kong@outlook.com
# Created Time: 2026-09-17 16:13:07
# ---------------------------------------------------
# Modified By: R-Sh1ki
# Modified Time: 2026-09-17 16:33:12

from __future__ import annotations

import ast
import textwrap
from pathlib import Path

type CellNode = ast.FunctionDef | ast.AsyncFunctionDef | ast.ClassDef


class CellSource:
    def __init__(self, notebook: str | Path) -> None:
        self.notebook = Path(notebook)

        if not self.notebook.exists():
            raise FileNotFoundError(f"Notebook not found: {self.notebook}")

        self.source = self.notebook.read_text(encoding="utf-8")

        self.tree = ast.parse(self.source, filename=str(self.notebook))

    def _find_cell(self, name: str) -> CellNode:
        for node in self.tree.body:
            if not isinstance(
                node, (ast.FunctionDef, ast.AsyncFunctionDef, ast.ClassDef)
            ):
                continue

            if node.name == name and self._is_marimo_cell(node):
                return node

        raise ValueError(f"Cannot find marimo cell: {name!r}")

    def _is_marimo_cell(self, node: CellNode) -> bool:
        for decorator in node.decorator_list:
            target = decorator.func if isinstance(decorator, ast.Call) else decorator

            if isinstance(target, ast.Attribute) and target.attr in {
                "cell",
                "class_definition",
            }:
                return True

        return False

    def get_cell(self, name: str) -> str:
        node = self._find_cell(name)

        start = min(
            [decorator.lineno for decorator in node.decorator_list] or [node.lineno]
        )

        lines = self.source.splitlines()

        return "\n".join(lines[start - 1 : node.end_lineno])

    def get_body(self, name: str) -> str:
        node = self._find_cell(name)

        # Reusable top-level classes are serialized directly as
        # @app.class_definition, so the node itself is the cell body.
        if isinstance(node, ast.ClassDef):
            lines = self.source.splitlines()
            return "\n".join(lines[node.lineno - 1 : node.end_lineno])

        if not node.body:
            return ""

        start = node.body[0].lineno
        end = node.body[-1].end_lineno

        lines = self.source.splitlines()

        body = "\n".join(lines[start - 1 : end])

        return textwrap.dedent(body)

    def get_markdown(self, name: str) -> str:
        node = self._find_cell(name)

        for child in ast.walk(node):
            if not isinstance(child, ast.Call):
                continue

            func = child.func

            if not isinstance(func, ast.Attribute) or func.attr != "md":
                continue

            if not child.args:
                continue

            arg = child.args[0]

            if isinstance(arg, ast.Constant) and isinstance(arg.value, str):
                return arg.value

        raise ValueError(f"Cell {name!r} does not contain mo.md(...)")

    def get_solution(self, class_name: str = "Solution") -> str:
        node = self._find_cell(class_name)

        if not isinstance(node, ast.ClassDef):
            raise TypeError(f"Cell {class_name!r} is not a class definition")

        lines = self.source.splitlines()

        return "\n".join(lines[node.lineno - 1 : node.end_lineno])
