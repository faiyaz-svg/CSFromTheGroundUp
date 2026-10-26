# Authentication and authorization

Cheat sheet for the chapter. Each lesson teaches the idea; this page collects the terms, rules and tables.

## Lessons

1. [Authentication vs authorization](01-authentication-vs-authorization.md): who you are, versus what you may do.
2. [Sessions, cookies and JWT](02-sessions-cookies-and-jwt.md): how a server remembers a login.
3. [OAuth and SSO](03-oauth-and-sso.md): letting another provider log users in.
4. [CORS and same origin](04-cors-and-same-origin.md): what a browser lets a page read.

## Key terms

| Term | Meaning |
|---|---|
| Authentication (authn) | Verifying who is making the request |
| Authorization (authz) | Deciding whether that identity may do this action |
| RBAC | Permissions granted through roles |
| Least privilege | Each account gets only the permissions its job needs |
| Session | Server-side record of a login, found by a random id in a cookie |
| JWT | `header.payload.signature`, base64url, signed (not encrypted) |
| Access / refresh token | Short-lived credential for requests / longer-lived one used to get new access tokens |
| OAuth 2.0 | Delegated authorization with scoped tokens |
| OIDC | Identity layer on OAuth; adds the ID token |
| PKCE | Code verifier and challenge that bind an authorization code to the client that asked |
| SSO | One login at an identity provider for many apps (OIDC or SAML) |
| Origin | Scheme, host and port |
| Preflight | `OPTIONS` request the browser sends before a non-simple cross-origin request |

## Status codes

| Code | Use |
|---|---|
| 401 | Not authenticated: no, expired or invalid credentials |
| 403 | Authenticated, but not allowed |
| 404 | Also used to hide that another user's record exists |

## Cookie flags

| Flag | Effect |
|---|---|
| `HttpOnly` | JavaScript can't read the cookie |
| `Secure` | Sent only over HTTPS |
| `SameSite=Lax` / `Strict` | Not attached to most cross-site requests |
| `Max-Age` / `Expires` | Lifetime |

## Rules

- Check authentication and authorization on the server, on every request, and deny by default.
- Take identity and role from the verified session or token, never from the request body.
- Prefer a server session in an `HttpOnly`, `Secure`, `SameSite` cookie for a website; use short-lived JWTs for APIs.
- Never put secrets in a JWT payload; always pass `algorithms=[...]` when verifying.
- Use the authorization code flow with PKCE, check `state`, verify the ID token's `iss`, `aud`, `exp`; use a library.
- CORS is a browser rule about reading responses, not a firewall. Never reflect any `Origin` or use `*` with credentials.

## Syntax

```javascript
app.use(session({ secret, resave: false, saveUninitialized: false,
  cookie: { httpOnly: true, secure: true, sameSite: "lax" } }));
app.use(cors({ origin: "https://app.example.com", credentials: true }));
```

```python
jwt.decode(token, key, algorithms=["HS256"])
```

## Sources

[RFC 6749](https://datatracker.ietf.org/doc/html/rfc6749) (OAuth 2.0), [RFC 7636](https://datatracker.ietf.org/doc/html/rfc7636) (PKCE), [RFC 7519](https://datatracker.ietf.org/doc/html/rfc7519) (JWT), [OWASP Session Management](https://cheatsheetseries.owasp.org/cheatsheets/Session_Management_Cheat_Sheet.html), [OWASP Authorization](https://cheatsheetseries.owasp.org/cheatsheets/Authorization_Cheat_Sheet.html), [MDN: CORS](https://developer.mozilla.org/en-US/docs/Web/HTTP/Guides/CORS).
