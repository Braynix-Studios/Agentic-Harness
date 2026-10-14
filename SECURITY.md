# Security Policy

P3 is an early-stage project. Do not use it with production credentials, sensitive personal information, or unrestricted tool permissions until the applicable security controls have been implemented and reviewed.

## Reporting a vulnerability

Please do not open a public issue containing exploit details, credentials, tokens, or sensitive evidence. Contact the repository maintainers privately through the GitHub organization/account's available private reporting channel. If no private reporting channel is configured, contact a repository administrator and request a private disclosure route.

## Security expectations

- Never commit secrets or real production data.
- Use least-privilege credentials and provider permissions.
- Validate and authorize tool calls at execution boundaries.
- Keep approval-required actions blocked until explicit approval is recorded.
- Treat retrieved documents and tool outputs as untrusted input.
- Redact secrets from logs, traces, error reports, and test fixtures.
- Document trust boundaries, threat assumptions, and security-relevant design changes.
