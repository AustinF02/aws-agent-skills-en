# Real AWS Verification

Confirm account, Region, resources, read/write operations, costs, limits,
stop conditions, created/retained resources, and cleanup.
Preserve existing authentication.

- Stay within authorization; clarify missing material permissions.
- Prefer the cheapest sufficient check. Do not overstate what validation or dry-run proves.
- Isolate and identify test resources.
- Bound polling by deadline, attempts, interval, and exit conditions.
- Never treat deployment, IAM changes, or data mutation as implicitly authorized.
- Follow the core’s two-attempt repair limit.

## Cleanup

Attempt authorized cleanup even after failure or cancellation.
Touch only intended test resources, never existing/shared data.

Verify disappearance and residual resources—not merely successful deletion requests.
If cleanup is unauthorized, unavailable, or fails, stop and report remaining costs/actions.

Report cleanup results, verification method, retained resources, and failures.
Claim “nothing remains” only after verification.
