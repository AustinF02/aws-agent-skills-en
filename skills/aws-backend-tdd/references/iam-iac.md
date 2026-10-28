# IAM and IaC Verification

Read applicable sections. AWS API checks require real-aws authorization.

## IAM

Inspect generated Action, Resource, and Condition values locally.
Include negative cases: allow intended resources; deny unintended resources.

Use Access Analyzer validation or IAM Policy Simulator/
simulate-principal-policy as appropriate.
Specify actions, resources, and context.
Syntax validation does not prove effective permissions; simulations have limitations.
Never perform dangerous writes merely to test denial.

## IaC

- Prefer CloudFormation YAML; use cfn-lint and, when appropriate, cfn-guard.
- Assert important resources, properties, and policies—not only whole-template snapshots.
- Inspect synth lookups and external execution.
- Before applying, inspect replacement, deletion, and IAM changes using
  cdk diff or change sets. Check version, execution mode, and authorization.
- Change-set creation and execution are separate operations.
- Check drift when relevant; distinguish it from proposed changes.

Report local validation, AWS-side validation, and deployed behavior separately.
