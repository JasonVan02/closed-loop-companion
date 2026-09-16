# Evidence Pack

Claim is not Evidence。实施总结是导航，证据必须能独立核查。

使用 [Evidence 模板](../templates/evidence-pack.json)。必须记录 task_id、review_round、implementation_summary、changed_files（path/purpose）、acceptance_results（AC + PASS/FAIL/NOT_VERIFIED + evidence refs）、commands、raw_outputs、exit_codes、screenshots、renders、diffs、known_issues、unverified_items、deviations、material_manifest。空集合可明确 `[]`，但必需项目为空就不能 PASS。

命令记录 cwd、原样 command、开始时间、exit_code、stdout/stderr 文件路径与 SHA-256；输出无内容也保存空文件并注明真实空输出。对失败检查如实记录，不先写成功退出码。标准库脚本校验结构与引用一致性，不能证明日志是由某命令产生；保留真实 tool 结果及独立 Reviewer 对照这一来源。

AC 的证据应指向具体文件/行/截图状态，而非只有“tests passed”。测试数量不代替覆盖；相关测试缺失标 NOT_VERIFIED。每次修复运行受影响检查和必要回归；没有新变化或疑点不重复无关昂贵检查。

## Manifest

Included：文件名、用途、分类、原始字节数、完整内容哈希、对应包编号。Referenced but NOT included：实际被引用但没有发给 Reviewer 的材料及理由。Known unavailable evidence：环境或权限不能取得的证据及受影响 AC。

引用链接不意味着已提供正文。示例：02 宣称 03 有21节，但未发03，审查者只能说 MATERIAL_MISSING，不能猜03缺节。不要为了缺附件在产品里重复生成内容。

## Visual / UX

视觉 AC 需要 target/reference 与 actual screenshot/render 的成对证据，注明 desktop/mobile、viewport、必要状态、场景、相机/渲染上下文和版本。检查层级、布局、一致性、真实感与目标对齐。界面截图需来自实际产品；生成参考图不能冒充运行截图。

外审必须通过**已验证的实际图片传输与可见读取通道**收到图片。当前只含文本 prompt 的 send 工具不能证明传图，不能把本地路径、base64字符串、URL或哈希当作模型已看图。可验证可访问的图像工具/连接器时才使用；没有渠道，受影响 AC = NOT_VERIFIED，Review = BLOCKED。代码静态检查和非视觉 AC 可继续。视觉 PASS 仍需用户最终审美验收。

## 版本

输入材料冻结后计算 snapshot_id，审查请求、原始回读、内部审查和外审绑定同一产物版本。新修复创建新 round，至少发送变化材料及足够上下文；有必要材料的历史包不能无条件借用，需在本轮 manifest 证明原内容仍一致、可读取。最可靠的默认是新轮重发当前完整的小型文本快照。
