# Recheck Request

Task {task_id}, round {round}, request {request_id}, snapshot {snapshot_id}。

Re-review this round independently. Do not assume previous findings are resolved merely because Codex claims they are resolved. Verify against current evidence.

逐项提供 previous finding → triage → change/counterevidence/supplement → raw verification → current status；完整新 Manifest 在本轮包内。
仍有疑点直接指出，缺材料返回 BLOCKED，方向错误允许 STOP_AND_RETHINK。完成材料屏障后按统一 Review JSON 返回。
