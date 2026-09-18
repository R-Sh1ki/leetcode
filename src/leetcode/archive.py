# File:  archive.py
# Author:  R-Sh1ki
# E-mail:  ryougi.shiki.kong@outlook.com
# Created Time: 2026-09-17 13:41:15
# ---------------------------------------------------
# Modified By: R-Sh1ki
# Modified Time: 2026-09-18 12:09:29


from __future__ import annotations

from pathlib import Path

from .paths import archiveDir
from .problem import Problem
from .render import problem_md


class Archive:
    def __init__(self, archive_dir: Path = archiveDir) -> None:
        self.archive_dir = archive_dir

    def archive(self, problem: Problem, topic: str, code: str, note: str = "") -> Path:
        topic = problem.topic_slug(topic)

        notebook = self.archive_dir / f"{topic}.py"

        self._ensure_notebook(notebook)

        block = self._create_archive_block(problem=problem, code=code, note=note)

        self._write_block(notebook, problem.slug, block)

        return notebook

    def _ensure_notebook(self, path: Path) -> None:
        if path.exists():
            return

        path.parent.mkdir(parents=True, exist_ok=True)

        content = """\
import marimo

app = marimo.App(width="medium")


@app.cell
def _():
    import marimo as mo
    return (mo,)


if __name__ == "__main__":
    app.run()
"""
        path.write_text(content, encoding="utf-8")

    def _create_archive_block(self, problem: Problem, code: str, note: str) -> str:
        name = problem.slug.replace("-", "_")
        desc = problem_md(problem.display_content)

        return f'''

# >>> leetcode:{problem.slug}

@app.cell(hide_code=True)
def {name}_problem(mo):
    mo.md(r"""
# {problem.id}. {problem.display_title}

{desc}
""")
    return


@app.cell(hide_code=True)
def {name}_note(mo):
    mo.md(r"""
{note}
""")
    return


@app.cell(hide_code=True)
def {name}_code(mo):
    mo.md(r"""
```python
{code}
```
""")
    return


# <<< leetcode:{problem.slug}

'''

    def _write_block(self, path: Path, slug: str, block: str) -> None:
        content = path.read_text(encoding="utf-8")

        start = f"# >>> leetcode:{slug}"
        end = f"# <<< leetcode:{slug}"

        if start in content and end in content:
            before, rest = content.split(start, maxsplit=1)
            _, after = rest.split(end, maxsplit=1)
            path.write_text(before + block.strip("\n") + after, encoding="utf-8")
            return

        marker = '\nif __name__ == "__main__":\n    app.run()\n'

        if marker not in content:
            raise RuntimeError(f"Invalid marimo notebook: {path}")

        content = content.replace(marker, block + marker)

        path.write_text(content, encoding="utf-8")
