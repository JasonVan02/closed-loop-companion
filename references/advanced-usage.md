# Advanced usage / CLI 与交接记录

以下是高级用户和协调代理的参考。普通使用从 [README](../README.md) 的 Quick Start 开始。
在 Skill 根目录运行命令，示例绝对路径需替换成当前任务的真实路径。

## FULL 运行路径

1. 在项目可写目录建独立 `run/`，复制并填写 [Contract](../templates/task-contract.json)、[Evidence](../templates/evidence-pack.json)。证据必须来自实际执行。
2. 定义精确授权并填写 `prepare.json`。原样工具消息来自 Bundle，不手工复制巨型文本。
3. `prepare` 成功后发送 request 和所有材料包，逐个等待当前包回读，收集完整 `read_thread` 原始结果。
4. `verify-readback --materials-only` 通过后才发送 Bundle 最后一条 MATERIAL_COMPLETE。读取真实对应回复，保存 Review JSON。
5. `validate-review` 检查格式和一致性；按真实 findings triage、修正/补证，再冻结新轮。
6. `gate` CLI只支持FULL。当前证据、独立内部 Review、真实外审齐全后使用 `gate`；其结果仍需要主代理检查证据语义充分性，并交用户验收。

```sh
python3 scripts/closed_loop.py prepare --spec /absolute/run/prepare.json --out /absolute/run/bundle.json
python3 scripts/closed_loop.py verify-readback --bundle /absolute/run/bundle.json --readback /absolute/run/readback.json --materials-only --out /absolute/run/transport-before-complete.json
python3 scripts/closed_loop.py verify-readback --bundle /absolute/run/bundle.json --readback /absolute/run/readback.json --out /absolute/run/transport.json
python3 scripts/closed_loop.py validate-review --bundle /absolute/run/bundle.json --contract /absolute/run/contract.json --review /absolute/run/review.json --out /absolute/run/review-validation.json
python3 scripts/closed_loop.py gate --spec /absolute/run/gate.json --out /absolute/run/gate-result.json
```

退出码0仅表示该项机械检查通过；`VALID`可能对应 FAIL Review。错误退出码2、status BLOCKED 会给原因，不能忽略后继续通关。不要覆盖已审旧轮，新的材料使用新目录/round/request。

### prepare.json

```json
{
  "task_id":"T-001", "review_round":1, "request_id":"T-001-R01-unique",
  "destination":"verified-canonical-chatgpt-id", "purpose":"本任务独立审查",
  "files":[{"path":"/absolute/run/contract.json","material_type":"task_contract","classification":"PROJECT_INTERNAL"}],
  "authorization":{
    "approved":true,"destination":"verified-canonical-chatgpt-id","purpose":"本任务独立审查",
    "files":["/absolute/run/contract.json"],"approval_evidence":"用户已明确授权的原话与记录定位"
  },
  "referenced_but_not_included":[], "unavailable_evidence":[],
  "review_instructions":"附本轮范围、AC和统一Review schema；材料齐全后独立检查。"
}
```

文件列表应包含实际产物、Contract、Evidence和所有必需原始证据。示例只有一个文件用于展示结构，不是完整审查包。缺项对象用 `name,reason`；V1 对显式缺项保守阻塞，纯可选参考应在清晰标注的说明中与必需材料区分。

Bundle 包含 `messages` 原文数组、manifest、snapshot_id、授权、最大消息长度。每条都须原样发送。先本地比对，不能让 Reviewer 手算哈希。

### readback.json / review.json

`readback.json` 为 `{"pages":[完整的 read_thread 工具结果, 其他分页结果]}`。可直接存工具原始 `{content:[...],isError:false}` 对象；不要删掉 userMessage、agentMessage、turn status、kind/id 或截断字段。

Review 字段见 [review schema](review-schema.md)，`round` 用整数，`message_type` 为 REVIEW_RESULT；finding 和 AC 的 `evidence` 均为非空引用列表（NOT_VERIFIED AC 可以空）。当前轮 PASS 的 ready_for_recheck=false。

### Evidence 与 Gate

Evidence除了交接字段，还需 `implementation_complete`、`artifacts`、`required_evidence_results`、`open_decisions`。每个 artifact 为 `id,path,sha256`；真实空输出另标 `kind:raw_output`，路径在 run_root 内，不能 symlink 逃逸。每条必需 command 为 `id,command,cwd,exit_code,raw_output,execution_record`；最后两项是 artifact ID。

execution_record 是实际运行记录的 JSON，字段 `command,cwd,exit_code,output_sha256`；同时留存原始工具结果供独立核查。AC 和 required_evidence_results 的 evidence 引用 artifact/command ID。历史失败留在旧轮或诊断记录，当前必需命令必须通过。

独立内部审查 JSON 为 `role:internal_reviewer,reviewer_id,review,raw_transcript:{path,sha256},review_message`。review 使用同一 schema 绑定当前快照；review_message必须原样存在于独立代理记录。外审则从 MATERIAL_COMPLETE 对应 completed turn 的真实 agentMessage匹配，不能手写一个 PASS。

```json
{
  "run_root":"/absolute/run",
  "bundle":"/absolute/run/bundle.json", "contract":"/absolute/run/contract.json",
  "evidence":"/absolute/run/evidence.json", "internal_review":"/absolute/run/internal-review.json",
  "implementer_id":"actual-implementer-id", "direction_reassessment_pending":false,
  "readback":"/absolute/run/readback.json", "chatgpt_review":"/absolute/run/review.json"
}
```

运行日志和审查来源来自实际工具结果；脚本不能鉴定人为伪造的本地记录，不能证明测试足够。LIGHT / DIRECT 按 [精简 Gate](completion-gate.md)保留实际证据，不为使用这个外审辅助器而强制建立云端材料包。
