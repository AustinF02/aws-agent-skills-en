# Testing AWS Backends

Read only applicable sections. Prefer existing tooling; add dependencies only when needed.

| Tool | Useful for |
| --- | --- |
| botocore Stubber | Python SDK requests, responses, service errors |
| moto | Stateful tests for supported AWS services |
| aws-sdk-client-mock | JavaScript SDK v3 commands and responses |
| DynamoDB Local | Persistence and conditional updates |
| SAM local invoke | Lambda runtime and event input |
| LocalStack | Supported service integrations |

Check coverage and actual endpoints; SAM can call real AWS.
Use isolated ports/data and bounded readiness checks.
Treat setup failures as infrastructure failures, not application defects.

## Observable contracts

- API: validation, authorization, responses, errors.
- SDK: requests, pagination, failures, retries.
- Lambda: fixtures from official schemas, SAM generate-event, or sanitized events.
  Do not mix event formats.
- Async: control clocks, waits, randomness, and injected failures.
  Verify processing state, deduplication, and partial failures—not fixed sleeps.
  Handler output and actual DLQ delivery require separate verification.
- Persistence: conditional updates, races, post-failure state.
  [DynamoDB GSI reads are eventually consistent](https://docs.aws.amazon.com/amazondynamodb/latest/developerguide/HowItWorks.ReadConsistency.html);
  [S3 object reads have strong read-after-write consistency](https://docs.aws.amazon.com/AmazonS3/latest/userguide/Welcome.html#ConsistencyModel).
  Test notifications, replication, and concurrent updates separately.
- Operations: required log fields and metric names, values, and units.
  Avoid whole-log assertions; verify sensitive data stays excluded.

## Illustrative RED → GREEN

Contract: reject an empty ID.
Assume validate_item_id currently returns its input.

```python
# tests/test_validation.py
import unittest
from validation import validate_item_id

class ValidationTests(unittest.TestCase):
    def test_rejects_empty_item_id(self):
        with self.assertRaises(ValueError):
            validate_item_id("")
```

Run:
`python -m unittest discover -s tests -p test_validation.py -v`

Confirm failure because ValueError was not raised—not an import error.

```python
# validation.py
def validate_item_id(value):
    if value == "":
        raise ValueError("item_id must not be empty")
    return value
```

Rerun the same command. Refactor only if needed.
