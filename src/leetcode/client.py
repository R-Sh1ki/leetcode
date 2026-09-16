# File:  client.py
# Author:  R-Sh1ki
# E-mail:  ryougi.shiki.kong@outlook.com
# Created Time: 2026-09-16 13:01:05
# ---------------------------------------------------
# Modified By: R-Sh1ki
# Modified Time: 2026-09-16 19:50:53


from __future__ import annotations

import os
import time
from typing import Any

import requests
from dotenv import load_dotenv

base_url = "https://leetcode.cn"
graphQL_url = f"{base_url}/graphql"

question_query = """
query questionData($titleSlug: String!) {
  question(titleSlug: $titleSlug) {
    questionId
    questionFrontendId

    title
    titleSlug
    translatedTitle

    content
    translatedContent

    difficulty
    isPaidOnly

    topicTags {
      name
      translatedName
      slug
    }

    codeSnippets {
      lang
      langSlug
      code
    }

    hints

    sampleTestCase
    exampleTestcases

    metaData

    stats

    enableRunCode

    __typename
  }
}
"""

load_dotenv()


class LeetCodeClient:
    def __init__(self, timeout: float = 10.0) -> None:
        self.timeout = timeout
        self.session_token = os.environ["LEETCODE_SESSION"]
        self.csrf_token = os.environ["LEETCODE_CSRF_TOKEN"]

        self.session = requests.Session()

        self.session.cookies.update(
            {
                "LEETCODE_SESSION": self.session_token,
                "csrftoken": self.csrf_token,
            }
        )

        self.session.headers.update(
            {
                "User-Agent": "Mozilla/5.0",
                "X-CSRFToken": self.csrf_token,
                "X-Requested-With": "XMLHttpRequest",
            }
        )

    def fetch_problem(self, slug: str) -> dict[str, Any]:
        response = self.session.post(
            graphQL_url,
            json={
                "operationName": "questionData",
                "variables": {
                    "titleSlug": slug,
                },
                "query": question_query,
            },
            headers={
                "Referer": f"https://leetcode.cn/problems/{slug}/",
            },
            timeout=self.timeout,
        )

        if not response.ok:
            print("status:", response.status_code)
            print("response:", response.text)
            print("request body:", response.request.body)

        response.raise_for_status()

        payload = response.json()

        if "errors" in payload:
            raise RuntimeError(f"LeetCode GraphQL error: {payload['errors']}")

        problem = payload.get("data", {}).get("question")

        if problem is None:
            raise ValueError(f"Problem not found: {slug}")

        return problem

    def submit_code(
        self,
        *,
        slug: str,
        question_id: str,
        code: str,
        lang: str = "python3",
    ) -> int:
        response = self.session.post(
            f"{base_url}/problems/{slug}/submit/",
            json={
                "lang": lang,
                "question_id": str(question_id),
                "typed_code": code,
            },
            headers={
                "Referer": (f"{base_url}/problems/{slug}/"),
            },
            timeout=self.timeout,
        )

        if not response.ok:
            raise RuntimeError(
                "LeetCode submission failed\n"
                f"status: {response.status_code}\n"
                f"response: {response.text}"
            )

        payload = response.json()

        submission_id = payload.get("submission_id")

        if submission_id is None:
            raise RuntimeError(f"Missing submission id: {payload}")

        return int(submission_id)

    def check_submission(
        self,
        submission_id: int,
    ) -> dict[str, Any]:
        response = self.session.get(
            (f"{base_url}/submissions/detail/{submission_id}/check/"),
            timeout=self.timeout,
        )

        if not response.ok:
            raise RuntimeError(
                "LeetCode check failed\n"
                f"status: {response.status_code}\n"
                f"response: {response.text}"
            )

        return response.json()

    def wait_for_submission(
        self,
        submission_id: int,
        *,
        interval: float = 0.5,
        attempts: int = 60,
    ) -> dict[str, Any]:
        for _ in range(attempts):
            result = self.check_submission(submission_id)

            state = result.get("state")

            if state == "SUCCESS":
                return result

            if state not in {
                "PENDING",
                "STARTED",
            }:
                return result

            time.sleep(interval)

        raise TimeoutError("Timed out waiting for submission result.")

    def run_code(
        self,
        *,
        slug: str,
        question_id: str,
        code: str,
        data_input: str,
        lang: str = "python3",
    ) -> dict[str, Any]:
        response = self.session.post(
            f"{base_url}/problems/{slug}/interpret_solution/",
            json={
                "data_input": data_input,
                "lang": lang,
                "question_id": question_id,
                "typed_code": code,
            },
            headers={
                "Referer": f"{base_url}/problems/{slug}",
            },
            timeout=self.timeout,
        )

        if not response.ok:
            raise RuntimeError(
                "LeetCode run failed\n"
                f"status: {response.status_code}\n"
                f"response: {response.text}"
            )

        payload = response.json()

        interpret_id = payload.get("interpret_id")

        if interpret_id is None:
            raise RuntimeError(f"Missing interpret id: {payload}")

        return self.wait_for_submission(interpret_id)
