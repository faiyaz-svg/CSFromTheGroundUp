# Cryptography

A compact reference for the chapter. For explanations, follow the lesson links.

## Lessons

1. [Hashing and salts](01-hashing-and-salts.md)
2. [Symmetric encryption](02-symmetric-encryption.md)
3. [Public-key encryption and signatures](03-public-key-encryption-and-signatures.md)
4. [RSA step by step](04-rsa-step-by-step.md)
5. [The TLS handshake](05-the-tls-handshake.md)
6. [Privacy and PIPEDA](06-privacy-and-pipeda.md)

## Which primitive for which job

| Job | Use | Not this |
|---|---|---|
| Store a password | Argon2id (or scrypt, bcrypt, PBKDF2) with a random salt | SHA-256, MD5, any fast hash |
| Check a file was not corrupted | SHA-256 (or a CRC for accidents only) | Nothing secret needed |
| Check a message is genuine and unchanged, shared secret | HMAC-SHA256, compared with `hmac.compare_digest` | A plain hash |
| Encrypt data with one shared key | AES-256-GCM or ChaCha20-Poly1305 | ECB, unauthenticated CBC |
| Agree on a key with a stranger | X25519 (Diffie-Hellman), authenticated by a signature | Sending the key in the clear |
| Prove who wrote something | Ed25519 or RSA-PSS signature | "Encrypting with the private key" |
| Encrypt to someone's public key | Hybrid: X25519 or RSA-OAEP for a key, AES-GCM for the data | RSA on the whole message, textbook RSA |
| Secure a connection | TLS 1.3 | Disabling verification |

## Hash properties

| Property | Meaning |
|---|---|
| Deterministic | Same input, same digest |
| Fixed size | SHA-256 always gives 32 bytes |
| Preimage resistance | Cannot find an input for a digest |
| Collision resistance | Cannot find two inputs with the same digest |
| Avalanche | One input bit flips about half the output bits |

MD5 and SHA-1 are broken for security use. Password-hashing minimums from [OWASP](https://cheatsheetseries.owasp.org/cheatsheets/Password_Storage_Cheat_Sheet.html) (as of 2026): Argon2id 19 MiB, 2 iterations, 1 lane; bcrypt work factor 10 or more; PBKDF2-HMAC-SHA256 600,000 iterations.

## Rules

- Never reuse a nonce with the same key.
- A key stored beside the data it protects protects nothing.
- Public keys must be authenticated (certificates, fingerprints).
- RSA: 2048 bits at least, with OAEP for encryption and PSS for signatures, and encrypt only a symmetric key.
- Never write your own primitives. Use a maintained library.

## RSA in five lines

$$n = pq \qquad \varphi = (p-1)(q-1) \qquad ed \equiv 1 \pmod{\varphi}$$

$$c = m^e \bmod n \qquad m = c^d \bmod n$$

```python
d = pow(e, -1, phi)
c = pow(m, e, n)
m == pow(c, d, n)
```

## TLS 1.3 in four steps

1. ClientHello: ciphers and key share.
2. ServerHello: chosen cipher and key share. Keys derived, the rest is encrypted.
3. Certificate, CertificateVerify and Finished from the server.
4. Finished from the client, then application data after 1 round trip.

```bash
echo | openssl s_client -connect example.com:443 -servername example.com -tls1_3
```

## PIPEDA

The 10 fair information principles, in order:

1. Accountability
2. Identifying purposes
3. Consent
4. Limiting collection
5. Limiting use, disclosure and retention
6. Accuracy
7. Safeguards
8. Openness
9. Individual access
10. Challenging compliance

A breach with a real risk of significant harm is reported to the Office of the Privacy Commissioner of Canada and to the affected individuals as soon as feasible. Keep breach records for 24 months. See [priv.gc.ca](https://www.priv.gc.ca/).
