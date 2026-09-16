# File:  catalog.py
# Author:  R-Sh1ki
# E-mail:  ryougi.shiki.kong@outlook.com
# Created Time: 2026-09-16 22:24:31
# ---------------------------------------------------
# Modified By: R-Sh1ki
# Modified Time: 2026-09-16 23:24:27


from __future__ import annotations

import json
from pathlib import Path
from typing import Any


class Catalog:
    def __init__(self, path: str | Path) -> None:
        self.path = Path(path)

        self.problems: dict[str, dict[str, Any]] = {}
        self.tags: dict[str, list[str]] = {}

        self.load()

    def load(self) -> None:
        if not self.path.exists():
            return

        data = json.loads(self.path.read_text(encoding="utf-8"))

        self.problems = data.get("problems", {})
        self.tags = data.get("tags", {})

    def save(self) -> None:
        self.path.parent.mkdir(parents=True, exist_ok=True)
        data = {
            "problems": self.problems,
            "tags": self.tags,
        }

        self.path.write_text(
            json.dumps(
                data,
                ensure_ascii=False,
                indent=2,
            ),
            encoding="utf-8",
        )

    def build(self, questions: list[dict]) -> None:
        self.problems = {}
        self.tags = {}

        for question in questions:
            problem_id = str(question["questionFrontendId"])
            tags = [tag["slug"] for tag in question.get("topicTags", [])]
            title = question.get("translatedTitle") or question["title"]
            status = question.get("status") or "TO_DO"

            self.problems[problem_id] = {
                "slug": question["titleSlug"],
                "title": title,
                "difficulty": question["difficulty"],
                "paidOnly": question.get("PaidOnly", False),
                "tags": tags,
                "status": status,
                "remoteSolved": (question.get("status") == "SOLVED"),
            }

            for tag in tags:
                self.tags.setdefault(tag, []).append(problem_id)

        self._sort()
        self.save()

    def _sort(self) -> None:
        def problem_sort_key(problem_id: str):
            try:
                return (0, int(problem_id))
            except ValueError:
                return (1, problem_id)

        self.problems = dict(
            sorted(
                self.problems.items(),
                key=lambda item: problem_sort_key(item[0]),
            )
        )

        self.tags = {
            tag: sorted(
                problem_ids,
                key=problem_sort_key,
            )
            for tag, problem_ids in sorted(self.tags.items())
        }

    def get(self, problem_id: str | int) -> dict | None:
        return self.problems.get(str(problem_id))

    def get_by_slug(self, slug: str) -> dict | None:
        for problem in self.problems.values():
            if problem["slug"] == slug:
                return problem

        return None

    def get_by_tag(self, tag: str) -> list[dict]:
        problem_ids = self.tags.get(
            tag,
            [],
        )

        return [
            {
                "id": problem_id,
                **self.problems[problem_id],
            }
            for problem_id in problem_ids
        ]

    def solved(self) -> list[dict]:
        return [
            {
                "id": problem_id,
                **problem,
            }
            for problem_id, problem in self.problems.items()
            if problem["remoteSolved"]
        ]

    def unsolved(self) -> list[dict]:
        return [
            {
                "id": problem_id,
                **problem,
            }
            for problem_id, problem in self.problems.items()
            if not problem["remoteSolved"]
        ]
