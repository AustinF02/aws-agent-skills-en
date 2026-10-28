# Contributing

Open an issue or pull request with the problem, a small proposed change, and verification evidence. Keep skill entrypoints concise; place conditional detail in references and preserve relative links. Check AWS-specific claims against current official documentation and link the source. Name or link third-party tools without copying their documentation.

For code changes, add a meaningful failing test before the smallest fix; documentation-only changes do not need artificial RED tests. Run `python -m unittest discover -s tests -v`. CI uses mocks and must not authenticate to AWS or operate real resources. Separate unit, local-integration, and real-AWS checks, and report unverified behavior. Include sanitized reproduction steps, never credentials, authentication URLs, or personal configuration.

Update [CHANGELOG.md](CHANGELOG.md) under Unreleased for user-visible changes. Published version tags, when introduced, should use semantic versioning; draft iteration numbers are not releases. Contributions are provided under the repository's [MIT License](LICENSE).
