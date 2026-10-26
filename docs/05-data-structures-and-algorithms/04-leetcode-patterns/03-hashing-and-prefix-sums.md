# Hashing and prefix sums

After this you can turn "search the array again" into a constant-time lookup, and answer range-sum questions by remembering running totals.

Before this: [Two pointers and sliding window](02-two-pointers-and-sliding-window.md) and [hash tables](../02-data-structures/04-hash-tables.md).

## The idea

You are checking names against a guest list. Reading the list again for every name is slow; looking the name up in an index is instant. Many problems hide this: your brute force keeps asking "have I seen a value like this before?", and a hash map or set answers that in $O(1)$ on average.

Prefix sums extend the same idea to ranges. If you store the running total after each item, the sum of any stretch is one subtraction: total up to the end of the stretch minus total up to its start. Together with a hash map, this finds stretches with a given sum without checking every stretch.

| Signal in the problem | Pattern |
|---|---|
| "Find two items with a given sum or difference", unsorted | Complement lookup in a map |
| "Have I seen it", duplicates, counts, groups | Set or counter |
| Number of subarrays with sum $k$ (negatives allowed) | Prefix sum plus a counter of earlier prefixes |
| Answer at $i$ depends on everything left and right of $i$ | Prefix and suffix arrays |

```text
nums     =  3   4   7   2  -3   1   4   2
prefix P = 0   3   7  14  16  13  14  18  20     P[i] = sum of the first i numbers

sum of nums[2..4] = 7 + 2 + (-3) = 6
                  = P[5] - P[2] = 13 - 7 = 6
```

## Key terms

A **hash map** (dictionary) stores key-value pairs with $O(1)$ average lookup; a **set** stores keys only. A **prefix sum** at position $i$ is the sum of the first $i$ elements, with `P[0] = 0`.

A **frequency counter** is a map from value to how many times it appeared; Python's `collections.Counter` is one.

## How it works

Complement lookup scans once. For each value, check whether its partner is already stored, then store the value:

```python
def two_sum(nums, target):
    seen = {}                        # value -> index
    for i, x in enumerate(nums):
        if target - x in seen:
            return [seen[target - x], i]
        seen[x] = i
```

For subarray sums, the sum of `nums[i..j]` equals $k$ exactly when `P[j+1] - P[i] == k`. Going left to right with a running total, ask how many earlier prefixes equal `running - k`. Seed the counter with `{0: 1}` so that a subarray starting at index 0 is found.

```python
def count_subarrays(nums, k):
    count = {0: 1}                   # prefix sum -> times seen
    running = ans = 0
    for x in nums:
        running += x
        ans += count.get(running - k, 0)
        count[running] = count.get(running, 0) + 1
    return ans
```

Why a map and not a window: with negative numbers the running total can go up and down, so the window trick from the last lesson does not apply. A map of earlier totals does not care about signs.

## Worked examples

<div class="example" markdown>

### Example 1: 1 Two Sum

[1 Two Sum](https://leetcode.com/problems/two-sum/) is the complement-lookup template above, solved step by step in [How to approach a problem](01-how-to-approach-a-problem.md). The point to keep is the order: check the map first, then store, so a value never pairs with itself. Time $O(n)$, space $O(n)$.

</div>

<div class="example" markdown>

### Example 2: 560 Subarray Sum Equals K

[560 Subarray Sum Equals K](https://leetcode.com/problems/subarray-sum-equals-k/): count the contiguous subarrays whose sum is $k$. The numbers can be negative, so we use prefix sums with a counter. We trace `[3, 4, 7, 2, -3, 1, 4, 2]` with $k = 7$:

```text
x    running   need (running - 7)   times seen   ans
 3       3         -4                  0           0
 4       7          0                  1           1     [3, 4]
 7      14          7                  1           2     [7]
 2      16          9                  0           2
-3      13          6                  0           2
 1      14          7                  1           3     [7, 2, -3, 1]
 4      18         11                  0           3
 2      20         13                  1           4     [1, 4, 2]
```

Each row asks how many earlier prefix totals equal `running - 7`. Each one found is the start of a subarray ending here.

```python
def subarray_sum(nums, k):                    # LeetCode 560
    count = {0: 1}                            # prefix sum -> times seen
    running = ans = 0
    for x in nums:
        running += x
        ans += count.get(running - k, 0)      # earlier prefixes that make sum k
        count[running] = count.get(running, 0) + 1
    return ans

def subarray_sum_brute(nums, k):
    return sum(sum(nums[i:j]) == k
               for i in range(len(nums)) for j in range(i + 1, len(nums) + 1))

assert subarray_sum([1, 1, 1], 2) == 2
assert subarray_sum([1, 2, 3], 3) == 2
assert subarray_sum([3, 4, 7, 2, -3, 1, 4, 2], 7) == 4
assert subarray_sum([0, 0, 0], 0) == 6        # zeros: every subarray counts
assert subarray_sum([], 0) == 0
import random
for _ in range(300):
    a = [random.randint(-3, 3) for _ in range(random.randint(0, 9))]
    k = random.randint(-4, 4)
    assert subarray_sum(a, k) == subarray_sum_brute(a, k)
print(subarray_sum([3, 4, 7, 2, -3, 1, 4, 2], 7))
```

```text
4
```

Time $O(n)$, space $O(n)$. The brute force is $O(n^3)$ as written, which is why it is only the test oracle.

Check: the `[0, 0, 0]` case catches a counter that stores a prefix before using it, or one not seeded with `{0: 1}`.

</div>

<div class="example" markdown>

### Example 3: 238 Product of Array Except Self

[238 Product of Array Except Self](https://leetcode.com/problems/product-of-array-except-self/): return a list where entry $i$ is the product of every number except `nums[i]`, without using division. Position $i$ needs everything to its left and everything to its right, which is the prefix and suffix signal. The answer at $i$ is (product of items before $i$) times (product of items after $i$).

```text
nums          =  1    2    3    4
left product  =  1    1    2    6        product of everything before i
right product = 24   12    4    1        product of everything after i
answer        = 24   12    8    6        left times right
```

We fill `out` with the left products on a forward pass, then multiply in the right products on a backward pass using one running variable, so no extra array is needed.

```python
def product_except_self(nums):                # LeetCode 238
    n = len(nums)
    out = [1] * n
    left = 1
    for i in range(n):                        # out[i] = product before i
        out[i] = left
        left *= nums[i]
    right = 1
    for i in range(n - 1, -1, -1):            # multiply in product after i
        out[i] *= right
        right *= nums[i]
    return out

assert product_except_self([1, 2, 3, 4]) == [24, 12, 8, 6]
assert product_except_self([-1, 1, 0, -3, 3]) == [0, 0, 9, 0, 0]
assert product_except_self([2, 3]) == [3, 2]
print(product_except_self([1, 2, 3, 4]))
```

```text
[24, 12, 8, 6]
```

Time $O(n)$, space $O(1)$ beyond the output. Zeros are why division is a bad idea here: dividing the total by a zero entry fails.

</div>

## Common mistakes

<div class="warning" markdown>

Watch out: forgetting `{0: 1}` in the prefix counter. Subarrays that start at index 0 are never counted, and the code passes the sample but fails on a case such as `[3]` with $k = 3$.

Watch out: updating the map before the lookup. A value then pairs with itself in Two Sum, and a prefix matches itself when $k = 0$.

Watch out: assuming a hash map lookup is always $O(1)$. It is $O(1)$ on average. Only hashable values can be keys, so a list must become a tuple first.

</div>

## Working with AI

<div class="ai" markdown>

Words to use: complement, hash map, frequency counter, prefix sum, running total, subarray, suffix.

Prompts to try:

- "Solve LeetCode 560 in Python with a prefix sum and a dictionary. Explain why the dictionary starts as `{0: 1}`, and give a case where negatives break a sliding window."
- "Write a brute-force checker and a random test for my `subarray_sum` so I can compare them."

What to check:

- A sliding window offered for a sum problem with negative numbers. Test it on `[1, -1, 1]`, $k = 1$.
- A solution that uses division for 238. Run it with a zero in the input.
- A `{0: 1}` seed missing, or a counter storing indices where counts were needed.

</div>

## Quiz

1\. Which pattern fits "count pairs of equal numbers in a list"?

<details class="solution" markdown>
<summary>Answer</summary>

A frequency counter. For each value that appears $c$ times there are $c(c-1)/2$ pairs.

</details>

2\. With `P = [0, 3, 7, 14, 16]`, what is the sum of the third and fourth numbers of the original list (positions 2 and 3, 0-based)?

<details class="solution" markdown>
<summary>Answer</summary>

`P[4] - P[2] = 16 - 7 = 9`. The numbers are 7 and 2.

</details>

3\. `subarray_sum([3], 3)` returns 0 from a student's code that starts with `count = {}`. Why?

<details class="solution" markdown>
<summary>Answer</summary>

The running total 3 minus $k$ is 0, and no prefix equal to 0 was stored. The empty prefix must be seeded with `{0: 1}`.

</details>

4\. Why can 238 not divide the product of all numbers by `nums[i]`?

<details class="solution" markdown>
<summary>Answer</summary>

Division by zero when the array contains 0, and the problem forbids division. Prefix and suffix products avoid both issues.

</details>

## Lab

<div class="lab" markdown>

### Lab: Longest Consecutive Sequence

Goal: solve [128 Longest Consecutive Sequence](https://leetcode.com/problems/longest-consecutive-sequence/) in $O(n)$ with a set. Time: about 15 minutes. Runs in: any terminal with Python 3.

1. Statement: given unsorted integers, return the length of the longest run of consecutive values (such as 1, 2, 3, 4), in any order in the input.
2. Put all numbers in a set. Sorting would be $O(n \log n)$.
3. Only start counting from a number whose predecessor `x - 1` is not in the set. Count upward while `x + 1` is present.
4. Assert on `[100, 4, 200, 1, 3, 2]` (4), `[0, 3, 7, 2, 5, 8, 4, 6, 0, 1]` (9) and `[]` (0).

<details class="solution" markdown>
<summary>Solution</summary>

```python
def longest_consecutive(nums):
    values = set(nums)
    best = 0
    for x in values:
        if x - 1 not in values:           # x starts a run
            length = 1
            while x + length in values:
                length += 1
            best = max(best, length)
    return best

assert longest_consecutive([100, 4, 200, 1, 3, 2]) == 4
assert longest_consecutive([0, 3, 7, 2, 5, 8, 4, 6, 0, 1]) == 9
assert longest_consecutive([]) == 0
print("ok")
```

Time $O(n)$: each run is walked once, from its start. Space $O(n)$.

</details>

</div>

## Where this shows up

- Database indexes, caches and deduplication are hash lookups; running totals appear in analytics queries.
- Next, [stacks and monotonic stacks](04-stacks-and-monotonic-stacks.md) handles "the next bigger item" questions.
