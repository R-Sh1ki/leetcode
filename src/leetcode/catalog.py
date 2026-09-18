# File:  catalog.py
# Author:  R-Sh1ki
# E-mail:  ryougi.shiki.kong@outlook.com
# Created Time: 2026-09-16 22:24:31
# ---------------------------------------------------
# Modified By: R-Sh1ki
# Modified Time: 2026-09-18


from __future__ import annotations

import sqlite3
from pathlib import Path
from typing import Any


class Catalog:
    def __init__(self, path: str | Path) -> None:
        self.path = Path(path)
        self.path.parent.mkdir(parents=True, exist_ok=True)

        self.connection = sqlite3.connect(self.path)
        self.connection.row_factory = sqlite3.Row

        self._create_tables()

    def _create_tables(self) -> None:
        self.connection.executescript(
            """
            CREATE TABLE IF NOT EXISTS problems (
                id TEXT PRIMARY KEY,
                slug TEXT UNIQUE NOT NULL,
                title TEXT NOT NULL,
                difficulty TEXT NOT NULL,
                paid_only INTEGER NOT NULL,
                remote_status TEXT NOT NULL,
                archived INTEGER NOT NULL DEFAULT 0
            );

            CREATE TABLE IF NOT EXISTS topics (
                slug TEXT PRIMARY KEY,
                name TEXT NOT NULL,
                translated_name TEXT
            );

            CREATE TABLE IF NOT EXISTS problem_topics (
                problem_id TEXT NOT NULL,
                topic_slug TEXT NOT NULL,
                PRIMARY KEY (problem_id, topic_slug),
                FOREIGN KEY (problem_id) REFERENCES problems(id),
                FOREIGN KEY (topic_slug) REFERENCES topics(slug)
            );
            """
        )

    def build(self, questions: list[dict[str, Any]]) -> None:
        archived = {
            row["id"]: row["archived"]
            for row in self.connection.execute(
                "SELECT id, archived FROM problems"
            ).fetchall()
        }
        problems = []
        topics = {}
        problem_topics = []

        for question in questions:
            problem_id = str(question["questionFrontendId"])

            problems.append(
                (
                    problem_id,
                    question["titleSlug"],
                    question.get("translatedTitle") or question["title"],
                    question["difficulty"],
                    question.get("paidOnly", False),
                    question.get("status") or "TO_DO",
                    archived.get(problem_id, False),
                )
            )

            for topic in question.get("topicTags", []):
                topic_slug = topic["slug"]
                topics[topic_slug] = (
                    topic_slug,
                    topic["name"],
                    topic.get("nameTranslated") or topic.get("translatedName"),
                )
                problem_topics.append((problem_id, topic_slug))

        with self.connection:
            self.connection.execute("DELETE FROM problem_topics")
            self.connection.execute("DELETE FROM topics")
            self.connection.execute("DELETE FROM problems")

            self.connection.executemany(
                "INSERT INTO problems VALUES (?, ?, ?, ?, ?, ?, ?)",
                problems,
            )
            self.connection.executemany(
                "INSERT INTO topics VALUES (?, ?, ?)",
                topics.values(),
            )
            self.connection.executemany(
                "INSERT INTO problem_topics VALUES (?, ?)",
                problem_topics,
            )

    def _all(self, query: str, parameters: tuple = ()) -> list[dict]:
        rows = self.connection.execute(query, parameters).fetchall()
        return [dict(row) for row in rows]

    def get(self, problem_id: str | int) -> dict | None:
        row = self.connection.execute(
            "SELECT * FROM problems WHERE id = ?",
            (str(problem_id),),
        ).fetchone()

        return dict(row) if row else None

    def get_by_slug(self, slug: str) -> dict | None:
        row = self.connection.execute(
            "SELECT * FROM problems WHERE slug = ?",
            (slug,),
        ).fetchone()

        return dict(row) if row else None

    def get_by_topic(self, topic: str) -> list[dict]:
        return self._all(
            """
            SELECT problems.*
            FROM problems
            JOIN problem_topics
                ON problem_topics.problem_id = problems.id
            WHERE problem_topics.topic_slug = ?
            ORDER BY CAST(problems.id AS INTEGER)
            """,
            (topic,),
        )

    def solved(self) -> list[dict]:
        return self._all(
            """
            SELECT * FROM problems
            WHERE archived = 1
            ORDER BY CAST(id AS INTEGER)
            """
        )

    def unsolved(self) -> list[dict]:
        return self._all(
            """
            SELECT * FROM problems
            WHERE archived = 0
            ORDER BY CAST(id AS INTEGER)
            """
        )

    def remote_solved(self) -> list[dict]:
        return self._all(
            """
            SELECT * FROM problems
            WHERE remote_status = 'SOLVED'
            ORDER BY CAST(id AS INTEGER)
            """
        )

    def mark_archived(self, slug: str) -> None:
        with self.connection:
            self.connection.execute(
                "UPDATE problems SET archived = 1 WHERE slug = ?",
                (slug,),
            )

    def problem_count(self) -> int:
        return self.connection.execute("SELECT COUNT(*) FROM problems").fetchone()[0]

    def topic_count(self) -> int:
        return self.connection.execute("SELECT COUNT(*) FROM topics").fetchone()[0]
