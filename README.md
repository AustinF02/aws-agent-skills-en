# AWS Agent Skills — English

**Set up AWS authentication, MCP connections, and Agent Toolkit, and develop AWS backends with behavior-first tests in Codex, Kiro, or Claude Code.**

This skillset helps when you are unsure which configuration to edit, AWS MCP will not connect, or an expired login interrupts your work. It checks your existing setup before making changes and uses your own AWS account. It does not include the author's credentials or machine configuration.

[Japanese edition](https://github.com/AustinF02/aws-agent-skills-ja) · [Validation workflow](https://github.com/AustinF02/aws-agent-skills-en/actions/workflows/validate.yml)

> This repository distributes Agent Skills. It is not a one-click marketplace plugin. “Claude” means **Claude Code** here; Claude Desktop and ordinary browser chats are not covered.

## What's included

| Skill | Purpose | AWS sign-in |
| --- | --- | --- |
| [aws-knowledge-mcp-setup](skills/aws-knowledge-mcp-setup/SKILL.md) | Connect Knowledge MCP for official documentation search | Not required |
| [aws-login-helper](skills/aws-login-helper/SKILL.md) | Check session expiration, authenticate only when needed, and start AWS MCP | Required |
| [aws-mcp-setup](skills/aws-mcp-setup/SKILL.md) | Connect and troubleshoot the official AWS MCP server | Required |
| [aws-agent-toolkit-setup](skills/aws-agent-toolkit-setup/SKILL.md) | Follow AWS's official Toolkit setup and verify skills and MCP | Required |
| [aws-backend-tdd](skills/aws-backend-tdd/SKILL.md) | Test AWS infrastructure and backend behavior using separate test tiers | Only for real-AWS verification |

Start with Knowledge MCP if you only need documentation. You do not need an AWS account or AWS CLI for that connection. Add authenticated AWS MCP when you need to work with account resources.

## Get started

Ask your agent:

```text
Read the README and relevant skill in:
https://github.com/AustinF02/aws-agent-skills-en

Install aws-knowledge-mcp-setup for my agent and verify the connection.
Preserve my existing configuration. Explain the scope and proposed changes first.
```

For authenticated AWS setup:

```text
Use aws-agent-toolkit-setup and follow the official AWS setup.md.
Ask me for my AWS profile name and workload Region.
Preserve my existing authentication method, MCP settings, skills, and project rules.
Explain any required authentication steps before proceeding.
```

To add sign-in automation:

```text
Use aws-login-helper to check authentication when AWS MCP starts.
Start immediately if the session is valid. Authenticate again only if it has expired.
First check my OS and profile, then explain what can be automated in my environment.
```

If the agent cannot read GitHub, download the relevant skill folder and install it manually. Providing a URL does not, by itself, mean a skill has been installed.

## Install the skills

Copy each `skills/<skill-name>/` directory, including its supporting files, to your agent's skill directory. Compare existing same-named folders instead of overwriting them.

| Agent | Personal skill directory |
| --- | --- |
| Codex | `~/.agents/skills/<skill-name>/` |
| Kiro | `~/.kiro/skills/<skill-name>/` |
| Claude Code | `~/.claude/skills/<skill-name>/` |

**Choose one language edition per agent.** The English and Japanese editions use the same skill names. Installing both in the same scope can create duplicate or conflicting entries.

If Codex's built-in skill-installer is available, ask it to install the desired paths from this repository. Confirm the installation location supported by your version.

In Kiro, open **Agent Steering & Skills**, select **Import a skill**, and provide a skill-folder URL, such as:

https://github.com/AustinF02/aws-agent-skills-en/tree/main/skills/aws-knowledge-mcp-setup

Use the skill-folder URL, not the repository root.

In Claude Code, install the folder and start a new session, then use `/aws-knowledge-mcp-setup`. In Codex, use `$aws-knowledge-mcp-setup`. In Kiro, select the skill or describe the task in ordinary language.

Installing a skill and configuring its MCP connection are separate steps. The skill checks your environment and guides the connection setup.

## AWS backend TDD: a small example

After installing the complete `aws-backend-tdd` folder, ask your agent:

```text
Use aws-backend-tdd. The item-ID validator currently accepts an empty string.
Change it to raise ValueError. Keep this change at the unit tier; do not call AWS.
```

**Before:** an empty ID passes validation. **After:** it raises `ValueError`.

1. Read the core skill, identify the validation boundary, and choose the unit tier.
2. Open only [testing.md](skills/aws-backend-tdd/references/testing.md) for this change.
3. RED: run a test expecting `ValueError`; confirm it fails because the exception was not raised.
4. GREEN: add the smallest validation, rerun, then check affected tests. Refactor only if needed.

No IAM/IaC or real-AWS reference is needed for this example. The skill loads details on demand; relative reference paths resolve from the installed skill directory. Agents need file-reading access to those supporting files. A pasted SKILL.md alone is incomplete.

**This skill provides guidance, not an enforced safety control. You are responsible for operations run against your AWS account.** It does not grant permissions, sandbox commands, or guarantee safety. Check service behavior, limits, IAM actions, and regional availability against current official AWS documentation.

## How the login helper works

The bundled script uses only the Python standard library. Authentication uses AWS CLI; starting MCP uses uvx and the official AWS proxy. It requires AWS CLI v2.32+ and Python 3.11+.

1. Check STS access with the selected profile without printing account IDs or ARNs.
2. If authentication is valid, start the AWS MCP proxy without opening sign-in.
3. If the error indicates expired authentication, start browser sign-in.
4. For network errors or unclassified failures, stop instead of opening sign-in.
5. Coordinate simultaneous starts for the same profile with a lock.

| Launch environment | Authentication behavior |
| --- | --- |
| macOS terminal | Run `aws login` in the terminal |
| macOS GUI app | Open Terminal and wait for browser authentication |
| Windows/Linux terminal | Run `aws login` in the terminal |
| Windows/Linux GUI app | Ask the user to authenticate in a terminal; do not open one automatically |
| SSH/headless | Outside the automation scope; use the applicable official authentication workflow |

**This does not bypass browser interaction or MFA.** macOS may ask for permission to control Terminal. The wait is normally limited to 3 minutes. If sign-in takes longer, or a user cancels it, finish authentication and reconnect the MCP server.

The app's initialization timeout can end the connection before authentication finishes. The helper runs **when MCP starts**, rather than as an independent trigger every time an app window opens.

The helper does not automatically migrate IAM Identity Center SSO, static access keys, credential_process, or other authentication methods. To keep the selected profile separate from ambient authentication, the child process does not inherit key-based AWS credential environment variables. Do not apply it to a setup that requires those environment variables.

### Manual checks

Run these from the installed `aws-login-helper` directory. `example-dev` is an illustrative, non-secret profile name. Replace it and the Region with your existing profile and selected workload Region.

```sh
python3 scripts/aws_mcp_login.py --profile example-dev --region ap-northeast-1 --check
python3 scripts/aws_mcp_login.py --profile example-dev --region ap-northeast-1 --login-only
```

On Windows, use your installed Python command. When registering MCP, resolve the Python executable and script to absolute paths on your own computer. Do not copy paths from someone else's machine.

## Existing configuration and security

- Inspect an existing same-named MCP server and its behavior before changing it. Do not replace the entire configuration file.
- AWS CLI manages authentication on your computer. This script does not read credential caches or send them to GitHub.
- The helper creates a local lock file to coordinate sign-in.
- Connecting AWS MCP does not grant new IAM permissions. Operations allowed by your existing permissions can still change resources or incur charges. Write operations are not automatically approved.
- Review this repository and the AWS and agent distribution sources before running code. The first proxy start downloads an external package.
- Example Regions and profiles are not forced defaults. Keep the MCP endpoint Region separate from the workload Region.
- Do not diagnose `Invalid request parameters` as an expired session without checking the underlying evidence.

## Verification scope

GitHub Actions runs unit tests on macOS, Windows, and Linux without AWS authentication. The tests cover input validation, valid and expired sessions, network failure handling, post-login verification, GUI routing, and concurrent-startup isolation.

These tests do **not** verify real browser/MFA flows, macOS Terminal permissions, live AWS IAM access, or end-to-end behavior inside each agent. **We do not claim verified support for every version of Codex, Kiro, or Claude Code.**

```sh
python -m unittest discover -s tests -v
```

The setup skills translate the [original Japanese source](https://github.com/AustinF02/aws-agent-skills-ja/tree/86c909dc63916ae1a45f58ae244fc64fc0c0bce7); aws-backend-tdd adapts the [Japanese TDD edition](https://github.com/AustinF02/aws-agent-skills-ja/tree/cea1c82be73dca543d312d36b2a6f85a3c45fb7e/skills/aws-backend-tdd). The launcher logic is preserved; user-facing messages and instructions use English. The Japanese repository retains the original test-first failure and subsequent passing runs. This repository records regression checks for the English edition.

## Development guidelines

[AGENTS.md](AGENTS.md) is the source of the development policy. Claude Code refers to it through [CLAUDE.md](CLAUDE.md), and Kiro through [.kiro/steering/development.md](.kiro/steering/development.md). The Kiro file contains a single `inclusion: always` declaration.

To adopt this policy in another project, merge the relevant guidance into its existing AGENTS.md before adding the reference files. Do not replace existing project instructions wholesale.

### Recommended external skills

These are links only. Their skill instructions, installers, and hooks are not bundled or installed automatically.

- [ponytail](https://github.com/DietrichGebert/ponytail) — Keep changes focused and simple.
- [caveman](https://github.com/JuliusBrussee/caveman) — Keep reports concise without omitting necessary facts.

Check each upstream project's installation instructions, supported agents, and license. The bundled AWS skills do not require these external development skills. The repository development policy additionally uses ponytail and caveman.

## Official references

- [AWS Agent Toolkit setup instructions](https://raw.githubusercontent.com/aws/agent-toolkit-for-aws/refs/heads/main/setup-instructions/setup.md)
- [AWS Knowledge MCP](https://awslabs.github.io/mcp/servers/aws-knowledge-mcp-server)
- [AWS MCP Proxy](https://github.com/aws/mcp-proxy-for-aws)
- [AWS CLI login](https://docs.aws.amazon.com/cli/latest/reference/login/)
- [Codex Skills](https://developers.openai.com/codex/skills)
- [Kiro Skills](https://kiro.dev/docs/skills/)
- [Claude Code Skills](https://code.claude.com/docs/en/skills)

This is an unofficial community project, not an official distribution from AWS, OpenAI, or Anthropic. Official instructions may change; check the current documentation when setting up your environment.

## Contributing and changes

See [CONTRIBUTING.md](CONTRIBUTING.md) for focused contributions and [CHANGELOG.md](CHANGELOG.md) for changes. Unreleased entries are not version tags.

## License and sharing

Code and documentation created in this repository are available under the [MIT License](LICENSE). Linked external skills and official documentation remain subject to their own terms.

If this helps you, consider giving the repository a star. For bug reports, include your OS, agent and version, reproduction steps, and a sanitized error summary. Do not post credentials, AWS account IDs, ARNs, email addresses, or browser authentication URLs.
