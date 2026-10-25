# Data structures

A cheat sheet for the chapter. Costs use $n$ for the number of items; for graphs, $V$ is the number of vertices and $E$ the number of edges. "Avg" means average case, and "amort." means amortized (see [arrays and dynamic arrays](01-arrays-and-dynamic-arrays.md)).

## Operations and costs

| Structure | Access by index | Search | Insert | Delete | Notes |
|---|---|---|---|---|---|
| [Array / dynamic array](01-arrays-and-dynamic-arrays.md) | $O(1)$ | $O(n)$ | end: $O(1)$ amort.; middle: $O(n)$ | end: $O(1)$; middle: $O(n)$ | contiguous, cache-friendly |
| [Singly linked list](02-linked-lists.md) | $O(n)$ | $O(n)$ | head: $O(1)$; after a held node: $O(1)$ | head: $O(1)$; after a held node: $O(1)$ | no index; pointer per node |
| [Stack](03-stacks-and-queues.md) | none | $O(n)$ | push: $O(1)$ | pop: $O(1)$ | last in, first out |
| [Queue / deque](03-stacks-and-queues.md) | none (deque middle: $O(n)$) | $O(n)$ | enqueue: $O(1)$ | dequeue: $O(1)$ | first in, first out; a deque works at both ends |
| [Hash table](04-hash-tables.md) | none | by key: $O(1)$ avg, $O(n)$ worst | $O(1)$ avg | $O(1)$ avg | no useful order of keys |
| [Binary search tree](05-trees-and-binary-search-trees.md), balanced | none | $O(\log n)$ | $O(\log n)$ | $O(\log n)$ | in-order walk is sorted, $O(n)$; unbalanced is $O(n)$ |
| [Binary heap](06-heaps-and-priority-queues.md) | none | $O(n)$ | $O(\log n)$ | pop min: $O(\log n)$ | peek min: $O(1)$; build: $O(n)$ |
| [Graph, adjacency list](07-graphs-and-representations.md) | none | edge check: $O(\deg u)$ | add edge: $O(1)$ | remove edge: $O(\deg u)$ | memory $O(V + E)$ |
| [Graph, adjacency matrix](07-graphs-and-representations.md) | none | edge check: $O(1)$ | add edge: $O(1)$ | remove edge: $O(1)$ | memory $O(V^2)$ |
| [Trie](08-tries-and-union-find.md) | none | word or prefix of length $L$: $O(L)$ | $O(L)$ | $O(L)$ | memory grows with distinct prefixes |
| [Union find](08-tries-and-union-find.md) | none | find: about $O(\alpha(n))$ amort. | union: about $O(\alpha(n))$ amort. | not supported | with path compression and union by size |

## What Python and JavaScript provide

| Structure | Python | JavaScript |
|---|---|---|
| Dynamic array | `list` | `Array` |
| Linked list | none (write a `Node` class) | none |
| Stack | `list`: `append`, `pop` | `Array`: `push`, `pop` |
| Queue, deque | `collections.deque`: `append`, `popleft` | no built-in; `Array.shift` can be slow when large |
| Hash table, set | `dict`, `set`, `collections.Counter`, `defaultdict` | `Map`, `Set` |
| Sorted collection | `list` with `bisect`; third-party `sortedcontainers` | none |
| Heap | `heapq` (min-heap on a `list`) | none |
| Graph | `dict` of `list` or `set` | `Map` of arrays |
| Trie, union find | nested `dict`, `parent` list | nested `Map`, array |

## Choosing a structure

| You need | Use |
|---|---|
| Fast lookup by position, or a general sequence | dynamic array |
| Fast lookup by key, or "have I seen this?" | hash table or set |
| Last in, first out (undo, brackets, DFS) | stack |
| First in, first out (work waiting its turn, BFS) | queue (`deque`) |
| Always the smallest or largest item next, or the top $k$ | heap |
| Keys in sorted order with fast insert, or range queries | balanced tree, or a sorted list with `bisect` |
| Things and the connections between them | graph (adjacency list unless the graph is dense) |
| All words that start with a prefix | trie |
| Are these two items connected, as links are added? | union find |

## Key terms

- **Contiguous**: stored side by side in memory, with no gaps.
- **Amortized**: the average cost per operation over a long run.
- **LIFO, FIFO**: last in first out, first in first out.
- **Collision**: two keys in one hash table bucket. **Load factor**: entries divided by buckets.
- **Hashable**: has a hash that never changes; lists, dicts and sets are not.
- **Invariant**: a rule that always holds. The BST rule: left keys smaller, right keys larger. The heap rule: a parent is not larger than its children.
- **Height**: nodes on the longest root-to-leaf path. **Balanced**: height near $\log_2 n$.
- **Degree**: the number of edges at a vertex. **Sparse**: $E$ much smaller than $V^2$.

## Rules of thumb

- A list used as a queue (`pop(0)`, `insert(0, x)`) is an $O(n)$ loop body. Use `deque`.
- Turn a list into a set before repeated "is it in there?" checks.
- A heap is not sorted. It only guarantees that the root is the minimum.
- A tree is $O(\log n)$ only when balanced.
- Use an adjacency list for sparse graphs. Add both directions for undirected edges.
- The heap indexes are $2i + 1$, $2i + 2$ and $(i - 1) // 2$.

Back to the [analysis](../01-analysis/index.md) cheat sheet for Big O, or forward to the [algorithms](../03-algorithms/index.md) chapter.
