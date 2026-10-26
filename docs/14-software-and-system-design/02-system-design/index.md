# System design

A compact page of the chapter's ideas. Lessons 01 to 06 are summarised here as the standard ideas; follow the links for the detail.

## Lessons

1. [Scalability basics](01-scalability-basics.md)
2. [Load balancing](02-load-balancing.md)
3. [Caching strategies](03-caching-strategies.md)
4. [Database scaling: replication and sharding](04-database-scaling-replication-and-sharding.md)
5. [CAP and consistency](05-cap-and-consistency.md)
6. [Queues and event-driven design](06-queues-and-event-driven-design.md)
7. [Rate limiting and API gateways](07-rate-limiting-and-api-gateways.md)
8. [Back-of-the-envelope estimates](08-back-of-the-envelope-estimates.md)
9. [System design interviews](09-system-design-interviews.md)
10. [Case study: a URL shortener](10-case-study-url-shortener.md)
11. [Case study: a chat app](11-case-study-chat-app.md) (optional)

## Key terms

| Term | Meaning |
|---|---|
| Vertical scaling | A bigger machine. Simple, but it has a ceiling and is one point of failure. |
| Horizontal scaling | More machines behind a load balancer. Needs stateless servers. |
| Stateless server | Keeps no per-user data between requests, so any server can take any request. |
| Load balancer | Spreads requests over servers. Layer 4 routes by IP and port, layer 7 by HTTP content. |
| Cache hit rate | Share of lookups answered from the cache. A low rate means the cache adds cost. |
| Replication | Copies of data on several nodes: read capacity and failover. |
| Sharding | Splitting data across nodes by a key: write capacity and size. |
| Consistent hashing | Mapping keys to nodes so adding a node moves few keys. |
| Eventual consistency | Replicas agree if writes stop for long enough, but reads can be stale. |
| Message queue | Holds work between producer and consumer, so spikes are absorbed. |
| Idempotent | Doing it twice has the same effect as doing it once. Needed with retries. |
| Rate limit | Cap on requests per caller per period. |
| API gateway | Single entry point: routing, auth, rate limits, TLS termination. |
| Peak factor | Busiest moment divided by the daily average, usually 2 to 5. |

## Patterns and rules

| Situation | Usual answer |
|---|---|
| Read-heavy | Cache, then read replicas, then CDN for static content |
| Write-heavy | Queue the writes, then shard |
| Spiky or slow work | Put it on a queue, process in the background |
| One server is a single point of failure | Two or more behind a load balancer, with health checks |
| Cache must stay correct | Cache-aside with a TTL, delete the key on write |
| Strong consistency needed | Single primary, or consensus. Accept higher latency. |
| Availability matters more than freshness | Eventual consistency, accept stale reads |
| Retries can duplicate work | Idempotency keys |

CAP says that during a network partition a system chooses between consistency and availability. Without a partition the choice is latency against consistency.

## Rate limiting

| Algorithm | Allows bursts | Note |
|---|---|---|
| Fixed window | At window edges | Cheapest, can pass twice the limit |
| Sliding window | No | Exact, uses more memory |
| Token bucket | Up to bucket size | Usual default |
| Leaky bucket | No, smooths output | Queues requests |

Reject with `429 Too Many Requests` and a `Retry-After` header. Count in a shared store (Redis) with an atomic step. Key by user or API key, by IP only before login.

## Numbers to remember

| Quantity | Value |
|---|---|
| Seconds per day | 86,400 (about $10^5$) |
| 1 million requests per day | about 12 per second |
| $2^{10}$, $2^{20}$, $2^{30}$, $2^{40}$ | thousand, million, billion, trillion |
| Round trip in a data centre | about 0.5 ms |
| SSD random read | about 100 µs |
| $62^6$, $62^7$ | 56.8 billion, 3.5 trillion |

Estimate chain: DAU, requests per day, average QPS, peak QPS, then storage (records times size times 365) and bandwidth (peak QPS times response size). Bytes times 8 gives bits.

## The interview sequence

1. Requirements, functional then non-functional.
2. Estimates.
3. API.
4. Data model.
5. High-level design.
6. Detailed design on the hard parts.
7. Trade-offs and bottlenecks.

## Case study facts

- URL shortener: 7 base62 characters, counter blocks per server, `302` to count clicks, cache-aside Redis, analytics on a queue.
- Chat app: WebSocket connection servers, a shared user to server map, per-conversation sequence numbers, save then deliver, push notifications for offline users, heartbeat presence.
