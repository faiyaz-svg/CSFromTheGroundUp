# Discrete math for CS

The math that algorithms, databases and cryptography rest on: logic, sets, proofs, counting, probability, graphs and modular arithmetic.

Before this folder: Programming fundamentals.

The lessons and chapter cheat sheets for this folder are written in reading order.

<!-- lessons:start -->
## Lessons

1. [Logic and truth tables](01-logic-and-truth-tables.md)
2. [Sets, functions and relations](02-sets-functions-and-relations.md)
3. [Proof techniques and induction](03-proof-techniques-and-induction.md)
4. [Counting](04-counting.md)
5. [Discrete probability](05-discrete-probability.md)
6. [Graphs and trees](06-graphs-and-trees.md)
7. [Modular arithmetic](07-modular-arithmetic.md)
8. [Sums, logs and recurrences](08-sums-logs-and-recurrences.md)

<!-- lessons:end -->

## Cheat sheet

Each section links its lesson. This page collects the rules; the lessons explain them.

### Logic

[Logic and truth tables](01-logic-and-truth-tables.md)

- De Morgan: $\lnot(p \land q) \equiv \lnot p \lor \lnot q$ and $\lnot(p \lor q) \equiv \lnot p \land \lnot q$. Negating flips the connective.
- Implication: $p \to q \equiv \lnot p \lor q$. It equals its contrapositive $\lnot q \to \lnot p$, not its converse $q \to p$.
- Quantifiers: `all()` is "for every", `any()` is "there exists"; negating one gives the other with the condition negated.
- `a and b` skips `b` when `a` is false; `a or b` skips `b` when `a` is true.
- To prove two conditions equivalent, compare all $2^n$ rows of the truth table.

### Sets, functions and relations

[Sets, functions and relations](02-sets-functions-and-relations.md)

| Operation | Math | Python | SQL |
|---|---|---|---|
| Union | $A \cup B$ | `a \| b` | `UNION` |
| Intersection | $A \cap B$ | `a & b` | `INTERSECT` |
| Difference | $A \setminus B$ | `a - b` | `EXCEPT` |
| Symmetric difference | | `a ^ b` | |

- $\lvert A \cup B \rvert = \lvert A \rvert + \lvert B \rvert - \lvert A \cap B \rvert$.
- A function gives one output per input. Injective: no two inputs share an output. Surjective: every output is hit. Bijective: both, so it can be inverted.
- A relation is any set of pairs (a subset of $A \times B$). `UNION ALL` keeps duplicates; `UNION` removes them.

### Proofs and induction

[Proof techniques and induction](03-proof-techniques-and-induction.md)

- Passing tests is not a proof. One counterexample disproves "for every".
- Induction: base case, then assume $P(k)$ and prove $P(k+1)$.
- Loop invariant: initialization, maintenance, termination. Check it with an `assert` while developing.
- Formula to remember: $1 + 2 + \dots + n = n(n+1)/2$.

### Counting

[Counting](04-counting.md)

| Order matters | Repetition | Count |
|---|---|---|
| Yes | Yes | $n^k$ |
| Yes | No | $n!/(n-k)!$ |
| No | No | $\binom{n}{k}$ |
| No | Yes | $\binom{n+k-1}{k}$ |

- Rule of product multiplies the options per step; rule of sum adds disjoint cases.
- Complement rule: count "at least one" as total minus "none".
- Pigeonhole: more than $n$ items in $n$ boxes forces a shared box.
- Python: `math.comb`, `math.perm`, `math.factorial`, `itertools.product`, `permutations`, `combinations`.

### Discrete probability

[Discrete probability](05-discrete-probability.md)

- $P(E) = \lvert E \rvert / \lvert S \rvert$ for equally likely outcomes; $P(\text{not } E) = 1 - P(E)$.
- Independent events: $P(A \cap B) = P(A)\,P(B)$. Conditional: $P(A \mid B) = P(A \cap B)/P(B)$.
- Expected value is linear: $E[X + Y] = E[X] + E[Y]$.
- Collision among $n$ keys in $N$ slots: $1 - \prod_{i=0}^{n-1} (N-i)/N$; 50% at about $1.18\sqrt{N}$ keys. Quick estimate: $\binom{n}{2}/N$.
- Rare events produce mostly false alarms: check the base rate.

### Graphs and trees

[Graphs and trees](06-graphs-and-trees.md)

- Graph $(V, E)$: directed or undirected; path, cycle, connected, degree.
- DAG: directed, no cycle. A topological order exists exactly for a DAG: `graphlib.TopologicalSorter`.
- Tree: connected, no cycle, $n - 1$ edges for $n$ vertices. One path between any two vertices. One extra edge makes a cycle.
- Adjacency list: space about $\lvert V \rvert + \lvert E \rvert$. Reverse the edges to ask "who depends on this".

### Modular arithmetic

[Modular arithmetic](07-modular-arithmetic.md)

- $a \equiv b \pmod n$ means $n$ divides $a - b$. Reduce sums and products at any step.
- Python: `a % n`, `pow(b, e, n)`, `pow(a, -1, n)` (inverse, needs $\gcd(a, n) = 1$). In JavaScript, C and Java `%` can be negative.
- Hash bucket: `h % m`; for $m$ a power of two, `h & (m - 1)`.
- Luhn: double every second digit from the right, subtract 9 above 9, sum, total divisible by 10.
- Toy RSA: $c = m^e \bmod n$, $m = c^d \bmod n$, with $ed \equiv 1 \pmod{(p-1)(q-1)}$. Never use unpadded RSA.

### Sums, logs and recurrences

[Sums, logs and recurrences](08-sums-logs-and-recurrences.md)

| Sum | Closed form |
|---|---|
| $1 + 2 + \dots + n$ | $n(n+1)/2$ |
| $1 + 2 + 4 + \dots + 2^k$ | $2^{k+1} - 1$ |
| $1 + \tfrac12 + \dots + \tfrac1n$ | about $\ln n + 0.58$ |

| Recurrence | Total cost |
|---|---|
| $T(n) = T(n/2) + 1$ | $\log_2 n$ |
| $T(n) = 2T(n/2) + n$ | $n \log_2 n$ |
| $T(n) = T(n-1) + n$ | $n(n+1)/2$ |
| $T(n) = 2T(n-1) + 1$ | $2^n - 1$ |

- Halving $n$ down to 1 takes $\lfloor \log_2 n \rfloor + 1$ steps, which is `n.bit_length()`. Log bases differ by a constant.
- Solve a recurrence by cost per level times number of levels.
