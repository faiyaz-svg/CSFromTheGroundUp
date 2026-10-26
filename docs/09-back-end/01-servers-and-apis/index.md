# Servers and APIs

Cheat sheet for the chapter. Facts as of 2026: Node.js 24 (LTS), Express 5, zod 4, FastAPI 0.162, Django 6.1.

## Lessons

1. [What a back end does](01-what-a-back-end-does.md)
2. [Node.js and its runtime](02-nodejs-and-its-runtime.md)
3. [Express: routing and middleware](03-express-routing-and-middleware.md)
4. [REST API design](04-rest-api-design.md)
5. [Validation and error handling](05-validation-and-error-handling.md)
6. [Other API styles: GraphQL, gRPC and webhooks](06-other-api-styles-graphql-grpc-webhooks.md) (optional)
7. [Python back ends: FastAPI and Django](07-python-back-ends-fastapi-and-django.md) (optional)

## Key terms

| Term | Meaning |
|---|---|
| Back end | Program that handles requests, applies business logic, talks to data and other services |
| Event loop | Runs finished operations' callbacks one at a time on Node's main thread |
| Blocking | Code that keeps the main thread busy so no other request runs |
| Middleware | `(req, res, next)` function that runs before the handler |
| Idempotent | Same effect whether sent once or many times |
| Schema validation | Checking input shape and values against a declared schema |
| Problem details | Standard JSON error body (RFC 9457, `application/problem+json`) |
| Webhook | Request a service sends to your URL when an event happens |

## REST conventions

| Request | Meaning | Idempotent | Success status |
|---|---|---|---|
| `GET /tasks` | list (paginated) | yes | 200 |
| `POST /tasks` | create | no | 201 + `Location` |
| `GET /tasks/42` | read one | yes | 200 |
| `PUT /tasks/42` | replace | yes | 200 |
| `PATCH /tasks/42` | change some fields | not guaranteed | 200 |
| `DELETE /tasks/42` | remove | yes | 204 |

Plural nouns, lowercase with hyphens, no verbs, one level of nesting. Filter and sort in the query string. Version in the path (`/v1/`). One error shape everywhere.

## Status codes for APIs

| Status | Use it when |
|---|---|
| 200 / 201 / 204 | OK / created / done, no body |
| 400 | malformed request (bad JSON) |
| 401 | no valid credentials |
| 403 | authenticated but not allowed |
| 404 | no such resource |
| 409 | conflicts with current state |
| 422 | well-formed but fails validation |
| 429 | rate limit exceeded |
| 500 | the server failed |

## Express snippet

```javascript
import express from "express";
import { z } from "zod";

const app = express();
app.use(express.json());                              // before routes that read req.body

const Body = z.object({ title: z.string().min(1) });

app.get("/items/:id", (req, res) => res.json({ id: Number(req.params.id) }));
app.post("/items", (req, res) => {
  const parsed = Body.safeParse(req.body);
  if (!parsed.success) return res.status(422).json({ errors: parsed.error.issues });
  res.status(201).location("/items/1").json(parsed.data);
});

app.use((err, req, res, next) => {                    // four parameters, registered last
  console.error(err.stack);
  res.status(err.status ?? 500).json({ title: "Error" });
});

app.listen(3000);
```

## Node.js rules

- One JavaScript thread. Never run long CPU work or a `Sync` call inside a handler.
- The libuv thread pool has 4 threads by default (`UV_THREADPOOL_SIZE`). CPU work goes to a worker thread or another process.
- Configuration comes from `process.env`; `node --env-file=.env app.mjs` loads a file. Don't commit secrets.
- `package.json` scripts: `npm start`, `npm run dev` (for example `node --watch server.mjs`).

## Rules for every endpoint

1. Validate input with a schema at the edge; use the parsed result, not the raw body.
2. Log the full error on the server; send a generic message for 5xx.
3. Use the status code that matches the failure; never 200 with an error body.
4. Paginate every list.
5. Verify webhook signatures on the raw body.

## Frameworks side by side

| Idea | Express | FastAPI | Django |
|---|---|---|---|
| Run | `node app.mjs` | `uvicorn main:app` | `python manage.py runserver` |
| Route | `app.get("/x/:id", fn)` | `@app.get("/x/{id}")` | `path("x/<int:id>/", view)` |
| Validate | zod | Pydantic | forms / serializers |
| Docs | add-on | `/docs`, `/openapi.json` | add-on |
