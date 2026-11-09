# Receiving mail and email authentication

After this you can receive mail at your own domain, publish the SPF, DKIM and DMARC records that let receivers trust mail from it, and read a receiver's verdict on a message.

Before this: [Pointing a domain at a host](../05-domains-and-hosting/02-pointing-a-domain-at-a-host.md), [DNS and domains](../../07-networking/01-how-the-internet-works/05-dns-and-domains.md) and [public-key encryption and signatures](../../12-security/02-cryptography/03-public-key-encryption-and-signatures.md).

## The idea

You want `hello@yourdomain.ca` on your resume, and your app will send receipts from `orders@yourdomain.ca`. Two separate things have to work. Receiving means other servers can find where to deliver mail for your domain. Sending means receivers believe that mail claiming to be from your domain really is, because anyone can type any `From:` address into an email.

Email has no built-in sender check, so three DNS-published policies were added over the years. The receiving server runs all three on every message:

```mermaid
sequenceDiagram
    participant S as Sending server<br/>(203.0.113.5)
    participant R as Receiving server<br/>(gmail.com)
    participant D as DNS for yourdomain.ca
    S->>R: MAIL FROM bounce@yourdomain.ca, then the message<br/>(From: orders@yourdomain.ca, DKIM-Signature d=yourdomain.ca)
    R->>D: TXT yourdomain.ca (SPF)
    D-->>R: v=spf1 include:... -all
    Note over R: SPF: is 203.0.113.5 allowed to send for yourdomain.ca?
    R->>D: TXT selector._domainkey.yourdomain.ca (DKIM key)
    D-->>R: v=DKIM1; p=MIIB...
    Note over R: DKIM: does the signature verify with this public key?
    R->>D: TXT _dmarc.yourdomain.ca
    D-->>R: v=DMARC1; p=quarantine
    Note over R: DMARC: did SPF or DKIM pass for the From domain?<br/>If not, apply p=quarantine
```

In the diagram, each check is a DNS lookup on the sender's domain, which is why only the domain's owner can make mail pass.

## Key terms

An **MX record** names the server that accepts mail for a domain. A **mailbox provider** stores mail and gives you an inbox (Google Workspace, Microsoft 365, Zoho Mail, Fastmail, Proton). **Email forwarding** accepts mail for your domain and passes it on to an inbox you already have, such as a personal Gmail; many registrars and Cloudflare Email Routing do this ([Cloudflare Email Routing](https://developers.cloudflare.com/email-routing/), as of 2026).

Every message has two sender addresses. The **envelope sender** (`MAIL FROM`, shown afterwards as `Return-Path`) is where bounces go. The **header From** is what the reader sees. They often differ: a sending service uses its own bounce domain.

**SPF** (Sender Policy Framework) is a TXT record at the domain listing which servers may use it as the envelope sender ([RFC 7208](https://www.rfc-editor.org/rfc/rfc7208)). **DKIM** (DomainKeys Identified Mail) signs each message with a private key; the receiver fetches the public key from `selector._domainkey.domain` and checks the signature, which also proves the content wasn't changed ([RFC 6376](https://www.rfc-editor.org/rfc/rfc6376)). A **selector** is a name that lets one domain publish several keys, one per sending service.

**DMARC** is a TXT record at `_dmarc.domain` that ties the two to the visible address: a message passes DMARC if SPF or DKIM passes for a domain that matches the header From. That match is called **alignment**. The `p=` tag says what receivers should do with failures: `none` (just report), `quarantine` (spam folder) or `reject` ([RFC 7489](https://www.rfc-editor.org/rfc/rfc7489)). The `rua=` tag asks receivers to email you daily reports.

The receiver records its verdict in an **Authentication-Results** header at the top of the message.

## How it works

Set up a domain in this order:

1. Receiving. Pick a mailbox provider or a forwarding service and add exactly the MX records it shows.
2. SPF. Publish one TXT record at the apex that lists every service that sends as you, ending in `-all` (everything else fails) or `~all` (soft fail). A domain may have only one SPF record, and evaluating it may take at most 10 DNS lookups.
3. DKIM. Each sending service gives you a record (usually a CNAME or TXT under `_domainkey`). Add one per service.
4. DMARC. Start with `v=DMARC1; p=none; rua=mailto:you@yourdomain.ca`. Read the reports for a few weeks, then move to `p=quarantine` and later `p=reject`.
5. Test. Send yourself a message and read the verdict (Example 1).

Gmail requires SPF or DKIM from every sender, and SPF, DKIM, DMARC and alignment from anyone sending more than 5,000 messages a day to Gmail accounts ([Gmail sender guidelines](https://support.google.com/a/answer/81126), as of 2026). Setting all three up from the start costs a few records.

A domain that never sends mail, such as the second TLD that only redirects, should say so: `v=spf1 -all` at the apex and `v=DMARC1; p=reject` at `_dmarc`. Otherwise it is a free domain for someone else to forge.

## Worked example

<div class="example" markdown>

### Example 1: reading a real domain's mail records

Look up GitHub's records with a public resolver. In PowerShell:

```powershell
nslookup -type=MX github.com 1.1.1.1
nslookup -type=TXT _dmarc.github.com 1.1.1.1
nslookup -type=TXT google._domainkey.github.com 1.1.1.1
nslookup -type=TXT github.com 1.1.1.1
```

```text
github.com	MX preference = 0, mail exchanger = github-com.mail.protection.outlook.com
_dmarc.github.com	text = "v=DMARC1; p=quarantine; sp=reject; pct=100; rua=mailto:dmarc@github.com; ruf=mailto:dmarc@github.com; fo=1"
google._domainkey.github.com	text = "v=DKIM1; k=rsa; p=MIIBIjANBgkqhkiG9w0BAQEFAAOCAQ8AMIIBCgKCAQEAj6T5sl/RwdSqGoYWaWaF..."
"v=spf1 ip4:192.30.252.0/22 include:spf.protection.outlook.com include:_netblocks.google.com include:mail.zendesk.com include:_spf.salesforce.com include:servers.mcsv.net include:mktomail.com include:sendgrid.net ..."
```

(Output shortened: the DKIM key and the SPF list continue.)

1. MX: GitHub receives mail through Microsoft 365.
2. DMARC: failing mail from `github.com` goes to spam (`p=quarantine`), failing mail from any subdomain is rejected (`sp=reject`), and reports go to `dmarc@github.com`.
3. DKIM: the selector `google` holds an RSA public key, so some GitHub mail is signed by Google's servers.
4. SPF: one record lists GitHub's own address range plus each service that sends for it, including Microsoft, Google, Zendesk (support), Salesforce, Mailchimp (`mcsv.net`), Marketo and SendGrid. Each `include:` is a lookup counting toward the limit of 10.

To read a verdict on a message, open it in Gmail, choose the three-dot menu and then "Show original". The summary at the top lists SPF, DKIM and DMARC as PASS or FAIL, and the raw headers contain a line like this (shape from [RFC 8601](https://www.rfc-editor.org/rfc/rfc8601); values illustrative):

```text
Authentication-Results: mx.google.com;
       dkim=pass header.i=@yourdomain.ca header.s=resend;
       spf=pass smtp.mailfrom=send.yourdomain.ca;
       dmarc=pass (p=QUARANTINE) header.from=yourdomain.ca
```

Check: run the same lookups for `gmail.com` and compare. `_dmarc.gmail.com` has `p=none`, a reminder that the policy is the domain owner's choice.

</div>

## Common mistakes

<div class="warning" markdown>

Watch out: two SPF records, one added for each service. Receivers then treat SPF as an error. Merge them into one record with several `include:` terms.

Watch out: jumping to `p=reject` on day one. A service you forgot (the invoicing tool, the newsletter) starts bouncing. Start at `p=none`, read the reports, then tighten.

Watch out: expecting forwarding to make replies come "from" your domain. Forwarding only receives. To send as `hello@yourdomain.ca` from Gmail, you need an SMTP service that is in your SPF and signs with DKIM.

</div>

## Working with AI

<div class="ai" markdown>

Words to use: MX record, envelope sender, header From, SPF, DKIM selector, DMARC policy, alignment, Authentication-Results.

Prompts to try:

- "My domain `yourdomain.ca` receives mail through Zoho and sends app email through Resend and newsletters through Mailchimp. Write the single SPF record, list the DKIM records I need to get from each service, and give a DMARC record to start with. Explain each tag."
- "Here are the Authentication-Results and Return-Path headers from a message that went to spam (paste). Which check failed, and was it an alignment problem?"

What to check:

- More than one SPF record, or more than 10 lookups. Count the `include:` terms, including nested ones.
- DKIM values written by the model. Keys come from the sending service's dashboard; a made-up key never verifies.
- `p=reject` suggested before you have read any DMARC reports.

</div>

## Quiz

1\. A message's `Return-Path` is `bounce@send.shopmail.com` and its `From:` is `orders@yourdomain.ca`. SPF passes for `send.shopmail.com`. Does that make DMARC pass?

<details class="solution" markdown>
<summary>Answer</summary>

Not through SPF, because `send.shopmail.com` doesn't align with `yourdomain.ca`. DMARC passes only if DKIM passes with `d=yourdomain.ca` (or SPF passes for an envelope domain under `yourdomain.ca`).

</details>

2\. Why does DKIM survive forwarding when SPF usually doesn't?

<details class="solution" markdown>
<summary>Answer</summary>

SPF checks the IP address of the server that delivered the message, which after forwarding is the forwarder's. DKIM checks a signature on the message itself, which stays valid as long as the signed headers and body aren't changed.

</details>

3\. You add `include:_spf.mailprovider.com` as a second TXT record starting with `v=spf1`. What happens?

<details class="solution" markdown>
<summary>Answer</summary>

The domain now has two SPF records, which is a permanent error for SPF checks, so SPF fails for every sender. Merge them into one record.

</details>

4\. Your `.com` only redirects to your `.ca` and never sends mail. Which two records should it have, and why?

<details class="solution" markdown>
<summary>Answer</summary>

`v=spf1 -all` (no server may send for it) and `_dmarc` with `v=DMARC1; p=reject` (reject anything claiming to be from it), so nobody can send convincing phishing from it.

</details>

## Lab

<div class="lab" markdown>

### Lab: receive mail and publish the policies

Goal: `hello@yourdomain` reaches your personal inbox, and the domain publishes SPF and DMARC. Time: about 20 minutes. Runs in: your DNS host's dashboard, PowerShell and Gmail. Needs: your domain.

1. Run Example 1's lookups on your school's domain and your bank's domain. Note who receives their mail and each DMARC policy.
2. Turn on email forwarding at your registrar (or Cloudflare Email Routing if Cloudflare hosts your DNS) from `hello@` to your personal inbox. Add the MX (and any TXT) records it shows.
3. Add an SPF record. Until the next lesson adds a sending service, use the one your forwarding service documents, or `v=spf1 -all` if it documents none.
4. Add `_dmarc` with `v=DMARC1; p=none; rua=mailto:hello@yourdomain`.
5. Check with `nslookup -type=MX`, `-type=TXT` on the apex and on `_dmarc`, against `1.1.1.1`.
6. From another account, send a message to `hello@yourdomain`. Open it, use "Show original", and read the headers.

Expected result: the message arrives in your personal inbox; the lookups show one MX set, one SPF record and one DMARC record.

<details class="solution" markdown>
<summary>Solution</summary>

A zone with forwarding at a registrar and no sending service yet might hold:

```text
Type  Host     Value
MX    @        <forwarder's mail servers, with priorities>
TXT   @        v=spf1 include:<forwarder's SPF domain> -all
TXT   _dmarc   v=DMARC1; p=none; rua=mailto:hello@yourdomain.ca
```

Not run while writing this lesson, since it needs a purchased domain. In step 6 the Authentication-Results show the sender's domain (for example `gmail.com`), not yours, because you received the message; your own records are tested in the next lesson, when you send. If nothing arrives, check for leftover MX records from the registrar's defaults, and that forwarding is switched on for the address.

</details>

</div>

## Where this shows up

- Sending from an app, with a sending subdomain and its DKIM records, is [sending email from code](02-sending-email-from-code.md).
- Gmail's and Yahoo's bulk-sender rules and Canada's anti-spam law are in [email law and deliverability](03-email-law-and-deliverability.md).
