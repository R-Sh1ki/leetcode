import marimo

app = marimo.App(width="medium")


@app.cell
def _():
    import marimo as mo
    return (mo,)



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


if __name__ == "__main__":
    app.run()
