---
name: aws-backend-tdd
description: Use behavior-first tests for AWS infrastructure and backend changes. Separate test tiers and cloud side effects; favor minimal implementation and recorded verification.
---

# AWS Backend TDD

## Principles

- Catch realistic bugs; do not optimize for test counts.
- Inspect existing code, contracts, callers, and tests. Keep changes scoped.
- Stop after two unsuccessful repair/recheck attempts for the same failure.
- Follow user and project instructions. Do not expand permissions, dependencies, or scope.

## Choose the test

Determine whether behavior, contracts, permissions, or retention changes.
Skip ceremonial tests for documentation, translation, or formatting.

First explain: “What incorrect implementation would make this test fail?”
Identify the observable boundary and risk. Ask only about material ambiguities.

Derive expectations independently from specifications or checked examples.
Test public behavior, not internal structure or mock existence.
Verify arguments, counts, or ordering when they are contractual.

## Start with the cheapest sufficient tier

| Tier | Automatic execution requires |
| --- | --- |
| unit | No real AWS connection |
| local-integration | Verified endpoints, credentials, outbound access, and readiness |
| real-aws | Authorized targets, operations, costs, and cleanup |

Escalate only what lower tiers cannot prove.
Separate tiers using existing directories, markers, or commands.
Inspect unclassified suites before running them.
“Local” and emulator success do not establish AWS safety or compatibility.

## RED → GREEN → REFACTOR

1. RED: Demonstrate one intended behavioral failure—not syntax, dependency, readiness, or network errors.
2. GREEN: Implement only enough to pass. Do not weaken expectations or add speculative features.
3. REFACTOR: Make necessary improvements and rerun. Skip unnecessary cleanup.

Do not break passing behavior to manufacture RED.
Do not automatically delete pre-test code or misrepresent later tests as test-first.
Expand verification to affected checks; distinguish existing failures.

## Load references selectively

Determine the boundary and tier first. Resolve ambiguity before loading references.

Resolve paths from this SKILL.md’s directory, not the working directory.
Explicitly open required files. Report missing files instead of inventing guidance.

- SDKs, runtime contracts, local integration, examples: [testing.md](references/testing.md)
- IAM and IaC: [iam-iac.md](references/iam-iac.md)
- Before real AWS access: [real-aws.md](references/real-aws.md)

## Safety and reporting

Keep secrets and personal information out of logs, fixtures, and evidence.
Never widen IAM or network access to pass tests.
Verify uncertain AWS details against official documentation.

Report status, files, tier-specific commands/results, RED/GREEN evidence,
unverified behavior, risks, and next steps.
For real AWS, include cleanup verification and remaining resources.
Distinguish configuration saved, local success, deployment success, and live behavior.
