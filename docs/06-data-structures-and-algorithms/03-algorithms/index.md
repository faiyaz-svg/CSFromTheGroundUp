# Algorithms

A cheat sheet for the chapter. Each lesson link has the explanation; this page only collects the terms, tables and rules.

## Lessons

1. [Binary search](01-binary-search.md)
2. [Sorting](02-sorting.md)
3. [BFS and DFS](03-bfs-and-dfs.md)
4. [Shortest paths](04-shortest-paths.md)
5. [Greedy algorithms](05-greedy-algorithms.md)
6. [Dynamic programming](06-dynamic-programming.md)

## The algorithms at a glance

Here $n$ is the number of items, $V$ the number of nodes and $E$ the number of edges.

| Algorithm | Idea | Time | Extra space | When to use |
|---|---|---|---|---|
| Binary search | Compare with the middle, drop half | $O(\log n)$ | $O(1)$ | Sorted array, or a yes/no test that flips once |
| Insertion sort | Slide each item into the sorted left part | $O(n^2)$, $O(n)$ if nearly sorted | $O(1)$ | Tiny or nearly sorted lists |
| Merge sort | Split, sort halves, merge | $O(n \log n)$ always | $O(n)$ | Stable sort with a guaranteed bound |
| Quick sort | Partition around a pivot, recurse | $O(n \log n)$ average, $O(n^2)$ worst | $O(\log n)$ average | Fast in-memory sort, stability not needed |
| Timsort (`sorted`) | Find sorted runs, merge them | $O(n \log n)$, close to $O(n)$ on sorted input | $O(n)$ | Almost always, in Python |
| BFS | Queue, layer by layer | $O(V + E)$ | $O(V)$ | Fewest edges, level order, nearest target |
| DFS | Stack or recursion, dive then back up | $O(V + E)$ | $O(V)$ | Reachability, components, cycles, exploring options |
| Dijkstra | Heap, always finish the nearest node | $O((V + E) \log V)$ | $O(V)$ | Cheapest path, weights at least 0 |
| Bellman-Ford | Relax every edge $V - 1$ times | $O(VE)$ | $O(V)$ | Negative weights, detecting negative cycles |
| A* | Dijkstra ordered by distance plus a never-too-high estimate | Depends on the estimate | $O(V)$ | One start and one goal with a good heuristic |
| Greedy (interval scheduling) | Sort by end time, take what fits | $O(n \log n)$ | $O(1)$ beyond the sort | Only when a greedy-choice argument holds |
| Dynamic programming | Store answers to repeated subproblems | States times work per state | Often the table size | Overlapping subproblems and optimal substructure |

## Key terms

| Term | Meaning |
|---|---|
| Invariant | A statement that stays true on every pass of a loop |
| Predicate | A function returning true or false; binary search on the answer needs one that flips once |
| Stable sort | Equal keys keep their original order |
| Frontier | Nodes found but not yet processed; a queue in BFS, a stack in DFS |
| Visited set | Nodes already reached; stops cycles from looping forever |
| Relax an edge | If `dist[u] + w < dist[v]`, set `dist[v] = dist[u] + w` |
| Greedy-choice property | Some optimal solution starts with the greedy choice |
| Exchange argument | Swap an optimal solution's first choice for the greedy one without making it worse |
| State, recurrence, base case | What identifies a subproblem, how its answer comes from smaller ones, and the smallest known answers |
| Memoization, tabulation | Top-down with a cache; bottom-up with a table |

## Python tools

| Need | Use |
|---|---|
| First index where `a[i] >= x` | `bisect_left(a, x)` |
| One past the last item equal to `x` | `bisect_right(a, x)` |
| Sort a copy, or in place | `sorted(items, key=f)`, `items.sort(key=f)` |
| Sort descending, keeping ties stable | `sorted(items, key=f, reverse=True)` |
| BFS queue | `collections.deque`, `append` and `popleft` |
| DFS stack | a `list`, `append` and `pop` |
| Priority queue | `heapq.heappush`, `heapq.heappop` on `(priority, item)` tuples |
| Cache a recursive function | `@functools.cache` |

## Rules of thumb

- Binary search needs sorted input. Use one loop style: `lo <= hi` with `hi = mid - 1`, or `lo < hi` with `hi = mid`.
- Do not write your own sort for real work; use `sorted` with a key.
- Mark a node visited when you add it to the frontier, not when you remove it.
- BFS gives the fewest edges. It does not give the cheapest path when edges have different weights.
- Dijkstra fails on negative weights; Bellman-Ford handles them.
- A greedy rule needs a proof or a brute-force check against small inputs. One counterexample kills it.
- DP running time is the number of states times the work per state.

## Choosing an algorithm

| The problem says | Think of |
|---|---|
| Sorted array, find a value or a boundary | Binary search |
| "Smallest value that works" and a yes/no test | Binary search on the answer |
| Fewest steps, equal-cost moves, grid maze | BFS |
| Is it reachable, count groups, find a cycle | DFS or BFS |
| Cheapest route with positive costs | Dijkstra |
| Costs can be negative | Bellman-Ford |
| Maximum number of non-overlapping things | Greedy, sort by end |
| Fewest or number of ways, with repeated subproblems | Dynamic programming |
| Compare two strings or sequences | LCS or edit distance table |
