# Minecraft Identity Protocol (MIP)

[![CI](https://github.com/Deftu/minecraft-identity-protocol/actions/workflows/ci.yml/badge.svg)](https://github.com/Deftu/minecraft-identity-protocol/actions/workflows/ci.yml)
[![License: Apache-2.0](https://img.shields.io/badge/license-Apache--2.0-blue.svg)](LICENSE)
[![Spec version](https://img.shields.io/badge/spec-1.0-blue.svg)](docs/spec/index.md)

A backend-agnostic protocol for authenticating a Minecraft account over HTTP, either from
inside a game client/mod or from a plain browser, converging on one identity representation
and one session-issuance step.

- **Spec**: [`docs/spec/index.md`](docs/spec/index.md) — the sole normative source. Also
  published as a browsable site (see below).
- **Overview**: [`docs/index.md`](docs/index.md) — a plain-language walkthrough for anyone
  who doesn't want to start with RFC-2119 prose.
- **Schemas**: [`schemas/`](schemas/) — JSON Schema for every wire shape the spec defines.
- **Examples**: [`examples/`](examples/) — worked, schema-validated request/response payloads.
- **Changelog**: [`CHANGELOG.md`](CHANGELOG.md)

**Status:** `1.0`. Not yet implemented anywhere.

## Contributing

See [`CONTRIBUTING.md`](CONTRIBUTING.md) for how to propose a spec change, and
[`SECURITY.md`](SECURITY.md) to report a vulnerability in the protocol design itself.

## License

Apache License 2.0 — see [`LICENSE`](LICENSE). Applies to the spec text, schemas, and
examples alike.
