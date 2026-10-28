---
name: aws-agent-toolkit-setup
description: Follow AWS's official setup.md to install Agent Toolkit while preserving existing configuration, then check authentication, skills, and MCP for Codex, Kiro, or Claude Code. Explain the workflow in American English.
---

# Set Up Agent Toolkit for AWS

At the start, fetch and read the full [official AWS setup.md](https://raw.githubusercontent.com/aws/agent-toolkit-for-aws/refs/heads/main/setup-instructions/setup.md). Do not execute remembered commands without checking the current instructions. This skill adds English guidance and safeguards for existing environments; it does not copy the official runbook.

## Inputs and boundaries

Detect the operating system. Confirm the agent, AWS profile name, workload Region, and whether the user has the new or advanced AWS experience. Do not ask again for information already supplied.

Do not receive credentials. Authentication stays in the user's browser. Never silently change an existing SSO or static-key profile to another authentication method.

Inspect the existing CLI, uv, MCP entries, rules files, and same-named skills. Creating resources, deploying applications, and changing IAM are out of scope. Make authorization for installation and sign-in clear.

## Apply the official instructions

- Even when AWS CLI exists, check `aws configure agent-toolkit help`. If unsupported, follow the official update instructions without removing an existing installation.
- Do not rewrite a Region that already matches the user's choice. If STS confirms valid authentication, skip another login and explain this departure from the runbook.
- Do not use `--yes` to configure every detected agent in a multi-agent environment. Use the interactive wizard to select only the agents the user requested.
- Use the Toolkit service Region required by the current official instructions. Do not change the workload's default Region just to reach that service.
- Preserve the generated MCP command and arguments. Add the named-profile environment setting using the client's actual configuration format.
- Do not overwrite same-named MCP entries or skills. Present the difference and confirm how to reconcile it.
- Fetch the official rules for the selected AWS experience. Preserve existing AGENTS.md, CLAUDE.md, and Kiro steering content. Add one clearly marked block and keep project-specific rules authoritative.
- If the runbook and current authentication documentation disagree about session duration, explain the discrepancy and verified limits. Do not guarantee a fixed 90-day renewal period.

## Completion criteria

Fetch the skill catalog with the chosen profile. Verify the installation paths and skill files. Verify MCP through tools/list. If behavior in a fresh session has not been tested, say so. Separate completed checks from pending user actions and unverified behavior.

On failure, read the matching section in the [official troubleshooting guide](https://raw.githubusercontent.com/aws/agent-toolkit-for-aws/refs/heads/main/setup-instructions/setup-troubleshooting.md). Do not retry indefinitely.

The runbook's final example about creating and deploying a game is a separate task, not part of setup.
