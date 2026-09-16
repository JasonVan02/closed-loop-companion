# Invocation and trigger calibration

## Intent, not keyword matching

This companion is considered for complex work that benefits from execution governance and independent verification. It is not a global middleware hook. The host selects from the name/description; selecting the skill loads its instructions. A phrase below is an intent clue, not a regex that forces FULL.

| Intent family | English examples | 中文例子 |
|---|---|---|
| Lifecycle | closed loop; closed-loop review; complex implementation; review repair recheck | 闭环；完整闭环；复杂任务；修正后复核 |
| Independence | independent review; ChatGPT review; external review; don't self approve | 独立审查；ChatGPT 审查；外部审查；不要自己宣布完成 |
| Direction | architecture review; evidence-based review | 架构审查；证据验证 |
| Handoff | completion gate; ready for user acceptance; do not mark complete | 完成门禁；正式验收 |

“formal verification” may describe a user's wish for rigor, but this skill does not perform mathematical formal verification. Clarify whether proof is actually required and use suitable domain methods. An isolated phrase such as “architecture review” may just request analysis, not implementation or a new external handoff; preserve the task's actual scope.

## Selection and routing are separate

- Explicit `$closed-loop-companion` selects the companion. A typo can take DIRECT.
- Combined invocation keeps the selected domain skill responsible for domain methods and this skill responsible for lifecycle evidence. If a domain skill is unavailable, state it; do not pretend to load it.
- Conditional selection considers impact, risk, ambiguity, verification difficulty, architectural consequence, user importance and reversibility. File/line counts and the existence of tests are insufficient on their own.
- Explicit full independent/ChatGPT review means FULL even for a small edit. Explicit local-only review stays local; do not add an unrequested cloud review.
- Ordinary low-impact review wording does not automatically require the whole implementation loop. A user asking “explain the review findings” has not requested product changes.
- If FULL cannot run, apply [capability fallback](capabilities.md); never silently weaken the acceptance standard.

Examples: three files changed only for spelling → DIRECT; a one-line access-control change → consider FULL; a bounded README packaging update with no runtime change → LIGHT when local verification and independent review are sufficient; complex UI matching a visual reference → FULL with visible render evidence.

Automatic discovery depends on host behavior and available context. Explicit invocation is the practical fallback if natural-language selection misses; these examples are not a promise of deterministic activation across every model.
