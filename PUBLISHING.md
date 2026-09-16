# Publishing copy and release notes

## Name

Closed Loop Companion

## Repository slug / Skill name / Directory

`closed-loop-companion`

## Brand

Companion workflow skill for complex agent tasks.

**Make agents prove the work before calling it done.**

Built for Codex workflows, with independent ChatGPT review when supported.

> Closed Loop Companion is an independent open-source project.
> It is not affiliated with, endorsed by, or sponsored by OpenAI.
> ChatGPT, Codex, and OpenAI are trademarks of OpenAI.


## Short description

Add evidence-based execution, independent ChatGPT review, repair loops, and completion gates to complex Codex tasks.

## 中文短描述

为复杂 Codex 任务增加证据验证、独立 ChatGPT 审查、修正闭环与完成门禁。

## Long description

Closed Loop Companion is a workflow companion for important, complex Codex tasks. It works alongside domain-specific skills: your development, design, marketing or game skill supplies the domain expertise, while this companion structures execution, acceptance criteria, evidence collection, independent review, repair and recheck.

The workflow connects implementation to observable evidence rather than relying on completion claims. It distinguishes tiny mechanical edits, moderate local work and full independent review, so routine changes do not inherit an unnecessary heavyweight process. Findings are classified before action, and repeated failures prompt a reassessment of direction.

Real ChatGPT review depends on compatible environment tools, accessible sessions and authorized material transfer. When those capabilities are unavailable, the skill clearly reports local-only review and the unmet external gate. It never substitutes a Codex subagent for a real ChatGPT reviewer. Passing the agreed checks means ready for user acceptance; the user always retains the final acceptance decision. Review helps detect gaps without guaranteeing correctness or replacing human judgment.

## Positioning and labels

- Type: **Companion Skill**; also describable as a workflow/meta skill.
- Descriptive category: **Workflow / Quality / Review**.
- Suggested search terms: `workflow`, `codex`, `review`, `quality`, `verification`, `agents`, `chatgpt`, `orchestration`, `developer-tools`.

These are editorial labels. This standalone Skill does not define a marketplace `tags` field. Its `SKILL.md` uses the existing optional `metadata` mapping for package-owned strings (`version`, `skill-type`, `category`); these keys do not register a marketplace listing or change routing.

## Platform and version mapping

Checked against current official documentation on 2026-09-10:

| Surface | What applies to this delivery |
|---|---|
| Standalone Codex Skill | Required `SKILL.md` name/description; optional `agents/openai.yaml` for presentation/invocation policy. Deliver the folder or ZIP for local installation. [Build skills](https://learn.chatgpt.com/docs/build-skills). |
| Package release | `VERSION` contains `1.0.0`, mirrored in package-owned metadata. This is our release convention, not a required Codex version field or a created Git tag. |
| Plugin distribution | Official plugin manifests support `version` and `keywords`; OpenAI presentation and marketplace records support `category`. These belong to a separate plugin package, not new fields in Skill UI YAML. A documented category example is `Productivity`; final platform selection must use the actual submission choices. [Package your plugin](https://developers.openai.com/plugins/build/plugins). |
| Public directory submission | A separate submission process, including publisher information and review. This ZIP and copy are prepared materials, not a submitted or approved listing. [Submit plugins](https://developers.openai.com/plugins/deploy/submission). |

No plugin wrapper, account access, marketplace record or public repository URL is fabricated by this release. The project uses Apache License 2.0. If a plugin listing is requested later, recheck the current schema and map these labels to supported fields.

## v1.0.0 release notes

Initial public release. [CHANGELOG.md](CHANGELOG.md) lists the existing V1 capabilities now packaged under the public brand. The public name and documentation changed; core workflow, protocol identifiers, schema, route/state values, CLI and test logic did not.

Earlier core validation applies to its original snapshot. This public packaging revision receives its own LIGHT checks; it does not claim a new real ChatGPT external PASS. No v1.1 functionality is added.

The architecture is designed as a reusable review-governance pattern, while v1.0.0 is implemented and tested primarily around Codex workflows and supported ChatGPT review. No support for arbitrary agents/reviewers, Claude/Gemini adapters, CI-native review, GitHub Actions integration or background orchestration is implied.

## GitHub repository preparation

Repository name: `closed-loop-companion`

Description:

```text
Evidence-based execution, independent review, repair loops and completion gates for complex Codex workflows.
```

Topics: `codex`, `chatgpt`, `agents`, `agentic-workflows`, `review`, `verification`, `workflow`, `developer-tools`, `ai-agents`.

These nine topics follow GitHub's documented format; set them only when a repository is actually created. [GitHub topics](https://docs.github.com/en/repositories/managing-your-repositorys-settings-and-features/customizing-your-repository/classifying-your-repository-with-topics).

Upload the contents of this clean Skill directory as the repository root. Include no surrounding private audit, local backup or generated run evidence. No owner, repository URL or remote is assumed. See [SECURITY.md](SECURITY.md); creating that file alone does not enable private vulnerability reporting in GitHub settings.

## GitHub Release preparation

Tag to create later: `v1.0.0`

Title: **Closed Loop Companion v1.0.0**

Release body:

```text
Initial public release of Closed Loop Companion.

Closed Loop Companion adds a review-governance layer around complex Codex work:

- structured task contracts
- DIRECT / LIGHT / FULL routing
- evidence-based verification
- independent ChatGPT review when supported
- review finding triage
- repair and recheck loops
- direction reassessment
- authorization boundaries
- completion gates
- domain skill composition

The user always retains final acceptance.

See README for installation, capability requirements and limitations.

Licensed under the Apache License 2.0.
Independent project; not affiliated with, endorsed by, or sponsored by OpenAI.
```

Prepared asset name: `closed-loop-companion-v1.0.0.zip`; publish its matching SHA256SUMS alongside it. The prepared tag, title, body and filenames are not evidence that a GitHub tag or release exists.

## License and attribution

Licensed under the Apache License 2.0; see [LICENSE](LICENSE). The LICENSE file is an unmodified copy of the [official full text](https://www.apache.org/licenses/LICENSE-2.0.txt), including its standard appendix. Appendix fields are examples in the official license, not an invented project owner or an unfinished runtime setting.

The source candidate contained no existing third-party NOTICE file or attribution header to carry forward. No separate NOTICE is added and no company or maintainer identity is invented. Keep any applicable third-party notices if future contributions add such material. Contribution expectations are in [CONTRIBUTING.md](CONTRIBUTING.md).

## Publication status

This package and its GitHub metadata are prepared for owner review. No public repository, remote, tag, release, Skill directory listing or Plugin directory submission has been created. The owner must explicitly authorize those later actions and choose the hosting account/repository. Before public hosting, configure an actual private vulnerability reporting route or a real security contact; do not invent an address.
