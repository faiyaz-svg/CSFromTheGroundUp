# Stacks and monotonic stacks

After this you can recognize matching and "next bigger item" problems, and write the stack template that solves them in one pass.

Before this: [Two pointers and sliding window](02-two-pointers-and-sliding-window.md) and [stacks and queues](../02-data-structures/03-stacks-and-queues.md).

## The idea

Think of a pile of plates: you only touch the top one. A stack fits any problem where the most recent unfinished thing must be dealt with first. Brackets are the classic case: the last bracket you opened is the first one you must close.

A second use is a stack that keeps its contents in order, always shrinking from the top when a new item breaks the order. This is a **monotonic stack**. It answers "for each item, where is the next bigger (or smaller) one?" in $O(n)$ instead of scanning right from every item.

| Signal in the problem | Pattern |
|---|---|
| Brackets, nesting, undo, "most recent first" | Plain stack |
| "Next greater element", "days until warmer" | Monotonic stack (decreasing) |
| "Largest rectangle", "span", nearest smaller on either side | Monotonic stack (increasing) |

```text
s = "([{}])"        stack after each character (top on the right)

 (   push        [ (         ]
 [   push        [ ( [       ]
 {   push        [ ( [ {     ]
 }   top is {  -> pop        [ ( [       ]
 ]   top is [  -> pop        [ (         ]
 )   top is (  -> pop        [           ]    empty at the end: valid
```

## Key terms

A **stack** is a collection where the last item added is the first removed. In Python a `list` with `append` and `pop` is one.

A **monotonic stack** keeps its items in sorted order (always decreasing, or always increasing). Before pushing a new item, it pops every item that would break the order, and those pops are where the answers are found.

## How it works

In the next-greater template, the stack holds indices of items still waiting for a bigger one, and their values decrease from bottom to top. When a new value `x` is bigger than the value on top, `x` is the answer for that top item: pop it and record the result. Then push the new index.

```python
def next_greater_distance(a):
    ans = [0] * len(a)
    stack = []                         # indices; values decrease bottom to top
    for i, x in enumerate(a):
        while stack and a[stack[-1]] < x:
            j = stack.pop()
            ans[j] = i - j             # x is the next greater for j
        stack.append(i)
    return ans                         # items left on the stack stay 0
```

Each index is pushed once and popped at most once, so the cost is $O(n)$ although a `while` sits in the `for`. Flip the comparison for "next smaller". Store indices rather than values so you can compute distances and widths.

## Worked examples

<div class="example" markdown>

### Example 1: 20 Valid Parentheses

[20 Valid Parentheses](https://leetcode.com/problems/valid-parentheses/): the string contains only `()[]{}`; return whether every bracket is closed by the right kind in the right order. The stack holds the openers not yet closed (see the diagram in The idea). On a closer, the top must be its matching opener.

```python
def is_valid(s):                              # LeetCode 20
    pairs = {")": "(", "]": "[", "}": "{"}
    stack = []
    for ch in s:
        if ch in pairs:                       # closer
            if not stack or stack.pop() != pairs[ch]:
                return False
        else:                                 # opener
            stack.append(ch)
    return not stack                          # leftovers are unclosed

assert is_valid("()[]{}")
assert is_valid("([{}])")
assert not is_valid("(]")
assert not is_valid("(")                      # unclosed opener
assert not is_valid(")")                      # closer with empty stack
assert is_valid("")
print("20 ok")
```

```text
20 ok
```

Time $O(n)$, space $O(n)$. Check: `")"` and `"("` test the two ways to fail, an empty stack at a closer and leftovers at the end.

</div>

<div class="example" markdown>

### Example 2: 739 Daily Temperatures

[739 Daily Temperatures](https://leetcode.com/problems/daily-temperatures/): for each day, return how many days you wait for a warmer one, or 0 if none. This is exactly "next greater distance". For `[73, 74, 75, 71, 69, 72, 76, 73]` the stack of waiting days evolves like this (temperatures shown, top on the right):

```text
day  temp   pops (days answered)    stack after
 0    73    none                    [73]
 1    74    day 0 (wait 1)          [74]
 2    75    day 1 (wait 1)          [75]
 3    71    none                    [75, 71]
 4    69    none                    [75, 71, 69]
 5    72    day 4 (1), day 3 (2)    [75, 72]
 6    76    day 5 (1), day 2 (4)    [76]
 7    73    none                    [76, 73]

answer = [1, 1, 4, 2, 1, 1, 0, 0]
```

Days 6 and 7 stay on the stack to the end, so they keep the default 0.

```python
def daily_temperatures(temps):                # LeetCode 739
    return next_greater_distance(temps)

assert daily_temperatures([73, 74, 75, 71, 69, 72, 76, 73]) == [1, 1, 4, 2, 1, 1, 0, 0]
assert daily_temperatures([30, 40, 50, 60]) == [1, 1, 1, 0]
assert daily_temperatures([30, 60, 90]) == [1, 1, 0]
assert daily_temperatures([5]) == [0]
print(daily_temperatures([73, 74, 75, 71, 69, 72, 76, 73]))
```

```text
[1, 1, 4, 2, 1, 1, 0, 0]
```

Time $O(n)$, space $O(n)$.

</div>

<div class="example" markdown>

### Example 3: 84 Largest Rectangle in Histogram

[84 Largest Rectangle in Histogram](https://leetcode.com/problems/largest-rectangle-in-histogram/): bars of width 1 with given heights; find the area of the largest rectangle that fits. A bar of height `h` can extend left and right until a shorter bar blocks it. So for each bar we want the nearest shorter bar on each side, which the increasing stack finds.

Here the stack holds indices of bars with increasing heights. When a new bar is shorter than the top, the top bar cannot extend further right, so we pop it and compute its rectangle: its height times the width from just after the new top of the stack to just before the current bar. A final bar of height 0 forces every remaining bar off the stack.

```text
heights = [2, 1, 5, 6, 2, 3]       R marks the best rectangle: bars 2 and 3 at height 5

6          [ ]      
5       [R][R]      
4       [R][R]      
3       [R][R]   [ ]
2 [ ]   [R][R][ ][ ]
1 [ ][ ][R][R][ ][ ]
   0  1  2  3  4  5

bar 4 (height 2) arrives: pops bar 3 (h=6): width 1, area 6
                          pops bar 2 (h=5): width 2, area 10
```

```python
def largest_rectangle(heights):               # LeetCode 84
    stack = []                                # indices; heights increase
    best = 0
    for i, h in enumerate(heights + [0]):     # the 0 empties the stack
        while stack and heights[stack[-1]] > h:
            height = heights[stack.pop()]
            left = stack[-1] if stack else -1 # nearest shorter bar on the left
            best = max(best, height * (i - left - 1))
        stack.append(i)
    return best

def largest_rectangle_brute(heights):
    return max((min(heights[i:j]) * (j - i)
                for i in range(len(heights)) for j in range(i + 1, len(heights) + 1)),
               default=0)

assert largest_rectangle([2, 1, 5, 6, 2, 3]) == 10
assert largest_rectangle([2, 4]) == 4
assert largest_rectangle([5]) == 5
assert largest_rectangle([]) == 0
import random
for _ in range(300):
    a = [random.randint(0, 6) for _ in range(random.randint(0, 8))]
    assert largest_rectangle(a) == largest_rectangle_brute(a)
print(largest_rectangle([2, 1, 5, 6, 2, 3]))
```

```text
10
```

Time $O(n)$, space $O(n)$. The random test against the $O(n^3)$ brute force is the check that matters here; this problem is easy to get subtly wrong.

</div>

## Common mistakes

<div class="warning" markdown>

Watch out: storing values instead of indices. You then cannot compute how far away the answer is or how wide a rectangle is.

Watch out: using `>` where the problem needs `>=` (or the reverse). With equal heights the choice changes which bar owns the width, and equal values are where random tests catch it.

Watch out: forgetting the leftover items. After the loop, anything still on the stack never found a bigger item. Leave the default, or use a sentinel as in 84.

</div>

## Working with AI

<div class="ai" markdown>

Words to use: stack, monotonic stack, next greater element, sentinel, amortized $O(n)$, nearest smaller.

Prompts to try:

- "Explain LeetCode 739 using a monotonic stack of indices. Show the stack after each step for `[73, 74, 75, 71, 69, 72, 76, 73]`."
- "Here is my solution to LeetCode 84. Write a brute-force version and a random test that compares them."

What to check:

- The wrong direction of monotonicity. Trace two or three steps by hand.
- A nested loop labelled "stack". Count how many times each index can be pushed and popped.
- Missing empty-stack checks (`stack[-1]` on an empty list raises `IndexError`). Run the empty input and the all-increasing input.

</div>

## Quiz

1\. A problem asks for the next smaller element to the right. How does the template change?

<details class="solution" markdown>
<summary>Answer</summary>

Flip the comparison: pop while the top is greater than the new value. The stack then keeps values increasing from bottom to top.

</details>

2\. What does `is_valid("{[}]")` return?

<details class="solution" markdown>
<summary>Answer</summary>

`False`. After `{` and `[`, the closer `}` finds `[` on top, which is not its match.

</details>

3\. A solution to 739 uses two nested loops that scan right from each day. What is its cost, and what replaces it?

<details class="solution" markdown>
<summary>Answer</summary>

$O(n^2)$ in the worst case (for a falling sequence). A monotonic stack makes it $O(n)$.

</details>

4\. In 84, why is a bar of height 0 added to the end of the list?

<details class="solution" markdown>
<summary>Answer</summary>

It is shorter than every real bar, so it pops everything left on the stack and each remaining rectangle gets computed.

</details>

## Lab

<div class="lab" markdown>

### Lab: Min Stack

Goal: solve [155 Min Stack](https://leetcode.com/problems/min-stack/), a stack that also returns its minimum in $O(1)$. Time: about 15 minutes. Runs in: any terminal with Python 3.

1. Build a class with `push(x)`, `pop()`, `top()` and `get_min()`, all $O(1)$. (LeetCode names the last method `getMin`.)
2. Hint: store with each item the minimum of the stack up to and including it.
3. Assert on the sequence push 5, push 3, push 7, then check the minimum is 3, pop, pop, and the minimum is 5.

<details class="solution" markdown>
<summary>Solution</summary>

```python
class MinStack:
    def __init__(self):
        self.stack = []                  # (value, minimum so far)

    def push(self, x):
        low = min(x, self.stack[-1][1]) if self.stack else x
        self.stack.append((x, low))

    def pop(self):
        self.stack.pop()

    def top(self):
        return self.stack[-1][0]

    def get_min(self):
        return self.stack[-1][1]

s = MinStack()
s.push(5); s.push(3); s.push(7)
assert s.get_min() == 3 and s.top() == 7
s.pop(); s.pop()
assert s.get_min() == 5 and s.top() == 5
print("ok")
```

Every operation is $O(1)$; space is $O(n)$.

</details>

</div>

## Where this shows up

- Parsers and compilers match brackets with a stack, and the call stack of a running program is one too.
- Next, [tree and graph problems](05-tree-and-graph-problems.md) uses recursion and an explicit stack or queue to explore branching data.
