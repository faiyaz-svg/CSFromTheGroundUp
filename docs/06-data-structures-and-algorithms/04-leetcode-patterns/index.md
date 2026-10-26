# LeetCode patterns

A cheat sheet for the chapter. Start with the method, match the signal in the problem to a pattern, then fill in the template. $n$ is the input size.

## The method

1. Clarify the input, output and edge conditions.
2. Work examples by hand, including empty, one element, duplicates and the largest size.
3. State the brute force and its cost.
4. Find the bottleneck (repeated work).
5. Pick a pattern from the table below.
6. Code it, talking as you go.
7. Test on your examples.
8. State time and space.

Details: [How to approach a problem](01-how-to-approach-a-problem.md).

| Input size $n$ | Complexity that usually fits |
|---|---|
| up to about 20 | $O(2^n)$ (backtracking, subsets) |
| up to about 100 | $O(n^3)$ |
| up to a few thousand | $O(n^2)$ |
| around $10^5$ | $O(n \log n)$ |
| $10^6$ or more | $O(n)$ or $O(\log n)$ |

## Signal, pattern, template

| Signal in the problem | Pattern | Template | Time, space |
|---|---|---|---|
| Sorted array, pair or triple with a target | Opposite-end two pointers | `lo, hi = 0, n-1`; move the end that is wrong | $O(n)$, $O(1)$ |
| Longest or shortest substring or subarray with a property | Sliding window | extend `right`; `while invalid: left += 1` | $O(n)$, $O(k)$ |
| "Have I seen it", pair with a sum, duplicates, counts | Hash map or set | check `target - x in seen`, then store | $O(n)$, $O(n)$ |
| Subarray sum equals $k$, negatives allowed | Prefix sum and counter | `count[running - k]`, seed `{0: 1}` | $O(n)$, $O(n)$ |
| Value depends on everything left and right | Prefix and suffix passes | forward pass, then backward pass | $O(n)$, $O(1)$ extra |
| Brackets, nesting, undo | Stack | push openers, pop on closers | $O(n)$, $O(n)$ |
| Next greater or smaller item, histogram | Monotonic stack | `while stack and a[top] < x: pop` | $O(n)$, $O(n)$ |
| Binary tree depth, path, "for each node" | Recursion on children | base case `None`, combine child answers | $O(n)$, $O(h)$ |
| Connected regions in a grid or graph | DFS or BFS with visited set | loop cells, flood unseen ones | $O(V + E)$, $O(V)$ |
| Fewest steps, unweighted | BFS | queue, mark when added | $O(V + E)$, $O(V)$ |
| Prerequisites, ordering, cycle in directed graph | Topological sort | indegree array, queue of zeros | $O(V + E)$, $O(V + E)$ |
| All subsets, permutations, combinations; $n \le 20$ | Backtracking | choose, recurse, undo | exponential |
| Count ways, min or max over choices, overlapping subproblems | Dynamic programming | state, recurrence, base case, cache or table | states times work per state |
| Two sequences, "longest common ..." | 2D DP | `dp[i][j]` from `dp[i-1][j-1]`, `dp[i-1][j]`, `dp[i][j-1]` | $O(mn)$ |
| $k$ largest, $k$ most frequent, $k$ closest | Min-heap of size $k$ | push, pop when size exceeds $k$ | $O(n \log k)$, $O(k)$ |
| Merge or count overlapping intervals | Sort by start, then sweep or heap | compare with the last result or earliest end | $O(n \log n)$ |

## Templates

Opposite-end pointers and variable window ([lesson](02-two-pointers-and-sliding-window.md)):

```python
lo, hi = 0, len(a) - 1
while lo < hi:
    s = a[lo] + a[hi]
    if s == target: break
    if s < target: lo += 1
    else: hi -= 1

left = best = 0
for right, ch in enumerate(s):
    add(ch)
    while invalid():
        remove(s[left]); left += 1
    best = max(best, right - left + 1)
```

Hashing and prefix sums ([lesson](03-hashing-and-prefix-sums.md)):

```python
seen = {}
for i, x in enumerate(nums):
    if target - x in seen: return [seen[target - x], i]
    seen[x] = i

count, running, ans = {0: 1}, 0, 0
for x in nums:
    running += x
    ans += count.get(running - k, 0)
    count[running] = count.get(running, 0) + 1
```

Monotonic stack ([lesson](04-stacks-and-monotonic-stacks.md)):

```python
stack = []
for i, x in enumerate(a):
    while stack and a[stack[-1]] < x:
        j = stack.pop(); ans[j] = i - j
    stack.append(i)
```

Tree recursion and topological sort ([lesson](05-tree-and-graph-problems.md)):

```python
def solve(node):
    if node is None: return BASE
    return combine(node.val, solve(node.left), solve(node.right))

indegree = [0] * n
queue = deque(i for i in range(n) if indegree[i] == 0)
# pop a node, lower its neighbours' indegree, queue those that reach 0
# an order exists when every node was popped
```

Backtracking ([lesson](06-backtracking.md)):

```python
def backtrack(start):
    result.append(path[:])
    for i in range(start, len(nums)):
        path.append(nums[i]); backtrack(i + 1); path.pop()
```

DP ([lesson](07-dp-patterns.md)):

```python
dp = [0] + [INF] * amount
for a in range(1, amount + 1):
    for c in coins:
        if c <= a: dp[a] = min(dp[a], dp[a - c] + 1)
```

Heap top-$k$ and intervals ([lesson](08-heaps-intervals-and-top-k.md)):

```python
heap = []
for x in items:
    heapq.heappush(heap, x)
    if len(heap) > k: heapq.heappop(heap)

intervals.sort(key=lambda iv: iv[0])
```

## Problems in this chapter

| Number | Title | Pattern | Lesson |
|---|---|---|---|
| [1](https://leetcode.com/problems/two-sum/) | Two Sum | Hash map | [1](01-how-to-approach-a-problem.md), [3](03-hashing-and-prefix-sums.md) |
| [167](https://leetcode.com/problems/two-sum-ii-input-array-is-sorted/) | Two Sum II - Input Array Is Sorted | Two pointers | [2](02-two-pointers-and-sliding-window.md) |
| [3](https://leetcode.com/problems/longest-substring-without-repeating-characters/) | Longest Substring Without Repeating Characters | Sliding window | [2](02-two-pointers-and-sliding-window.md) |
| [76](https://leetcode.com/problems/minimum-window-substring/) | Minimum Window Substring | Sliding window | [2](02-two-pointers-and-sliding-window.md) |
| [560](https://leetcode.com/problems/subarray-sum-equals-k/) | Subarray Sum Equals K | Prefix sum | [3](03-hashing-and-prefix-sums.md) |
| [238](https://leetcode.com/problems/product-of-array-except-self/) | Product of Array Except Self | Prefix and suffix | [3](03-hashing-and-prefix-sums.md) |
| [20](https://leetcode.com/problems/valid-parentheses/) | Valid Parentheses | Stack | [4](04-stacks-and-monotonic-stacks.md) |
| [739](https://leetcode.com/problems/daily-temperatures/) | Daily Temperatures | Monotonic stack | [4](04-stacks-and-monotonic-stacks.md) |
| [84](https://leetcode.com/problems/largest-rectangle-in-histogram/) | Largest Rectangle in Histogram | Monotonic stack | [4](04-stacks-and-monotonic-stacks.md) |
| [104](https://leetcode.com/problems/maximum-depth-of-binary-tree/) | Maximum Depth of Binary Tree | Tree recursion | [5](05-tree-and-graph-problems.md) |
| [200](https://leetcode.com/problems/number-of-islands/) | Number of Islands | Grid DFS | [5](05-tree-and-graph-problems.md) |
| [207](https://leetcode.com/problems/course-schedule/) | Course Schedule | Topological sort | [5](05-tree-and-graph-problems.md) |
| [78](https://leetcode.com/problems/subsets/) | Subsets | Backtracking | [6](06-backtracking.md) |
| [46](https://leetcode.com/problems/permutations/) | Permutations | Backtracking | [6](06-backtracking.md) |
| [39](https://leetcode.com/problems/combination-sum/) | Combination Sum | Backtracking | [6](06-backtracking.md) |
| [70](https://leetcode.com/problems/climbing-stairs/) | Climbing Stairs | 1D DP | [7](07-dp-patterns.md) |
| [322](https://leetcode.com/problems/coin-change/) | Coin Change | 1D DP | [7](07-dp-patterns.md) |
| [1143](https://leetcode.com/problems/longest-common-subsequence/) | Longest Common Subsequence | 2D DP | [7](07-dp-patterns.md) |
| [215](https://leetcode.com/problems/kth-largest-element-in-an-array/) | Kth Largest Element in an Array | Heap | [8](08-heaps-intervals-and-top-k.md) |
| [347](https://leetcode.com/problems/top-k-frequent-elements/) | Top K Frequent Elements | Heap | [8](08-heaps-intervals-and-top-k.md) |
| [56](https://leetcode.com/problems/merge-intervals/) | Merge Intervals | Intervals | [8](08-heaps-intervals-and-top-k.md) |
| [253](https://leetcode.com/problems/meeting-rooms-ii/) | Meeting Rooms II | Intervals and heap | [8](08-heaps-intervals-and-top-k.md) |

Lab problems: 121 Best Time to Buy and Sell Stock, 11 Container With Most Water, 128 Longest Consecutive Sequence, 155 Min Stack, 102 Binary Tree Level Order Traversal, 22 Generate Parentheses, 198 House Robber, 973 K Closest Points to Origin.
