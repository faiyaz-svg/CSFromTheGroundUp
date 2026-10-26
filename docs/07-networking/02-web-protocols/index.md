# Web protocols

A compact reference for the chapter. For explanations, follow the lesson links.

## Lessons

1. [HTTP requests and responses](01-http-requests-and-responses.md)
2. [HTTP headers, cookies and caching](02-http-headers-cookies-and-caching.md)
3. [TLS, HTTPS and certificates](03-tls-https-and-certificates.md)
4. [Client-server architecture](04-client-server-architecture.md)
5. [Proxies and CDNs](05-proxies-and-cdns.md)
6. [WebSockets and real-time communication](06-websockets-and-real-time.md)
7. [Network debugging tools](07-network-debugging-tools.md)

## The shape of a message

```text
GET /path HTTP/1.1            <- request line (method, path, version)
Host: example.com             <- headers
                              <- blank line
(body)

HTTP/1.1 200 OK               <- status line (version, code, reason)
Content-Type: application/json
                              <- blank line
(body)
```

Standards: [RFC 9110](https://www.rfc-editor.org/rfc/rfc9110) (semantics), [RFC 9111](https://www.rfc-editor.org/rfc/rfc9111) (caching), [RFC 9112](https://www.rfc-editor.org/rfc/rfc9112) (HTTP/1.1), [RFC 9113](https://www.rfc-editor.org/rfc/rfc9113) (HTTP/2), [RFC 9114](https://www.rfc-editor.org/rfc/rfc9114) (HTTP/3). Readable references: [MDN HTTP](https://developer.mozilla.org/en-US/docs/Web/HTTP).

## HTTP methods

| Method | Meaning | Safe | Idempotent | Typical body |
|---|---|---|---|---|
| `GET` | Read | yes | yes | no |
| `HEAD` | Read headers only | yes | yes | no |
| `POST` | Create or run an action | no | no | yes |
| `PUT` | Replace | no | yes | yes |
| `PATCH` | Partial update | no | not guaranteed | yes |
| `DELETE` | Remove | no | yes | usually no |
| `OPTIONS` | Ask what is allowed (CORS preflight) | yes | yes | no |

Safe: changes nothing. Idempotent: repeating it leaves the same state.

## Status codes

| Class | Meaning |
|---|---|
| 1xx | Informational |
| 2xx | Success |
| 3xx | Redirect, or reuse your cached copy |
| 4xx | Client error |
| 5xx | Server error |

| Code | Name | Use |
|---|---|---|
| 101 | Switching Protocols | WebSocket upgrade accepted |
| 200 | OK | Success with a body |
| 201 | Created | A `POST` made a resource |
| 204 | No Content | Success, nothing to return |
| 301 | Moved Permanently | URL changed for good |
| 302 | Found | Temporary redirect |
| 304 | Not Modified | Your cached copy is current |
| 400 | Bad Request | Malformed or invalid request |
| 401 | Unauthorized | Not authenticated |
| 403 | Forbidden | Authenticated but not allowed |
| 404 | Not Found | No such resource |
| 409 | Conflict | Clashes with current state |
| 422 | Unprocessable Content | Well-formed but fails validation |
| 429 | Too Many Requests | Rate limited |
| 500 | Internal Server Error | Unhandled failure |
| 502 | Bad Gateway | Proxy got a bad reply from the origin |
| 503 | Service Unavailable | Overloaded or down |
| 504 | Gateway Timeout | Proxy timed out waiting for the origin |

## Important headers

| Header | Side | Purpose |
|---|---|---|
| `Host` | request | Which site on this server |
| `Content-Type` | both | Body format (`application/json`) |
| `Content-Length` | both | Body size in bytes |
| `Accept` | request | Formats the client accepts |
| `Authorization` | request | Credentials (`Bearer <token>`) |
| `User-Agent` | request | Client software |
| `Cookie` / `Set-Cookie` | request / response | Send and store cookies |
| `Cache-Control` | both | `max-age`, `no-cache`, `no-store`, `public`, `private` |
| `ETag` / `If-None-Match` | response / request | Revalidation, gives `304` |
| `Location` | response | Redirect target |
| `X-Forwarded-For`, `Forwarded` | request | Original client behind a proxy |
| `Upgrade`, `Sec-WebSocket-Key` | request | Ask for a WebSocket |

Cookie attributes: `Secure` (HTTPS only), `HttpOnly` (hidden from JavaScript), `SameSite=Lax|Strict|None`, `Max-Age`, `Path`, `Domain`.

## TLS and certificates

- TLS gives confidentiality, integrity and authentication. HTTPS is HTTP over TLS (port 443). SSL is the obsolete older name.
- A certificate binds a name to a public key. A CA signs it; the chain ends at a trusted root.
- Common errors: expired, name mismatch, self-signed or missing intermediate.
- The padlock means an encrypted connection to the named domain, nothing more.

## Real-time options

| Option | Direction | Use when |
|---|---|---|
| Polling | client asks on a timer | Updates are rare and delay is fine |
| Long polling | server holds the request | Fallback |
| SSE | server to client | One-way events, progress, streaming text |
| WebSocket | both ways | Chat, games, collaboration |

## Proxies and architecture

- A forward proxy acts for clients; a reverse proxy acts for servers; a CDN is a global set of caching reverse proxies; a load balancer spreads requests across servers.
- Stateless servers keep no per-user state in memory, so any server can handle any request. State lives in the client (verify it) or in a shared store.
- Trust `X-Forwarded-*` headers only from your own proxy.

## Debugging commands

| Task | Command |
|---|---|
| Show full exchange | `curl -v URL` |
| Headers only | `curl -sI URL` |
| Send JSON | `curl -X POST URL -H "Content-Type: application/json" -d '{"a":1}'` |
| Timing breakdown | `curl -s -o /dev/null -w "dns %{time_namelookup} tls %{time_appconnect} ttfb %{time_starttransfer}\n" URL` |
| DNS lookup | `nslookup NAME` or `dig NAME` |
| Reachability | `ping -c 4 HOST` (Windows `-n 4`) |
| Path | `traceroute HOST` (Windows `tracert`) |
| Listening ports | `ss -tlnp` (Windows `netstat -an`) |
| Certificate chain | `openssl s_client -connect HOST:443 -servername HOST` |

| Symptom | Likely step |
|---|---|
| `Could not resolve host` | DNS |
| Timeout | Firewall or host down |
| `Connection refused` | Nothing listening on the port |
| Certificate error | TLS |
| `502` / `504` | Proxy fine, origin failing |
