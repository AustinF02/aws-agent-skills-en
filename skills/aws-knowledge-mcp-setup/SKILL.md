---
name: aws-knowledge-mcp-setup
description: Connect AWS Knowledge MCP to Codex, Kiro, or Claude Code and verify official documentation search. Explain the setup in English. Do not sign in to AWS or operate account resources.
---

# Connect AWS Knowledge MCP

The official endpoint is `https://knowledge-mcp.global.api.aws`. It requires no AWS authentication and is rate-limited. It is separate from AWS MCP, which can operate AWS resources.

1. Confirm the app and configuration scope. Read existing settings without printing unrelated tokens or headers.
2. If the server name already exists, test it first. Leave a working configuration alone. For a conflicting configuration, explain the difference and reason before merging.
3. Add only the relevant entry. Do not replace a complete configuration file with these snippets.

Codex TOML:
```toml
[mcp_servers.aws-knowledge-mcp-server]
url = "https://knowledge-mcp.global.api.aws"
```

Kiro JSON:
```json
{
  "mcpServers": {
    "aws-knowledge-mcp-server": {
      "url": "https://knowledge-mcp.global.api.aws",
      "disabled": false,
      "autoApprove": []
    }
  }
}
```

For Claude Code, check the current CLI help and run this only if the server is not registered:
```sh
claude mcp add --transport http --scope user aws-knowledge-mcp-server https://knowledge-mcp.global.api.aws
```

4. Reconnect and run tools/list. Use the tool names actually returned. Verify one documentation search, such as finding an official reference for Lambda runtimes.
5. Do not expand automatic approvals by default. If requested, approve only the read-only tools the user selected.
6. Report configuration saved separately from search verified. If prompted for credentials, do not enter AWS keys; check the endpoint and client requirements instead.

References: [AWS Knowledge MCP](https://awslabs.github.io/mcp/servers/aws-knowledge-mcp-server), [Codex MCP](https://developers.openai.com/codex/mcp), [Kiro MCP](https://kiro.dev/docs/mcp/configuration/), [Claude Code MCP](https://code.claude.com/docs/en/mcp).
