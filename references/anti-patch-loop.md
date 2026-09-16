# Anti-Patch Loop

以下任一信号触发 `DIRECTION_REASSESSMENT`，暂停继续 patch：同 AC 连续两轮 FAIL；同区域多次修正仍无改善；修复引入同类回归；Reviewer 重复否定基本方法；复杂度提高而质量不改善；为保留旧实现持续增加特殊 case；视觉/架构问题反复靠局部调整遮盖。

从审计记录判断，不只依赖措辞。`BLOCKED` 因缺材料不是执行 FAIL，不计入同 AC 两轮失败；但持续缺证仍需改证据方法。新轮编号不能重置同一个问题的历史。

写入 direction-reassessment.md，逐题回答：

1. 原目标是什么？
2. 当前实现方法是什么？
3. 为什么连续失败？列出两轮实际证据。
4. 是执行问题还是方向问题？哪些证据能区分？
5. 是否应回退，影响什么？
6. 是否应该换实现方法，哪种验证可以先比较？
7. 是否应该废弃当前方案，代价和授权范围如何？

结论只取 CONTINUE_CURRENT_DIRECTION / REFACTOR_DIRECTION / REPLACE_APPROACH / ROLLBACK / HUMAN_DECISION_REQUIRED。继续原方向需给新证据或可证伪的新验证，不能只是“再试一次”。重构/替换在既定可逆范围内可自主做；重大架构路线、范围和成本取舍交用户。ROLLBACK 不构成删除或不可逆操作的自动许可。

保存决定、依据、影响的 AC、下一步验证和授权，再恢复状态。下轮 Reviewer 同时审方向决定和实际变化，不只是看局部补丁。
