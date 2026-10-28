# Development Guidelines

## Working standards

- Read the existing code, specifications, and relevant tests before implementing changes.
- Change only the requested scope. Do not add unrelated cleanup or features.
- In Plan mode, investigate and plan only. Do not implement before authorization.

## Choosing skills

- Use the installed tdd and ponytail skills when adding or changing behavior.
- Use caveman's concise style for progress and completion reports.
- Read the applicable SKILL.md before using a skill. Report a missing skill rather than installing it without authorization.
- Do not copy external skill instructions into this file.

## Resolving conflicts

- First run a test that fails for the behavior being changed.
- Make the smallest implementation that passes. Refactor only when needed.
- Do not use ponytail's simplicity principle to skip TDD, input validation, or necessary error handling.
- Do not use caveman's brevity to omit commands, results, failure causes, or unverified behavior.
- Write blog posts and specifications in clear, ordinary English unless the intended audience requires another language.

## Completion reports

Include:

- Completed behavior
- Changed files
- Commands run and their results
- Check and verification records
- Remaining limitations, unverified behavior, and risks
- Status
- Next action

Never report a check as completed if it was not run.

## Repository boundaries

Do not commit AWS credentials, authentication caches, local MCP configuration, or environment files. Tests use mocked results; they do not sign in to AWS or operate resources. Do not silently change an existing authentication method, IAM permissions, or default Region.
