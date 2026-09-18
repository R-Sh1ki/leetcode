import marimo

__generated_with = "0.24.0"
app = marimo.App()


@app.cell
def _():
    import marimo as mo

    return (mo,)


@app.cell
def _():
    from leetcode.paths import notebookDir
    from leetcode import LeetCode, problem_md, render_problem

    notebook = notebookDir / "testbook.py"
    lc = LeetCode(notebook)
    return lc, render_problem


@app.cell
def _(lc):
    problem = lc.get_problem("two-sum")
    return (problem,)


@app.cell
def problem_desc(problem, render_problem):
    render_problem(problem)
    return


@app.cell(hide_code=True)
def solution_note(mo):
    mo.md(r"""
    ### 解题思路

    #### 遍历

    通过两层遍历`nums`中的数字，查找两数之和是目标数字`target`的两个数字，返回结果。时间复杂度是$O(n^2)$，空间复杂度是$O(1)$。

    #### 哈希表

    在遍历的同时使用哈希表纪录出现的数字及其索引，当`target-num`可以在哈希表中查找到的时候，直接返回结果。时间复杂度是$O(n)$，空间复杂度是$O(n)$。
    """)
    return


@app.class_definition
class Solution:
    def twoSum(self, nums: list[int], target: int) -> list[int]:
        visited = {}

        for i, num in enumerate(nums):
            x = target - num
            if x in visited:
                return [visited[x], i]
            visited[num] = i
        return []


@app.cell
def testing(lc, problem):
    test_res = lc.test_problem(problem, Solution)
    return


@app.cell
def submission(lc, problem):
    result = lc.submit_problem(problem)
    return


@app.cell
def archive(lc, problem):
    lc.archive_problem(problem, topic="array")
    return


if __name__ == "__main__":
    app.run()
