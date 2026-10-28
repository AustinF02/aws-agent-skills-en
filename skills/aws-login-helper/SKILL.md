---
name: aws-login-helper
description: Check an existing AWS CLI profile, authenticate again only when its session has expired, and start AWS MCP. Explain the workflow in English. Do not migrate SSO or change authentication methods.
---

# AWS Login Helper

Explain the purpose and scope in English. Ask only for the profile name, workload Region, operating system, and agent. Never ask for credentials or access to someone else's AWS account.

## Preserve the existing setup

- Check the AWS CLI version and whether the selected profile exists. Do not print entire configuration files or authentication caches.
- For IAM Identity Center profiles, keep the existing `aws sso login` workflow. Do not apply this helper.
- Do not switch static keys, credential_process, role assumption, or another authentication method to `aws login` without authorization.
- Obtain approval for initial sign-in and for opening a browser automatically when the session expires. Do not repeatedly ask for approval within an already authorized scope.
- This helper does not change IAM permissions, billing, or MFA requirements.

## Bundled helper

[aws_mcp_login.py](scripts/aws_mcp_login.py) requires Python 3.11+, AWS CLI v2.32+, and uvx when starting MCP. Read the script before running it. If a dependency is missing, follow its official installation instructions without removing an existing installation.

Use the non-secret values selected by the user. In these examples, `example-dev` is an example profile name; do not create it automatically.

```sh
python3 scripts/aws_mcp_login.py --profile example-dev --region ap-northeast-1 --check
python3 scripts/aws_mcp_login.py --profile example-dev --region ap-northeast-1 --login-only
```

Resolve the script's actual path inside this skill. On Windows, use the installed Python executable.

- `--check`: Check authentication only. Do not print credentials, account IDs, or ARNs.
- `--login-only`: Run browser sign-in from a terminal. Do not copy sensitive information into the conversation.
- Neither flag: Start MCP immediately when authentication is valid; authenticate again when it has expired.
- Stop without opening sign-in for network failures or errors that cannot be classified as expired authentication.
- GUI launches on macOS open Terminal. GUI launches on Windows/Linux instruct the user to authenticate in a terminal. Headless authentication is out of scope.
- A lock coordinates simultaneous starts for the same profile. The wait is normally limited to 3 minutes. If authentication takes longer, finish it and reconnect the MCP server.
- The helper creates only a local lock file. AWS CLI manages its own authentication cache.

## Connect it to MCP

In the agent's MCP configuration, set the existing `aws-mcp` command to the detected Python executable's absolute path. Pass the helper's absolute path, `--profile`, the chosen profile, `--region`, and the chosen Region as separate arguments.

Preserve unrelated settings. If the existing server has custom proxy arguments or multiple profiles, ask before replacing it with this single-profile helper.

For startup, allow `startup_timeout_sec = 240` in Codex. For Kiro, confirm the current schema before setting `timeout = 240000`. For Claude Code, check its current `MCP_TIMEOUT` documentation and set the launch environment accordingly. A longer timeout does not bypass authentication.

Report a verified connection only after tools/list succeeds. Distinguish configuration saved, authentication passed, MCP initialized, and use inside the actual app.

References: [AWS login](https://docs.aws.amazon.com/cli/latest/reference/login/), [AWS MCP Proxy](https://github.com/aws/mcp-proxy-for-aws).
