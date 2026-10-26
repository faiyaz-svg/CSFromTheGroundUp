# Heaps, intervals and top-k

After this you can solve "k largest" and "k most frequent" problems with a size-$k$ heap, and merge or count overlapping intervals by sorting first.

Before this: [heaps and priority queues](../02-data-structures/06-heaps-and-priority-queues.md) and [sorting](../03-algorithms/02-sorting.md).

## The idea

You are keeping a leaderboard of the top 3 scores while scores stream in. You do not need to sort everything. You keep a list of the current top 3 and, for each new score, drop whichever is lowest. The lowest of the top 3 is the one thing you must find quickly, and a min-heap gives it in $O(1)$ and removes it in $O(\log k)$.

Intervals are a different shape with a similar trick. Once the intervals are sorted by start time, each one only needs to be compared with the last result (to merge) or with the earliest finishing meeting (to count rooms).

| Signal in the problem | Pattern |
|---|---|
| "k largest", "kth largest", "k most frequent", "k closest" | Min-heap of size $k$ |
| Continuous stream, "keep the best $k$ so far" | Min-heap of size $k$ |
| "Merge overlapping intervals", "insert an interval" | Sort by start, then sweep |
| "Minimum rooms / platforms", "maximum overlap" | Sort by start plus heap of end times |

```text
nums = [3, 2, 1, 5, 6, 4], k = 2      min-heap of the 2 largest so far (smallest on the left)

 read 3   heap [3]
 read 2   heap [2, 3]
 read 1   push 1, size 3 > k, pop the smallest (1)   heap [2, 3]
 read 5   push 5, pop 2                              heap [3, 5]
 read 6   push 6, pop 3                              heap [5, 6]
 read 4   push 4, pop 4                              heap [5, 6]

 heap[0] = 5 is the 2nd largest
```

## Key terms

A **min-heap** gives the smallest item in $O(1)$ and adds or removes in $O(\log n)$. Python's `heapq` module is a min-heap on a list.

**Top-k** means the $k$ best items by some measure. Two intervals **overlap** when one starts before the other ends; in LeetCode's Merge Intervals, ones that touch at an endpoint (`[1, 4]` and `[4, 5]`) also merge.

## How it works

The top-k template keeps the heap at size $k$. For the largest items we use a min-heap, so the smallest of the keepers sits on top, ready to be evicted. Cost: $O(n \log k)$ time, $O(k)$ space, better than sorting when $k$ is small.

```python
import heapq

def top_k(items, k):
    heap = []
    for x in items:
        heapq.heappush(heap, x)
        if len(heap) > k:
            heapq.heappop(heap)      # evict the smallest
    return heap                      # the k largest, smallest first
```

The interval template sorts by start, then compares each interval with the last one kept:

```python
def sweep(intervals):
    intervals.sort(key=lambda iv: iv[0])
    out = [intervals[0]]
    for start, end in intervals[1:]:
        if start <= out[-1][1]:                  # overlaps the last one
            out[-1][1] = max(out[-1][1], end)
        else:
            out.append([start, end])
    return out
```

## Worked examples

<div class="example" markdown>

### Example 1: 215 Kth Largest Element in an Array

[215 Kth Largest Element in an Array](https://leetcode.com/problems/kth-largest-element-in-an-array/): return the $k$-th largest value (counting duplicates). The heap of size $k$ holds the $k$ largest seen so far, and its smallest element is the $k$-th largest. The trace in The idea is this problem with $k = 2$.

```python
import heapq

def find_kth_largest(nums, k):                # LeetCode 215
    heap = []
    for x in nums:
        heapq.heappush(heap, x)
        if len(heap) > k:
            heapq.heappop(heap)
    return heap[0]

assert find_kth_largest([3, 2, 1, 5, 6, 4], 2) == 5
assert find_kth_largest([3, 2, 3, 1, 2, 4, 5, 5, 6], 4) == 4
assert find_kth_largest([1], 1) == 1
import random
for _ in range(200):
    a = [random.randint(-5, 5) for _ in range(random.randint(1, 10))]
    k = random.randint(1, len(a))
    assert find_kth_largest(a, k) == sorted(a, reverse=True)[k - 1]
print(find_kth_largest([3, 2, 1, 5, 6, 4], 2))
```

```text
5
```

Time $O(n \log k)$, space $O(k)$. Check: the random test compares with the obvious sort.

</div>

<div class="example" markdown>

### Example 2: 347 Top K Frequent Elements

[347 Top K Frequent Elements](https://leetcode.com/problems/top-k-frequent-elements/): return the $k$ most frequent values. Count with a `Counter` (see [hashing and prefix sums](03-hashing-and-prefix-sums.md)), then run the same size-$k$ heap, using the count as the sort key by pushing `(count, value)` pairs.

```python
from collections import Counter
import heapq

def top_k_frequent(nums, k):                  # LeetCode 347
    heap = []
    for value, count in Counter(nums).items():
        heapq.heappush(heap, (count, value))
        if len(heap) > k:
            heapq.heappop(heap)               # drop the least frequent
    return [value for count, value in heap]

assert sorted(top_k_frequent([1, 1, 1, 2, 2, 3], 2)) == [1, 2]
assert top_k_frequent([1], 1) == [1]
assert sorted(top_k_frequent([4, 4, 4, 5, 5, 6, 6, 6, 6], 2)) == [4, 6]
print(sorted(top_k_frequent([1, 1, 1, 2, 2, 3], 2)))
```

```text
[1, 2]
```

Time $O(n + u \log k)$ for $u$ distinct values, space $O(u)$. The order of the returned list is not specified by the problem, so the tests sort it.

</div>

<div class="example" markdown>

### Example 3: 56 Merge Intervals

[56 Merge Intervals](https://leetcode.com/problems/merge-intervals/): merge all overlapping intervals. Sorting by start puts every interval that could overlap right next to the last result. Here is `[[1,3],[2,6],[8,10],[15,18]]`:

```text
 1   2   3   4   5   6   7   8   9  10 ... 15  16  17  18
 [1-----3]
     [2---------6]                      merged: [1, 6]
                                 [8---10]
                                                 [15-----18]

 [2, 6] starts at 2 <= 3 (end of last), so the end becomes max(3, 6) = 6
 [8, 10] starts at 8 > 6, so it starts a new interval
```

```python
def merge(intervals):                         # LeetCode 56
    intervals = sorted(intervals, key=lambda iv: iv[0])
    out = []
    for start, end in intervals:
        if out and start <= out[-1][1]:
            out[-1][1] = max(out[-1][1], end)
        else:
            out.append([start, end])
    return out

assert merge([[1, 3], [2, 6], [8, 10], [15, 18]]) == [[1, 6], [8, 10], [15, 18]]
assert merge([[1, 4], [4, 5]]) == [[1, 5]]          # touching ends merge
assert merge([[1, 10], [2, 3]]) == [[1, 10]]        # one inside another
assert merge([[5, 6], [1, 2]]) == [[1, 2], [5, 6]]  # unsorted input
assert merge([]) == []
print(merge([[1, 3], [2, 6], [8, 10], [15, 18]]))
```

```text
[[1, 6], [8, 10], [15, 18]]
```

Time $O(n \log n)$ for the sort, space $O(n)$. Check: the `[1, 10], [2, 3]` case is why the end uses `max`, not just the new end.

</div>

<div class="example" markdown>

### Example 4: 253 Meeting Rooms II

[253 Meeting Rooms II](https://leetcode.com/problems/meeting-rooms-ii/): given meeting `[start, end]` times, return the fewest rooms needed. LeetCode marked this problem Premium (paid) as of 2026, so the statement may need a subscription; the idea is what matters. Sort by start. Keep a min-heap of the end times of rooms in use. If the earliest ending room is free by the next start, reuse it; otherwise open a new one. The heap size at the end is the number of rooms.

```text
meetings sorted: [0, 30]  [5, 10]  [15, 20]

 [0, 30]    heap of ends: [30]          1 room
 [5, 10]    earliest end 30 > 5, so a new room        [10, 30]    2 rooms
 [15, 20]   earliest end 10 <= 15, so reuse it        [20, 30]    2 rooms
```

```python
import heapq

def min_meeting_rooms(intervals):             # LeetCode 253
    ends = []                                 # end times of rooms in use
    for start, end in sorted(intervals):
        if ends and ends[0] <= start:
            heapq.heapreplace(ends, end)      # reuse the room that frees first
        else:
            heapq.heappush(ends, end)         # open a new room
    return len(ends)

assert min_meeting_rooms([[0, 30], [5, 10], [15, 20]]) == 2
assert min_meeting_rooms([[7, 10], [2, 4]]) == 1
assert min_meeting_rooms([[1, 5], [5, 8]]) == 1       # back to back reuses a room
assert min_meeting_rooms([[1, 5], [2, 6], [3, 7]]) == 3
assert min_meeting_rooms([]) == 0
print(min_meeting_rooms([[0, 30], [5, 10], [15, 20]]))
```

```text
2
```

Time $O(n \log n)$, space $O(n)$.

</div>

## Common mistakes

<div class="warning" markdown>

Watch out: using a max-heap of everything and popping $k$ times. It works, but costs $O(n + k \log n)$ and keeps all $n$ items. Python's `heapq` is a min-heap only; to get a max-heap, push negated values.

Watch out: forgetting to sort the intervals first, or sorting by end instead of start. The sweep depends on the order.

Watch out: strict versus non-strict comparison at endpoints. Whether `[1, 4]` and `[4, 5]` overlap is stated in the problem. Read it, and test the touching case.

</div>

## Working with AI

<div class="ai" markdown>

Words to use: min-heap, top-k, size-$k$ heap, `heapq`, interval, overlap, sort by start, sweep.

Prompts to try:

- "Solve LeetCode 215 in Python with a min-heap of size k. State the time complexity in terms of n and k, and compare it with sorting."
- "Explain why Meeting Rooms II sorts by start time and keeps a heap of end times. Show the heap for `[[0, 30], [5, 10], [15, 20]]`."

What to check:

- A max-heap written with `heapq` directly (it is a min-heap). Check for negated values.
- Tuple comparison errors when heap items tie and the second element cannot be compared.
- Merging without `max` on the end, or mutating the input list when the caller still needs it. Run the nested-interval test.

</div>

## Quiz

1\. Why use a min-heap, not a max-heap, to find the $k$ largest?

<details class="solution" markdown>
<summary>Answer</summary>

The smallest of the current $k$ keepers is the one to evict when a bigger value arrives, and a min-heap exposes it at the top.

</details>

2\. What does `merge([[1, 4], [0, 4]])` return?

<details class="solution" markdown>
<summary>Answer</summary>

`[[0, 4]]`. After sorting, `[0, 4]` comes first and `[1, 4]` starts inside it, so the end stays 4.

</details>

3\. A solution to 253 sorts by end time and gets wrong answers. Why?

<details class="solution" markdown>
<summary>Answer</summary>

The sweep assumes meetings arrive in start order, so that each new start is compared with the earliest end among those running. Sorted by end, a late-starting short meeting can appear before a long meeting that started earlier.

</details>

4\. You need the 10 largest of $10^7$ numbers. Heap or full sort?

<details class="solution" markdown>
<summary>Answer</summary>

The heap: $O(n \log 10)$ time and $O(10)$ space, versus $O(n \log n)$ and $O(n)$.

</details>

## Lab

<div class="lab" markdown>

### Lab: K Closest Points to Origin

Goal: solve [973 K Closest Points to Origin](https://leetcode.com/problems/k-closest-points-to-origin/) with a heap. Time: about 15 minutes. Runs in: any terminal with Python 3.

1. Given points `[x, y]`, return the `k` closest to `(0, 0)` in any order.
2. Compare squared distances, `x*x + y*y`, so no square root is needed.
3. You want the $k$ smallest distances, so keep a max-heap of size $k$: push the negated distance and pop when the size exceeds $k$.
4. Assert on `[[1, 3], [-2, 2]]` with `k = 1` (`[[-2, 2]]`) and `[[3, 3], [5, -1], [-2, 4]]` with `k = 2` (the points `[3, 3]` and `[-2, 4]`).

<details class="solution" markdown>
<summary>Solution</summary>

```python
import heapq

def k_closest(points, k):
    heap = []                                 # max-heap by distance, via negation
    for x, y in points:
        heapq.heappush(heap, (-(x * x + y * y), x, y))
        if len(heap) > k:
            heapq.heappop(heap)               # drop the farthest
    return [[x, y] for _, x, y in heap]

assert k_closest([[1, 3], [-2, 2]], 1) == [[-2, 2]]
assert sorted(k_closest([[3, 3], [5, -1], [-2, 4]], 2)) == [[-2, 4], [3, 3]]
print("ok")
```

Time $O(n \log k)$, space $O(k)$.

</details>

</div>

## Where this shows up

- Job schedulers, rate limiters, "trending" lists and leaderboards use size-$k$ heaps; calendar apps merge intervals.
- The [chapter cheat sheet](index.md) collects the signals and templates from all eight lessons.
