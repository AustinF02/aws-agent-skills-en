# Consolidation / 統合と移行

[English](README.md) | [日本語](README.ja.md)

The canonical repository is [AustinF02/aws-agent-skills](https://github.com/AustinF02/aws-agent-skills). Use this URL for both languages.

## Existing installations

1. Compare your installed skill folders with `skills/<skill-name>/` here. Back up local customizations.
2. Update each complete folder, including scripts and references, from this repository. Keep one copy of each skill per agent scope; reconcile duplicate installations before removing any copy.
3. Keep existing AWS profiles, caches, Keychain entries, and MCP settings. Updating skill files does not migrate those settings or authorize sign-in. If a helper's absolute path changes, update only that MCP command path after reviewing the difference.
4. Start a new agent session if required, then request English or Japanese. Test actual MCP discovery separately if you change MCP configuration.

CLI diagnostics remain English. The legacy `aws-agent-skills-ja` lock-cache directory remains unchanged so existing helper processes keep coordinating. There is no new language flag or automatic reinstall.

## 既存の導入環境

統合先は上記リポジトリです。このURLから日英両言語のスキルを導入できます。ローカル変更をバックアップして比較し、各スキルをフォルダ全体で更新してください。同じエージェントの同じ範囲には各スキルを一つだけ置きます。AWSプロファイル、認証キャッシュ、Keychain、MCP設定は保持します。スクリプトの絶対パスが変わる場合だけ、差分を確認して該当のMCP設定を更新します。必要なら新しいセッションを開始し、希望の言語を指定してください。更新だけで認証や接続確認が完了するわけではありません。

## Provenance

- English source: [70b7ae7](https://github.com/AustinF02/aws-agent-skills/tree/70b7ae7db6b68a35de7f1589191e0aaf8230904e).
- Japanese source: [197b254](https://github.com/AustinF02/aws-agent-skills-ja/tree/197b25466672008b65b2b460850596d5b793b6d3).
- Tests and event-auth code are identical at those revisions. Login-helper differences are translated text/comments; shared code retains English diagnostics. CI differs only in its displayed name.
- Japanese skill text and reference guides are preserved as supporting `.ja.md` documents. Each skill has one authoritative `SKILL.md`, one implementation, and one shared test suite.
- The Japanese guides are included in the consolidated repository.
