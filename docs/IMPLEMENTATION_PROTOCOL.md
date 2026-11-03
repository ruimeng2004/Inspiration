# 实现规格摘要

完整版本：https://claude.ai/artifact/P7MMjiDNah7TXtpknEG5BF

## 实验顺序
| 编号 | 问题 | 通过后才进入 |
| --- | --- | --- |
| X0 | 框架能否端到端运行 | 工具调用测试 |
| X1 | 无 SFT 能否调用工具 | 重放测试 |
| X2 | prefix 或 evidence_only 重放是否可靠 | 结构诊断 |
| X3 | 互补、冗余、无关结构是否足够 | 证据组测试 |
| X4 | 证据组是否优于打乱对照和现有信用 | 查询分配 |
| X5 | Gittins、Neyman、UCB 等是否减少查询 | RL 基线 |
| X6 | LoRA GRPO 基线和吞吐 | 完整比较 |
| X7 | Full 是否优于 GRPO、TRACE、CounterCredit 式基线 | 论文主结果 |

## 核心方法
1. 只重组已获取观察，不读取未付费候选。
2. 用 null patch 计算全观察和留一效用。
3. 用逆向删除得到近似最小证据组。
4. 组内调用给正信用，组外调用付成本，有害观察额外惩罚。
5. 过程信用限幅，保持结果优先。
6. 所有训练比较匹配有效更新量，并设打乱对照。

## 代码现状
已实现内容见 `code/evidence_rl_project`。`backends/hf_qwen.py`、数据适配器、GRPO 和 LoRA 训练均未完成。
