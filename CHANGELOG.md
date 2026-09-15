# Changelog

All notable changes to the Minecraft Identity Protocol are documented here. Format follows
[Keep a Changelog](https://keepachangelog.com/en/1.1.0/). Versioning follows §12 of the spec:
`MAJOR.MINOR`, with a `-draft` suffix while a version has not yet been finalized.

## [1.0] - 2026-09-15

### Added

- Initial release of the protocol: Flow A (MIP-Session, in-client), Flow B (MIP-OAuth,
  browser), Identity Session issuance (§7), refresh tokens (§9, optional), account linking
  (§10, optional), discovery document (Appendix A), and a non-production development/offline
  testing profile (Appendix C).
- Conformance levels: MIP-Core, MIP-Full (§11).
- JSON Schemas and worked examples for every wire shape the spec defines.
