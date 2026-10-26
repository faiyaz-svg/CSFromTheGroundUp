# Operations

A compact reference for watching a running system and responding when it breaks. Lessons: [logging, metrics and monitoring](01-logging-metrics-and-monitoring.md) and [incidents and on-call](02-incidents-and-on-call.md).

## Signals

| Signal | Answers | Example |
|---|---|---|
| Log | What happened in this event? | `{"level": "ERROR", "message": "payment failed", "request_id": "req-7f3a"}` |
| Metric | How much, how often, how fast? | requests per second, p99 latency |
| Trace | Where did one request spend its time? | spans sharing one trace ID |

## Logging

- Structured logs: one JSON object per line, to standard output.
- Python levels: `DEBUG` 10, `INFO` 20, `WARNING` 30, `ERROR` 40, `CRITICAL` 50.
- Attach a request ID to every line. Log IDs, never secrets, tokens or personal data ([privacy and PIPEDA](../../12-security/02-cryptography/06-privacy-and-pipeda.md)).

## Metrics

| Type | Behaviour | Example |
|---|---|---|
| Counter | only goes up | requests served |
| Gauge | up and down | queue length |
| Histogram | values counted into buckets | request durations |

| Method | For | Measures |
|---|---|---|
| RED | request-handling services | Rate, Errors, Duration |
| USE | resources (CPU, disk, pool) | Utilization, Saturation, Errors |
| Golden signals | any service | latency, traffic, errors, saturation |

Use p50, p95 and p99, not the mean. Keep label values bounded.

## Tracing

- A trace is made of spans. A span has a name, start and end time, parent and attributes.
- Context propagation carries the trace ID between services (the `traceparent` header).
- OpenTelemetry is the standard. Prometheus and Grafana, CloudWatch and Datadog store and display the data.

## Alerting

- Alert on symptoms (error rate, latency), not causes (CPU).
- Every page needs a human decision. Too many pages cause alert fatigue.

## Reliability targets

| Term | Meaning |
|---|---|
| SLI | measurement, such as the share of successful requests |
| SLO | target for the SLI over a window |
| SLA | contract with consequences |
| Error budget | $1 - \text{SLO}$ |
| Burn rate | share of budget used divided by share of window elapsed |

Budget for 99.9% over 30 days: 43.2 minutes of full downtime, or 0.1% of requests.

## Incidents

1. Acknowledge the page.
2. Check the symptom and what changed.
3. Set severity, and declare an incident if serious.
4. Mitigate (rollback, feature flag, scale, failover) before root-causing.
5. Communicate on a schedule.
6. Write a blameless postmortem with owned action items.

Roles: incident commander, ops lead (the only one changing the system), communications lead.
