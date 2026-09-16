# Capability detection / 环境能力检查

在启动时按选定路线检查实际能力，不能把安装 Skill 当成安装了外审工具。这是协调代理执行的检查指令，不是新增 CLI 命令、后端或账号连接器。

| 能力 | 要核实什么 | 不可用时 |
|---|---|---|
| Local execution | 当前文件访问、执行检查和记录原始证据的能力 | 列出受影响 AC，不能自报实施验证完成 |
| Independent internal review | 独立代理或合同认可的独立审查来源，能看原始产物 | 继续可做的检查；不能自审后填写内部独立 PASS |
| Real ChatGPT handoff | 当前工具 schema 支持目标类型；可访问的正式 ID，读取确认 kind=chatgpt；有准确 send/read 能力 | 保持原 FULL 外审要求未满足，报告 LOCAL_REVIEW_ONLY |
| Integrity and timing | 当前每条/每页读取限制、分页、截断标记、正确回复与时间顺序 | 减小材料粒度或读取分页，仍无法证明完整就 BLOCKED |
| Visual evidence | 对方实际可看到图像而非本地路径；参考图、viewport与当前渲染齐全 | 视觉 AC 未验证，不能用 build/test 替代 |
| Authorization | 具体材料、目的地、用途仍在用户授权范围内 | 保留本地工作；需要外发时请求缺少的具体授权 |

先检查当前提供的工具说明及可读状态，不探查凭据来“证明登录”。能力或限制未知就记录 unknown，不能用上一次的固定 task ID、用户路径、模型或账号假设填空。最小握手/往返测试只能在任务允许的目的地与范围内进行；不要求用户反复批准已经明确授权的动作。

若已有符合本任务要求且授权可用的真实 ChatGPT session，可复用并重新核对身份。需要新建时遵守当前工具对用户授权与目标类型的要求；缺少普通 ChatGPT 创建入口时，不自动替换为云端 Work、Codex task、内部代理或 API 模型。参考 [handoff protocol](chatgpt-handoff-protocol.md)。

## 两条路径

**能力齐全：** 使用 FULL 原流程，独立内部审查、材料完整核验、真实外审、triage、修正复核和 Completion Gate 缺一不可。

**能力不齐：** 继续有价值且已授权的本地实施/验证；如有独立内部审查则如实保留。报告示例：

```text
Requested route: FULL
Review coverage: LOCAL_REVIEW_ONLY
External review: UNAVAILABLE (state the observed missing capability)
Original FULL completion gate: BLOCKED
Independent real ChatGPT review unavailable in this environment.
READY_FOR_USER_ACCEPTANCE requiring external review was not reached.
```

LOCAL_REVIEW_ONLY 表示能力受限时的审查覆盖，不表示本地工作全部通过，也不是 `review_mode` 新值或 `REVIEW_RESULT.status` 新值。保持 V1 的 FULL/LIGHT/DIRECT 与 PASS/FAIL/BLOCKED 枚举不变，原 CLI 不会替没有外审的 FULL 开门。缺内部独立审查、缺图或缺必需本地证据，也须逐项报告。

只有用户明确允许改变验收标准，才能修订 Contract 并执行适当的本地 Gate；保留原标准、用户决定和具体未做的外审，不能声称通过原 FULL。若只是工具恢复，沿原 Contract 继续外审即可。已经收到 FAIL、材料上传被拒、回复旧轮/缺包，都不能通过换成 LOCAL_REVIEW_ONLY 擦掉问题或绕过审批。

## 保存与恢复

在当前任务的项目审计目录记录能力检查时间、实测结果、所用工具、授权边界、缺项和恢复条件；不要写进发布包。未知发送结果先读回确认，避免盲重发；按当前材料规模设定有界重试与等待成本。外部失败时继续可独立完成的本地工作，结束任务不意味着后台仍在运行。
