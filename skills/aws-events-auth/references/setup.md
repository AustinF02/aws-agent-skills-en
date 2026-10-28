# Setup and Verification

## Choose the authentication path

AWS Events uses AWS Builder ID, not your AWS account profile. No AWS CLI installation or IAM permission change is needed for this flow. Confirm event registration separately.

Prefer a working native MCP connection. Read the current [AWS MCP setup](https://docs.aws.amazon.com/events/latest/devguide/mcp-server.html) before editing settings.

- **Kiro:** use the documented awsevents HTTP connection, public client ID, scopes, and redirectUri ending at port 8976. Kiro appends its callback path; do not append a second path.
- **Claude Code:** the official command uses callback port 8484 and the shared public client ID. Merge into existing configuration only within authorization.
- **Codex:** check current OAuth/header-helper support and the exact callback it generates. AWS matches host, port, and path exactly. Do not repeatedly retry a redirect mismatch or silently replace a working connection.

All clients connect to https://api.awsevents.com/mcp. The public client ID is 7vmom55m1qstvq8i71ph127bfq; scopes are openid, email, events/access. These are public protocol settings, not credentials. Do not substitute IAM keys or an ID token for the access token.

## Bundled macOS fallback

The helper requires macOS, Python 3.11+, and the pinned [requirements-macos.txt](../requirements-macos.txt). Windows/Linux users should use their supported client's OAuth flow; the script stops before accessing Keychain or opening login there.

From the installed skill directory:

```sh
python3 -m venv .venv
.venv/bin/python -m pip install -r requirements-macos.txt
.venv/bin/python scripts/events_auth.py login
```

Run login only after authorization. Complete Builder ID/MFA in the browser; never copy its URL, code, or tokens into chat. The script binds loopback only, uses fresh PKCE/state, and tries the documented callback ports 8484–8489.

Tokens remain in the user's macOS Keychain under the generic service aws-agent-skills.aws-events-auth. No author's tokens, Keychain export, caches, profile, or account identifiers are bundled. The helper updates an existing Keychain item in place; storage failure stops the operation without deleting that item. The native storage adapter uses the pinned keyring version; review compatibility before upgrading it. A local refresh.lock coordinates this helper's refreshes.

```sh
.venv/bin/python scripts/events_auth.py status
.venv/bin/python scripts/events_auth.py get "/v1/events/example-event/schedule"
```

Replace example-event with the user's selected event ID. status displays metadata only; get returns the requested JSON, which may contain personal schedule data. Keep that output out of public logs. get attaches the bearer header without token arguments or environment-variable copying. refresh renews an existing session without opening a browser. Native clients and this fallback have separate token stores.

### Codex header integration

If supported by the installed Codex version, resolve the venv Python and script to actual absolute paths, quote paths correctly, and merge only the awsevents entry:

```toml
[mcp_servers.awsevents]
url = "https://api.awsevents.com/mcp"
http_headers_helper = "<ABSOLUTE_PYTHON_PATH> <ABSOLUTE_SCRIPT_PATH> headers"
```

Do not execute placeholder paths or print headers manually. The REST wrapper's retry handling applies to get calls; native MCP retries and header precedence are controlled by the client. Do not claim the REST wrapper intercepts arbitrary curl or MCP calls. Preserve existing native OAuth unless a replacement is explicitly authorized.

## Recovery and verification

- 401: refresh once and retry once. A second 401 or rejected refresh requires a new authorized interactive sign-in.
- 403: check event registration/authorization; another sign-in does not grant registration.
- Network failures: stop and diagnose rather than opening login.
- Keychain failures: check OS access permissions; do not export tokens, delete the record, or fall back to plaintext.
- Successful config save or token refresh is not proof of working MCP tools. Verify tool discovery and a requested read. Public catalog success alone does not prove personal schedule access.
- Only an absent nextToken ends session pagination. Keep read-only requests bounded.
- The packaged helper is tested with mocked OAuth/Keychain calls. Its underlying local flow has been exercised on macOS; this repository does not claim end-to-end verification across all agent versions.

References: [Getting started](https://docs.aws.amazon.com/events/latest/devguide/getting-started.html), [PKCE login](https://docs.aws.amazon.com/events/latest/devguide/auth-signing-in.html), [Refresh](https://docs.aws.amazon.com/events/latest/devguide/auth-refreshing.html), [Public endpoints and client ID](https://docs.aws.amazon.com/events/latest/devguide/auth-endpoints.html), [Codex MCP](https://learn.chatgpt.com/docs/extend/mcp).
