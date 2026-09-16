# Review 与 Triage

真实 ChatGPT 返回一个 JSON Review。人可读 prose 可保留为原始证据，但不能在未校正结构前自动打开 Gate。字段名以脚本接口说明为准；语义必须包含：

```json
{
  "message_type": "REVIEW_RESULT", "task_id": "T-001", "round": 1, "request_id": "unique-per-round",
  "snapshot_id": "current-manifest-sha256", "status": "BLOCKED",
  "summary": "缺少必需材料",
  "findings": [], "missing_materials": ["test-output.txt"],
  "acceptance_criteria": [{"id":"AC01","status":"NOT_VERIFIED","evidence":[]}],
  "architecture_direction": "CONTINUE", "ready_for_recheck": true
}
```

finding 全字段：id、severity、category、claim、evidence、reasoning、required_change、verification_method。severity 见 [severity](severity.md)。状态只取 PASS / FAIL / BLOCKED。AC 状态只取 PASS / FAIL / NOT_VERIFIED；必须覆盖 Contract 每个 AC，不能空集合或漏项后 PASS。

需要的材料不全、缺包、截断、无法核对哈希时总状态 BLOCKED；可以同时记录从已得材料证明的缺陷，不能假装全量审查 FAIL 已完成。材料完整且有阻塞缺陷为 FAIL；所有必需 AC 已证实、无阻塞缺陷才 PASS。`architecture_direction` 只取 CONTINUE / REWORK / STOP_AND_RETHINK；后两者阻塞 READY。

架构审查不只找 bug，还回答：方向根本上正确吗？补偿性复杂度是否增加？是否保留项目边界？应继续、重构还是替换？不把历史赞同和实现者“已修复”当证据。

## Triage 逐条记录

| 分类 | 证据与下一步 |
|---|---|
| VALID | 原文/代码/复现证明问题；在范围内修复，运行针对性和必要回归检查，提交新快照 |
| FALSE_POSITIVE | 提供直接反证及定位，解释为何冲突，提交 ChatGPT 重新判断；本地分类不等于 Reviewer 已撤回 |
| MATERIAL_MISSING | 标出缺的具体材料及受影响 AC，补材料重新审；不为缺证盲改产品 |
| DECISION_REQUIRED | 描述超出边界的操作、方案影响和必须由 Human 决定的取舍；等待回答期间做独立工作 |

记录 `finding_id,classification,evidence,action,verification,status`；每条都处置，不偷偷忽略。反证仍争议且不能由证据裁决，升级用户。Reviewer 要求删除未授权核心能力时不得执行，属于 DECISION_REQUIRED。

同一个 AC 连续两轮失败或方向反复被否定，优先进入 [anti-patch-loop](anti-patch-loop.md)，不得无界修补。
