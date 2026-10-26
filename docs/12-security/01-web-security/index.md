# Web security

A compact reference for the chapter. Lessons: [security mindset and threat modelling](01-security-mindset-and-threat-modelling.md), [OWASP top 10](02-owasp-top-10.md), [injection and input validation](03-injection-and-input-validation.md), [XSS, CSRF and browser security](04-xss-csrf-and-browser-security.md), [secure authentication](05-secure-authentication.md), [secrets and dependency security](06-secrets-and-dependency-security.md).

## Threat modelling

Four questions: what are we building, what can go wrong, what do we do about it, did we do enough. Draw assets, flows and trust boundaries, then walk STRIDE (spoofing, tampering, repudiation, information disclosure, denial of service, elevation of privilege). Design rules: defence in depth, least privilege, secure by default, never trust the client.

## OWASP Top 10:2025

Source: [top10.owasp.org/2025](https://top10.owasp.org/2025) (as of 2026).

| # | Category | One-line defence |
|---|---|---|
| A01 | Broken access control | Deny by default; check ownership and role on the server for every request |
| A02 | Security misconfiguration | Hardened, repeatable config; no defaults, debug or open storage in production |
| A03 | Software supply chain failures | Lockfiles, audits, pinned versions, few dependencies, an SBOM |
| A04 | Cryptographic failures | HTTPS everywhere, Argon2id for passwords, vetted libraries |
| A05 | Injection | Parameterized queries, argument lists, allow-lists, output encoding |
| A06 | Insecure design | Threat model before building; secure design patterns |
| A07 | Authentication failures | Rate limits, MFA or passkeys, generic errors, new session after login |
| A08 | Software or data integrity failures | Verify signatures and checksums; never deserialize untrusted data |
| A09 | Security logging and alerting failures | Log auth and access events; alert on patterns; protect the logs |
| A10 | Mishandling of exceptional conditions | Fail closed; central error handling; generic error messages |

## Injection fixes

| Attack | Fix |
|---|---|
| SQL injection | Placeholders (`$1`, `?`); allow-list identifiers |
| Command injection | Argument list, no `shell=True`; avoid shelling out |
| Template injection | Never build template source from input; pass data as variables |
| Path traversal | `resolve()` then check the path is inside the base folder |
| XSS | Output encoding; sanitizer for HTML; CSP; `HttpOnly` cookies |

## Security headers

| Header | Example value | Purpose |
|---|---|---|
| `Content-Security-Policy` | `default-src 'self'; script-src 'self'; frame-ancestors 'none'` | Limits where scripts, styles and frames load from; blocks inline injected scripts |
| `Strict-Transport-Security` | `max-age=31536000; includeSubDomains` | Browser uses HTTPS only for this site |
| `X-Content-Type-Options` | `nosniff` | Browser does not guess content types |
| `Referrer-Policy` | `strict-origin-when-cross-origin` | Limits URL leakage to other sites |
| `Permissions-Policy` | `camera=(), microphone=()` | Turns off browser features you do not use |
| `X-Frame-Options` | `DENY` | Older clickjacking defence; `frame-ancestors` replaces it |
| `Set-Cookie` flags | `HttpOnly; Secure; SameSite=Lax` | Hides cookie from scripts, HTTPS only, limits cross-site sending |

Reference: [MDN HTTP headers](https://developer.mozilla.org/en-US/docs/Web/HTTP/Reference/Headers) and the [OWASP HTTP Headers Cheat Sheet](https://cheatsheetseries.owasp.org/cheatsheets/HTTP_Headers_Cheat_Sheet.html).

## Browser attacks

| Attack | How it works | Defence |
|---|---|---|
| Stored XSS | Payload saved in the database, shown to all visitors | Escape output, CSP |
| Reflected XSS | Payload in a link, echoed in the response | Escape output, CSP |
| DOM XSS | Own JavaScript writes untrusted data via `innerHTML` | `textContent`, sanitizer |
| CSRF | Victim's browser sends a forged request with its cookie | `SameSite`, CSRF token, no state change on `GET` |
| Clickjacking | Your site in a hidden frame | `frame-ancestors` |

## Authentication rules

- Passwords: Argon2id (minimum 19 MiB memory, 2 iterations, 1 parallelism as of 2026); bcrypt only if needed (cost at least 10, 72-byte limit). The library makes the salt.
- Check new passwords against breached lists; require length, not odd complexity rules.
- Rate limit per account and per IP; prefer delays to hard lockout.
- Same message and similar timing for unknown user and wrong password, on login, signup and reset.
- New session id after login. Reset tokens: random, single use, short expiry, stored hashed.
- Prefer passkeys or authenticator-app MFA over SMS.

## Secrets and dependencies

| Task | Command or rule |
|---|---|
| Read a secret | `os.environ["NAME"]` or `process.env.NAME`; never log it |
| Ignore local secrets | `.env` in `.gitignore`; commit `.env.example` |
| Leaked a key | Revoke and rotate first, then clean up |
| Audit npm | `npm audit` |
| Audit Python | `pip-audit` |
| Reproducible install | `npm ci`, locked requirements |
| Auto-updates | Dependabot pull requests |
| Inventory | Generate an SBOM (CycloneDX or SPDX) in CI |
