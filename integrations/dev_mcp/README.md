# dev-mcp Integration

This directory is the intended integration boundary for the existing `dev-mcp` subsystem. The goal is to wrap it as the first MCP provider for P3, not to fork or rebuild its internal capabilities.

Before implementation, document its transport/authentication model, capability discovery, invocation payloads, error mapping, timeouts, and permission boundary. Add adapter contract tests using a fake provider and integration tests against an authorized dev-mcp environment.
