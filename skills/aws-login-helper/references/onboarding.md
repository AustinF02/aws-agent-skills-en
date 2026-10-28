# First-Time Setup and Troubleshooting

Read this for initial setup or a failed prerequisite. Do not run login merely because an AWS operation failed.

## Onboarding

1. Identify the OS, selected profile, Region, and existing authentication method. Run `aws --version` locally. The helper requires Python 3.11+, AWS CLI v2.32.0+ in the v2 series, and uvx for MCP startup. Use the [official CLI installation guide](https://docs.aws.amazon.com/cli/latest/userguide/getting-started-install.html) if needed; obtain authorization before installing or changing authentication.
2. Keep IAM Identity Center on `aws sso login`. Preserve static keys, credential_process, and assumed-role workflows. Do not register this helper for those profiles.
3. For a new console-login workflow, explain the browser/MFA step and obtain approval. Run `aws login --profile <PROFILE_NAME> --region <REGION>` in the user's local terminal, using their chosen non-secret values. Use a separate named profile when preserving an existing method. Never silently choose or overwrite the default profile.
4. The helper requires an existing nonempty `login_session`. It rejects other/mixed authentication options and any same-named profile section in the shared credentials file, even an empty section. Do not delete or rewrite existing settings to bypass this check; select a dedicated compatible profile.
5. Run the helper's `--check` with that profile. Obtain authorization for later automatic browser sign-in on expiration, then configure MCP. Do not report connection success until MCP tool discovery succeeds.

The script reads configuration files locally, including the shared credentials file, to check profile compatibility. It does not print their contents or read authentication caches. Custom `AWS_CONFIG_FILE` and `AWS_SHARED_CREDENTIALS_FILE` paths are honored by the prerequisite check; keep the launch environment consistent.

## Troubleshooting

| Symptom | Response |
| --- | --- |
| CLI missing, unsupported, or version unreadable | Install/update from the official guide; never infer that login is supported |
| Profile missing or no login_session | Complete the authorized first-time named-profile login outside the helper |
| SSO, another method, or mixed settings | Keep that workflow; do not migrate it automatically |
| Sign-in permission denied | Check permissions for AWS Sign-In; ask the administrator rather than attaching policies automatically |
| AWS service access denied after successful login | Investigate that service's IAM permissions; signing in again or granting sign-in permissions does not grant service access |
| Network failure or unclassified error | Diagnose the connection/error; do not treat it as session expiration |
| Browser unavailable | For a separately authorized manual flow, check `aws login --remote`; the helper does not automate headless/cross-device login |
| Canceled or timed-out sign-in | Complete authentication in a terminal, then reconnect MCP |

`SignInLocalDevelopmentAccess` covers sign-in token actions, not workload permissions. Verify the actual error and current policy documentation. Do not use interactive login for CI/CD; use the appropriate role/federation workflow. Check current partition/Region support before setup.

References: [CLI console login](https://docs.aws.amazon.com/cli/latest/userguide/cli-configure-sign-in.html), [Sign-in policy](https://docs.aws.amazon.com/aws-managed-policy/latest/reference/SignInLocalDevelopmentAccess.html), [Configuration files](https://docs.aws.amazon.com/cli/latest/userguide/cli-configure-files.html).
