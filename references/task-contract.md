# Task Contract

FULL 使用 [JSON 模板](../templates/task-contract.json)。字段必须出现：task_id、title、goal、context、requirements、constraints、non_goals、acceptance_criteria、required_evidence、known_risks、open_decisions、review_mode、authorized_material_scope。

每 AC 包含稳定 id、可观察 criterion、verification 方法。不要使用“高质量”“完美”作为唯一条件。技术条件可从目标和项目推导，标注 `origin: inferred` 与理由；目标不清且涉及业务选择时列 open_decisions，给 ChatGPT 比较方案，交 Human 定重要取舍。

示例：导出功能的技术 AC 是“空列表导出有表头、中文 UTF-8 正确、无越权数据”；“默认导出哪些用户数据、价格哪个方案”可能涉及产品决策，不能假定。用户的要求不是被 AC 限制的最大集合，审查还应回看原要求是否遗漏；发现遗漏补充 Contract 版本并重审影响。

LIGHT 的 Contract Lite 至少保留 task_id、goal、constraints、non_goals、AC、required_evidence、review_mode。DIRECT 可在工作记录内简记目标、范围和检查。模式变更必须记录理由，不能仅因工具失败降级。

`authorized_material_scope` 不是一段“可上传”的空泛文字；绑定具体文件/明确目录下材料种类、ChatGPT 目的地、用途、用户授权证据，按 [authorization](authorization.md) 展开精确清单。`minor_findings_block` 默认 true；合同明确要求细节必须通过时设 true。
