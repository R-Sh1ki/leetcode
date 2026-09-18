# File:  render.py
# Author:  R-Sh1ki
# E-mail:  ryougi.shiki.kong@outlook.com
# Created Time: 2026-09-16 13:30:50
# ---------------------------------------------------
# Modified By: R-Sh1ki
# Modified Time: 2026-09-18 10:44:23


from __future__ import annotations

import marimo as mo
from bs4 import BeautifulSoup
from markdownify import markdownify

from .problem import Problem


def problem_md(content: str) -> str:
    soup = BeautifulSoup(content, "html.parser")

    for code in soup.find_all("code"):
        code.unwrap()

    return markdownify(str(soup), heading_style="ATX", sup_symbol="^", sub_symbol="~")


def render_problem(problem: Problem):
    info = mo.hstack(
        [
            mo.icon("lucide:gauge"),
            mo.md(problem.difficulty),
            mo.icon("lucide:tags"),
            mo.md(" · ".join(problem.topics)),
            mo.icon("lucide:external-link"),
            mo.md(f"[{problem.slug}]({problem.url})"),
        ],
        justify="start",
        align="center",
    )

    return mo.md(rf"""
## {problem.id}. {problem.display_title}

{info}

---

{problem_md(problem.display_content)}
""")
