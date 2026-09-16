# File:  problem.py
# Author:  R-Sh1ki
# E-mail:  ryougi.shiki.kong@outlook.com
# Created Time: 2026-09-16 13:21:22
# ---------------------------------------------------
# Modified By: R-Sh1ki
# Modified Time: 2026-09-16 21:56:10


from __future__ import annotations

import json
from dataclasses import dataclass
from typing import Any

from .testcase import TestCase


@dataclass
class Problem:
    data: dict[str, Any]

    @property
    def id(self) -> str:
        return self.data["questionFrontendId"]

    @property
    def question_id(self) -> str:
        return self.data["questionId"]

    @property
    def slug(self) -> str:
        return self.data["titleSlug"]

    @property
    def title(self) -> str:
        return self.data["title"]

    @property
    def translated_title(self) -> str | None:
        return self.data.get("translatedTitle")

    @property
    def display_title(self) -> str:
        return self.translated_title or self.title

    @property
    def difficulty(self) -> str:
        return self.data["difficulty"]

    @property
    def content(self) -> str:
        return self.data.get("content") or ""

    @property
    def translated_content(self) -> str:
        return self.data.get("translatedContent") or ""

    @property
    def display_content(self) -> str:
        return self.translated_content or self.content

    @property
    def topics(self) -> list[str]:
        result = []

        for tag in self.data.get("topicTags", []):
            name = tag.get("name") or tag.get("translatedName")

            if name:
                result.append(name)

        return result

    @property
    def sample_test_case(self) -> str:
        return self.data.get("sampleTestCase") or ""

    @property
    def example_testcases(self) -> str:
        return self.data.get("exampleTestcases") or ""

    @property
    def example_outputs(self) -> list[str]:
        return self.data.get("exampleOutputs") or []

    def code_template(self, lang: str = "python3") -> str:
        for snippet in self.data.get("codeSnippets", []):
            if snippet.get("langSlug") == lang:
                return snippet["code"]

        raise ValueError(f"No code template for language: {lang}")

    @property
    def url(self) -> str:
        return f"https://leetcode.cn/problems/{self.slug}/"

    @property
    def metadata(self) -> dict[str, Any]:
        raw = self.data.get("metaData")

        if not raw:
            return {}

        return json.loads(raw)

    @property
    def local_tests(self) -> list[TestCase]:
        return [TestCase.from_dict(item) for item in self.data.get("localTests", [])]

    def add_local_test(
        self,
        testcase: TestCase,
    ) -> None:
        self.data.setdefault("localTests", [])

        self.data["localTests"].append(testcase.to_dict())
