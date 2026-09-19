import marimo

app = marimo.App(width="medium")


@app.cell
def _():
    import marimo as mo
    return (mo,)



# >>> leetcode:two-sum

@app.cell(hide_code=True)
def problem_two_sum(mo):
    mo.md(r"""
# 1. 两数之和

给定一个整数数组 nums 和一个整数目标值 target，请你在该数组中找出 **和为目标值** *target*  的那 **两个** 整数，并返回它们的数组下标。

你可以假设每种输入只会对应一个答案，并且你不能使用两次相同的元素。

你可以按任意顺序返回答案。

**示例 1：**

```
输入：nums = [2,7,11,15], target = 9
输出：[0,1]
解释：因为 nums[0] + nums[1] == 9 ，返回 [0, 1] 。
```

**示例 2：**

```
输入：nums = [3,2,4], target = 6
输出：[1,2]
```

**示例 3：**

```
输入：nums = [3,3], target = 6
输出：[0,1]
```

**提示：**

* 2 <= nums.length <= 10^4^
* -10^9^ <= nums[i] <= 10^9^
* -10^9^ <= target <= 10^9^
* **只会存在一个有效答案**

**进阶：**你可以想出一个时间复杂度小于 O(n^2^) 的算法吗？
""")
    return


@app.cell(hide_code=True)
def note_two_sum(mo):
    mo.md(r"""

    ### 解题思路

    #### 遍历

    通过两层遍历`nums`中的数字，查找两数之和是目标数字`target`的两个数字，返回结果。时间复杂度是$O(n^2)$，空间复杂度是$O(1)$。

    #### 哈希表

    在遍历的同时使用哈希表纪录出现的数字及其索引，当`target-num`可以在哈希表中查找到的时候，直接返回结果。时间复杂度是$O(n)$，空间复杂度是$O(n)$。
    
""")
    return


@app.cell(hide_code=True)
def code_two_sum(mo):
    mo.md(r"""
```python
class Solution:
    def twoSum(self, nums: list[int], target: int) -> list[int]:
        visited = {}

        for i, num in enumerate(nums):
            x = target - num
            if x in visited:
                return [visited[x], i]
            visited[num] = i
        return []
```
""")
    return


# <<< leetcode:two-sum



# >>> leetcode:guess-numbers

@app.cell(hide_code=True)
def problem_guess_numbers(mo):
    mo.md(r"""
# LCP 01. 猜数字

小A 和 小B 在玩猜数字。小B 每次从 1, 2, 3 中随机选择一个，小A 每次也从 1, 2, 3 中选择一个猜。他们一共进行三次这个游戏，请返回 小A 猜对了几次？

输入的guess数组为 小A 每次的猜测，answer数组为 小B 每次的选择。guess和answer的长度都等于3。

**示例 1：**

```
输入：guess = [1,2,3], answer = [1,2,3]
输出：3
解释：小A 每次都猜对了。
```

**示例 2：**

```
输入：guess = [2,2,3], answer = [3,2,1]
输出：1
解释：小A 只猜对了第二次。
```

**限制：**

1. guess的长度 = 3
2. answer的长度 = 3
3. guess的元素取值为 {1, 2, 3} 之一。
4. answer的元素取值为 {1, 2, 3} 之一。
""")
    return


@app.cell(hide_code=True)
def note_guess_numbers(mo):
    mo.md(r"""

    ### 解题思路

    #### 遍历

    一层遍历，对比每个索引下两个数字的值是否相等。
    
""")
    return


@app.cell(hide_code=True)
def code_guess_numbers(mo):
    mo.md(r"""
```python
class Solution:
    def game(self, guess: list[int], answer: list[int]) -> int:
        res = 0
        for i in range(3):
            if guess[i] == answer[i]:
                res += 1
        return res
```
""")
    return


# <<< leetcode:guess-numbers



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



# >>> leetcode:broken-board-dominoes

@app.cell(hide_code=True)
def problem_broken_board_dominoes(mo):
    mo.md(r"""
# LCP 04. 覆盖

你有一块棋盘，棋盘上有一些格子已经坏掉了。你还有无穷块大小为1 \* 2的多米诺骨牌，你想把这些骨牌**不重叠**地覆盖在**完好**的格子上，请找出你最多能在棋盘上放多少块骨牌？这些骨牌可以横着或者竖着放。

输入：n, m代表棋盘的大小；broken是一个b \* 2的二维数组，其中每个元素代表棋盘上每一个坏掉的格子的位置。

输出：一个整数，代表最多能在棋盘上放的骨牌数。

**示例 1：**

```
输入：n = 2, m = 3, broken = [[1, 0], [1, 1]]
输出：2
解释：我们最多可以放两块骨牌：[[0, 0], [0, 1]]以及[[0, 2], [1, 2]]。（见下图）
```

![](https://assets.leetcode.cn/aliyun-lc-upload/uploads/2019/09/09/domino_example_1.jpg)

**示例 2：**

```
输入：n = 3, m = 3, broken = []
输出：4
解释：下图是其中一种可行的摆放方式
```

![](https://assets.leetcode.cn/aliyun-lc-upload/uploads/2019/09/09/domino_example_2.jpg)

**限制：**

1. 1 <= n <= 8
2. 1 <= m <= 8
3. 0 <= b <= n \* m
""")
    return


@app.cell(hide_code=True)
def note_broken_board_dominoes(mo):
    mo.md(r"""

    ### Solution Approach

    #### Method 1: Bipartite Graph + Hungarian Algorithm

    The grid is naturally a bipartite graph: color cells like a chessboard, so cell $(i, j)$ is `black` if $(i+j) \% 2 = 0$, otherwise `white`. Each domino covers exactly one black cell and one adjacent white cell, so the problem reduces to **maximum bipartite matching**.

    **Steps:**
    1. **Build the Graph.** For each intact black cell, connect it to its intact white neighbors (up, down, left, right). Skip broken cells.
    2. **Hungarian Algorithm.** For each black cell $u$, adapt the deep-first searching method to find an **augmenting path**: a path starting from an unmatched black cell, alternating between unmatched and matched edges, ending at an unmatched white cell. If found, flip the matching along the path (matching size +1).
    3. The total matching size is the answer.

    **Why it works:** By **Berge's theorem**, a matching is maximum if and only if no augmenting path exists. Each DFS in the Hungarian algorithm searches for exactly such a path.

    **Complexity:** $V \le 64$ cells, $E \le 128$ edges, total $O(V \cdot E)$.

    ```python
    class Solution:
        def domino(self, n: int, m: int, broken: list[list[int]]) -> int:
            blocked = set(map(tuple, broken))

            # create the bipartite graph.
            adj = {}
            for i in range(n):
                for j in range(m):
                    if (i+j) % 2 == 0 and (i, j) not in blocked:
                        adj[(i, j)] = []
                        for di, dj in [(0,1),(0,-1),(1,0),(-1,0)]:
                            ni, nj = i + di, j + dj
                            if 0 <= ni < n and 0 <= nj < m:
                                if (ni + nj) % 2 == 1 and (ni, nj) not in blocked:
                                    adj[(i, j)].append((ni, nj))

            # Hungarian algorithm
            match = {}
            def dfs(black, visited):
                for white in adj[black]:
                    if white in visited: continue
                    visited.add(white)
                    if white not in match or dfs(match[white], visited):
                        match[white] = black
                        return True
                return False

            ans = 0
            for black in adj:
                if dfs(black, set()):
                    ans += 1
            return ans
    ```

    ---


    #### Method 2: Bitmask DP (Profile DP)

    Since $m \le 8$, we can encode the "profile" of a row as a bitmask of length $m$. Scan left-to-right, row by row.
    1. **State:** $dp[\text{mask}]$ = max dominoes placed so far, where bit $j$ of `mask` is $1$ if cell $(i, j)$ is already occupied by a vertical domino extending down from the row above.
    2. **Transition:** For each cell $(i, j)$ that is **not** broken and **not** occupied from above, try up to 3 options:
        1. skip: intentionally skip this cell, move to the next cell with no change.
        2. horizontal: requires the right cell to exist, be intact, and not occupied from above. Place a 1×2 domino, advance to $j+1$ , cnt+1.
        3. vertical: requires the cell below to exist and be intact. Place a 2×1 domino, set bit $j$ in the next row's mask, cnt+1.
    3. When $j = m$ (end of row), write the result into the next row:
    $$
       dp_{i+1}[\text{new\_mask}] = \max(dp_{i+1}[\text{new\_mask}],\; \text{cnt}).
    $$

    **Complexity:** $O(n \cdot 2^m \cdot m)$: for each of $n$ rows, each of $2^m$ masks, scan $m$ cells with constant branching.

    ```python
    class Solution:
        def domino(self, n: int, m: int, broken: list[list[int]]) -> int:
            blocked = [[False] * m for _ in range(n)]
            for r, c in broken:
                blocked[r][c] = True

            # dp store the previous masks and their max count.
            dp = {0: 0}

            for i in range(n):
                ndp = {}
                # scan each row and update the dp states.
                for mask, cnt in dp.items():
                    self._scan(i, 0, mask, 0, cnt, ndp, blocked, n, m)
                dp = ndp
            return max(dp.values())

        def _scan(self, i, j, mask, nmask, cnt, ndp, blocked, n, m):
            # if scan finished, store the finial masks and its max count.
            if j == m:
                ndp[nmask] = max(ndp.get(nmask, 0), cnt)
                return

            # if the cell is masked or broken, skip.
            if (mask >> j) & 1 or blocked[i][j]:
                self._scan(i, j+1, mask, nmask, cnt, ndp, blocked, n, m)
                return

            # don't place the domino, skip
            self._scan(i, j+1, mask, nmask, cnt, ndp, blocked, n, m)

            # place the domino horizonally
            if j + 1 < m and not ((mask >> (j+1)) & 1) and not blocked[i][j+1]:
                self._scan(i, j+2, mask, nmask, cnt+1, ndp, blocked, n, m)

            # place the domino vertically
            if i + 1 < n and not blocked[i+1][j]:
                self._scan(i, j+1, mask, nmask | (1 << j), cnt+1, ndp, blocked, n, m)
    ```
    
""")
    return


@app.cell(hide_code=True)
def code_broken_board_dominoes(mo):
    mo.md(r"""
```python
class Solution:    
    def domino(self, n: int, m: int, broken: list[list[int]]) -> int:
        blocked = [[False] * m for _ in range(n)]
        for r, c in broken:
            blocked[r][c] = True

        # dp store the previous masks and their max count.
        dp = {0: 0}
        
        for i in range(n):
            ndp = {}
            # scan each row and update the dp states.
            for mask, cnt in dp.items():
                self._scan(i, 0, mask, 0, cnt, ndp, blocked, n, m)
            dp = ndp
        return max(dp.values())

    def _scan(self, i, j, mask, nmask, cnt, ndp, blocked, n, m):
        # if scan finished, store the finial masks and its max count.
        if j == m:
            ndp[nmask] = max(ndp.get(nmask, 0), cnt)
            return
        
        # if the cell is masked or broken, skip.
        if (mask >> j) & 1 or blocked[i][j]:
            self._scan(i, j+1, mask, nmask, cnt, ndp, blocked, n, m)
            return

        # don't place the domino, skip
        self._scan(i, j+1, mask, nmask, cnt, ndp, blocked, n, m)

        # place the domino horizonally
        if j + 1 < m and not ((mask >> (j+1)) & 1) and not blocked[i][j+1]:
            self._scan(i, j+2, mask, nmask, cnt+1, ndp, blocked, n, m)

        # place the domino vertically
        if i + 1 < n and not blocked[i+1][j]:
            self._scan(i, j+1, mask, nmask | (1 << j), cnt+1, ndp, blocked, n, m)
```
""")
    return


# <<< leetcode:broken-board-dominoes



# >>> leetcode:na-ying-bi

@app.cell(hide_code=True)
def problem_na_ying_bi(mo):
    mo.md(r"""
# LCP 06. 拿硬币

桌上有 n 堆力扣币，每堆的数量保存在数组 coins 中。我们每次可以选择任意一堆，拿走其中的一枚或者两枚，求拿完所有力扣币的最少次数。

**示例 1：**

> 输入：[4,2,1]
>
> 输出：4
>
> 解释：第一堆力扣币最少需要拿 2 次，第二堆最少需要拿 1 次，第三堆最少需要拿 1 次，总共 4 次即可拿完。

**示例 2：**

> 输入：[2,3,10]
>
> 输出：8

**限制：**

* 1 <= n <= 4
* 1 <= coins[i] <= 10
""")
    return


@app.cell(hide_code=True)
def note_na_ying_bi(mo):
    mo.md(r"""

    ### Solution Approach

    #### Math

    Easy math problem, for each coin stack with $n$ coins, the min count is $\mod(n) + \lfloor n / 2 \rfloor$.
    
""")
    return


@app.cell(hide_code=True)
def code_na_ying_bi(mo):
    mo.md(r"""
```python
class Solution:
    def minCount(self, coins: list[int]) -> int:
        res = 0
        for n in coins:
            res += n // 2 + n % 2
        return res
```
""")
    return


# <<< leetcode:na-ying-bi



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



# >>> leetcode:2vYnGI

@app.cell(hide_code=True)
def problem_2vYnGI(mo):
    mo.md(r"""
# LCP 18. 早餐组合

小扣在秋日市集选择了一家早餐摊位，一维整型数组 `staple` 中记录了每种主食的价格，一维整型数组 `drinks` 中记录了每种饮料的价格。小扣的计划选择一份主食和一款饮料，且花费不超过 `x` 元。请返回小扣共有多少种购买方案。
注意：答案需要以 `1e9 + 7 (1000000007)` 为底取模，如：计算初始结果为：`1000000008`，请返回 `1`
\*\*示例 1：\*\*
>输入：`staple = [10,20,5], drinks = [5,5,2], x = 15`
>
>输出：`6`
>
>解释：小扣有 6 种购买方案，所选主食与所选饮料在数组中对应的下标分别是：
>第 1 种方案：staple[0] + drinks[0] = 10 + 5 = 15；
>第 2 种方案：staple[0] + drinks[1] = 10 + 5 = 15；
>第 3 种方案：staple[0] + drinks[2] = 10 + 2 = 12；
>第 4 种方案：staple[2] + drinks[0] = 5 + 5 = 10；
>第 5 种方案：staple[2] + drinks[1] = 5 + 5 = 10；
>第 6 种方案：staple[2] + drinks[2] = 5 + 2 = 7。
\*\*示例 2：\*\*
>输入：`staple = [2,1,1], drinks = [8,9,5,1], x = 9`
>
>输出：`8`
>
>解释：小扣有 8 种购买方案，所选主食与所选饮料在数组中对应的下标分别是：
>第 1 种方案：staple[0] + drinks[2] = 2 + 5 = 7；
>第 2 种方案：staple[0] + drinks[3] = 2 + 1 = 3；
>第 3 种方案：staple[1] + drinks[0] = 1 + 8 = 9；
>第 4 种方案：staple[1] + drinks[2] = 1 + 5 = 6；
>第 5 种方案：staple[1] + drinks[3] = 1 + 1 = 2；
>第 6 种方案：staple[2] + drinks[0] = 1 + 8 = 9；
>第 7 种方案：staple[2] + drinks[2] = 1 + 5 = 6；
>第 8 种方案：staple[2] + drinks[3] = 1 + 1 = 2；
\*\*提示：\*\*
+ `1 <= staple.length <= 10^5`
+ `1 <= drinks.length <= 10^5`
+ `1 <= staple[i],drinks[i] <= 10^5`
+ `1 <= x <= 2\*10^5`
""")
    return


@app.cell(hide_code=True)
def note_2vYnGI(mo):
    mo.md(r"""

    ### Solution Approach

    #### 1. Two pointers

    Sort both arrays. Use the pointer `ptr1` to scan `staple` from left to right and  pointer `ptr2` to scan `drinks` from right to left. For each `staple[ptr1]`, move the drink pointer left until `staple[ptr1] + drinks[ptr2] <= x`.

    Since drinks is sorted, all drinks in `drinks[0..ptr2]` are valid, so they contribute `ptr2 + 1` combinations.

    As `staple[i]` increases, the maximum valid drink index can only move left, so each pointer moves at most once through its array.

    ```python
    class Solution:
        def breakfastNumber(self, staple: list[int], drinks: list[int], x: int) -> int:
            staple.sort()
            drinks.sort()

            res = 0
            mod = 10**9 + 7 # ! the problem requires the result mod the 10e9 + 7
            ptr1, ptr2 = 0, len(drinks) - 1

            while ptr1 < len(staple) and ptr2 >= 0:
                if staple[ptr1] > x:
                    break
                if staple[ptr1] + drinks[ptr2] <= x:
                    res += ptr2 + 1
                    ptr1 += 1
                else:
                    ptr2 -= 1
            return res % mod
    ```

    #### 2. Binary Search

    Sort drinks. For each staple price `s`, we need to count the drinks satisfying `d <= x - s`.

    Since drinks is sorted, use binary search to find the first position greater than `x - s`. This position is exactly the number of valid drinks for `s`.



    #### 3. Prefix Sum

    Count how many drinks have each price, then build a prefix sum where `prefix[p]` represents the number of drinks with price at most p.

    For each staple price `s`, the remaining budget for a drink is `x-s`. Therefore, `prefix[x - s]` directly gives the number of drinks that can be paired with `s`.

    This avoids sorting and uses the bounded price range for \( O(1) \) queries.

    ```python
    class Solution:
        def breakfastNumber(self, staple: list[int], drinks: list[int], x: int) -> int:
            mod = 10**9 + 7 # ! the problem requires the result mod the 10e9 + 7

            prefix = [0] * (x+1)

            for d in drinks:
                if d <= x:
                    prefix[d] += 1
            for i in range(1, x+1):
                prefix[i] += prefix[i-1]

            res = 0
            for s in staple:
                if s <= x:
                    res += prefix[x-s]

            return res % mod
    ```
    
""")
    return


@app.cell(hide_code=True)
def code_2vYnGI(mo):
    mo.md(r"""
```python
class Solution:
    def breakfastNumber(self, staple: list[int], drinks: list[int], x: int) -> int:
        mod = 10**9 + 7 # ! the problem requires the result mod the 10e9 + 7
        drinks.sort()
        res = 0
        for s in staple:
            if s > x: continue

            l, r = 0, len(drinks)
            while l < r:
                mid = (l + r) // 2
                if drinks[mid] <= x - s:
                    l = mid + 1
                else:
                    r = mid
            res += l

        return res % mod
```
""")
    return


# <<< leetcode:2vYnGI



# >>> leetcode:4xy4Wx

@app.cell(hide_code=True)
def problem_4xy4Wx(mo):
    mo.md(r"""
# LCP 28. 采购方案

小力将 N 个零件的报价存于数组 `nums`。小力预算为 `target`，假定小力仅购买两个零件，要求购买零件的花费不超过预算，请问他有多少种采购方案。
注意：答案需要以 `1e9 + 7 (1000000007)` 为底取模，如：计算初始结果为：`1000000008`，请返回 `1`
\*\*示例 1：\*\*
>输入：`nums = [2,5,3,5], target = 6`
>
>输出：`1`
>
>解释：预算内仅能购买 nums[0] 与 nums[2]。
\*\*示例 2：\*\*
>输入：`nums = [2,2,1,9], target = 10`
>
>输出：`4`
>
>解释：符合预算的采购方案如下：
>nums[0] + nums[1] = 4
>nums[0] + nums[2] = 3
>nums[1] + nums[2] = 3
>nums[2] + nums[3] = 10
\*\*提示：\*\*
- `2 <= nums.length <= 10^5`
- `1 <= nums[i], target <= 10^5`
""")
    return


@app.cell(hide_code=True)
def note_4xy4Wx(mo):
    mo.md(r"""

    ### Solution Approach

    #### 1. Two pointers

    Sort `nums` and use two pointers, `left` and `right`, starting from both ends. If `nums[left] + nums[right] <= target`, then every element in `nums[left+1..right]` can form a valid pair with `nums[left]`, contributing `right - left` pairs. Move `left` forward. Otherwise, the sum is too large, so move `right` backward.

    ```python
    class Solution:
        def purchasePlans(self, nums: list[int], target: int) -> int:
            nums.sort()
            mod = 10**9 + 7

            res = 0
            ptr1, ptr2 = 0, len(nums) - 1

            while ptr1 < len(nums) and ptr2 >= 0 and ptr1 < ptr2:
                if nums[ptr1] > target:
                    break
                if nums[ptr1] + nums[ptr2] <= target:
                    res += ptr2 - ptr1
                    ptr1 += 1
                else:
                    ptr2 -= 1
            return res % mod
    ```

    #### 2. Binary Search

    Sort `nums`. For each index `i`, we need to count the elements after it that satisfy `nums[j] <= target - nums[i]`.

    Use binary search on the range after `i` to find the first element greater than `target - nums[i]`. If this position is `j`, then all elements in `[i+1, j)` form valid pairs with nums[i], contributing `j-i-1` pairs.

    Searching only after i ensures that each pair is counted exactly once.

    ```python
    class Solution:
        def purchasePlans(self, nums: list[int], target: int) -> int:
            nums.sort()
            mod = 10**9 + 7

            res = 0
            for i in range(len(nums)):
                if nums[i] > target:
                    break

                left, right = i + 1, len(nums)
                while left < right:
                    mid = (left + right) // 2
                    if nums[mid] <= target - nums[i]:
                        left = mid + 1
                    else:
                        right = mid
                res += (left - i - 1)
            return res % mod
    ```
    
""")
    return


@app.cell(hide_code=True)
def code_4xy4Wx(mo):
    mo.md(r"""
```python
class Solution:
    def purchasePlans(self, nums: list[int], target: int) -> int:
        nums.sort()
        mod = 10**9 + 7

        res = 0
        for i in range(len(nums)):
            if nums[i] > target:
                break
            
            left, right = i + 1, len(nums)
            while left < right:
                mid = (left + right) // 2
                if nums[mid] <= target - nums[i]:
                    left = mid + 1
                else:
                    right = mid
            res += (left - i - 1)
        return res % mod
```
""")
    return


# <<< leetcode:4xy4Wx


if __name__ == "__main__":
    app.run()
