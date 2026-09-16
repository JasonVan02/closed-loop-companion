---
name: closed-loop-companion
description: "Closed Loop Companion: workflow governance for complex Codex tasks. Use for acceptance criteria, evidence-based verification, independent ChatGPT review, repair/recheck, architecture-direction checks or completion gates before user acceptance. Works alongside domain skills; avoid trivial mechanical edits unless explicitly invoked. 闭环执行、独立审查与完成门禁。"
license: Apache-2.0
metadata:
  version: "1.0.0"
  skill-type: "Companion Skill"
  category: "Workflow / Quality / Review"
---

# Closed Loop Companion

为复杂任务提供执行治理、证据验证、真实 ChatGPT 独立审查、修正复核与完成门禁。领域 Skill 负责业务推理与实现方法；本 Skill 管理执行生命周期，用户保留目标、重要取舍与最终验收。metadata 下的类型、类别与版本为本包自述，不是平台分类字段。

## 调用与组合

- **Explicit：** 用户使用 `$closed-loop-companion`。明确选中本 Skill，不代表所有任务都必须 FULL；指定修 typo 可以 DIRECT。
- **Combined：** 与用户选择、当前可用的领域 Skill 联用。领域 Skill 定义业务方法，本 Skill 定义证据、审查和交付；不替代或接管领域推理，不凭示例名称假定已安装依赖。
- **Conditional：** 仅在影响、风险、模糊度、验证难度、架构后果、用户重要性或可逆性说明审查有价值时考虑自动加入；不按文件数、代码行数、有无测试机械触发。
- 识别“完整闭环、独立审查、外部审查、证据验证、完成门禁、不要自己宣布完成、修正后复核、正式验收”等真实意图。更多英文/中文表达和边界见 [invocation](references/invocation.md)。单独“检查一下”不强制外审，“formal verification”不构成本 Skill 能做形式化证明的承诺。

## 先分流

记录模式及一句理由，优先判断影响、风险与验证价值。修改3个文件、100行代码或存在测试都不足以单独升级 FULL。

| 模式 | 适用 | 路径 |
|---|---|---|
| FULL | 有明显行为影响的新功能、新 Skill、架构/数据模型、复杂 Bug、高保真视觉、正式复杂交付、用户明确要求完整独立或 ChatGPT 审查 | Contract → 实施 → 验证 → 独立内部审查 → Evidence → 真实 ChatGPT → triage → 修正/补证 → 复核 |
| LIGHT | 中等且局部、风险有限、不改核心架构、可充分本地验证 | Contract Lite → 实施 → 验证 → 独立内部审查 → 报告；发现更大影响升 FULL |
| DIRECT | typo、无行为变化格式调整、极低风险机械修改 | 实施 → 针对改动检查 → 报告 |

普通“检查一下”不自动等于外部审查；用户明确要求 Review 时至少执行该检查，明确独立/ChatGPT 审查时默认 FULL；用户明确只要本地独立审查时按其范围执行并说明未做外审。不得为绕开外审失败而降级。

## 启动时检查能力

选定路线后、承诺外审前读取 [capabilities](references/capabilities.md)。确认当前工具、可读写的真实 ChatGPT 目的地、内部独立审查条件、读回/长度/图像能力与授权。不能继承开发者的账号、会话、20k读取行为或 Subagent 能力。

FULL 所需真实 ChatGPT 能力不可用时，继续有价值且已授权的本地工作，报告 `LOCAL_REVIEW_ONLY` 及原 FULL Gate 未达成。它是审查覆盖说明，不是新 CLI 模式或 Review JSON status；真实外审要求仍为 BLOCKED，不生成替代 PASS。用户明确修改验收标准后才记录新的标准及本地路线，不能伪称原 FULL 已通过。

## 执行

1. **Discovery / Contract。** 先读真实项目、适用 AGENTS.md 和已有证据；区分事实与假设。读取 [task-contract](references/task-contract.md)，建立可观察 AC、范围、非目标和所需证据。模糊产品方向可交 ChatGPT 做方案比较；重大取舍由用户决定。常规技术 AC 自行推导并标记来源。
2. **实施与验证。** 可用时按 [architecture](references/architecture.md) 分派有界 Explorer / Implementer / Tester / Internal Reviewer；独立 Reviewer 不复用实现者结论。没有独立代理则如实记录限制。领域实现仍由领域 Skill 决定。
3. **收集证据。** LIGHT/FULL 读取 [evidence-pack](references/evidence-pack.md)，保留实际命令、原始输出、退出码、diff 与所需截图/Render。**Claim is not Evidence.** 引用了但没交付的文件必须列入 Manifest 缺项。
4. **FULL 外审。** 发送前读取 [authorization](references/authorization.md)、[handoff protocol](references/chatgpt-handoff-protocol.md)、[review schema](references/review-schema.md)。使用当前真实工具能力，先确认授权范围与 canonical `kind=chatgpt`。缺少工具或权限时保存状态，按能力规则说明 LOCAL_REVIEW_ONLY 与外审 BLOCKED；不拿子代理冒充 ChatGPT，不扩大上传授权。
5. **Triage / 修正。** 每条 finding 按 [review schema](references/review-schema.md) 分类 VALID / FALSE_POSITIVE / MATERIAL_MISSING / DECISION_REQUIRED。真实问题修；反证提交复核；缺材料补证；越界取舍交用户。不要机械服从 Reviewer。
6. **防止错误补丁。** 同 AC 连续两轮 FAIL、同类回归或反复基础方向异议，立即读取 [anti-patch-loop](references/anti-patch-loop.md)，进入 DIRECTION_REASSESSMENT，暂停继续 Patch。
7. **复核与验收。** 每轮使用新编号、请求标记和固定快照。产物变化使旧 PASS 失效。使用 [completion gate](references/completion-gate.md) 判断状态，按 [final report](templates/final-report.md) 交付实际结果、证据、偏差和未验证项。

## 不可省略的规则

- accepted 不是 completed；idle 不是本轮已回复。回读核对 task / round / request / snapshot 及原始消息完整性。
- 私有材料授权绑定具体材料、目的地和用途；文件 A 的授权不扩展为仓库。SECRET 和凭据永不发送。
- 缺少必需材料时外审 BLOCKED。图片路径、摘要、哈希都不能证明 Reviewer 看到了图像。
- FULL 只有实现完成、AC 与必需证据通过、独立内部审查通过、当前真实 ChatGPT PASS、无阻塞问题或待定方向，才是 `READY_FOR_USER_ACCEPTANCE`。
- `USER_ACCEPTED` 只来自用户明确验收；自动化脚本不得替用户做该决定。
- 常规 bug、测试失败、路径错误自行修；只为产品取舍、授权扩大、不可逆操作、证据无法裁决的事实冲突及主观验收打断用户。

## 工具与维护

用户入口见 [README](README.md)；确定性 CLI 使用 [advanced usage](references/advanced-usage.md)；测试与维护见 [testing](references/testing.md)。恢复执行先读取该任务审计目录的 Contract、session、当前轮 Manifest、发送记录和最后状态，重新核验当前文件哈希；不要重发不确定已接受的消息。

本 Skill 不创建永久后台监听。工具、账号、长度、图片能力边界见 [known limitations](references/known-limitations.md)。修改 Skill 自身仅做一层 dogfood，不递归创建审查体系。
