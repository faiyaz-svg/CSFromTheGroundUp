# Two pointers and sliding window

After this you can recognize problems on sorted arrays, strings and contiguous ranges that two moving indices solve in one pass, and write the template for each.

Before this: [How to approach a problem](01-how-to-approach-a-problem.md) and [arrays and dynamic arrays](../02-data-structures/01-arrays-and-dynamic-arrays.md).

## The idea

Suppose you want two numbers in a sorted list that add to 10. Checking every pair is slow. But if you put one finger on the smallest number and one on the largest, each look at their sum tells you which finger to move: too small, move the left finger right; too big, move the right finger left. Each step rules out a whole group of pairs, so one pass is enough.

The same idea works on a stretch of consecutive items. A window with a left and a right edge slides along the data, growing on the right and shrinking on the left, and you keep track of what is inside it instead of recounting.

| Signal in the problem | Pattern |
|---|---|
| Sorted array, find a pair or triple with a target sum | Opposite-end pointers |
| Reverse, palindrome check, partition in place | Opposite-end or same-direction pointers |
| Longest or shortest substring or subarray with a property | Sliding window |
| "Contiguous", "substring", "at most $k$ distinct" | Sliding window |

```text
sorted a = [1, 3, 4, 6, 8, 11], target 10       (lo moves right, hi moves left)

 lo=0 hi=5   [1 . . . . 11]   1+11 = 12  too big    -> hi moves left
 lo=0 hi=4   [1 . . . 8 .]    1+8  =  9  too small  -> lo moves right
 lo=1 hi=4   [. 3 . . 8 .]    3+8  = 11  too big    -> hi moves left
 lo=1 hi=3   [. 3 . 6 . .]    3+6  =  9  too small  -> lo moves right
 lo=2 hi=3   [. . 4 6 . .]    4+6  = 10  found
```

## Key terms

A **pointer** here is an index into an array or string, not a memory address. **Two pointers** moves two indices through the data under a rule that never makes you revisit a pair.

A **sliding window** is the range between a `left` and a `right` index. It is **variable** when its size changes to keep a condition true, and **fixed** when its size is a given $k$.

A window is **valid** if it satisfies the condition the problem sets, such as "no repeated characters".

## How it works

Opposite-end pointers need an order (usually sorted input) so that a move can discard candidates for sure.

```python
def two_pointers(a):
    lo, hi = 0, len(a) - 1
    while lo < hi:
        if too_small(a[lo], a[hi]):
            lo += 1
        elif too_big(a[lo], a[hi]):
            hi -= 1
        else:
            return lo, hi
```

A variable window always follows the same loop: extend the right edge, then shrink the left edge while the window is invalid, then record the answer.

```python
def window(s):
    left = best = 0
    state = ...                      # what is inside the window
    for right, ch in enumerate(s):
        add_to(state, ch)
        while invalid(state):        # shrink until valid again
            remove_from(state, s[left])
            left += 1
        best = max(best, right - left + 1)
    return best
```

Each index enters the window once and leaves once, so the total work is $O(n)$ even though a `while` sits inside a `for`. For the shortest valid window, record the answer inside the shrink loop instead (while the window is valid).

```text
s = "abcabcbb"   longest window with no repeated character

 a b c a b c b b      size
[a]                   1
[a b]                 2
[a b c]               3
  [b c a]             3   adding a: drop the left a first
    [c a b]           3
      [a b c]         3
          [c b]       2   adding b: drop the left a and b
              [b]     1
```

In the diagram, brackets mark the window, and the left bracket only moves right.

## Worked examples

<div class="example" markdown>

### Example 1: 167 Two Sum II - Input Array Is Sorted

[167 Two Sum II - Input Array Is Sorted](https://leetcode.com/problems/two-sum-ii-input-array-is-sorted/): given a sorted list and a target, return the 1-based positions of two numbers that sum to the target. The signal is "sorted" plus "pair", so we use opposite-end pointers.

Why moving is safe: if `numbers[lo] + numbers[hi]` is too small, then `numbers[lo]` paired with any index at or below `hi` is no bigger, so `numbers[lo]` cannot be part of the answer and we drop it.

```python
def two_sum_sorted(numbers, target):          # LeetCode 167 (1-indexed answer)
    lo, hi = 0, len(numbers) - 1
    while lo < hi:
        s = numbers[lo] + numbers[hi]
        if s == target:
            return [lo + 1, hi + 1]
        if s < target:
            lo += 1                           # need a bigger sum
        else:
            hi -= 1                           # need a smaller sum

assert two_sum_sorted([2, 7, 11, 15], 9) == [1, 2]
assert two_sum_sorted([2, 3, 4], 6) == [1, 3]
assert two_sum_sorted([-1, 0], -1) == [1, 2]
assert two_sum_sorted([1, 3, 4, 6, 8, 11], 10) == [3, 4]
print("167 ok")
```

```text
167 ok
```

Time $O(n)$, space $O(1)$. A hash map would also work but costs $O(n)$ space; the sorted order is what buys the constant space.

</div>

<div class="example" markdown>

### Example 2: 3 Longest Substring Without Repeating Characters

[3 Longest Substring Without Repeating Characters](https://leetcode.com/problems/longest-substring-without-repeating-characters/): return the length of the longest substring with all distinct characters. "Longest substring with a property" is the window signal. The state is a set of the characters inside; the window is invalid when the new character is already in it.

```python
def length_of_longest_substring(s):           # LeetCode 3
    in_window = set()
    left = best = 0
    for right, ch in enumerate(s):
        while ch in in_window:                # window invalid: shrink
            in_window.remove(s[left])
            left += 1
        in_window.add(ch)
        best = max(best, right - left + 1)
    return best

assert length_of_longest_substring("abcabcbb") == 3
assert length_of_longest_substring("bbbbb") == 1
assert length_of_longest_substring("pwwkew") == 3
assert length_of_longest_substring("") == 0
print("3 ok")
```

```text
3 ok
```

Time $O(n)$, space $O(\min(n, m))$ for an alphabet of size $m$.

</div>

<div class="example" markdown>

### Example 3: 76 Minimum Window Substring

[76 Minimum Window Substring](https://leetcode.com/problems/minimum-window-substring/): return the shortest substring of `s` that contains every character of `t`, counting repeats. Now we want the shortest valid window, so we record the answer while the window is valid and shrink as far as possible.

The state is `need`, a count of what the window still owes (it goes negative for extras), and `missing`, how many required characters are still absent. The window is valid when `missing == 0`.

```python
from collections import Counter

def min_window(s, t):                         # LeetCode 76
    need = Counter(t)
    missing = len(t)                          # characters still needed
    left = 0
    best = (float("inf"), 0, 0)               # (length, start, end)
    for right, ch in enumerate(s):
        if need[ch] > 0:
            missing -= 1
        need[ch] -= 1                         # may go negative: extras
        if missing == 0:                      # window valid: shrink
            while need[s[left]] < 0:
                need[s[left]] += 1
                left += 1
            if right - left + 1 < best[0]:
                best = (right - left + 1, left, right + 1)
            need[s[left]] += 1                # drop s[left]: window invalid
            missing += 1
            left += 1
    return "" if best[0] == float("inf") else s[best[1]:best[2]]

assert min_window("ADOBECODEBANC", "ABC") == "BANC"
assert min_window("a", "a") == "a"
assert min_window("a", "aa") == ""
assert min_window("ab", "b") == "b"
print(min_window("ADOBECODEBANC", "ABC"))
```

```text
BANC
```

Time $O(|s| + |t|)$ because each index enters and leaves once. Space $O(|t|)$ for the counter (more precisely, the alphabet size).

Check: the asserts include a window that does not exist (`"a"` needing `"aa"`) and an answer of length 1.

</div>

## Common mistakes

<div class="warning" markdown>

Watch out: using opposite-end pointers on unsorted data. The "this value cannot be in the answer" argument needs the order. Sort first (and give up the original indices) or use a hash map.

Watch out: shrinking with `if` instead of `while`. One new element can invalidate the window by more than one step, so the left edge may need to move several times.

Watch out: sliding windows on arrays with negative numbers when the condition is a sum. Adding an element no longer makes the sum only grow, so shrinking is no longer safe. That case is a [prefix sum](03-hashing-and-prefix-sums.md) problem.

</div>

## Working with AI

<div class="ai" markdown>

Words to use: two pointers, sliding window, window invariant, shrink condition, sorted input, contiguous.

Prompts to try:

- "Solve LeetCode 76 in Python with a sliding window. State the window invariant, what `missing` means, and the time complexity. Then give three tests, including no valid window."
- "Why is this `while` inside a `for` loop still $O(n)$? Here is my code: ..."

What to check:

- Opposite-end pointers on input that is not sorted. Check the problem statement.
- Off-by-one errors in the window length (`right - left + 1`) and in 1-based versus 0-based answers.
- A window that is recorded before it is valid. Run the empty string, a one-character string and no-answer cases.

</div>

## Quiz

1\. Which pattern fits "longest subarray with at most 2 distinct values"?

<details class="solution" markdown>
<summary>Answer</summary>

A variable sliding window: "longest", "contiguous", and a condition (at most 2 distinct) that can be checked as the window changes.

</details>

2\. What does `two_sum_sorted([1, 3, 4, 6, 8, 11], 10)` return, and how many sums are checked?

<details class="solution" markdown>
<summary>Answer</summary>

`[3, 4]` (1-based positions of 4 and 6). It checks 5 sums: 12, 9, 11, 9 and 10, as in the diagram.

</details>

3\. A student's window code uses `if ch in in_window:` instead of `while`. On `"abba"` what goes wrong?

<details class="solution" markdown>
<summary>Answer</summary>

On `"abba"`, the second `b` finds `b` in the window, and a single `if` removes only the left `a`, leaving the first `b` in place. Now `b` is added twice and the window `"bb"` is counted as valid. With `while`, the left edge keeps moving until the duplicate is gone.

</details>

4\. Why is a sliding window $O(n)$ when it has a loop inside a loop?

<details class="solution" markdown>
<summary>Answer</summary>

`left` only moves right and never passes `right`, so across the whole run it moves at most $n$ times. Total work is at most $2n$ steps.

</details>

## Lab

<div class="lab" markdown>

### Lab: Container With Most Water

Goal: solve [11 Container With Most Water](https://leetcode.com/problems/container-with-most-water/) with opposite-end pointers. Time: about 15 minutes. Runs in: any terminal with Python 3.

1. Statement: `heights[i]` is a vertical line at position `i`. Pick two lines; the water held is the distance between them times the shorter height. Return the maximum.
2. Start with `lo = 0` and `hi = n - 1`, compute the area, and decide which pointer to move. Hint: moving the taller line can only shrink the width without raising the limit.
3. Assert on `[1, 8, 6, 2, 5, 4, 8, 3, 7]` (49) and `[1, 1]` (1).

<details class="solution" markdown>
<summary>Solution</summary>

```python
def max_area(heights):
    lo, hi = 0, len(heights) - 1
    best = 0
    while lo < hi:
        best = max(best, (hi - lo) * min(heights[lo], heights[hi]))
        if heights[lo] < heights[hi]:
            lo += 1                  # the shorter line limits the area
        else:
            hi -= 1
    return best

assert max_area([1, 8, 6, 2, 5, 4, 8, 3, 7]) == 49
assert max_area([1, 1]) == 1
print("ok")
```

Time $O(n)$, space $O(1)$.

</details>

</div>

## Where this shows up

- Merging two sorted lists, partitioning in [quicksort](../03-algorithms/02-sorting.md) and checking palindromes all use two pointers.
- Next, [hashing and prefix sums](03-hashing-and-prefix-sums.md) handles the cases where order or sign breaks the window.
