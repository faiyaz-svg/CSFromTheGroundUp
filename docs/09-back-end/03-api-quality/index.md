# API quality

Cheat sheet for the chapter. Each lesson teaches the idea; this page collects the terms and rules.

## Lessons

1. [Background jobs](01-background-jobs.md): move slow work to a queue and a worker.
2. [Testing and documenting APIs](02-testing-and-documenting-apis.md): endpoint tests, contract tests and an OpenAPI description.

## Key terms

| Term | Meaning |
|---|---|
| Job / queue / worker | A unit of deferred work / where jobs wait / the process that runs them |
| 202 Accepted | Received, processing continues later |
| At-least-once delivery | A job may be delivered twice after a crash |
| Idempotent | Doing it twice has the same effect as once |
| Idempotency key | Unique id used to recognize and skip a repeat |
| Exponential backoff | Retry delays that double: 1 s, 2 s, 4 s |
| Dead letter queue | Where jobs go after all retries fail |
| Cron job | Work that runs at fixed times |
| Endpoint test | Real HTTP request, assert on status and body |
| Contract test | Check that responses match the promised schema |
| OpenAPI / Swagger UI | Machine-readable API description / interactive page built from it |
| Deprecation | Marking a field or version for removal, with notice |

## Libraries

| Job | Node.js | Python |
|---|---|---|
| Queue and workers | BullMQ (Redis) | Celery, RQ |
| Endpoint tests | supertest with `node:test` | httpx with pytest |
| Schema check | a JSON Schema library | `jsonschema` |
| Docs UI | `swagger-ui-express` | built into FastAPI |

## Rules

- Do in the request only what the response needs; queue email, reports, resizing and calls to slow services.
- Every job must be safe to run twice. Give it a stable id and record it as done.
- Retry with backoff up to a limit, fail permanent errors at once, and watch the dead letter queue.
- Test success, each validation failure, 401, 403 and not-found. Assert on the body as well as the status.
- Keep the spec next to the code and test against it. Document error responses. Version breaking changes.

## Sources

[BullMQ docs](https://docs.bullmq.io), [OpenAPI Specification](https://spec.openapis.org/oas/latest.html).
