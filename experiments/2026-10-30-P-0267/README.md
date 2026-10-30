# P-0267: public signals on a closure-sale dropship shop

From H-0465 (a vault thread: a shop offering free jewellery "after 46 years of trading", pay shipping
only). Detection side only. `signals.py` pulls RDAP through rdap.org, certificate-transparency names
from crt.sh and the shop's response headers, keyless, one HEAD request to the shop. Raw output in
`signals.json`.

## What the public record says (30 Oct 2026, 23:39 UTC)

| signal | value | reading |
|---|---|---|
| Domain registered | 12 Jan 2026, 290 days ago; expires 12 Jan 2027 | a one-year registration against a 46-year trading claim |
| Registrar | Tucows Domains Inc. | the registrar Shopify's own domain product uses, so the domain was most likely bought inside the shop builder |
| Nameservers | ns-cloud-c1 to c4.googledomains.com | Google Cloud DNS, the pool Shopify-bought domains land on; shared by a very large number of unrelated sites |
| Platform | `powered-by: Shopify`, served from gcp-europe-west1 behind Cloudflare | a stock Shopify store |
| Certificates | 49 issued, first at 23:02 UTC on 12 Jan 2026, 54 minutes before the RDAP registration timestamp; only `www`, `checkout` and the apex ever certified | the certificate and the domain were created in the same sitting; no other hostnames, no earlier life |
| Registrant | not shown (redacted) | the usual post-2018 state, not a signal on its own |

## The two questions

1. **Does RDAP show a 2026 registration?** Yes: 12 Jan 2026. The claim of 46 years of trading
   cannot be true of this domain, and the certificate log shows it had no life before that day.
2. **How many sibling domains share its nameservers or registrant?** Not answerable keyless, and not
   a signal here: the nameservers are Google Cloud DNS's shared pool and the registrant is redacted.
   A reverse-nameserver or reverse-registrant search needs a paid passive-DNS or WHOIS-history
   service. Sibling hunting by shared infrastructure only works when the operator self-hosts.

## What a cheap checker can rely on

Domain age against the trading claim (RDAP, free, hard to fake: a 1980s business with a 2026 domain
has to explain itself), registrar equals platform (bought in the builder, not by a company's IT),
and a certificate footprint of exactly the platform's three hostnames with no history. Shared
nameservers and redacted registrants are noise on any Shopify shop and should not count.

## Verdict

Works: the registration-age signal is public, free and decisive against the shop's own claim; the
sibling-count half of the question is blocked keyless and would be noise on this platform anyway.
