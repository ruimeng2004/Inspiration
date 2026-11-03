# ICML 2027 视觉证据互补项目

## 工作原则
- 目标会议是 ICML 2027。研究方向是“视觉证据互补下的获取与学习”。
- 立题前先读 ICML 和顶会同期工作，先学习再判断。未核对的内容不得写成结论。
- 不声明新颖性，除非完成文献核对。不编造结果、日志、引用或复现状态。
- 现有历史结果只作诊断，使用前要回到原始产物。

## 固定约束
- 只做 RL 后训练，只训练 LoRA，不做 SFT，不做全参数训练。
- 不依赖外部 teacher 或 judge；工具模板可用，few-shot 只作对照。
- 基模候选：Qwen3-VL-8B。
- 计算资源：1 张 H200。单卡只是实验条件，不写成论文创新。

## 服务器
- SSH 别名：xzhanglab（读取本机 SSH config，不复制凭据）
- 代码目录：/net/csefiles/xzhanglab/rmeng41/ICML/evidence_rl_project
- 数据目录：/data/ycheng430/rmeng41/ICML
- 历史代码：/net/csefiles/xzhanglab/rmeng41/CVPR/evidence_credit（只读）

## 安全边界
- 未经用户确认，不启动 GPU 任务，不结束进程，不修改共享环境，不下载大数据。
- 启动 GPU 前必须重新检查显存和运行进程。显存不足时跳过 GPU 测试。
- 历史实验目录只读，新实验使用独立目录。
- 不修改线上工作台，除非用户明确要求。
- MedGaze、简历和 GRA 材料不属于本项目。
