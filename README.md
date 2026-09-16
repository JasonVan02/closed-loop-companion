# Closed Loop Companion

**Make agents prove the work before calling it done.**

Companion workflow skill for complex agent tasks.

Built for Codex workflows, with independent ChatGPT review when supported.

A companion workflow skill for Codex that adds structured execution,
evidence-based verification, independent ChatGPT review, repair loops,
and completion gates to complex tasks.

**让 Agent 不只是“说做完了”，而是证明它真的完成了。**

为复杂 Codex 任务增加结构化执行、证据验证、真实 ChatGPT 独立审查、修正闭环和完成门禁。
当前主要面向 Codex 工作流，并在环境支持时使用真实 ChatGPT 做独立审查。

> Closed Loop Companion is an independent open-source project.
> It is not affiliated with, endorsed by, or sponsored by OpenAI.
> ChatGPT, Codex, and OpenAI are trademarks of OpenAI.

**Type:** Companion Skill · **Category:** Workflow / Quality / Review · **Release:** v1.0.0

These are this package's descriptive labels, not marketplace registration fields.

| In 30 seconds / 快速了解 | Answer / 答案 |
|---|---|
| What is it? / 做什么？ | Governs how important work is executed, proven, reviewed and handed back. / 管理重要任务的执行、证据、审查与交付。 |
| When should I use it? / 何时使用？ | Meaningful behavior changes, difficult verification, architectural consequences or explicit independent review. / 有明显影响、难验证、涉及架构或明确要求独立审查时。 |
| When should I skip it? / 何时不用？ | Typos, formatting and other low-risk mechanical edits. / 拼写、格式等低风险机械修改。 |
| How does it combine? / 如何组合？ | Domain Skill handles domain decisions; this skill handles the execution and review lifecycle. / 领域 Skill 管业务方法，本 Skill 管执行与审查流程。 |

Real ChatGPT review requires compatible tools and access. Without them, the result is `LOCAL_REVIEW_ONLY`; a FULL gate requiring external review remains unmet.

## What it is

This skill does not teach Codex how to build a specific product. It governs how complex work is executed, reviewed, verified, repaired, and handed back to the user. In Codex workflows, this means implementation is not treated as complete merely because Codex reports success.

它不负责告诉 Codex“业务应该怎么做”，而是约束复杂任务“应该如何可靠地完成”。It wraps the execution lifecycle, not the domain reasoning. It is a workflow companion, not a replacement for development, design, marketing, testing or architecture expertise.

## Why it exists / What problem does this solve?

An implementation can finish while missing the user's intent. Tests may pass even though a design looks wrong, an architectural approach keeps accumulating patches, or required evidence is absent. This skill adds structured checks between implementation and user acceptance. It helps detect such gaps; it does not guarantee correctness.

实现完成、测试通过，不等于目标达成。闭环要求对照原始目标和实际产物检查，而不是只认可执行者的总结。

## Quick Start

After [installation](#installation), send a task like this in Codex:

```text
Use $closed-loop-companion to implement this task.

Goal:
Add CSV export to the transaction page.

Requirements:
- Export current filtered transactions.
- Preserve current sorting.
- UTF-8 CSV.
- No server-side persistence.

Return it for my acceptance only after the FULL review reaches
READY_FOR_USER_ACCEPTANCE. If real ChatGPT review is unavailable,
report LOCAL_REVIEW_ONLY and the unmet gate.
```

```text
使用 $closed-loop-companion 完成这个任务。

目标：为交易页面增加 CSV 导出。
要求：
- 导出当前筛选结果
- 保留排序
- UTF-8 CSV
- 不新增服务端持久化

只有完整闭环达到 READY_FOR_USER_ACCEPTANCE 后再提交给我验收。
真实 ChatGPT 不可用时，明确报告 LOCAL_REVIEW_ONLY 和未满足的门禁。
```

Codex first inspects the project, clarifies material gaps and checks capabilities. Routine implementation choices stay with Codex; important product decisions and new material-sharing authorization stay with you.

## When to use / 何时使用

Consider the companion when review adds meaningful value:

| Situation | 中文 |
|---|---|
| New features with meaningful behavior changes | 有明显行为变化的新功能 |
| Architecture or data-model changes | 架构或数据模型调整 |
| Large refactors with behavior or regression risk | 存在行为或回归风险的大型重构 |
| Multi-file work with non-trivial acceptance criteria | 验收复杂的多文件实现 |
| High-fidelity UI or important visual work | 高保真 UI 或重要视觉交付 |
| Games, 3D or rendering where technical success cannot establish visual quality | 技术成功不能证明视觉质量的游戏、3D、渲染任务 |
| New Skill creation | 新 Skill 创建 |
| Complex bugs with regression risk | 有回归风险的复杂 Bug |
| Repeated failures or accumulating patches | 反复失败或不断累积补丁 |
| Explicit independent ChatGPT review | 明确要求真实 ChatGPT 独立审查 |
| Formal deliverables before user acceptance | 用户验收前的重要正式交付 |

Judge impact, risk, ambiguity, verification difficulty, architectural consequence, user importance and reversibility. File count is a weak signal: three files, 100 lines, or having tests does not automatically mean FULL.

## When not to use / 何时不必使用

- Typos / 拼写错误。
- Simple local renames without behavior or public API changes / 不改行为或公共接口的局部更名。
- Formatting-only changes / 纯格式调整。
- Trivial copy edits / 轻微文字修订。
- Obvious one-line fixes with verified low impact / 已确认影响很小的单行修复。
- Low-risk mechanical changes / 低风险机械修改。
- Tasks with no meaningful review value / 没有实质审查价值的任务。

The skill is intentionally not designed to wrap every Codex action in a heavy review loop. An explicitly invoked typo task can still use DIRECT. An explicit request for full independent review overrides that default. A one-line permissions change may still need FULL because its impact matters more than its size.

## How it works

```text
Goal and boundaries → project inspection → implementation → verification
→ evidence → independent review → finding triage → repair and recheck
→ completion gate → user acceptance
```

Findings are classified as `VALID`, `FALSE_POSITIVE`, `MATERIAL_MISSING` or `DECISION_REQUIRED`. Fix proven defects, submit counterevidence for false positives, supply missing material, and return consequential decisions to the user. Repeated failure of the same criterion triggers direction reassessment rather than endless patching.

问题需先分类，再修复、反证、补证或请用户决策；同一验收项连续失败时先复查方向。

## Three invocation modes / 三种调用方式

### A. Explicit invocation

```text
Use $closed-loop-companion for this task.
使用 $closed-loop-companion 执行这个任务。
```

The clearest way to select this companion. Selection does not by itself force FULL: the task's needs and your stated review requirements determine the route.

### B. Combined invocation

```text
Use $marketing-creative-director to design the campaign concept.
Use $closed-loop-companion to govern execution and independent review.
```

```text
使用 $godot-game-development 完成实现，
同时使用 $closed-loop-companion 做执行闭环和独立审查。
```

Domain skill names in examples must be replaced with skills installed in your environment. The companion does not install them or assume they exist.

### C. Conditional companion

Codex can consider this skill when the task has substantial impact, difficult verification or an explicit review requirement. Automatic discovery remains enabled, but selection depends on the host and the task; it is not a universal hook.

自然语言也可以表达意图：

```text
Build this with an independent ChatGPT review before completion.
Use a closed-loop implementation process.
Do not self-approve this task. Send the authorized final evidence to ChatGPT.
Implement, verify, independently review, repair if needed, then return it for my acceptance.

这个任务走完整闭环。
完成后让真实 ChatGPT 独立审查，不要自己宣布完成。
实现、验证、外审、修正后再提交给我验收。
这个任务比较重要，使用闭环审查模式。
```

Use explicit invocation if discovery misses your intent. [Invocation guidance](references/invocation.md) explains trigger boundaries. These prompts request a workflow; they do not authorize unspecified private files to be uploaded.

## FULL / LIGHT / DIRECT

| Route | What happens / 会做什么 |
|---|---|
| DIRECT | Very small, low-risk work: implement and inspect the change. / 实施并针对性核验。 |
| LIGHT | Moderate local work: verify and obtain independent internal review. / 本地验证与独立内部检查。 |
| FULL | Important or complex work: package evidence and obtain real ChatGPT review, then repair/recheck as needed. / 证据包、真实外审、必要修正复核。 |

Missing tools do not silently turn a requested FULL task into a successful LIGHT task. See [architecture](references/architecture.md) for full routing and state rules.

## Example workflows

Short examples show the request, route and honest final state:

- [CSV export and a typo](examples/simple-feature.md)
- [Architecture change](examples/architecture-change.md)
- [High-fidelity UI](examples/ui-review.md)
- [Skill creation](examples/skill-build.md)
- [Marketing with a domain skill](examples/domain-composition.md)

## Using with other Skills / Works with domain skills

| Domain | Example pairing |
|---|---|
| Product | `$product-development` + `$closed-loop-companion` |
| UI | `$ui-design` + `$closed-loop-companion` |
| Godot | `$godot-game-development` + `$closed-loop-companion` |
| Marketing | `$marketing-creative-director` (or your installed marketing skill) + `$closed-loop-companion` |

These domain names are illustrative, not bundled dependencies. Use your installed equivalents.

**Domain skill:** what good work looks like and how to produce it in that domain.
**Closed Loop Companion:** how that work is executed, proven, reviewed, repaired and handed off.

Domain Skill decides what good work looks like. Closed Loop Companion governs how that work is executed, proven, reviewed, repaired and handed off.

领域 Skill 负责业务方法和领域质量标准；Closed Loop Companion 负责执行、证据、独立审查、修正和验收门禁。

例如营销 Skill 决定营销策略；Closed Loop 检查目标是否明确、策略产物是否有证据、是否完成独立审查。它不接管领域推理，也不越过用户的范围与取舍。

## Independent ChatGPT review

FULL starts with [capability detection](references/capabilities.md): identify currently available tools, an accessible real ChatGPT destination, exact send/readback support, independent internal review and any required visual channel. Tool names, accounts, models, message limits and session creation vary by environment.

If supported and authorized, Codex coordinates delivery and reads the real reply. An internal Codex subagent is not a real ChatGPT reviewer. A successful tool call, an idle task or an old PASS is not proof of this round's review.

If unavailable, continue useful authorized local work and report:

```text
LOCAL_REVIEW_ONLY
Independent real ChatGPT review unavailable in this environment.
READY_FOR_USER_ACCEPTANCE requiring external review was not reached.
```

`LOCAL_REVIEW_ONLY` describes the available review coverage, not a new CLI route or a passing FULL gate. Do not use it to relabel a failed external review. Only explicit user agreement can revise the acceptance standard; preserve the unmet original standard and never claim an external PASS.

## Evidence-based review / Claim is not Evidence

“Tests passed” is a claim. Useful evidence includes the actual command, working directory, exit code and unedited output. This is an illustrative record, not this package's test result:

```text
Command: npm test
Working directory: the project under review
Exit code: 0
Result: 64/64 passed
Raw output: attached execution log
```

“The UI matches the design” requires a design reference, actual screenshot, viewport and corresponding implementation. A local image path or successful build does not prove a reviewer saw the visual result.

源码、diff、真实执行记录和可见图像支持判断；执行者的总结不能代替它们。See [evidence requirements](references/evidence-pack.md).

## Completion Gate

For FULL:

```text
Implementation complete + evidence complete + all acceptance criteria pass
+ independent internal review passes + current real ChatGPT review passes
+ no unresolved blocking findings or decisions
= READY_FOR_USER_ACCEPTANCE
```

The helper validates identities, hashes, required evidence and review provenance. It cannot establish that a design is good or a test suite is sufficient. LIGHT and DIRECT use their documented local gates; the CLI `gate` command only supports FULL. [Full rules](references/completion-gate.md).

## Authorization & privacy

Evidence transmission requires authorization for the specific files, destination and purpose. A prior task's approval does not cover the next task. Secrets and credentials are excluded even from otherwise approved files. Content scanning is a heuristic and needs human/agent judgment.

This package contains instructions, synthetic tests and local helpers. It includes no reviewer account, session, private audit or credentials. The Python helper does not connect to ChatGPT; the host performs authorized handoff. [Authorization rules](references/authorization.md).

## What READY_FOR_USER_ACCEPTANCE means

```text
Implementation finished ≠ Task accepted
READY_FOR_USER_ACCEPTANCE ≠ USER_ACCEPTED
```

READY means the agreed checks for the declared route have passed and the result is ready for your judgment. It never means you already approved it. Only your explicit acceptance of the delivered version establishes `USER_ACCEPTED`.

“可提交验收”与“用户已验收”是两回事。The skill does not replace the user's final decision.

## Limitations

The architecture is designed as a reusable review-governance pattern, while v1.0.0 is implemented and tested primarily around Codex workflows and supported ChatGPT review. The broader “agents” slogan does not claim support for arbitrary agents or reviewers.

v1.0.0 includes no Claude/Gemini adapter, arbitrary-reviewer backend, CI-native reviewer, GitHub Actions integration or background orchestration service. Windows has not been fully tested; Python portability is not a claim of end-to-end Windows compatibility.

- Real ChatGPT handoff and independent subagents depend on available environment capabilities.
- Natural-language discovery can miss or misclassify a task; explicit invocation is more predictable.
- Text delivery does not establish image visibility; visual work needs verified visual evidence.
- Review helps detect issues but is not a correctness guarantee or formal verification.
- No promise of every-account compatibility, a particular model or permanent background operation.
- Consent, consequential decisions and final acceptance may require user participation.

See [known limitations](references/known-limitations.md). 本 Skill 不承诺零人工介入、无 Bug 或自动替代用户验收。

## Installation

Install the directory containing `SKILL.md`, not the ZIP itself. Current Codex documentation lists `~/.agents/skills` for user skills and `.agents/skills` for repository skills. Use the location your host discovers; some existing installations use `~/.codex/skills`. Avoid duplicate copies with the same name. [Official skill documentation](https://learn.chatgpt.com/docs/build-skills).

From a downloaded ZIP on macOS/Linux:

```sh
mkdir -p ./skill-unpack
unzip closed-loop-companion-v1.0.0.zip -d ./skill-unpack
mkdir -p "$HOME/.agents/skills"
# For a fresh install; back up an existing same-name directory before updating.
test ! -e "$HOME/.agents/skills/closed-loop-companion" && \
  cp -R ./skill-unpack/closed-loop-companion "$HOME/.agents/skills/"
```

From a Skill directory, copy that entire directory to the chosen skills folder. For project-only use, copy it into your repository's `.agents/skills/`. For Windows, the same directory layout can be used, but installation and end-to-end handoff have not been fully tested.

Check that the skill appears in your host's skill list, then invoke `$closed-loop-companion`. If it does not refresh, restart the client. Installation enables the instructions; it does not add ChatGPT handoff tools or grant account access.

The local helper and tests require **Python 3.9+**, using only its standard library. From the installed Skill directory:

```sh
python3 -m unittest discover -s tests -v
python3 scripts/closed_loop.py --help
```

解压后安装包含 `SKILL.md` 的整个目录；升级前保留旧副本，避免两个发现路径同时安装同名 Skill。

### Migrating from an internal build

Earlier internal builds used the working name `chatgpt-codex-closed-loop`.
The public v1.0.0 skill name is `closed-loop-companion` and its invocation is `$closed-loop-companion`.
Before installing, move the old internal skill directory outside every discovered skills location, keeping a backup if needed. Then install the new directory and refresh the skill list. Keep one active installation; the old working name is not a second entrypoint or alias.


## Repository / file structure

```text
closed-loop-companion/
  SKILL.md                 Agent entrypoint and routing
  README.md                User guide
  LICENSE                  Official Apache License 2.0 text
  SECURITY.md              Safe evidence handling and private reporting
  CONTRIBUTING.md          Reproduction and contribution guidance
  CHANGELOG.md             Initial public release history
  .gitignore               Keep local run data and caches out of source control
  PUBLISHING.md            Listing copy, release notes and distribution limits
  VERSION                  Package release label
  protocol.md              Protocol entrypoint
  agents/openai.yaml       UI metadata; implicit invocation remains enabled
  examples/                Short user requests, routes and outcomes
  references/              Architecture, capability, evidence and protocol details
  templates/               Contracts, review requests and report templates
  scripts/closed_loop.py   Existing deterministic local helper
  tests/test_closed_loop.py
```

Actual task logs belong in the user's project, outside the installed/released Skill. No private evidence or build caches belong in a release archive.

## Advanced configuration

Ordinary users supply goals and constraints, not transport JSON. Coordinating agents and advanced users can follow [CLI usage](references/advanced-usage.md), [protocol](protocol.md) and [testing guidance](references/testing.md). These describe the existing four CLI commands; this release adds no new runtime command or transport backend.

## License

Licensed under the Apache License 2.0. See [LICENSE](LICENSE) for details.
本项目采用 Apache License 2.0。

Commercial use is permitted subject to the license terms, including paid services, enterprise integrations, domain packs, consulting and hosted products. This does not promise any such offering. [Apache License 2.0](https://www.apache.org/licenses/LICENSE-2.0).

## Security / Contribution

Read [SECURITY.md](SECURITY.md) before sharing evidence or reporting a vulnerability.
Use [CONTRIBUTING.md](CONTRIBUTING.md) for issues and pull requests, with synthetic reproductions and relevant checks.
Release history is in [CHANGELOG.md](CHANGELOG.md); [PUBLISHING.md](PUBLISHING.md) contains GitHub and later distribution preparation. No public repository, tag, release or directory listing is created by these files.
