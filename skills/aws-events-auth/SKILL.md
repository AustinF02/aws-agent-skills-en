---
name: aws-events-auth
description: Set up AWS Events API and MCP authentication with AWS Builder ID, diagnose expired tokens, and read event schedules. Separate this OAuth flow from AWS CLI profiles and EventBridge.
---

# AWS Events Authentication

Use AWS Builder ID OAuth for AWS Events, not aws login, IAM keys, or EventBridge.
Public event listings may need no authentication; registered-event catalogs and personal schedules do.

## Inspect and preserve

Check OS, agent/version, existing awsevents configuration, and the requested event.
Keep working authentication and unrelated settings. Do not copy another person's credentials.
Prefer the client's supported OAuth setup. Read [setup.md](references/setup.md) for native client setup or the macOS fallback.

## Authenticate and read

- Obtain authorization before first-time browser sign-in or changing the connection.
- Within an authorized workflow, refresh an existing session silently when needed; do not request confirmation for every read. Refresh failure requiring a new interactive sign-in is a separate step.
- The bundled [events_auth.py](scripts/events_auth.py) is a macOS-only fallback. It stores tokens in Keychain and adds the bearer header internally for its read-only get command.
- Use the helper instead of extracting a token for curl. On 401, it refreshes once and retries once. On 403, investigate registration/authorization; do not loop through login.
- Keep rotated refresh tokens and use the returned expires_in. A valid refresh cannot extend the Builder ID session indefinitely.
- Do not reserve, cancel, favorite, or modify personal time unless separately requested. The bundled REST helper exposes GET only.
- Resolve script/reference paths from this skill's directory. Read only references needed for the current setup.

## Secret boundaries and verification

Never print passwords, tokens, authorization headers, callback URLs/codes, or Keychain contents.
Run headers only as the MCP client's private header command, never as displayed shell output.
The published OAuth client ID is a shared public identifier, not a secret.
Do not upload personal schedules or local configuration in issues, tests, or logs.

Verify authentication and a requested read separately from saved configuration.
Claim MCP connection success only after tool discovery succeeds.
Report OS/backend limitations, exact checks, and unverified app behavior.
This skill guides behavior; it does not enforce permissions or guarantee safety.
