# Testing

在技能根目录运行 `python3 -m unittest discover -s tests -v`。测试只用临时目录和合成资料，没有网络调用、真实凭据或真实 ChatGPT 身份伪装；mock readback 是协议单元测试，不能报告成真实联调。

| 用户测试 | 验证路径 |
|---|---|
| A typo | 独立代理在临时 README 实际修正并检查分流 |
| B 复杂多文件新功能 | 独立代理使用 Skill 建 Contract / Evidence / Review 路径 |
| C 缺 AC | 独立代理区分可推导技术标准和重大业务决策 |
| D 只有 tests passed | Gate 缺 raw_output / execution_record 必须拒绝 |
| E 引用材料没发 | Manifest 缺项要求 BLOCKED，不猜文件内容 |
| F Review误报 | 独立代理对原文件取反证并准备复核，不能盲改 |
| G 未授权核心删除 | 独立代理升级 DECISION_REQUIRED |
| H 连续两轮失败 | 独立代理触发七问与 DIRECTION_REASSESSMENT |
| I 超长 | Unicode/JSON envelope全长限制、分包重组、hash及丢包测试 |
| J 旧轮 | round/request/snapshot错误拒绝 |
| K queue id | 非canonical id与非chatgpt身份拒绝 |
| L 授权 | 指定文件、目的地/用途、symlink边界负测 |
| M SECRET | 文件名和具体合成秘密内容拦截，错误不泄漏秘密值 |
| N Gate | 本地检查PASS但ChatGPTFAIL不能READY |

还覆盖：篡改包、重复身份、截断回复、空AC/重复AC、非布尔字段、未知证据引用、当前文件变化、将userMessage中的PASS冒充agentMessage、MATERIAL_COMPLETE前过早Review。

行为演练要用新上下文，只给 Skill、真实最小请求和必要原始材料；不喂预期答案。记录实际选择、产物、失败及限制。完整安装包再由独立 Reviewer 对照原始需求与原始输出审查。测试通过不代表独立审查通过。

真实联调需另保留 kind、canonical task id、round/request/snapshot、实际发送原文、工具接受/拒绝、所有分页回读、传输检查及审查/修正/复核。合成数据先测，实际项目包仅在授权范围内。按真实 tool 结果记录 accepted、busy、stale、truncated等边界，不能用模拟成功代替线上证据。

维护时改了脚本就跑受影响负测和整个轻量单元套件；改了流程就重演受影响行为情境；工具变更重新探测真实连接。运行结果和版本报告放任务审计目录，避免安装包内写不断过期的“永久通过”声明。
