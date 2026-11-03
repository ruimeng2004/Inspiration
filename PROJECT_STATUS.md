# 项目状态

更新日期：2026-11-02（美东时间）

## 当前判断
主线候选是“无标注证据组信用”：没有金证据、路径标注或外部 judge 时，从 Agent 已获取的观察中估计证据组贡献，并用于 RL 后训练。

这还不是定稿立题。必须先证明证据组归因优于打乱对照，再比较 TRACE 和 CounterCredit 式信用，最后再做训练。

工作标题：Learning Evidence Sets Without Evidence Labels: Counterfactual Credit for Visual Agents。

## 已完成
- 完成同期文献调研第一轮和 TRACE、PBSD 精读。
- 完成实现规格与协议 v0.1。
- 完成 CPU 框架：解析器、预算环境、TRACE 基线、留一、证据组、打乱对照、Gittins、Neyman 式分配、日志和只读 GPU 检查。
- 本地通过 11 项单元测试和 CPU 冒烟测试，全部只使用合成数据。
- 完成公式层合成模拟，结果在 simulation/results.json。
- 2026-11-02 部署到 xzhanglab。代码在 `/net/csefiles/xzhanglab/rmeng41/ICML/evidence_rl_project`，`runs/` 是指向 `/data/ycheng430/rmeng41/ICML/runs` 的软链接。`deploy.sh` 已改为先切到脚本所在目录，并创建这个软链接。
- 服务器上 11 项单元测试和 CPU 冒烟测试通过（系统 Python 3.12.3，只用标准库），产物在 `runs/cpu_smoke_1793673905/`。
- 只读 GPU 检查：1 张 H200 NVL（143771 MiB）。检查时已用 87284 MiB、空闲 55883 MiB、利用率 100%，显存被 3 个其他用户的进程占用。结果在 `runs/gpu_check.json`。未启动 GPU 任务。
- 只读核对服务器环境：系统 Python 没有 torch。`/data/ycheng430/rmeng41/envs/` 下有 `m1b_trl024`（torch 2.6.0+cu124、transformers 4.57.1、peft 0.14.0、trl 0.24.0、vllm 0.8.5、flash-attn 2.7.4）和 `vllm0110`（torch 2.8.0、transformers 4.57.1、vllm 0.11.0，没有 trl）。`/data/ycheng430/rmeng41/models/` 下有 Qwen3-VL-4B-Instruct，没有 Qwen3-VL-8B。

## 未完成
- 未核对现有 evidence_credit 代码。
- 未验证现有环境能否加载 Qwen3-VL，需要实际 import。只查了 `models/`，不确定实验室有没有 Qwen3-VL-8B 共享副本。
- 未下载 SlideVQA 或 LongDocURL，未写数据适配器。
- 未接入 Qwen3-VL-8B，未实现 GRPO + LoRA。
- 未运行任何真实模型实验。

## 服务器注意事项
- `/net/csefiles/xzhanglab` 已用 100%（剩约 9.6G），只放代码。runs、缓存、checkpoint 和新环境都放 `/data`。
- HOME 剩约 27G，HF_HOME 未设置。下载模型前先把缓存指到 `/data`。
- H200 与其他用户共享。`scripts/check_gpu.py` 只看空闲显存，启动 GPU 前还要看利用率和他人进程。共享卡上测的吞吐不能直接当作单卡成本。
- 历史目录 `CVPR/evidence_credit` 权限上可写，只读靠约定。

## 文献待办
- 打开 AXPO 的 arXiv 原文，并读 VISOR、LAT、VRAG-RL 的方法部分。
- 精读 RVCO、OVC 和视频 Agent 信用研究。
- 系统检查 NeurIPS 2026、ICLR 2027、AAAI 2027 录用列表。
- 核对 SCORE 的会议状态。当前按 arXiv 预印本引用。

## 下一步
1. 核对现有 evidence_credit，优先复用工具环境。
2. 决定 Qwen3-VL-8B 的来源（共享副本，或下载约 17 GB 到 `/data`）和 Python 环境方案（原样复用或新建）。两者都需用户确认。
3. 准备 SlideVQA 多跳题，核对许可、划分和金页面字段。
4. 接入 Qwen3-VL-8B，先跑工具调用和只读测试。
5. 用真实轨迹做重放信度实验，比较打乱对照、TRACE K=1/2/3、CounterCredit 式和留一信用。

## 决策记录
- 不收窄为信用分配或前后动作互补；它们都是总方向下的子问题。
- ActiveEvidence 是监督控制器路线，不走相同创新点。
- “奖励证据集合”不能算创新，SCORE 已做过；可区分点是无证据标注。
- Gittins 只作预算实现选项，必须优于 Neyman 或 EPIG 风格分配。
- 单卡不写入立题。
- 证据逻辑作备选，当前不做。
- 代码留在 csefiles，产物放 `/data/ycheng430/rmeng41/ICML`，`runs/` 用软链接。2026-11-02 用户确认。
