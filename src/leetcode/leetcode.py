# File:  leetcode.py
# Author:  R-Sh1ki
# E-mail:  ryougi.shiki.kong@outlook.com
# Created Time: 2026-09-16 17:48:22
# ---------------------------------------------------
# Modified By: R-Sh1ki
# Modified Time: 2026-09-16 21:36:31


from __future__ import annotations

import ast
import inspect
import textwrap
from typing import Any

from . import cache
from .client import LeetCodeClient
from .problem import Problem
from .testcase import TestCase, parse_value


class LeetCode:
    def __init__(self) -> None:
        self.client = LeetCodeClient()

    def get_problem(self, slug: str, *, refresh: bool = False) -> Problem:
        if cache.exists(slug) and not refresh:
            data = cache.load(slug)
        else:
            data = self.client.fetch_problem(slug)
            cache.save(slug, data)

        problem = Problem(data)

        if not problem.example_outputs:
            self.cache_example_outputs(problem)

        self._init_local_tests(problem)

        return problem

    def get_solution_source(self, solution: type) -> str:
        source = inspect.getsource(solution)
        source = textwrap.dedent(source)

        tree = ast.parse(source)

        for node in tree.body:
            if isinstance(node, ast.ClassDef):
                node.decorator_list = []
                return ast.unparse(node)

        raise ValueError("Cannot find Solution class source")

    def display_result(self, result: dict) -> None:
        status = result.get("status_msg", "Unknown")

        print(f"Result: {status}")

        if status == "Accepted":
            runtime = result.get("status_runtime", "N/A")
            memory = result.get("status_memory", "N/A")

            runtime_percentile = result.get("runtime_percentile")
            memory_percentile = result.get("memory_percentile")

            print(f"Runtime: {runtime}, beats {runtime_percentile:.2f}%")
            print(f"Memory: {memory}, beats {memory_percentile:.2f}%")

            return

        testcase = result.get("last_testcase")
        expected = result.get("expected_output")
        actual = result.get("code_output")

        if testcase:
            print(f"Last testcase: {testcase}", end="")
        if expected:
            print(f", expected: {expected}", end="")
        if actual:
            print(f", output: {actual}", end="")
        print(".")

        runtime_error = result.get("runtime_error")
        if runtime_error:
            print(f"Runtime error: {runtime_error}")

    def submit_problem(
        self, problem: Problem, solution: type, *, lang: str = "python3"
    ) -> dict[str, Any]:
        code = self.get_solution_source(solution)

        submission_id = self.client.submit_code(
            slug=problem.slug,
            question_id=problem.question_id,
            code=code,
            lang=lang,
        )

        result = self.client.wait_for_submission(submission_id)

        self.display_result(result)

        if result.get("status_msg") != "Accepted":
            self._save_failed_testcase(problem, result)

        return result

    def cache_example_outputs(self, problem: Problem) -> None:
        if problem.example_outputs:
            return
        if not problem.example_testcases:
            return

        code = problem.code_template()

        result = self.client.run_code(
            slug=problem.slug,
            question_id=problem.question_id,
            code=code,
            data_input=problem.example_testcases,
        )

        # print(result)

        outputs = self.extract_example_outputs(result)

        problem.data["exampleOutputs"] = outputs

        cache.save(problem.slug, problem.data)

    def extract_example_outputs(self, result: dict) -> list[str]:
        for key in ("expected_code_answer", "expected_output", "expected_outputs"):
            value = result.get(key)

            if isinstance(value, list):
                return [str(item).strip() for item in value if str(item).strip()]

        value = result.get("expected_output")

        if value is not None:
            return [str(value)]

        raise RuntimeError(f"Cannot find expected outputs in run result: {result}")

    def _build_official_tests(self, problem: Problem) -> list[TestCase]:
        params = problem.metadata["params"]
        param_count = len(params)

        lines = [
            line for line in problem.example_testcases.splitlines() if line.strip()
        ]

        outputs = problem.example_outputs

        testcases = []

        for case_index, start in enumerate(range(0, len(lines), param_count)):
            raw_args = lines[start : start + param_count]
            args = [parse_value(value) for value in raw_args]
            expected = parse_value(outputs[case_index])

            testcases.append(
                TestCase(
                    args=args,
                    expected=expected,
                    source="official",
                )
            )

        return testcases

    def _init_local_tests(self, problem: Problem) -> None:
        if problem.data.get("localTests"):
            return

        testcases = self._build_official_tests(problem)

        problem.data["localTests"] = [test.to_dict() for test in testcases]

        cache.save(problem.slug, problem.data)

    def test_problem(self, problem: Problem, solution: type) -> bool:
        method_name = problem.metadata["name"]
        instance = solution()

        method = getattr(instance, method_name)

        tests = problem.local_tests

        passed = 0

        for index, testcase in enumerate(tests, start=1):
            actual = method(*testcase.args)
            ok = actual == testcase.expected

            print(f"[{'Pass' if ok else 'Failed'}] case {index} ({testcase.source})")
            print(f"    input: {testcase.args}, output: {actual}", end="")

            if not ok:
                print(f"expected: {testcase.expected}.")
            else:
                passed += 1
                print(".")

        print(f"{passed}/{len(tests)} passed.")

        return passed == len(tests)

    def _save_failed_testcase(self, problem: Problem, result: dict) -> None:
        if result.get("status_msg") == "Accepted":
            return

        raw_input = result.get("last_testcase")
        raw_expected = result.get("expected_output")

        if not raw_input or raw_expected is None:
            return

        params = problem.metadata["params"]
        param_count = len(params)

        lines = [line for line in raw_input.splitlines() if line.strip()]

        if len(lines) != param_count:
            return

        testcase = TestCase(
            args=[parse_value(value) for value in lines],
            expected=parse_value(raw_expected),
            source="failed",
        )

        self._add_testcase(problem, testcase)

    def _add_testcase(self, problem: Problem, testcase: TestCase) -> bool:
        existing = problem.data.setdefault("localTests", [])

        new_case = testcase.to_dict()

        for item in existing:
            if (
                item.get("args") == new_case["args"]
                and item.get("expected") == new_case["expected"]
            ):
                return False

        existing.append(new_case)

        cache.save(problem.slug, problem.data)

        return True

    def add_testcase(self, problem: Problem, *args, expected) -> bool:
        testcase = TestCase(
            args=list(args),
            expected=expected,
            source="manual",
        )

        return self._add_testcase(problem, testcase)
