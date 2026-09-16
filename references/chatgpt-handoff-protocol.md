# CHATGPT_CODEX_CLOSED_LOOP_V1

目录：身份与会话 → 授权与打包 → 发送与回读 → 完整屏障 → Review / Recheck → 失败与恢复。

## 1. 身份与会话

先读取当前工具 schema，不照抄旧参数。以下是协调步骤，不是独立 Python SDK：

1. 已有本任务已授权 session：list/read 再确认正式 ID 和 kind=chatgpt。没有 session 时，只有用户明确允许新建任务且工具支持对应 ChatGPT 目的地才 create。当前仅支持 Cloud Work 而用户要普通 ChatGPT 时不得静默替换。
2. 创建可能返回 `local-chatgpt:...` 或 clientThreadId；保留排队记录，通过 list_threads 找到正式候选，读取内容与本次随机握手标记核对。只凭相似标题不能认定目标。以工具返回的真实标题称呼任务。
3. 确认正式 ID、kind=chatgpt、握手 ACK 再绑定授权目的地。queue id、Codex task、内部代理都不能充当真实 ChatGPT session。
4. 默认一个 task_id 使用一个 session；新 scope / 污染 / 用户新审按 architecture 中策略切换。

ChatGPT 使用 list_threads 刷新和 read_thread 读取，**不用 wait_threads**。Codex app tasks 才用 wait_threads；collaboration subagents 用 collaboration 等待/消息。

## 2. 冻结与分包

发送前执行 authorization 检查并生成 Bundle。每轮 `review_round` 在机器记录中为正整数，展示可写 R01；review 的 `round` 必须同值。每轮 request_id 唯一且不可挪给变更后内容。

消息字段至少：

```text
PROTOCOL: CHATGPT_CODEX_CLOSED_LOOP_V1
TASK_ID: 任务标识
REVIEW_ROUND: 正整数
MESSAGE_TYPE: 类型
PACK: 序号/总数
MATERIAL: 材料标识
CHECKSUM: 原始 UTF-8 内容 SHA-256
```

实际采用 JSON envelope，并包含 request_id、snapshot_id、source_file、material_type、content_length、content。以 `prepare` 输出的完整原样消息为准；不要手写第二套 envelope 或发送前增删正文。

类型：REVIEW_REQUEST、MATERIAL_PACK、MATERIAL_COMPLETE、REVIEW_RESULT、RECHECK_REQUEST、DECISION_REQUEST；接收确认可用 ACK（扩展）。类型不是工具 API，仅为消息数据。

限制是**整个序列化消息 ≤16,000 UTF-16 units**，包括协议、路径、JSON 转义和正文；默认不改为接近20k。源文件按原始 UTF-8 字节 hash，保留原换行，不做 Unicode normalization；分片按 code point 边界。不得用 codepoint 长度替代 UTF-16 包长。Manifest 声明完整文件与包哈希、字节数和包编号；快照使用稳定规范 JSON 的 SHA-256，避免把 snapshot 字段本身循环包含。

源文件、目的地或用途变化需要重新预检；发送从冻结 Bundle 读取文本，不重新拼接源文件。发送前核对当前 scope仍授权、Bundle 未改；源文件变化后不得把旧 Bundle 当最终版本。

## 3. 发送、去重、回读

先发 REVIEW_REQUEST（或 RECHECK_REQUEST）说明只收材料，MATERIAL_COMPLETE 前不结论。逐条发送 MATERIAL_PACK，保存请求与真实 tool 结果。accepted 只表示工具接受；没有当前响应证据就不继续认为已审核。

包身份为 task_id + round + request_id + snapshot_id + pack index。相同身份相同正文重复只算一包；同身份不同正文立即 BLOCKED。不得因 ACK 超时盲目重发已接受的完整 Review。先刷新列表、按当前标记读回，确认实际缺失再补；无法判明则保留不确定状态。若工具明确返回 `already responding` 且 isError=true，记录该包未被接受，待当前回复结束再补该包；不要立即并发发送后续包。

读取使用当前允许的 maxOutputCharsPerItem（历史实测20,000），注意 turnLimit/分页；保存完整原始 tool JSON。查找与请求对应的 turn，不能按最新 title/idle猜。核对每个 userMessage原文与发送文本逐字相同、kind、正式ID、task/round/request/snapshot及未截断标识。不能让模型回显一个 hash 就当本地比对通过。

应用列表可能缓存；刷新 list 后再 read 是历史有效恢复方法，不是永久保证。每次等待不超过60秒；建议5、10、20、30秒退避，单条消息的确认最多10次读取或5分钟。整个评审批次应在Contract记录适合材料量的时间/成本上限，不能把每包额度叠加成无限运行。超过边界记录 BLOCKED/待恢复及缺的具体回复，不无限轮询。继续其他独立工作，真实后台续跑只有用户请求且平台支持时另设自动化。

## 4. 完整屏障

所有材料包回读一致后，发送 MATERIAL_COMPLETE，附 Included / Referenced-but-NOT-included / Unavailable清单、总包数、当前标记和传输核验结果，要求 Reviewer 列出收到的包ID与缺项。所有**必需**材料收到且当前原文核验通过才开始正式 Review。V1 的 COMPLETE 明确要求“确认完整后审核”，正式Review必须来自该屏障对应回复；单独另发任意Review开始消息不受当前Gate支持。

缺包、hash冲突、被截断、缺引用正文、缺图、缺原始测试输出 → BLOCKED。摘要和路径不能填补缺项。已知缺陷可记录，但不伪称完整审查。若必需材料太多超过可确认上下文，拆成明确 AC 子范围评审，再由最终审查确认全体 AC 及接口；不能把局部 PASS 自动加和成整体 PASS。

## 5. Review 与 Recheck

要求 [统一 Review](review-schema.md)，绑定当轮标记与 manifest snapshot；只有与当前请求对应的**真实 assistantMessage**才能作为 Review 来源。保留来源 turn/message ID 和原始读取；本地编辑过的 Review、用户消息里的 PASS、子代理 PASS 都不是 ChatGPT 外审证明。校验器可识别来源结构与一致性，无法防止人伪造整个本地证据文件，最终仍需对照真实工具记录。

每轮 Recheck 请求都包含：

> Re-review this round independently. Do not assume previous findings are resolved merely because Codex claims they are resolved. Verify against current evidence.

提交原 findings、逐项 triage、变更/反证/补证、实际新检查、未验证项及当前完整 Manifest。不要告诉 Reviewer 必须 PASS。Review格式不符时可先发格式说明，再原样重试同一 MATERIAL_COMPLETE 以取得绑定完整屏障的正式回复；记录重试和原因，不把格式修复伪装成新产品验证。只有材料未变、先前包完整且时间早于该屏障时可复用原轮；修改材料或审查范围就建新轮。

## 6. 恢复与拒绝

先读取 run 元数据，重验当前版本、授权和来源；分辨已发送未确认、已收到但旧轮、真正缺材料三类。未知状态不直接跳到 READY。审批拒绝必须报告来源和理由，只有批准的安全调整或新授权可重试，禁止换工具绕过。用户操作仅用于范围与关键决策，不要求人工搬运整段材料。
