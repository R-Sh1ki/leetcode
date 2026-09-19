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


if __name__ == "__main__":
    app.run()
