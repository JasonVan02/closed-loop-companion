# Contributing

Issues and pull requests should describe an observable problem and provide enough evidence to reproduce it. For potential security issues, follow [SECURITY.md](SECURITY.md) before posting publicly.

## Issue and pull request information

```text
Scenario:
Expected behavior:
Observed behavior:
Route: DIRECT / LIGHT / FULL
Environment: skill version, OS, Python version, host and relevant tool capabilities
Reproduction:
Relevant checks: commands, results and any unverified assumptions
```

For a pull request, explain what changed, why it is necessary, and how it was verified. Keep changes focused. Distinguish observed results from completion claims, simulated review from real external review, and required fixes from optional improvements. Preserve user acceptance as a separate decision.

## Privacy

Do not submit real ChatGPT conversation logs, real task IDs, authorization records, customer or project material, credentials, secrets, or private screenshots. Prefer synthetic fixtures, anonymized reproductions and minimal test cases. Anonymization requires checking the content, metadata and filenames, not just changing a display name. Use visibly synthetic identifiers and never insert real credentials into a test fixture.

## Local checks

From the skill root, run:

```sh
python3 -m unittest discover -s tests -v
python3 scripts/closed_loop.py --help
```

Run the Skill validator supplied by your Codex installation when changing skill metadata. Check relative documentation links and the installable package when changing names, paths or packaging. See [testing guidance](references/testing.md) for the existing suite and behavioral validation requirements.

Do not replace security negative tests with successful-path checks. Protocol, authorization, gate or other runtime changes need their relevant regression coverage and independent review; passing a documentation check does not validate those behaviors. Keep generated logs, local audits, caches and private material outside the public package.

Contributions are made under this project's [Apache License 2.0](LICENSE). Preserve applicable license and attribution notices for any third-party material you introduce.
