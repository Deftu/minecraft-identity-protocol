# Security Policy

This document covers vulnerabilities in the **protocol design** itself — a flaw in MIP's
wire protocol, session model, or security requirements as written in
[`docs/spec/index.md`](docs/spec/index.md). It does not cover vulnerabilities in any specific
implementation of MIP; report those to that implementation's own repository instead.

## Reporting a design flaw

If you believe you've found a way for an RP correctly implementing every MUST in §8 (Security
Considerations) to still be vulnerable — a replay path, a relay/proxy attack not covered by
§5.4, a session-fixation gap, an enumeration-resistance bypass, or similar — please report it
privately rather than opening a public issue first:

- Use GitHub's [private vulnerability reporting](https://github.com/Deftu/minecraft-identity-protocol/security/advisories/new)
  for this repository, or
- Email the maintainer directly (see the GitHub profile at
  [@Deftu](https://github.com/Deftu) for current contact details).

Include: the affected section(s), the attack scenario, and — if applicable — why existing
§8 mitigations don't close it.

## What's explicitly out of scope

- Mojang's or Microsoft's own identity infrastructure — MIP wraps it, it doesn't secure it.
- §5.4's relay attack itself is already documented and tracked as a known, only-partially-
  mitigated SHOULD (§8.11) — no need to re-report it as new.
- Appendix C's development/offline profile being insecure *when deliberately enabled and
  misconfigured* (e.g. exposed without a dev key, §C.4) — that's the documented trade-off of
  turning it on, not a flaw in the profile's own design.

## Disclosure

Once a reported issue is confirmed, it will be fixed in the spec text (with a CHANGELOG entry
and, if it requires a MUST-level behavior change, a version bump per §12) and credited here
unless the reporter asks to remain anonymous.
