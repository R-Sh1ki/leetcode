# File:  render.py
# Author:  R-Sh1ki
# E-mail:  ryougi.shiki.kong@outlook.com
# Created Time: 2026-09-16 13:30:50
# ---------------------------------------------------
# Modified By: R-Sh1ki
# Modified Time: 2026-09-16 16:42:55


from __future__ import annotations

import marimo as mo

from .problem import Problem


def problem_md(problem: Problem):
    tags = " · ".join(problem.topics)

    return mo.md(f"""
## {problem.id}. {problem.title}

**Difficulty:** {problem.difficulty}, **Tags:** {tags}, [LeetCode 题目页面]({problem.url})

---

{problem.display_content}
""")
