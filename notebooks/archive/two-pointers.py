import marimo

app = marimo.App(width="medium")


@app.cell
def _():
    import marimo as mo
    return (mo,)



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
