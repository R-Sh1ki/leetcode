import marimo

app = marimo.App(width="medium")


@app.cell
def _():
    import marimo as mo
    return (mo,)



# >>> leetcode:deep-dark-fraction

@app.cell(hide_code=True)
def problem_deep_dark_fraction(mo):
    mo.md(r"""
# LCP 02. 分式化简

有一个同学在学习分式。他需要将一个连分数化成最简分数，你能帮助他吗？

![](https://assets.leetcode.cn/aliyun-lc-upload/uploads/2019/09/09/fraction_example_1.jpg)

连分数是形如上图的分式。在本题中，所有系数都是大于等于0的整数。

输入的cont代表连分数的系数（cont[0]代表上图的a~0~，以此类推）。返回一个长度为2的数组[n, m]，使得连分数的值等于n / m，且n, m最大公约数为1。

**示例 1：**

```
输入：cont = [3, 2, 0, 2]
输出：[13, 4]
解释：原连分数等价于3 + (1 / (2 + (1 / (0 + 1 / 2))))。注意[26, 8], [-13, -4]都不是正确答案。
```

**示例 2：**

```
输入：cont = [0, 0, 3]
输出：[3, 1]
解释：如果答案是整数，令分母为1即可。
```

**限制：**

1. cont[i] >= 0
2. 1 <= cont的长度 <= 10
3. cont最后一个元素不等于0
4. 答案的n, m的取值都能被32位int整型存下（即不超过2 ^ 31 - 1）。
""")
    return


@app.cell(hide_code=True)
def note_deep_dark_fraction(mo):
    mo.md(r"""

    ### Solution Approach

    #### Number Theory

    Process the continued fraction from right to left. Let \(r_{pre}=\frac{p}{q}\) denote the reciprocal of the result constructed so far. After adding \(a_i\),

    \[
    r=\frac{1}{a_i+r_{pre}}
    =\frac{1}{a_i+\frac{p}{q}}
    =\frac{q}{a_i \times q+p}.
    \]

    Therefore, the numerator and denominator can be updated as

    \[
    (p, q) \leftarrow (q, a_i \times q + p).
    \]

    Initialize with \( r_{pre} = \frac{0}{1} \), so processing \(a_n\) gives \(r=\frac{1}{a_n}\).

    After all elements are processed, \(r\) is the reciprocal of the original continued fraction, so swap its numerator and denominator to obtain the final answer.

    The fraction is always in its simplest form. If \(\gcd(p,q)=1\), then after the update \((p,q)\leftarrow(q,a_i \times q+p)\), we have \(\gcd(q,a_i \times q+p)=\gcd(q,p)=1\). Since the initial pair is \((0,1)\), the numerator and denominator remain coprime throughout the process, so no extra reduction is needed.
    
""")
    return


@app.cell(hide_code=True)
def code_deep_dark_fraction(mo):
    mo.md(r"""
```python
class Solution:
    def fraction(self, cont: list[int]) -> list[int]:
        n, m = 0, 1
        for a in cont[::-1]:
            n, m = m, (a*m+n)
        return [m, n]
```
""")
    return


# <<< leetcode:deep-dark-fraction



# >>> leetcode:programmable-robot

@app.cell(hide_code=True)
def problem_programmable_robot(mo):
    mo.md(r"""
# LCP 03. 机器人大冒险

力扣团队买了一个可编程机器人，机器人初始位置在原点(0, 0)。小伙伴事先给机器人输入一串指令command，机器人就会**无限循环**这条指令的步骤进行移动。指令有两种：

1. U: 向y轴正方向移动一格
2. R: 向x轴正方向移动一格。

不幸的是，在 xy 平面上还有一些障碍物，他们的坐标用obstacles表示。机器人一旦碰到障碍物就会被**损毁**。

给定终点坐标(x, y)，返回机器人能否**完好**地到达终点。如果能，返回true；否则返回false。

**示例 1：**

```
输入：command = "URR", obstacles = [], x = 3, y = 2
输出：true
解释：U(0, 1) -> R(1, 1) -> R(2, 1) -> U(2, 2) -> R(3, 2)。
```

**示例 2：**

```
输入：command = "URR", obstacles = [[2, 2]], x = 3, y = 2
输出：false
解释：机器人在到达终点前会碰到(2, 2)的障碍物。
```

**示例 3：**

```
输入：command = "URR", obstacles = [[4, 2]], x = 3, y = 2
输出：true
解释：到达终点后，再碰到障碍物也不影响返回结果。
```

**限制：**

1. 2 <= command的长度 <= 1000
2. command由U，R构成，且至少有一个U，至少有一个R
3. 0 <= x <= 1e9, 0 <= y <= 1e9
4. 0 <= obstacles的长度 <= 1000
5. obstacles[i]不为原点或者终点
""")
    return


@app.cell(hide_code=True)
def note_programmable_robot(mo):
    mo.md(r"""

    ### Solution Approach

    #### Periodicity + Hash Table

    Naive simulation could take up to 10^9^ steps. Instead, we exploit the **periodicity**: the robot loops `command` infinitely, and each full cycle advances it by $(p_x, p_y)$. So every position the robot visits can be written as $(n \cdot p_x + dx,\; n \cdot p_y + dy)$ where $(dx, dy)$ is a **waypoint** within one cycle.

    1. Simulate one cycle of `command`, record every position. Store them in a **set** for \(O(1)\) lookup (but the list is faster than set/dict).
    2. Let \( n = \min(\lfloor x / p_x \rfloor,\; \lfloor y / p_y \rfloor) \). The target is reachable iff \( (x - n \cdot p_x,\; y - n \cdot p_y) \in \text{waypoints} \).
    3. For each obstacle \( (o_x, o_y) \) **within** the bounding box \( (o_x \le x,\; o_y \le y) \), compute \( n' = \min(\lfloor o_x / p_x \rfloor,\; \lfloor o_y / p_y \rfloor) \). It blocks the path iff \( (o_x - n' \cdot p_x,\; o_y - n' \cdot p_y) \in \text{waypoints} \).
    4. Return `true` only if the target is reachable **and** no obstacle is hit.
    5. Note: Obstacles beyond the target \( (o_x > x or o_y > y) \) are irrelevant, the robot stops before reaching them.
    
""")
    return


@app.cell(hide_code=True)
def code_programmable_robot(mo):
    mo.md(r"""
```python
class Solution:
    def robot(self, command: str, obstacles: list[list[int]], x: int, y: int) -> bool:
        px, py = 0, 0
        waypoints = [[px, py]]

        for c in command:
            if c == "U":
                py += 1
            if c == "R":
                px += 1
            waypoints.append([px, py])

        # check whether the robot can reach the target.
        n = min(x // px, y // py)
        if [x - n * px, y - n * py] not in waypoints:
            return False

        # check whether the obstacles are on the movement waypoints.
        for ob in obstacles:
            if ob[0] <= x and ob[1] <= y:
                n = min(ob[0] // px, ob[1] // py)
                if [ob[0] - n * px, ob[1] - n * py] in waypoints:
                    return False

        return True
```
""")
    return


# <<< leetcode:programmable-robot


if __name__ == "__main__":
    app.run()
