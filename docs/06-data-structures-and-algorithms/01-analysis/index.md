# Analysis

A cheat sheet for the chapter. Each lesson link has the explanation; this page only collects the terms, tables and rules.

## Lessons

1. [Big O and runtime](01-big-o-and-runtime.md)
2. [Space and amortized analysis](02-space-and-amortized-analysis.md)
3. [Analysing recursive algorithms](03-analysing-recursive-algorithms.md)

## Key terms

| Term | Meaning |
|---|---|
| Input size $n$ | The number of items the function works on |
| Step | One basic operation: a comparison, assignment, arithmetic operation or index |
| Big O, $O(g(n))$ | Upper bound: growth is at most a constant times $g$ past some $n_0$ |
| Omega, $\Omega(g(n))$ | Lower bound: growth is at least a constant times $g$ |
| Theta, $\Theta(g(n))$ | Both bounds: growth has exactly the shape $g$ |
| Best, worst, average case | Which inputs are analyzed; a bare Big O usually means the worst case |
| Auxiliary space | Extra memory beyond the input |
| Call stack, stack frame | Memory for each call that has started and not returned; recursion depth is space |
| Dynamic array | An array that grows by a constant factor when full; size is items held, capacity is room |
| Amortized cost | Total cost of $n$ operations divided by $n$, for the worst sequence |
| Recurrence | $T(n)$ written in terms of $T$ on smaller inputs |
| Recursion tree | Every call drawn as a node with its size and own work |
| Memoization | Store each result the first time; look it up on later calls |

## Growth classes

| Class | Name | Typical source | Steps at $n = 1{,}000$ |
|---|---|---|---|
| $O(1)$ | constant | list index | 1 |
| $O(\log n)$ | logarithmic | halve each step | 10 |
| $O(n)$ | linear | one pass | 1,000 |
| $O(n \log n)$ | linearithmic | good sorting | 9,966 |
| $O(n^2)$ | quadratic | loop in a loop | 1,000,000 |
| $O(2^n)$ | exponential | every subset | $10^{301}$ |

## Rules

Count steps, keep the fastest-growing term, drop the constant. Nested loops multiply, loops in sequence add. Doubling or halving a loop variable gives $\log n$. A loop that calls something costing $m$ costs $n \cdot m$.

Python costs: `x in list` is $O(n)$, `x in set` is $O(1)$ on average, `list.insert(0, x)` is $O(n)$, `list.append` is amortized $O(1)$, `sorted` is $O(n \log n)$, a slice copies.

Amortized $O(1)$ append needs growth by a constant factor. Growth by a fixed number of slots gives $O(n)$ per append.

Recursion uses $O(\text{depth})$ space. Python's default limit is 1,000 frames.

## Common recurrences

| Recurrence | Example | Solution |
|---|---|---|
| $T(n/2) + 1$ | binary search | $O(\log n)$ |
| $T(n-1) + 1$ | recursive sum by index | $O(n)$ |
| $2T(n/2) + n$ | merge sort | $O(n \log n)$ |
| $2T(n/2) + 1$ | balanced tree traversal | $O(n)$ |
| $T(n-1) + n$ | quicksort, worst pivot | $O(n^2)$ |
| $2T(n-1) + 1$ | Towers of Hanoi | $O(2^n)$ |

## Master theorem

For $T(n) = a\,T(n/b) + \Theta(n^d)$, with $a \ge 1$, $b > 1$, $d \ge 0$:

| Compare $d$ with $\log_b a$ | Result |
|---|---|
| $d < \log_b a$ | $\Theta(n^{\log_b a})$ |
| $d = \log_b a$ | $\Theta(n^d \log n)$ |
| $d > \log_b a$ | $\Theta(n^d)$ |

It does not cover $T(n-1)$ forms or uneven splits. Memoization costs (distinct subproblems) times (work per subproblem), and helps only when subproblems repeat.
