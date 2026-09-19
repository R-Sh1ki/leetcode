import marimo

app = marimo.App(width="medium")


@app.cell
def _():
    import marimo as mo
    return (mo,)



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



# >>> leetcode:qi-wang-ge-shu-tong-ji

@app.cell(hide_code=True)
def problem_qi_wang_ge_shu_tong_ji(mo):
    mo.md(r"""
# LCP 11. 期望个数统计

某互联网公司一年一度的春招开始了，一共有 n 名面试者入选。每名面试者都会提交一份简历，公司会根据提供的简历资料产生一个预估的能力值，数值越大代表越有可能通过面试。

小 A 和小 B 负责审核面试者，他们均有所有面试者的简历，并且将各自根据面试者能力值从大到小的顺序浏览。由于简历事先被打乱过，能力值相同的简历的出现顺序是从它们的全排列中**等可能**地取一个。现在给定 n 名面试者的能力值 scores，设 X 代表小 A 和小 B 的浏览顺序中出现在同一位置的简历数，求 X 的期望。

提示：离散的非负随机变量的期望计算公式为 ![1](http://latex.codecogs.com/svg.latex?E%28X%29%3D%5Csum_%7Bk%3D1%7D%5E%7B%5Cinfty%7D%20k%20%5CPr%28X%20%3D%20k%29)。在本题中，由于 X 的取值为 0 到 n 之间，期望计算公式可以是 ![2](http://latex.codecogs.com/svg.latex?E%28X%29%3D%5Csum_%7Bk%3D1%7D%5E%7Bn%7D%20k%20%5CPr%28X%20%3D%20k%29)。

**示例 1：**

> 输入：scores = [1,2,3]
>
> 输出：3
>
> 解释：由于面试者能力值互不相同，小 A 和小 B 的浏览顺序一定是相同的。X的期望是 3 。

**示例 2：**

> 输入：scores = [1,1]
>
> 输出：1
>
> 解释：设两位面试者的编号为 0, 1。由于他们的能力值都是 1，小 A 和小 B 的浏览顺序都为从全排列 [[0,1],[1,0]] 中等可能地取一个。如果小 A 和小 B 的浏览顺序都是 [0,1] 或者 [1,0] ，那么出现在同一位置的简历数为 2 ，否则是 0 。所以 X 的期望是 (2+0+2+0) \* 1/4 = 1

**示例 3：**

> 输入：scores = [1,1,2]
>
> 输出：2

**限制：**

* 1 <= scores.length <= 10^5
* 0 <= scores[i] <= 10^6
""")
    return


@app.cell(hide_code=True)
def note_qi_wang_ge_shu_tong_ji(mo):
    mo.md(r"""

    ### Solution Approach

    #### Math

    Let \(X\) be the number of positions containing the expected value, and define an indicator variable \(X_i\) for each position:
    \[
    X_i =
    \begin{cases}
    1, & \text{if position } i \text{ contains the expected value},\\
    0, & \text{otherwise}.
    \end{cases}
    \]

    Then
    \[
    X=\sum_{i=1}^{n} X_i.
    \]

    By linearity of expectation,
    \[
        \mathbb{E}[X]
        =\sum_{i=1}^{n} \mathbb{E}[X_i]
        =\sum_{i=1}^{n} \Pr(X_i=1).
    \]

    Therefore, the expected number of occurrences is simply the sum of the probabilities that the expected value appears at each position.
    
""")
    return


@app.cell(hide_code=True)
def code_qi_wang_ge_shu_tong_ji(mo):
    mo.md(r"""
```python
class Solution:
    def expectNumber(self, scores: list[int]) -> int:
        return len(set(scores))
```
""")
    return


# <<< leetcode:qi-wang-ge-shu-tong-ji


if __name__ == "__main__":
    app.run()
