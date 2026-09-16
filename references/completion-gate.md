# Completion Gate

FULL 必须同时满足：implementation_complete=true；required_evidence_complete=true；全部合同 AC 有对应充分证据并 PASS；独立内部审查 PASS；真实 ChatGPT 当前轮/请求/快照 PASS；CRITICAL=0、MAJOR=0、合同要求阻塞的 MINOR=0；没有未解决产品决策/授权/方向重评；architecture_direction=CONTINUE。收到全部材料的时间必须早于被接纳的 MATERIAL_COMPLETE/Review；事后补齐材料不能使较早的PASS有效。

任何状态字符串、自报布尔、测试数量或 Review 正面语气都不是单独证明。先核验原始证据与传输，使用 CLI 检查结构、哈希、AC 和 Review 一致性，再由主代理对未被脚本判定的语义条件负责。保留两种结论，不把脚本结果当形式化证明。

缺必需证据 → BLOCKED；已证实实现问题 → FAIL；旧轮/错任务/旧快照/截断回复 → 无有效当前 Review，Gate 保持关闭。文件发生变动必须重新生成快照、验证受影响内容并复核。不要把 install path 或报告更新时间变化混入产品内容后无意义循环；产品快照与只追加的审计元数据分开。

LIGHT 不要求 ChatGPT，但须相关验证与独立内部审查；DIRECT 只需对应低风险改动的实查。两者报告模式和未做的外部审查，不填写伪造 PASS。用户明确要求外审时不得使用 LIGHT 的简化 Gate。

通过后按实际路线说明完成了哪些检查，状态仅为 **READY_FOR_USER_ACCEPTANCE**。DIRECT 说明针对性检查结果，不宣称做过独立审查；LIGHT 说明本地验证及实际完成的内部独立审查，并标明未做外审；FULL 才可在全部条件满足后说明工程执行、内部独立审查与真实 ChatGPT 外审均已通过。

只有用户明确表示验收了对应交付版本，才记录 USER_ACCEPTED，并保存原话/时间/版本。用户只是“了解”、同意授权或允许继续，不是验收。没有用户验收证据，脚本不得输出 USER_ACCEPTED。

## 能力不足与用户修订标准

按 [capabilities](capabilities.md) 报告 LOCAL_REVIEW_ONLY 只说明可用审查覆盖。它不能替代真实 ChatGPT PASS，也不会改变 CLI Gate；原 FULL 标准仍未达到 READY_FOR_USER_ACCEPTANCE。用户明确同意降低外审要求时，记录修订 Contract、原要求未满足以及改用的本地 Gate，不宣称原 FULL 通过。单纯授权继续、缺工具、超时或外审失败都不是修订标准的同意。
