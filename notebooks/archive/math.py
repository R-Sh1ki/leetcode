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


if __name__ == "__main__":
    app.run()
