# Building with LLMs

A compact reference for the chapter. Facts marked "as of 2026" change; follow the links in each lesson.

## Lessons

1. [Calling an LLM API](01-calling-an-llm-api.md)
2. [Prompt and context engineering](02-prompt-and-context-engineering.md)
3. [Tool use](03-tool-use.md)
4. [RAG embeddings and pgvector](04-rag-embeddings-and-pgvector.md)
5. [Agents and harnesses](05-agents-and-harnesses.md)
6. [MCP (Model Context Protocol)](06-mcp.md)
7. [Evals](07-evals.md)

## Key terms

| Term | Meaning |
|---|---|
| Messages API | HTTP API: `POST /v1/messages` with `model`, `max_tokens`, `system`, `messages` |
| System prompt | Standing instructions, separate from the conversation |
| Usage | `input_tokens` and `output_tokens` in each response, the basis of cost |
| Stop reason | `end_turn`, `max_tokens`, `tool_use`, `refusal` |
| Context engineering | Choosing which tokens enter the window on each call |
| Tool use | The model returns a `tool_use` block, your code runs it, you return a `tool_result` |
| RAG | Retrieve relevant chunks, put them in the prompt, answer with citations |
| Agent | An LLM that picks its own next step in a loop |
| Harness | The code around the model: tools, permissions, context, memory, limits |
| MCP | Open protocol for connecting AI apps (hosts) to tool servers |
| Golden set | Fixed test cases with expected answers |
| LLM-as-judge | A model scoring outputs against a rubric |

## API facts (as of 2026)

| Item | Value |
|---|---|
| Endpoint | `POST https://api.anthropic.com/v1/messages` |
| Required headers | `Authorization: Bearer <key>` (or legacy `x-api-key`), `anthropic-version: 2026-10-21`, `content-type: application/json` |
| Model IDs | `claude-fable-5-1`, `claude-opus-5-5`, `claude-sonnet-5-5`, `claude-haiku-5-5` |
| Price per million tokens (input / output) | Fable 5.1 \$10 / \$50, Opus 5.5 \$4 / \$20, Sonnet 5.5 \$2 / \$10, Haiku 5.5 from \$0.10 / \$0.50 |
| Removed in `2026-10-21` | `temperature`, `top_p`, `top_k` (400 if sent) |
| Key storage | environment variable `ANTHROPIC_API_KEY`, server side only |

Sources: [API overview](https://platform.claude.com/docs/en/api/overview), [versions](https://platform.claude.com/docs/en/api/versioning), [models overview](https://platform.claude.com/docs/en/models/overview).

## Errors and retries

| Status | Meaning | Retry? |
|---|---|---|
| 400 | Bad request | No, fix it |
| 401, 403 | Bad key, no permission | No |
| 404 | Unknown model or path | No |
| 413 | Request too large | No |
| 429 | Rate limited | Yes, with backoff and `retry-after` |
| 500, 529 | Server error, overloaded | Yes, with backoff |

Backoff: wait a random time up to `min(cap, base * 2^attempt)`. The SDK retries 2 times by default (`max_retries`).

## Tool-use loop

1. Send `tools` and `messages`.
2. If `stop_reason` is `tool_use`, append the assistant response.
3. Validate each `tool_use` block (allowlist, JSON Schema), run it, build a `tool_result` with the same `tool_use_id`.
4. Send all results in one `user` message.
5. Repeat until `end_turn` or a turn cap.

## Prompt checklist

- State the task, audience and output format.
- Give the reason behind each rule.
- Three to five varied examples inside `<example>` tags.
- Tags around each kind of content; long documents first, question last.
- Include the context the model cannot know.
- Rerun a fixed test set after every edit.

## pgvector (unverified here, from the README)

| Item | Syntax |
|---|---|
| Enable | `CREATE EXTENSION vector;` |
| Column | `embedding vector(1024)` |
| Cosine / L2 / inner product distance | `<=>` / `<->` / `<#>` |
| HNSW index | `CREATE INDEX ON chunks USING hnsw (embedding vector_cosine_ops);` |
| Recall setting | `SET hnsw.ef_search = 100;` (default 40) |
| Top-k query | `ORDER BY embedding <=> $1 LIMIT k` |
| Hybrid merge | reciprocal rank fusion: score $= \sum 1/(60 + \text{rank})$ |

Source: [pgvector README](https://github.com/pgvector/pgvector).

## Agents and workflows

| Design | Use when |
|---|---|
| One call with retrieval and examples | The task fits in one prompt |
| Workflow (chain, routing, parallel, orchestrator-workers, evaluator-optimizer) | You can write the steps down |
| Agent | The number of steps is unpredictable, the task justifies the cost, mistakes can be caught |

Harness parts: tools, permissions (allow, ask, deny), context management, memory, subagents, step and cost limits. Source: [Building effective agents](https://www.anthropic.com/engineering/building-effective-agents).

## MCP

| Item | Value |
|---|---|
| Roles | host (app), client (one per server), server |
| Primitives | tools, resources, prompts |
| Transports | stdio (local process), streamable HTTP (network) |
| Core methods | `server/discover`, `tools/list`, `tools/call`, `resources/read`, `prompts/get` |
| Python SDK (2.x) | `from mcp.server import MCPServer`, `@mcp.tool()`, `mcp.run(transport="stdio")` |
| stdio rule | never write to stdout, log to stderr |

Source: [modelcontextprotocol.io](https://modelcontextprotocol.io/docs/learn/architecture).

## Eval checklist

- 20 to 50 real cases, including edge cases and "can't tell".
- Cheapest scorer that works: code first, rubric next, judge last.
- Judge: narrow rubric, different model, both orders, check against human labels.
- Held-out set; compare per case as well as the average.
- Record prompt version, model ID, score and cost.

## Common mistakes

- API key in code or a browser bundle.
- Ignoring `stop_reason` or retrying 400 and 401.
- Trusting tool arguments, or giving one tool broad powers.
- Blaming the model for a retrieval miss.
- Mixing embedding models in one column.
- An agent with no step cap, cost cap or approvals.
- `print()` in a stdio MCP server.
- Tuning a prompt on the cases used to score it.
