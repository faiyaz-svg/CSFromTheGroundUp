# Distributed systems

A compact page of the chapter's ideas. Follow the links for the detail.

## Lessons

1. [Why distributed systems are hard](01-why-distributed-systems-are-hard.md)
2. [Timeouts, retries and circuit breakers](02-timeouts-retries-and-circuit-breakers.md)
3. [Clocks, ordering and delivery](03-clocks-ordering-and-delivery.md)
4. [Consensus and leader election](04-consensus-and-leader-election.md)

## Key terms

| Term | Meaning |
|---|---|
| Distributed system | Computers that cooperate only by sending messages over a network. |
| Partial failure | Some parts fail while the rest keep running. |
| Network partition | Nodes are up but cannot reach each other. |
| Timeout | Longest wait for a reply. A timeout means "unknown", not "failed". |
| Exponential backoff | Retry waits that double up to a cap. |
| Jitter | Randomness added to waits so clients do not retry together. |
| Retry storm | Synchronized retries that keep an overloaded service overloaded. |
| Idempotent | Doing it twice has the same effect as once. |
| Idempotency key | Unique id sent with a request so the server recognizes a repeat. |
| Circuit breaker | Stops calls to a failing dependency: closed, open, half-open. |
| Bulkhead | Limit on resources one dependency can use, so its failure stays contained. |
| Clock skew | Difference between two machines' clocks at one instant. |
| Last write wins | Keep the write with the larger timestamp. Loses data under skew. |
| Happens-before | Event A could have influenced event B. Otherwise they are concurrent. |
| Lamport clock | Counter consistent with happens-before. Cannot detect concurrency. |
| Vector clock | One counter per node. Can detect concurrent events. |
| Consensus | Nodes agree on a value despite failures and lost messages. |
| Quorum | A majority of nodes: $\lfloor N/2 \rfloor + 1$. |
| Split brain | Two parts of a cluster both act as leader. |
| Raft | Consensus algorithm with terms, a leader and a replicated log. |

## Rules

| Situation | Rule |
|---|---|
| Any remote call | Set a timeout shorter than your caller's timeout. |
| Retrying | Only temporary errors, capped attempts, backoff with jitter, in one layer. |
| Retrying a `POST` | Send an idempotency key, created once before the first attempt. |
| Dependency down | Circuit breaker plus a fallback answer. |
| Ordering events across machines | Never compare wall clocks. Use a version number, a sequence from one node or a logical clock. |
| "Exactly once" | At-least-once delivery plus deduplication by message id. |
| Cluster size | 3 or 5 nodes. Even sizes add cost without more failures tolerated. |
| Leader election | Use etcd, ZooKeeper or similar, and a fencing token. Do not build your own. |

## Delivery guarantees

| Guarantee | Sender | Result |
|---|---|---|
| At-most-once | Never retries | May lose, never duplicates |
| At-least-once | Retries until acknowledged | Never loses, may duplicate |
| Exactly-once | At-least-once plus deduplication | One effect, inside the deduplicating system |

## Quorum sizes

| Nodes | Majority | Failures tolerated |
|---|---|---|
| 3 | 2 | 1 |
| 4 | 3 | 1 |
| 5 | 3 | 2 |
| 7 | 4 | 3 |

## Circuit breaker states

| State | Behaviour |
|---|---|
| Closed | Calls pass through and failures are counted. |
| Open | Calls fail at once until the cooldown ends. |
| Half-open | One trial call: success closes the breaker, failure reopens it. |

## Raft in one list

1. Followers expect heartbeats from the leader.
2. After a random election timeout without one, a follower becomes a candidate and starts a new term.
3. A candidate with votes from a majority becomes leader, one leader per term.
4. The leader appends commands to its log and sends them to followers.
5. An entry is committed once a majority hold it.
