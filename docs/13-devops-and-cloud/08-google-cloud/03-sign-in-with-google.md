# Sign in with Google

After this you can set up the Google Auth Platform for a web app, create an OAuth client with the right origins and redirect URIs, and verify the ID token on your server so a forged login is rejected.

Before this: [OAuth and SSO](../../09-back-end/02-auth/03-oauth-and-sso.md), [APIs, keys and service accounts](02-apis-keys-and-service-accounts.md) and [Google Search Console and analytics](../07-search-and-launch/02-google-search-console-and-analytics.md).

## The idea

The tutoring site from the launch case study wants a booking page where parents sign in with their Google account instead of creating a password. The [OAuth and SSO](../../09-back-end/02-auth/03-oauth-and-sso.md) lesson explained the protocol. This lesson is the Google-specific setup: what to fill in on the console's screens, where each value comes from, and the one check your server must not skip.

```mermaid
sequenceDiagram
    participant B as Browser on www.example.ca
    participant G as Google
    participant S as Your server
    B->>G: "Sign in with Google" button (client ID)
    Note over G: Is www.example.ca an authorized<br/>JavaScript origin for this client?
    G->>B: account chooser, consent
    G->>S: POST /auth/google: credential=ID token, g_csrf_token
    Note over S: Verify signature, aud = client ID,<br/>iss, exp; compare CSRF token
    S->>B: session cookie
```

In the diagram, Google checks your settings before showing anything, and your server checks Google's token before trusting it. The ID token is a signed [JWT](../../09-back-end/02-auth/02-sessions-cookies-and-jwt.md); anyone can make one that looks right, so only the signature check makes it proof.

## Key terms

The **Google Auth Platform** is the section of the Google Cloud console (formerly "OAuth consent screen") where you configure sign-in for a project. Its pages are Branding, Audience, Clients and Data access.

**Branding** holds the app name, support email, logo and the home page, privacy policy and terms links. Its **authorized domains** list every domain your URLs use; the home page must be on a domain you have verified, which you can do in Google Search Console ([Branding](https://support.google.com/cloud/answer/15549049), as of 2026).

**Audience** sets who can sign in. **External** apps accept any Google account; **internal** ones only your organization's. An external app starts in **Testing** status, where only up to 100 listed **test users** can sign in, and moves to **In production** when you publish ([Audience](https://support.google.com/cloud/answer/15549945)).

An **OAuth client** (client ID) identifies your app when it asks Google for tokens. A web client lists **authorized JavaScript origins** (the sites allowed to show the button) and **authorized redirect URIs** (where Google may send results). A mismatch fails with `origin_mismatch` or `redirect_uri_mismatch` ([Clients](https://support.google.com/cloud/answer/15549257)). A **client secret** is shown in full only once, at creation.

**Data access** lists the **scopes** you request. Sign-in needs only `openid`, `email` and `profile`. Sensitive or restricted scopes, such as reading Gmail or Drive, require **app verification** by Google before the public can use them without a warning.

## How it works

1. In the lab project, open Google Auth Platform, Branding. Enter the app name and support email, the home page and privacy policy URLs on your domain, and add the domain under authorized domains.
2. Audience: choose External. Add yourself as a test user while in Testing.
3. Clients: create a Web application client. Add `https://www.example.ca` (and `http://localhost:3000` for development) as JavaScript origins, and your login endpoint as a redirect URI if you use the redirect flow.
4. Put the button on the page with Google Identity Services, using the client ID (it is public; there is no secret in the page) ([display the button](https://developers.google.com/identity/gsi/web/guides/display-button)):

    ```html
    <script src="https://accounts.google.com/gsi/client" async></script>
    <div id="g_id_onload"
         data-client_id="1234567890-abc.apps.googleusercontent.com"
         data-login_uri="https://www.example.ca/auth/google"
         data-auto_prompt="false"></div>
    <div class="g_id_signin" data-type="standard"></div>
    ```

5. On the server, at `/auth/google`, read the `credential` and `g_csrf_token` form fields. Reject the request unless `g_csrf_token` equals the `g_csrf_token` cookie ([HTML reference](https://developers.google.com/identity/gsi/web/reference/html-reference)). Then verify the token, look up or create the user by the token's `sub` claim (Google's permanent user id), and start your own session.
6. When it works for test users, publish the app (In production). With only the sign-in scopes, that is usually enough; requesting sensitive scopes starts verification.

Verifying the token means checking that it is signed by Google, that `aud` equals your client ID, that `iss` is `accounts.google.com` or `https://accounts.google.com`, and that `exp` hasn't passed ([verify the Google ID token](https://developers.google.com/identity/gsi/web/guides/verify-google-id-token)). Google's libraries do all four.

## Worked example

<div class="example" markdown>

### Example 1: a forged token is rejected

This uses `google-auth` (as in the previous lesson) plus PyJWT and `cryptography` to make a token that looks like Google's, then verifies it the way your server would. Install `google-auth requests pyjwt cryptography` in a virtual environment and save this as `verify_login.py`:

```python
import time, jwt
from cryptography.hazmat.primitives.asymmetric import rsa
from google.oauth2 import id_token
from google.auth.transport import requests

CLIENT_ID = "1234567890-abc.apps.googleusercontent.com"

def verify(token):
    try:
        info = id_token.verify_oauth2_token(token, requests.Request(), CLIENT_ID)
        print("signed in:", info["sub"], info.get("email"))
    except ValueError as err:
        print("rejected:", err)

# A token that looks right but is signed with our own key, not Google's.
key = rsa.generate_private_key(public_exponent=65537, key_size=2048)
now = int(time.time())
claims = {"iss": "https://accounts.google.com", "aud": CLIENT_ID, "sub": "1089",
          "email": "ana@example.org", "iat": now, "exp": now + 3600}
forged = jwt.encode(claims, key, algorithm="RS256", headers={"kid": "not-a-google-key"})
print(jwt.decode(forged, options={"verify_signature": False}))
verify(forged)
```

```text
{'iss': 'https://accounts.google.com', 'aud': '1234567890-abc.apps.googleusercontent.com', 'sub': '1089', 'email': 'ana@example.org', 'iat': 1794258663, 'exp': 1794262263}
rejected: Certificate for key id not-a-google-key not found.
```

1. The decoded claims are exactly what a real token contains for this client: right issuer, right audience, not expired. Code that only decodes the token (the first `print`) would have signed Ana in.
2. `verify_oauth2_token` downloads Google's current public keys, finds none with this token's key id, and rejects it. A token signed by Google for a different app would fail the `aud` check instead.
3. `sub` is the stable user id. Use it as the key for the user record; an email address can change or be reused.

Check: change `CLIENT_ID` in `verify` to another value and the forged token is still rejected, for the same reason. With a real token from your button, `verify` prints `signed in:` and your `sub`.

</div>

## Common mistakes

<div class="warning" markdown>

Watch out: decoding the ID token without verifying it, or checking the signature but not `aud`. A token from any other app using Google sign-in would then log in to yours. Use Google's library with your client ID.

Watch out: leaving the app in Testing and wondering why parents can't sign in. Only listed test users can. Publish it once Branding is complete.

Watch out: requesting Drive or Gmail scopes "in case". They need app verification and scare users with warnings. Ask only for `openid email profile` to sign in, and request more later, when a feature needs it.

</div>

## Working with AI

<div class="ai" markdown>

Words to use: Google Auth Platform, OAuth client ID, authorized JavaScript origin, redirect URI, test users, ID token, `aud` claim, `sub` claim.

Prompts to try:

- "Write a FastAPI endpoint for Google Identity Services' `data-login_uri` POST: check the `g_csrf_token` cookie against the form field, verify the `credential` with `google.oauth2.id_token.verify_oauth2_token` for my client ID, upsert the user by `sub`, and set a session cookie. Link the docs for each check."
- "I get `redirect_uri_mismatch` signing in with Google from `http://localhost:3000`. Here is my client's configuration (paste). What exactly must match?"

What to check:

- Token handling that uses `jwt.decode` without verification, or skips the `aud` check.
- Users keyed by email instead of `sub`.
- Instructions for the old "OAuth consent screen" pages. The console now groups them under Google Auth Platform; the fields are the same but the menus differ.

</div>

## Quiz

1\. Is the OAuth client ID a secret? Is the client secret?

<details class="solution" markdown>
<summary>Answer</summary>

The client ID isn't secret; it is in your page's HTML. The client secret is, and is used only by servers in flows that exchange a code for tokens. The button flow in this lesson needs no secret.

</details>

2\. Sign-in works on `https://www.example.ca` but fails on `https://example.ca` with `origin_mismatch`. Name two fixes.

<details class="solution" markdown>
<summary>Answer</summary>

Add `https://example.ca` as an authorized JavaScript origin, or (better) redirect the apex to the canonical `www` host so the button only ever loads there.

</details>

3\. Why does the server compare the `g_csrf_token` cookie with the form field?

<details class="solution" markdown>
<summary>Answer</summary>

To make sure the POST came from Google's sign-in flow on your page, not from another site submitting a stolen or forged form to your login endpoint. Only your page's flow sets the matching cookie.

</details>

4\. Your app is External and In production, and asks only for `openid email profile`. A new feature needs read access to the user's Google Drive files. What changes?

<details class="solution" markdown>
<summary>Answer</summary>

Drive scopes are sensitive or restricted, so the app needs Google's verification (with a verified domain, privacy policy and possibly a security review) before the public can grant them without warnings. Request the scope only when the user uses that feature.

</details>

## Lab

<div class="lab" markdown>

### Lab: a Google sign-in button on your site

Goal: you can sign in with your Google account on your own domain, and the server verifies the token. Time: about 20 minutes. Runs in: the Google Cloud console, Search Console, your editor and Vercel. Needs: the lab project, your verified domain and your Vercel site.

1. Run Example 1 locally.
2. Fill in Branding with your domain's home page and a short privacy page (add `privacy.html` to the site). Add your domain under authorized domains.
3. Set Audience to External and add yourself as a test user. Create a Web client with your canonical origin.
4. Add the button from step 4 of How it works to a `login.html` page, with `data-login_uri` pointing at a function `/api/auth-google`.
5. Write the function: it checks the CSRF token, verifies the credential against your client ID and returns the `sub` and email as JSON. Deploy and sign in.

Expected result: clicking the button shows Google's account chooser, and the function returns your `sub` and email. Signing in from an account that isn't a test user fails while the app is in Testing.

<details class="solution" markdown>
<summary>Solution</summary>

A Vercel Python function `api/auth-google.py` (form parsing kept short):

```python
from http.server import BaseHTTPRequestHandler
from http.cookies import SimpleCookie
from urllib.parse import parse_qs
import json, os
from google.oauth2 import id_token
from google.auth.transport import requests

class handler(BaseHTTPRequestHandler):
    def do_POST(self):
        body = self.rfile.read(int(self.headers["Content-Length"])).decode()
        form = {k: v[0] for k, v in parse_qs(body).items()}
        cookie = SimpleCookie(self.headers.get("Cookie", ""))
        if "g_csrf_token" not in cookie or cookie["g_csrf_token"].value != form.get("g_csrf_token"):
            self.send_response(400); self.end_headers(); return
        info = id_token.verify_oauth2_token(form["credential"], requests.Request(), os.environ["GOOGLE_CLIENT_ID"])
        self.send_response(200)
        self.send_header("Content-Type", "application/json")
        self.end_headers()
        self.wfile.write(json.dumps({"sub": info["sub"], "email": info.get("email")}).encode())
```

Add `google-auth` and `requests` to `requirements.txt`, and `GOOGLE_CLIENT_ID` as an environment variable. Not run against Google while writing this lesson, since it needs a client and a domain; the verification call is the one run in Example 1. If verification fails with a wrong-audience error, the variable holds a different client ID from the one in the page.

</details>

</div>

## Where this shows up

- Sessions after sign-in, and cookie settings, are in [sessions, cookies and JWT](../../09-back-end/02-auth/02-sessions-cookies-and-jwt.md).
- The same OAuth client setup is needed to call Google APIs (Calendar, Drive) on a user's behalf, which adds the authorization flow from [OAuth and SSO](../../09-back-end/02-auth/03-oauth-and-sso.md).
