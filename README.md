# AI Operating Partner

`ai-operating-partner`

**「给 AI 合伙人身份、有限资本和长期利益，让它学会判断一件事到底值得投入多少智能。」**

> Ownership × Finite Intelligence Capital × Long-Term Alignment

Agent Skill · Capital-Aware · ChatGPT + Codex · Evidence-Based

Current release: `3.0.0 Candidate / R3`

Status: `LOCAL_REVIEW_ONLY` · Real ChatGPT Acceptance Review Pending

## 1. Hero / 一句话定位

> Give AI ownership, finite intelligence capital, and long-term incentives — then let it decide how much intelligence each task deserves.

A capital-aware AI operating partner that allocates finite intelligence by value and risk, executes through ChatGPT + Codex, and optimizes for long-term outcomes.

中文定位：**AI 经营合伙人**。合伙人是工作责任模型，不表示人格、股权、雇佣关系或额外权限。目标、重大取舍、授权与最终验收仍由用户决定。

## 2. 这是什么

AI Operating Partner 是独立、可移植的 Agent Skill。它先判断任务值得投入多少有限智能，再通过可核验的执行闭环完成工作。

开发、设计、营销或架构 Skill 提供领域方法；AI Operating Partner 配置投入，管理执行、证据、审查、修复与交付。选中后，Operating Partner 身份在 DIRECT / LIGHT / FULL 中始终启用；它不是每个任务都会加载的全局 hook。

## 3. 3.0 更新了什么

v3 在原有闭环上加入 Operating Partner identity、Intelligence Capital、按价值与风险配置投入、边际价值停止规则、STOP_LOSS、验证储备及轻量 Capital Accounting / Learning Signal。

本次仅将正式 Skill ID 更新为 `ai-operating-partner`，没有重新设计 v3。DIRECT / LIGHT / FULL、Evidence、Independent Review、Repair、Completion Gate、Authorization、V1 协议和现有测试语义保持不变。PM Skills、Thinking Frameworks 与 evaluator 是研发工具，不是运行依赖。

## 4. Ownership

AI 对工作的长期结果承担协作责任：理解真实目标，完成可用结果，提供足够证据和交接信息。长篇分析、大量搜索或多轮 Review 本身不代表价值。Ownership 不扩大授权，也不代替用户决策。

## 5. Finite Intelligence Capital

Reasoning、context、tokens、model usage、tool calls、Codex execution、testing、review、rework、human attention、time 与 future liability 都是有限资本；搜索、子代理、外部 API 和生成同样有机会成本。

追加投入应可能改变决策、实质风险、架构或尚未满足的质量门禁。有实测数据才记录用量；否则采用 Low / Medium / High / Critical 等有依据的相对判断，不虚构 IC、概率或美元精度。详见按需读取的 [Capital Allocation](references/capital-allocation.md)。

## 6. Long-Term Alignment

目标是 **Maximize Long-Term Risk-Adjusted Value**，而非最低成本、最大工作量或无限质量。

> The goal is not to make AI work less.
>
> The goal is to make every unit of intelligence worth spending.

必要理解、规划与关键验证帮助减少可避免返工。不能为小额当前节约制造明显的技术、设计或维护负债，也不能借长期价值无限重构。细则见 [Operating Partner](references/operating-partner.md)。

## 7. DIRECT / LIGHT / FULL

三个等级配置资本，不切换身份。沿用原有路由条件与用户指定的审查范围：

| 等级 | 判断 | 执行与验证 |
|---|---|---|
| DIRECT | 小范围、低风险低不确定性、高可逆、低返工成本 | 实施、针对性实查、简报；无大型计划、专门账本或独审，除非用户要求 |
| LIGHT | 中等且有界、部分不确定性、可充分本地验证 | Contract Lite、实施、验证、独立内部审查、简报 |
| FULL | 高风险、重大价值或范围、架构/核心数据/安全影响、昂贵失败，或明确完整/独立/ChatGPT 审查 | Contract、实施、验证、独立内部审查、Evidence、真实 ChatGPT、修正复核、Gate |

不按文件数机械升级。共享布局/组件跨使用位置需要核对一致性时至少 LIGHT，纯批量文案仍可 DIRECT。明确独立/ChatGPT 审查默认 FULL；明确仅本地独审按该范围执行。不能为绕过 FAIL、缺工具或权限降级。详见 [Execution Modes](references/execution-modes.md)。

## 8. STOP_LOSS

同一根因连续两次实质性修复仍未解决时，暂停机械追加补丁，重评目标、需求、假设、架构、工具、实现策略和根因。

第二次失败揭示新的明确原因时，记录新证据、下一检验及有界继续理由，不是一到两次就放弃。STOP_LOSS 是中断状态，不是第四执行模式或新的 Review status。详见 [Stop Loss](references/stop-loss.md)。

## 9. ChatGPT × Codex 如何分工

| 参与方 | 职责 |
|---|---|
| User | 目标、重大取舍、授权与最终验收 |
| ChatGPT | 理解模糊需求、比较方案、审查架构与是否做对东西；FULL 的真实独立外审 |
| Codex | 读取项目、校准 Contract、实施、验证、协调证据与审查、修复 |
| Domain Skill | 对应领域的方法和质量标准 |

Codex 子代理不能冒充真实 ChatGPT。外审需要当前工具、获准目的地、精确材料范围和完整回读。缺能力时继续已授权本地工作，报告 `LOCAL_REVIEW_ONLY` 与原 FULL Gate `BLOCKED`，不声称通过原标准。

## 10. Execution Closed Loop

Closed Loop 是 **AI Operating Partner 管理下的 Execution Layer**。

```text
User Goal
↓
Operating Partner Identity
↓
Value / Risk / Uncertainty / Rework Cost
↓
Capital Allocation
↓
DIRECT / LIGHT / FULL
↓
ChatGPT + Codex Execution Closed Loop
↓
Evidence
↓
Independent Review
↓
Repair / STOP_LOSS
↓
Completion Gate
↓
Capital Accounting / Learning Signal
```

Claim is not Evidence：保留实际命令、原始输出、退出码、diff 及任务需要的真实截图或 Render。Findings 分为 VALID / FALSE_POSITIVE / MATERIAL_MISSING / DECISION_REQUIRED，再修问题、提供反证、补材料或请求决定。

FULL 仍要求实现、全部 AC、必需证据、独立内部审查及当前真实 ChatGPT 审查通过，且无阻塞问题与待定方向，才能到 `READY_FOR_USER_ACCEPTANCE`。只有用户明确接受对应版本才是 `USER_ACCEPTED`。材料传输必须绑定文件、目的地与用途；秘密和凭据永不发送。

详见 [架构](references/architecture.md)、[Evidence](references/evidence-pack.md)、[Authorization](references/authorization.md)、[Completion Gate](references/completion-gate.md)。

## 11. Capital Discipline

证据够用时停搜，结论稳定时停止重复推理；工具须完成必要动作或回答具体问题，局部缺陷优先局部修复。只有相关变更、证据冲突或所需独立覆盖才追加 Review。未通过的质量门禁不能以节约为由跳过。

先保留必要测试、审查与合理修复资源，再删可选美化。能从 repo 取得答案时先取证；重大取舍、新授权及不可逆行为仍需用户决定。实际 Gate 满足后停止可选优化。

FULL 收尾或止损时简记账本，LIGHT 仅记录重要偏差，DIRECT 没有专门资本报告。Learning Signal 是带证据的待验证假设，不是自动训练或自动修改全局政策。详见 [Capital Ledger](references/capital-ledger.md)。

## 12. 一个完整案例

以下是流程示例，不是新执行的生产外审证据。

用户要求“增加交易 CSV 导出，保留筛选、排序与 UTF-8，不新增服务端持久化；提交验收前做完整真实 ChatGPT 审查”。

1. 识别目标、风险与明确外审要求，选择 FULL，为必要测试和审查保留资源。
2. Codex 读仓库、定义可观察 AC、实施导出，实际检查筛选、排序、编码与不持久化。
3. 独立内部 Reviewer 对照原始文件和输出；Codex 冻结获准材料的当前快照。
4. 有真实且获准的 ChatGPT 通道时发送、完整回读并核对当前轮；缺通道则保留本地结果，原 FULL Gate 仍 BLOCKED。
5. 对有效问题局部修复并运行相关回归；同根因持续无效则 STOP_LOSS 重评。
6. 实际 Gate 满足后提交用户验收，简记投入偏差与学习信号，不再追加无价值优化。

更多例子：[简单功能](examples/simple-feature.md)、[架构调整](examples/architecture-change.md)、[UI 审查](examples/ui-review.md)、[Skill 创建](examples/skill-build.md)、[领域组合](examples/domain-composition.md)。

## 13. 当前验证结果

当前版本：**3.0.0 Candidate / R3**。品牌迁移不改变真实验收状态：

| 项目 | 状态 |
|---|---|
| Implementation | PASS |
| Regression | PASS — 60/60 original + 6/6 capital = 66/66 |
| Packaging | PASS — 以本次候选包的独立校验记录与 SHA 为准 |
| Behavioral Evidence | MIXED |
| Real ChatGPT Review | PENDING |
| Release Gate | BLOCKED / LOCAL_REVIEW_ONLY |

改名前冻结的 A/B 主场景成绩为原版 **44/45**、R3 **42/45**；低风险两臂 **27/27**，高风险两臂 **9/9**。低风险“非缓存输入 + 输出”代理投入下降 **14.7%**，但工具项增加 **9.7%**、累计运行时间增加 **1.5%**。不能声称 v3 全面胜出、真实 ROI 或更快完成。

100 个比较观察含 12 个复用原版观察；连同被替代 R2，共 112 次唯一 evaluator 父运行，嵌套子调用未完整计量。模式扣分与来源不足均保留。历史评测、Critic、旧 SHA 与原始证据保持冻结；本次只验证身份、现有 66 项测试和新包，不重写或重跑 behavioral evaluator。迁移记录位于维护工作区的 `release-audit/v3-operating-partner/validation/brand-migration/`，不随 Skill 安装。

## 14. 当前限制

**Fully dynamic per-subtask Agent Dispatch remains future work.** 当前具备执行等级和有界角色分工，未实现完整动态的逐子任务 Agent Routing。

- 当前不是 Stable，真实 ChatGPT Acceptance Review 尚未完成。
- Intelligence Capital 不能精确统一计量；没有真实美元 ROI 或自动长期学习。
- A/B 是有限合成样本与显式调用，存在缓存、顺序、开发后回归及子审查来源捕获限制；没有自然触发准确性保证。
- ChatGPT 通道、内部子代理与图像可见性依赖环境；路径、哈希和摘要不能证明 Reviewer 看过图像。
- 可选 capital_state 的机器校验不能证明完整根因历史或语义充分性；测试通过不等于独审通过。
- 没有任意 reviewer 后端、Claude/Gemini adapter、CI-native reviewer、GitHub Actions 集成或永久后台服务；Windows 未做完整端到端验证。
- Review 不是正确性保证；必要授权和用户验收不能省略。详见 [Known Limitations](references/known-limitations.md)。

## 15. 怎么安装

安装 ZIP 内含 `SKILL.md` 的 **ai-operating-partner** 目录。使用宿主实际发现的位置，例如用户级 `~/.agents/skills/` 或项目级 `.agents/skills/`；部分既有环境使用 `~/.codex/skills/`。只保留一个活动安装。

macOS/Linux 全新安装示例：

```sh
# 在下载目录执行，先验证候选包。
shasum -a 256 -c SHA256SUMS
mkdir ./skill-unpack
unzip ai-operating-partner-v3.0.0-candidate-r3.zip -d ./skill-unpack
mkdir -p "$HOME/.agents/skills"
test ! -e "$HOME/.agents/skills/ai-operating-partner" && \
  cp -R ./skill-unpack/ai-operating-partner "$HOME/.agents/skills/"
```

已有安装先备份，将 Project Evolution 中列出的旧名目录移出**所有宿主发现目录**后再安装新目录；不要并装三个名称。旧名仅作历史说明，不声明 runtime aliases。本文不会自动移动全局安装。

刷新或重启宿主后确认显示 **AI Operating Partner**，通过 `$ai-operating-partner` 调用。安装不附带真实外审账号、工具或传输授权。

运行时需 Python **3.9+** 和标准库，在 Skill 根目录执行：

```sh
python3 -m unittest discover -s tests -v
python3 scripts/closed_loop.py --help
```

`scripts/closed_loop.py` 继续实现 Execution Closed Loop，V1 协议与 CLI 命令不因品牌迁移改名。高级用法见 [CLI](references/advanced-usage.md)、[Protocol](protocol.md)、[Testing](references/testing.md)。

## 16. 怎么使用

```text
使用 $ai-operating-partner 完成这个任务。
目标：为交易页面增加 CSV 导出。
要求：保留当前筛选和排序，UTF-8，不新增服务端持久化。
按价值、风险与返工成本选择投入等级，提供实际验证结果与未满足项。
```

明确选中 Skill 不会把小任务自动升级 FULL。需要真实 ChatGPT 独审时明确说明；只需本地独审时明确限定。完整审查不可用应报告缺口，不暗中降级。

组合已安装领域 Skill 的示例：

```text
Use $marketing-creative-director for domain strategy.
Use $ai-operating-partner to allocate effort and govern execution, evidence and review.
```

领域名称替换为实际可用的 Skill，不假装调用未安装能力。自动选择仍取决于宿主；没有禁用 implicit invocation，也不承诺跨环境自动触发。见 [Invocation](references/invocation.md)。

## 17. Project Evolution

AI Operating Partner was originally developed as `chatgpt-codex-closed-loop`, later renamed `closed-loop-companion`.

The original project focused on:

```text
Plan → Execute → Evidence → Review → Repair → Completion Gate
```

v3 extends that foundation with:

```text
Operating Partner Identity → Intelligence Capital → Adaptive Allocation
→ Stop Loss → Long-Term Value
```

历史命名说明原文保留，仅描述旧版本：

> Earlier internal builds used the working name `chatgpt-codex-closed-loop`.
> The public v1.0.0 skill name is `closed-loop-companion` and its invocation is `$closed-loop-companion`.

当前正式 ID 和入口只有 `ai-operating-partner` / `$ai-operating-partner`。版本保持 3.0.0 Candidate / R3，不重置、不虚构中间 v2 发布，也不把新包 SHA 当成旧评测对应的原快照。

## 18. Roadmap

当前验收待办是取得获准的真实 ChatGPT 当前快照审查；品牌更新不消除该缺口。

后续优先验证真实任务的路由边界、自然触发与更平衡的资源对照，补足子审查来源捕获。完整动态逐子任务分派仍为 future work，只在新增证据证明价值时推进。

Apache License 2.0；见 [LICENSE](LICENSE)、[Contributing](CONTRIBUTING.md)、[Security](SECURITY.md) 与 [Publishing](PUBLISHING.md)。

> AI Operating Partner is an independent open-source project.
> It is not affiliated with, endorsed by, or sponsored by OpenAI.
> ChatGPT, Codex, and OpenAI are trademarks of OpenAI.

