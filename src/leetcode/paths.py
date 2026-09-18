# File:  paths.py
# Author:  R-Sh1ki
# E-mail:  ryougi.shiki.kong@outlook.com
# Created Time: 2026-09-17 13:53:08
# ---------------------------------------------------
# Modified By: R-Sh1ki
# Modified Time: 2026-09-17 14:04:39


from pathlib import Path


def find_project_root() -> Path:
    current = Path.cwd().resolve()

    for path in (current, *current.parents):
        if (path / "pyproject.toml").exists():
            return path

    raise RuntimeError("Cannot find project root: pyproject.toml not found")


projectRoot = find_project_root()

problemsDir = projectRoot / "problems"
catalogPath = problemsDir / "catalog.db"
notebookDir = projectRoot / "notebooks"
archiveDir = notebookDir / "archive"
