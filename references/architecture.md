# 架构与运行边界

## 三方职责

Human 决定目标、重大取舍和最终验收；ChatGPT 负责理解模糊需求、比较方案、审查架构及是否做对东西；Codex 读项目、校准 Contract、实施、验证、协调审查与修复。主代理是消息协调者，用户不充当两端搬运者。必要的范围授权是用户决策，不是手动消息交接。

本 Skill 是 Companion Skill：领域 Skill 负责业务方法，它负责执行生命周期、审查和交付。无需把营销、UI、Godot、Three.js 等领域知识复制进来；在 Contract 标记需要的领域 Skill，并按该 Skill 实施。这里判断证据够不够和下一步允许做什么。

## 内部角色与真实工具

| 角色 | 交付 | 写权限 |
|---|---|---|
| Explorer | 文件定位、现状、约束、假设核验 | 默认只读 |
| Implementer | 有界改动、理由、待验证项 | 指定文件 |
| Tester | 可复现命令、原始输出/退出码、截图或 Render | 测试及隔离输出 |
| Internal Reviewer | 独立对照 Contract、源文件、证据的 findings | 默认只读 |

FULL 至少有独立内部检查，不强制每次开四个代理。并行任务必须独立有界，避免两人同时改同文件；说明每个代理输入、输出和权限。使用当前可用的 collaboration 工具：spawn_agent、send_message、followup_task、list_agents、wait_agent。代理 ID 属于这套工具。

Codex 应用的用户任务是另一个系统：需要用户明确要求新任务才能 create_thread；等待使用 wait_threads。`agents/openai.yaml` 只定义 Skill UI 信息，不会注册四个执行代理。

真实 ChatGPT 使用应用 list/read/send 交接；新建入口按当时 schema 与用户授权。有的环境只暴露 Cloud Work 创建入口，不能推定它等同于普通 ChatGPT 会话。只有符合用户目标且当前 schema 支持才调用；确认最终返回的 kind。需要的入口缺失时可请求用户允许兼容的真实 ChatGPT 目的地或使用已授权的已有 session。不能偷偷换成 Codex 或 API 模型。

## 启动能力与覆盖状态

按 [capabilities](capabilities.md) 检查所选路线的能力与授权。真实外审不可用时可报告 LOCAL_REVIEW_ONLY，记录原 FULL Gate 为 BLOCKED。这个覆盖标签不添加 CLI/Review 枚举，也不改变原状态机的通过条件；能力恢复后沿原流程继续，只有用户明确修订验收标准才切换相应本地路线。

## 状态转换

状态必须引用实际证据，不能靠修改字符串通关。每次记录 `from,to,reason,evidence,round,timestamp`。

| 当前状态 | 可进入 | 条件 |
|---|---|---|
| DISCOVERY | CONTRACT_READY / HUMAN_DECISION_REQUIRED | AC/边界足够 / 重大产品问题 |
| CONTRACT_READY | EXECUTING | 实施在授权边界内 |
| EXECUTING | VERIFYING | 有可检查产物 |
| VERIFYING | INTERNAL_REVIEW / REPAIRING | 必需本地检查齐全 / 明确实现失败 |
| INTERNAL_REVIEW | EVIDENCE_READY / REPAIRING | 独立检查通过 / 有真实问题 |
| EVIDENCE_READY | WAITING_FOR_CHATGPT_REVIEW | FULL，授权+传输准备通过 |
| WAITING_FOR_CHATGPT_REVIEW | CHATGPT_REVIEW_FAIL / CHATGPT_REVIEW_BLOCKED / READY_FOR_USER_ACCEPTANCE | 本轮有效回复；READY 还须完整 Gate |
| CHATGPT_REVIEW_BLOCKED | EVIDENCE_READY / HUMAN_DECISION_REQUIRED | 补材料/修传输 / 授权或产品决定 |
| CHATGPT_REVIEW_FAIL | REPAIRING / EVIDENCE_READY / DIRECTION_REASSESSMENT / HUMAN_DECISION_REQUIRED | triage 分别为真实问题/反证/重复失败/越界决定 |
| REPAIRING | REVERIFYING | 修正产物 |
| REVERIFYING | INTERNAL_REVIEW / REPAIRING | 验证通过 / 仍失败 |
| EVIDENCE_READY | READY_FOR_RECHECK | 有过外审且新证据冻结 |
| READY_FOR_RECHECK | WAITING_FOR_CHATGPT_REVIEW | 新 round/request/snapshot，逐字传输核验 |
| DIRECTION_REASSESSMENT | CONTRACT_READY / REPAIRING / HUMAN_DECISION_REQUIRED | 七问和结论已记录；必要授权已取得 |
| HUMAN_DECISION_REQUIRED | 上个明确可恢复状态 | 用户回答解决对应问题；超时不算回答 |
| READY_FOR_USER_ACCEPTANCE | USER_ACCEPTED / CONTRACT_READY / REPAIRING | 用户明确接受 / 范围变更 / 用户指出真实问题 |

DIRECT 在针对性检查后应用精简 Gate；LIGHT 在内部审查后应用本地 Gate。二者可直接进入 READY；不伪称 ChatGPT PASS。任何待处理状态都可因具体重大决策进入 HUMAN_DECISION_REQUIRED。BLOCKED 仅缺材料时禁止直接修产品；同时发现独立可证明实现缺陷，要单独记录 VALID 再修，不把缺证变成缺陷。

## 审计与恢复

每任务一个 `run/`（用户工作目录内）。Contract 有版本；`session.json` 保存 canonical ID、kind、握手、授权来源、实际模型若不可见写 unknown。`rounds/R01/` 保存发送正文、Manifest、回读原始 JSON、传输检查、Review、triage、fixes、verification、status。后续轮新目录，不覆盖旧轮。元记录存当前快照之外，避免 checksum 自引用。

默认一任务一外审 session，R01/R02 在同 session；新任务、重大 scope 变化、上下文污染、用户要求新审时切新 session并重新验证授权。FRESH_FINAL_REVIEW 是可选最终新 session，不能默认产生费用或绕过创建限制。修复声明不作为结案证据，每轮独立检查当轮快照。

设计参考：[OpenAI Build skills](https://learn.chatgpt.com/docs/build-skills) 的 frontmatter 与渐进加载；本地 skill-creator 是当前安装流程依据。在线工具可变，历史实验仅证明当时该账号环境的结果。
