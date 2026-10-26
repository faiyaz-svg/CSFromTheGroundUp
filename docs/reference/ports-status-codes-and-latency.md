# Ports, status codes and latency numbers

Three tables to look things up in: well-known network ports, HTTP status codes and the cost of common operations in time.

## Common ports

From the [IANA registry](https://www.iana.org/assignments/service-names-port-numbers/service-names-port-numbers.xhtml), as of 2026. Ports 0 to 1023 are well-known, 1024 to 49151 registered, 49152 to 65535 dynamic. Lesson: [ports and sockets](../07-networking/01-how-the-internet-works/04-ports-and-sockets.md).

| Port | Service |
|---|---|
| 21 | FTP (control) |
| 22 | SSH |
| 23 | Telnet |
| 25 | SMTP (mail between servers) |
| 53 | DNS (UDP, and TCP for large answers) |
| 67, 68 | DHCP (server, client) |
| 80 | HTTP |
| 110 | POP3 |
| 123 | NTP |
| 143 | IMAP |
| 443 | HTTPS |
| 445 | SMB (Windows file sharing) |
| 465, 587 | Mail submission (TLS, STARTTLS) |
| 993 | IMAP over TLS |
| 3306 | MySQL |
| 3389 | Remote Desktop |
| 5432 | PostgreSQL |
| 6379 | Redis |
| 8080 | HTTP alternate |
| 27017 | MongoDB |

## HTTP status codes

Lesson: [HTTP requests and responses](../07-networking/02-web-protocols/01-http-requests-and-responses.md). The standard is [RFC 9110](https://www.rfc-editor.org/rfc/rfc9110).

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

## Latency numbers

Lesson: [memory hierarchy and latency numbers](../01-how-computers-work/02-hardware/04-memory-hierarchy-and-latency-numbers.md). The table follows "latency numbers every programmer should know" ([Norvig](https://norvig.com/21-days.html), popularised by Jeff Dean), updated with Simon Eskildsen's cloud measurements in [napkin-math](https://github.com/sirupsen/napkin-math) and [Chips and Cheese's cache tests](https://chipsandcheese.com/p/previewing-meteor-lake-at-ces) for L3. Treat every value as an order of magnitude; a different CPU, SSD or cloud region can move a number by two or three times. What matters is the ratio between rows. The last column multiplies every time by one billion, so 1 ns becomes 1 second.

| Operation | Approximate time (as of 2026) | If 1 ns were 1 second |
|---|---|---|
| One CPU cycle, register access | 0.3 ns | 0.3 seconds |
| L1 cache hit | 1 ns | 1 second |
| L2 cache hit | 4 ns | 4 seconds |
| L3 cache hit | 12 ns | 12 seconds |
| RAM random read | 100 ns | 1.7 minutes |
| SSD random read | 100 µs | 1.2 days |
| Round trip inside one data centre | 500 µs | 5.8 days |
| HDD seek and read | 10 ms | 116 days |
| Round trip within one continent | 40 ms | 1.3 years |
| Round trip across the Atlantic | 90 ms | 2.9 years |
