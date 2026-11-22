# 从零复现《The emergence of economic rationality of GPT》

**论文：** Chen, Y., Liu, T. X., Shan, Y., & Zhong, S. (2023). The emergence of economic rationality of GPT. *PNAS*, 120(51), e2316205120. https://doi.org/10.1073/pnas.2316205120
**工作论文 / SI 文本：** arXiv:2305.12763（v3，2023 年 11 月），附录中有提示词和价格生成规则。
**指南：** Zhang Qi · v7 · 2026-11-20
**配套文件：** `gpt_rationality_guide.html`（概念讲解、GARP 互动演示、证据链）。本文件讲"怎么做"复现。

---

## 0. 先读这一节

### 0.1 2026 年的"完全复现"能做到什么、做不到什么

| 论文的组成部分 | 能否复现 | 怎么做 |
|---|---|---|
| Revealed preference analysis (显示偏好分析)：GARP、CCEI、HMI、MPI、MCI、Bronars 检验 | **能，完全一致** | 第 5 节的代码，已在已知答案上测试 |
| Downward-sloping demand (需求向下倾斜) 检验与 structural estimation (结构估计, Tobit) | **能，完全一致** | 第 5 节的代码 |
| 人类被试与 GPT-3.5 的结果 | **统计比较完全能；指数计算不能重做** | 作者的 `data.csv` 是被试层面的汇总数据，没有原始选择（第 7 节） |
| 用 **gpt-3.5-turbo** 重新生成 GPT 的选择 | **不能** | OpenAI 已于 **2026-10-23** 从 API 下线 `gpt-3.5-turbo`（含 `-0125`）；作者 2023 年用的快照（很可能是 `-0613`）在 2024 年就已停用 |
| 用 **当前模型** 生成 GPT 的选择 | **能：概念性复现 (conceptual replication)** | 设计相同、分析相同、换新模型；第 3 节讲模型选择 |
| 提示词的确切措辞 | **能，完全一致** | 原文来自 arXiv 版附录 A，写在 `src/prompts_paper.py`（默认使用）；最初的改写版保留在 `src/prompts.py`，用作提示词敏感性检验 |

所以写报告时最诚实的表述是：*"我们重新实现了作者的设计与分析，在已知情形和作者的人类数据上验证了分析代码，并用模型 X 重跑了 GPT 组。"* 复现真正回答的问题就变成：**经济理性，以及它对框架的脆弱性，在新一代 LLM 上是否依然存在？**

### 0.2 要对上的目标数值（来自论文）

基准条件 (baseline)，每个领域 100 个 GPT 观测，温度 0：

| 指标 | 风险 | 时间 | 社会 | 食物 | 出处 |
|---|---|---|---|---|---|
| GPT：CCEI = 1 的人数（共 100） | 95 | 89 | 81 | 92 | Results，图 1 |
| GPT：平均 CCEI | 0.998 | 0.997 | 0.997 | 0.999 | Results |
| 人类：平均 CCEI | 0.980 | 0.985 | 0.967 | 0.963 | Results |
| GPT：平均 Spearman ρ(ln xA/xB, ln pA/pB) | −0.984 | −0.966 | −0.951 | −0.992 | 图 2 |
| 人类：平均 Spearman | −0.826 | −0.788 | −0.681 | −0.673 | 图 2 |
| 合并估计 α：人类 / GPT | 0.618 / 0.508 | 0.513 / 0.504 | 0.735 / 0.512 | 0.583 / 0.501 | SI 表 S2 |
| 合并估计 ρ：人类 / GPT | 0.335 / 0.488 | 0.981 / 0.466 | 0.330 / 0.520 | 0.386 / 0.491 | SI 表 S2 |
| 价格框架：GPT 平均 CCEI（低于 0.9 的比例） | 0.901 (34%) | 0.884 (48%) | 0.698 (88%) | 0.894 (49%) | 图 4 |
| 价格框架：GPT 平均 Spearman | −0.053 | −0.116 | +0.267 | −0.499 | SI 图 S24 |
| 离散选择：GPT 平均 CCEI（低于 0.9 的比例） | 0.843 (51%) | 0.908 (32%) | 0.871 (33%) | 0.780 (55%) | 图 4 |
| 离散选择：GPT 平均 Spearman | −0.589 | −0.497 | −0.519 | −0.533 | SI 图 S24 |

其他参照：文献平均 CCEI 0.918（范围 0.81–0.99，SI 图 S1）；99.9% 的 Bronars 随机被试违反 GARP；无效回答率在温度 0.5 时为 4.7%、温度 1 时为 9.8%；温度和人设提示下平均 CCEI 仍约为 1（图 4），但 ρ 的标准差随温度上升（Levene p < 0.01）。

---

## 1. 一页读懂论文

**问题。** GPT 的选择看起来像一个 utility maximiser (效用最大化者) 吗？理性的度量方式与实验经济学家度量人的方式相同：检查来自不同预算的一组选择，能否都由同一个性质良好的效用函数产生。

**任务：budgetary decision (预算选择任务)。** 把 100 点分给商品 A 和 B。1 点 A 换 M 单位 A，1 点 B 换 N 单位 B，M, N ∈ [0.1, 1]，max{M, N} ≥ 0.5，保留两位小数。等价地，预算线为 xA/M + xB/N = 100，价格 pA = 1/M、pB = 1/N。每个被试面对 **25 条随机预算线**。

**四个 preference domain (偏好领域)。**

| 领域 | 商品 A | 商品 B | 选择揭示了什么 |
|---|---|---|---|
| Risk (风险) | 资产 A（状态 A 时支付，概率 0.5） | 资产 B（状态 B 时支付，概率 0.5） | 风险态度 |
| Time (时间) | 今天的现金 | 一个月后可兑现的支票 | 耐心 |
| Social (社会) | 给自己的钱 | 给匿名他人的钱 | 利他 / 公平 |
| Food (食物) | 火腿肉 | 番茄 | 口味 |

**GPT 的实验流程。** 每个"GPT 被试"是一段对话：system 消息（"act as a human decision maker…"）、一条存放规则的 *assistant* 角色消息、三道理解测试题，然后 25 轮 user 消息。基准条件下 100 个被试 × 4 个领域 = 10,000 个决策。

**实验变体。** Temperature (温度) 0.5 和 1；price framing (价格框架)，用"Y 点 = 1 单位"代替"1 点 = X 单位"；discrete choice (离散选择)，从预算线上的 11 个点中选一个；system 提示中的 demographic persona (人口统计人设)（女性 / 男性、幼儿 / 老年、小学 / 大学学历、亚裔 / 非裔美国人）。

**人类组。** 347 名 Prolific 被试（美国代表性样本，2023 年 7 月，预注册 AEARCTR-0011750），随机分入基准、价格框架或离散选择组；6 美元出场费，另外每 30 人抽 1 人发奖金。

**分析流程。**
```
选择 → CCEI（+ HMI、MPI、MCI）→ Bronars 检验效力 → Spearman（需求向下倾斜）
     → 保留 CCEI ≥ 0.95 → Tobit 估计 (α, ρ) → 比较 GPT 与人类、基准与各变体
```

---

## 2. 搭建环境（Windows + PowerShell + Anaconda）

```powershell
cd C:\Users\dell\Desktop
mkdir gpt-rationality-replication; cd gpt-rationality-replication
conda create -n gptrat python=3.11 -y
conda activate gptrat
pip install -r requirements.txt     # 文件内容见下
mkdir src, scripts, data, results
New-Item src\__init__.py -ItemType File
```

`requirements.txt`
```text
numpy>=1.24
scipy>=1.11      # scipy.optimize.milp is needed for MCI
pandas>=2.0
matplotlib>=3.7
openai>=1.40
python-dotenv>=1.0
```

`.env.example` → 复制为 `.env` 再填写（不要提交 `.env`，记得把它加进 `.gitignore`）：
```ini
# Copy to .env and fill in. Never commit .env.

# --- HKUST GenAI API (OpenAI-compatible gateway; key from https://hkust.developer.azure-api.net/) ---
LLM_PROVIDER=openai
LLM_BASE_URL=https://hkust.azure-api.net/hkust-genai/v1
LLM_KEY_HEADER=api-key
LLM_API_KEY=<your primary or secondary key>
LLM_MODEL=<a model name listed by scripts/00b_check_api.py>
LLM_MIN_CREDIT=30        # 02_run_llm.py stops when the balance falls below this
LLM_PROMPTS=paper        # paper = original prompts (Appendix A); paraphrase = our first version

# --- OpenAI directly ---
# LLM_PROVIDER=openai
# LLM_MODEL=<model name>
# LLM_API_KEY=sk-...

# --- Ollama on your laptop ---
# LLM_PROVIDER=openai
# LLM_BASE_URL=http://localhost:11434/v1
# LLM_MODEL=qwen2.5:7b

# --- Azure OpenAI style endpoint ---
# LLM_PROVIDER=azure
# LLM_MODEL=<deployment name>
# AZURE_ENDPOINT=<copy from your provider's portal>
# AZURE_API_VERSION=2024-10-21
```

> `scipy >= 1.11` 很重要：MCI 用到 `scipy.optimize.milp`，即 mixed-integer linear programming (混合整数线性规划)。

---

## 3. 接通 API、选择模型与预算

### 3.0 用 HKUST GenAI API 调用（具体操作）

HKUST 的 GenAI API 是一个 **OpenAI 兼容的网关 (OpenAI-compatible gateway)**，所以代码直接用 `openai` Python 库，只需改三处：`base_url`、模型名，以及把密钥放进名为 `api-key` 的请求头 (header)。

**第 1 步：拿到 API key。**
1. 打开 HKUST API Developer Portal：`https://hkust.developer.azure-api.net/`，用 HKUST 账号登录。
2. 顶部菜单 **Products** → 选 **HKUST GenAI** → 填一个描述 → **Subscribe**。
3. 在订阅里点 **Show** 显示密钥；primary key 和 secondary key 都能用。
4. 如果你有课程 / 项目额度（例如 DDM 项目额度），用挂着那笔额度的订阅的 key；不确定时用第 3 步的余额查询确认。

**第 2 步：写 `.env`。** 在项目根目录把 `.env.example` 复制为 `.env`，填上：
```ini
LLM_PROVIDER=openai
LLM_BASE_URL=https://hkust.azure-api.net/hkust-genai/v1
LLM_KEY_HEADER=api-key
LLM_API_KEY=你的key
LLM_MODEL=先留空，第 3 步查到后再填
```
`LLM_KEY_HEADER=api-key` 很关键：HKUST 网关要求密钥放在 `api-key` 请求头里，而不是 OpenAI 默认的 `Authorization: Bearer`。`src/llm_client.py` 读到这个变量后会自动加上这个请求头。

**第 3 步：检查连通性、模型列表和余额。**
```powershell
pip install python-dotenv openai
python scripts/00b_check_api.py
```
它会做三件事：列出这个 key 能用的模型名；查询余额（`https://hkust.azure-api.net/hkust-genai/v1/balance`）；用温度 0 发一次很短的测试请求。从列表里挑一个模型名填进 `LLM_MODEL`，再跑一次，直到看到 `Test call OK`。如果列不出模型，就到 ITSO 的 "Supported Generative AI Models" 页面查名字。

**第 4 步：冒烟测试与估算成本。** 在 ITSO 的 "Pricing of AI Models" 页面查到所选模型每百万 token 的输入 / 输出价格，然后：
```powershell
python scripts/01_smoke_test.py --price-in <输入价> --price-out <输出价>
```
逐条读打印出来的对话：理解测试题答对没有？是否按 `Asset A: <points>, Asset B: <points>` 的格式作答？最后一行会给出每个条件和全部条件的预估花费（单位与你填的价格一致）。

**第 5 步：正式运行。** 网关限流约为 **每分钟 60 次请求** (rate limit)。一个条件约 1.1 万次调用，所以：
```powershell
python scripts/02_run_llm.py --conditions baseline --workers 1
```
运行时每完成 20 个被试会打印一次剩余额度；余额低于 `.env` 里的 `LLM_MIN_CREDIT`（默认 30）就自动停止并提示充值，已完成的被试都会保存。`--workers 1` 最稳，baseline 大约要 3–4 小时；如果单次调用较慢（>2 秒），可以试 `--workers 2`。被限流时客户端会自动退避重试；中途断掉就重跑同一条命令，已完成的被试会被跳过。笔记本记得关掉自动休眠。

**常见报错：**

| 报错 | 原因 | 处理 |
|---|---|---|
| 401 / Access denied | key 错了，或没带 `api-key` 请求头 | 检查 `.env` 的 `LLM_API_KEY` 和 `LLM_KEY_HEADER=api-key` |
| 404 / model not found | 模型名不对 | 用 `00b_check_api.py` 列出的名字 |
| 429 Too Many Requests | 超过每分钟 60 次 | 降到 `--workers 1`；代码会自动重试 |
| 额度用完的提示 | 余额为 0 | 查余额；需要时到 `https://pmt2.ust.hk/openai/` 充值 |
| temperature 相关错误 | 推理模型不支持自定义温度 | 换一个非推理模型做主实验 |

> 旧的 "Azure OpenAI API Service"（`/openai/deployments/<名字>/chat/completions?api-version=...` 那种地址）也是 HKUST 提供的另一套接口，上面的 `gpt-35-turbo` 同样已经下线。本指南用新的 HKUST GenAI 网关。

### 3.1 模型选择

| 方案 | 优点 | 缺点 |
|---|---|---|
| 通过你的服务商调用当前的 OpenAI 系小模型（OpenAI 兼容或 Azure 风格接口，例如学校的 GenAI 服务） | 最接近 GPT-3.5-turbo 的"后代"；便宜 | 不是同一个模型；这个快照以后也可能下线 |
| 多个模型并排（小模型 + 旗舰模型，OpenAI + 开源权重） | 把复现变成一个发现：理性在模型代际间如何变化 | 成本更高 |
| 用 Ollama 在笔记本上跑开源权重模型（`LLM_BASE_URL=http://localhost:11434/v1`） | 免费，快照完全可复现 | 笔记本上很慢；小模型对指令的理解更差 |

让复现保持干净的规则：

1. **固定一个带日期的快照**（模型名带日期后缀），不要用会悄悄变化的别名 (alias)。
2. 在报告中**记录**模型名称、服务商、日期和全部设置（`data/meta/*.jsonl` 保存了完整对话记录）。
3. **推理模型** (reasoning models) 可能忽略或拒绝 `temperature` 参数，这时温度条件不适用。如实说明，不要强行设置。
4. 接口细节（base URL 或 Azure endpoint、API version、模型或 deployment 名称）以服务商自己的文档为准，然后填进 `.env`。

### 3.2 成本

每个被试是一段 28 次调用的对话（3 道理解题 + 25 轮），每次调用都会重发完整历史。用我们的提示词实测：

| 条件 | 每个被试的输入 token | 一个条件（400 个被试） |
|---|---|---|
| 连续选择（基准、温度、框架、人设） | 约 3.1 万 | 约 1200–1300 万 |
| 离散选择（每轮列出 11 个选项） | 约 5.8 万 | 约 2300 万 |

全部 13 个条件约 1.75 亿输入 token；输出很少（每轮约 10–20 token）。乘以你所用模型每百万 token 的价格即可。正式开跑前，先用真实模型运行 `scripts/01_smoke_test.py --price-in <美元> --price-out <美元>`，得到实测的成本估计。

**预算紧张时的分档计划：**

| 档 | 条件 | 重复次数 | 理由 |
|---|---|---|---|
| 1（必须） | baseline | 100 | 主结果 |
| 2（必须） | price_framing、discrete | 100 | 论文最核心的局限 |
| 3 | temp_0.5、temp_1 | 50 | 稳健性 |
| 4 | 8 种人设 | 30 | 稳健性；论文中效应为零 |

---

## 4. 项目结构

```text
gpt-rationality-replication/
├── config.py            设计常数、各条件、API 设置
├── requirements.txt
├── .env                 你的密钥（不提交）
├── src/
│   ├── __init__.py
│   ├── prices.py        预算线 (M, N)、离散选项
│   ├── prompts_paper.py 原文提示词（附录 A，默认）
│   ├── prompts.py       改写版提示词（敏感性检验）
│   ├── prompt_api.py    按 LLM_PROMPTS 切换两个版本
│   ├── parse.py         回复 → (points_a, points_b)
│   ├── llm_client.py    OpenAI / Azure 客户端，自动重试
│   ├── experiment.py    一个 GPT 被试 = 一段对话；MockClient 用于离线测试
│   ├── dataio.py        把 GPT 与人类的选择读成一张表
│   ├── rp.py            GARP、CCEI、HMI、MPI、MCI、Bronars
│   ├── demand.py        Spearman 需求向下倾斜检验
│   ├── estimate.py      双边截尾 Tobit 估计 (α, ρ)
│   └── stats.py         t 检验、Levene 检验、稳健标准误 OLS
├── scripts/
│   ├── 00_selftest.py   在已知答案上验证分析代码
│   ├── 00b_check_api.py 检查 API：模型列表、余额、一次测试调用
│   ├── 01_smoke_test.py 每个领域跑 1 个被试，打印对话，估算成本
│   ├── 02_run_llm.py    收集选择（可断点续跑、可并行）
│   ├── 03_indices.py    理性指数 + Bronars
│   ├── 04_estimate.py   偏好参数
│   ├── 05_tests.py      统计检验 → results/tests.md
│   ├── 06_figures.py    图 1–4
│   ├── 07_import_authors.py 导入作者的被试层面数据（人类 + GPT-3.5）
│   ├── 08_clean_failed.py  删除含 API 失败的被试，以便重跑
│   ├── 09_progress.py      查看进度、无效回答率和剩余额度
│   ├── 10_show_invalid.py  列出无法解析的回复
│   ├── 11_reparse.py       用新规则重新解析已保存的回复
│   └── 12_offmenu.py       离散条件的菜单外选择及稳健性检验
├── data/  raw/  meta/  data.csv（作者数据）  authors_*.csv
└── results/
```

---

## 5. 逐个文件搭建

下面每个文件都是完整的。按显示的文件名新建文件，粘贴代码即可。代码注释保留英文，与常见的开源代码习惯一致。

### 5.1 `config.py`：所有设计选择集中在一处

每个常数的来由：25 轮、100 次重复是论文的设计；价格规则来自 SI 附录 A；0.95 是估计时的 CCEI 门槛（论文脚注 ‡，沿用 Varian 1990）；0.1 点即"预算的 0.1%"，是 Spearman 检验中的角点调整；0.918 是单样本 t 检验用到的文献均值。

```python
"""Central settings for the GPT economic-rationality replication.

Chen, Liu, Shan & Zhong (2023), "The emergence of economic rationality of GPT", PNAS 120(51).
Edit this file (or set environment variables) instead of editing code elsewhere.
"""
import os
from pathlib import Path

try:                                    # read .env if python-dotenv is installed
    from dotenv import load_dotenv
    load_dotenv(Path(__file__).resolve().parent / ".env")
except ImportError:
    pass

ROOT = Path(__file__).resolve().parent
DATA = ROOT / "data"
RESULTS = ROOT / "results"
DATA.mkdir(exist_ok=True)
# each prompt set writes to its own folders, so the two versions never mix
RAW_DIR = DATA / ("raw" if os.getenv("LLM_PROMPTS", "paper") == "paper" else "raw_paraphrase")
META_DIR = DATA / ("meta" if os.getenv("LLM_PROMPTS", "paper") == "paper" else "meta_paraphrase")
RESULTS.mkdir(exist_ok=True)

# ---------------- design (paper: Methods) ----------------
N_ROUNDS = 25            # decisions per subject (budget lines)
N_REPS = 100             # GPT "subjects" per domain x condition
ENDOWMENT = 100          # points
PRICE_LOW, PRICE_HIGH = 0.10, 1.00   # M, N drawn from [0.1, 1]
PRICE_MAX_AT_LEAST = 0.50            # max{M, N} >= 0.5
N_DISCRETE_OPTIONS = 11              # discrete-choice condition
DOMAINS = ["risk", "time", "social", "food"]

# condition name -> settings. "demo" is the demographic phrase in the system prompt.
CONDITIONS = {
    "baseline":      dict(temperature=0.0, framing="baseline", choice="continuous", demo=None),
    "temp_0.5":      dict(temperature=0.5, framing="baseline", choice="continuous", demo=None),
    "temp_1":        dict(temperature=1.0, framing="baseline", choice="continuous", demo=None),
    "price_framing": dict(temperature=0.0, framing="inverse",  choice="continuous", demo=None),
    "discrete":      dict(temperature=0.0, framing="baseline", choice="discrete",   demo=None),
    "female":        dict(temperature=0.0, framing="baseline", choice="continuous", demo="female"),
    "male":          dict(temperature=0.0, framing="baseline", choice="continuous", demo="male"),
    "young_child":   dict(temperature=0.0, framing="baseline", choice="continuous", demo="young child"),
    "elderly":       dict(temperature=0.0, framing="baseline", choice="continuous", demo="elderly"),
    "elementary_edu":dict(temperature=0.0, framing="baseline", choice="continuous", demo="elementary_edu"),
    "college_edu":   dict(temperature=0.0, framing="baseline", choice="continuous", demo="college_edu"),
    "asian":         dict(temperature=0.0, framing="baseline", choice="continuous", demo="Asian"),
    "african_american": dict(temperature=0.0, framing="baseline", choice="continuous", demo="African American"),
}

# ---------------- analysis (paper: Results) ----------------
CCEI_CUTOFF_FOR_ESTIMATION = 0.95   # footnote: drop subjects with CCEI < 0.95
CORNER_ADJ_POINTS = 0.1             # 0.1% of the 100-point budget, for ln(xA/xB)
LITERATURE_MEAN_CCEI = 0.918        # SI Fig. S1 average of prior studies
N_BRONARS = 1000                    # simulated random subjects per domain
MIN_VALID_ROUNDS = 20               # keep a subject only if >= 20 of 25 answers parse

# ---------------- LLM access (fill in .env or environment) ----------------
# PROVIDER = "openai"  -> any OpenAI-compatible endpoint (OpenAI, a university gateway, Ollama, vLLM)
# PROVIDER = "azure"   -> Azure OpenAI style endpoint (deployment name + api-version)
PROVIDER = os.getenv("LLM_PROVIDER", "openai")
MODEL = os.getenv("LLM_MODEL", "gpt-4o-mini")
PROMPT_SET = os.getenv("LLM_PROMPTS", "paper")   # "paper" = authors' original prompts; "paraphrase" = our first version
SOURCE_LABEL = os.getenv("LLM_LABEL", MODEL)   # how this model's subjects are labelled in results
PARA_LABEL = SOURCE_LABEL + " (paraphrase)"    # label for runs made with the paraphrased prompts
PAPER_LABEL = "gpt-3.5-turbo (paper)"          # the authors' GPT subjects, imported by 07_import_authors.py
BASE_URL = os.getenv("LLM_BASE_URL")          # e.g. http://localhost:11434/v1 for Ollama
API_KEY = os.getenv("LLM_API_KEY", "")
KEY_HEADER = os.getenv("LLM_KEY_HEADER", "")  # "api-key" for gateways that want the key in an api-key header (e.g. HKUST)
AZURE_ENDPOINT = os.getenv("AZURE_ENDPOINT")  # copy from your provider's portal
AZURE_API_VERSION = os.getenv("AZURE_API_VERSION", "2024-06-01")
# No reply-length cap by default: the paper kept all API parameters at their defaults, and a cap cuts
# long answers before the model states its choice. Set LLM_MAX_TOKENS in .env to impose one.
MAX_TOKENS = int(os.getenv("LLM_MAX_TOKENS")) if os.getenv("LLM_MAX_TOKENS") else None
MIN_CREDIT = float(os.getenv("LLM_MIN_CREDIT", "30"))   # stop the run when the HKUST balance falls below this
SEED_BASE = 20231212   # any fixed integer; makes the price draws reproducible
```

### 5.2 `src/prices.py`：预算线

核心思想（预算线）：1 点能买 M 单位 A，那么 1 单位 A 的"价格"就是 1/M 点。价格 p = (1/M, 1/N)、数量 x = (a·M, b·N) 时，花费 p·x = a + b = 100 点。所有显示偏好代码都在 (p, x) 上运算。

一个设计决定（论文没有写明）：**每个 GPT 被试有自己的 25 条随机预算线**（带种子），与 Choi et al. (2007) 中的人类被试一样。温度为 0 时，如果 100 次重复都用同一组价格，这些重复几乎是彼此的复制品。种子只取决于（领域、重复编号），因此基准条件和每个变体面对的是**同样的**预算线：这是一个配对设计 (paired design)，能让条件之间的比较更精确。

```python
"""Budget lines. One point in A pays M units of A; one point in B pays N units of B.

So with 100 points the budget line is  xA / M + xB / N = 100,
i.e. prices pA = 1/M, pB = 1/N and income 100 (in points).
"""
import numpy as np
import config as C


def draw_prices(rng: np.random.Generator, n: int = C.N_ROUNDS) -> np.ndarray:
    """Return an (n, 2) array of (M, N): M, N ~ U[0.1, 1], two decimals, max(M, N) >= 0.5."""
    out = []
    while len(out) < n:
        m, k = np.round(rng.uniform(C.PRICE_LOW, C.PRICE_HIGH, size=2), 2)
        if max(m, k) >= C.PRICE_MAX_AT_LEAST:
            out.append((m, k))
    return np.array(out)


def subject_seed(domain: str, condition: str, rep: int) -> int:
    """Stable seed per (domain, condition, rep). Same rep -> same prices across conditions,
    so the baseline and its variations face identical budget lines (a paired design)."""
    d = {"risk": 1, "time": 2, "social": 3, "food": 4}[domain]
    return C.SEED_BASE + 1000 * d + rep


def to_quantities(points_a, points_b, m, n):
    """Points -> commodity quantities (xA, xB)."""
    return np.asarray(points_a) * m, np.asarray(points_b) * n


def price_vectors(m, n):
    """(M, N) -> price vectors p = (1/M, 1/N) so that p . x = points spent."""
    return np.column_stack([1.0 / np.asarray(m), 1.0 / np.asarray(n)])


def discrete_options(m, n, k: int = C.N_DISCRETE_OPTIONS):
    """11 points on the budget line: option j puts 10*j points in A (j = 0..10).
    Returns list of (points_a, points_b, xA, xB)."""
    step = C.ENDOWMENT / (k - 1)
    opts = []
    for j in range(k):
        a = step * j
        b = C.ENDOWMENT - a
        opts.append((a, b, round(a * m, 2), round(b * n, 2)))
    return opts
```

### 5.3 提示词：原文版 `src/prompts_paper.py` 与改写版 `src/prompts.py`

**原文版（默认，`LLM_PROMPTS=paper`）**逐字取自 arXiv:2305.12763v3 附录 A：(1) system 消息"I want you to act as a human decision maker…"，人设条件只替换其中的"a human decision maker"；(2) assistant 角色存放规则（作者的做法：只存储任务信息，不要求作答）；(3) 三道理解测试题，**与条件同框架**——价格框架条件用"1.25 points … returns 1 dollar"，离散条件用"($72, $2)"；(4) 25 轮决策，没有"Round k"前缀、没有固定回答格式；(5) 离散选项写成"($M1,$N1), …"，问"Which is the best?"。

**改写版（`LLM_PROMPTS=paraphrase`）**是本复现最初使用的版本，与原文有五处差异：理解测试题在所有条件下都用基准框架；每轮前加"Round k."；要求固定回答格式并说明两数之和为 100；离散选项带编号和标签（"Option j: (Asset A x, Asset B y)"）；若干措辞不同。两个版本的数据分别写入 `data/raw` 和 `data/raw_paraphrase`，结果中分别标为 `gpt-4o-mini` 和 `gpt-4o-mini (paraphrase)`，可以直接比较提示词的影响。

论文附录给出的离散选项公式 Ni = 100 − (i−1)×10×N 显然是笔误（这样的点不在预算线上）；本复现按预算线取 (Mi, Ni) = ((i−1)×10×M, (100 − (i−1)×10)×N)。

```python
"""Original prompts of Chen, Liu, Shan & Zhong (2023), copied from arXiv:2305.12763v3, Appendix A
(the paper is distributed under CC BY-NC-ND 4.0; reproduced verbatim, with attribution, for replication).

Choose this set with LLM_PROMPTS=paper (the default). Differences from the paraphrased set
(src/prompts.py): no "Round k." prefix, no fixed answer format, comprehension questions written in
the same frame as the condition (price framing / discrete), options listed as "($M1,$N1), ...".
Persona variants replace "a human decision maker" in the system message (paper, Section 2.2).
"""
from src.prices import discrete_options

SYSTEM = ("I want you to act as {who}. You will be given 25 rounds of decision-making tasks and will "
          "be responsible for making decisions. You should use your best judgment to come up with "
          "solutions that you like most. My first request is “You must provide your answers in every "
          "round.” If you do not provide an answer, I will assume that you make a random choice.")

WHO = {
    None: "a human decision maker",
    "female": "a female decision maker",
    "male": "a male decision maker",
    "young child": "a young child decision maker",
    "elderly": "an elderly decision maker",
    "elementary_edu": "a decision maker with an elementary school education",
    "college_edu": "a decision maker with a college education",
    "Asian": "an Asian decision maker",
    "African American": "an African American decision maker",
}

LABELS = {"risk": ("Asset A", "Asset B"), "time": ("today", "one month later"),
          "social": ("yourself", "the other"), "food": ("meat", "tomato")}

# ---------------- assistant messages ----------------
_RISK_CONT = ("In every round, the decision maker has 100 points that need to be invested between Asset A "
              "and Asset B. The decision maker has a 50% chance to get the return from Asset A or the other "
              "50% chance to get the return from Asset B. First please only tell me the number of points for "
              "investing Asset A, then please only tell me the number of points for investing Asset B.")
_TIME_CONT = ("In every round, the decision maker has 100 points that need to be invested between today and "
              "one month later. The decision maker will get dollars today from the points invested today and "
              "will get check that can be cashed in one month later from the points invested one month later. "
              "Please first only tell me the number of points for investing today, then please only tell me "
              "the number of points for investing one month later.")
_SOC_CONT = ("In every round, the decision maker is randomly matched with a new anonymous subject and there is "
             "no feedback across rounds. The decision maker has 100 points that need to be allocated between "
             "him/herself and the other one. The decision maker will get return from the points allocated to "
             "him/herself and the other one will get return from the points allocated to him/her. First please "
             "only tell me the number of points you want to allocate to yourself, then please only tell me the "
             "number of points you want to allocate to the other.")
_FOOD_CONT = ("In every round, the decision maker has 100 points that need to be spent between ham meat and "
              "tomato. The decision maker will get the amount of meat and tomato he/she spends on. First please "
              "only tell me the number of points for meat, then please only tell me the number of points for tomato.")

ASSISTANT = {
    ("risk", "continuous"): _RISK_CONT,
    ("time", "continuous"): _TIME_CONT,
    ("social", "continuous"): _SOC_CONT,
    ("food", "continuous"): _FOOD_CONT,
    ("risk", "discrete"): ("In every round, the decision maker will be presented with 11 options, each represented "
                           "in the form ($M, $N). The decision maker has a 50% chance to get M from Asset A or the "
                           "other 50% chance to get N from Asset B. Please only tell me about your best option in "
                           "every round."),
    ("time", "discrete"): ("In every round, the decision maker will be presented with 11 options, each represented "
                           "in the form ($M, $N). The decision maker will get M dollars today and will get a N "
                           "dollars check that can be cashed in one month later. Please only tell me about your "
                           "best option in every round."),
    ("social", "discrete"): ("In every round, the decision maker is randomly matched with a new anonymous subject "
                             "and there is no feedback across rounds. The decision maker will be presented with 11 "
                             "options, each represented in the form ($M, $N). The decision maker will get M dollars "
                             "and the other will get N dollars. Please only tell me about your best option in every "
                             "round."),
    ("food", "discrete"): ("In every round, the decision maker will be presented with 11 options, each represented "
                           "in the form (M Kg, N Kg). The decision maker will get M Kg of meat and get N Kg of "
                           "tomato. Please only tell me about your best option in every round."),
}

# ---------------- comprehension questions ----------------
_R_BASE = ("investing every 1 point for Asset A returns 0.8 dollars, and investing every 1 point for Asset B "
           "returns 0.2 dollars")
_R_INV = ("investing every 1.25 points for Asset A returns 1 dollar, and investing every 5 points for Asset B "
          "returns 1 dollar")
_T_BASE = ("investing every 1 point for today returns 0.8 dollars cash today, and investing every 1 point for one "
           "month later returns 0.2 dollars check which can be cashed one month later")
_T_INV = ("investing every 1.25 points for today returns 1 dollar cash today, and investing every 5 points for "
          "one month later returns 1 dollar check which can be cashed one month later")

TESTS = {
    ("risk", "baseline"): [
        "What is the probability you will get a return from Asset A?",
        f"Suppose that you invest 90 points to Asset A, and 10 points to Asset B. In this round, {_R_BASE}. What return will you get?",
        f"Suppose that you invest 90 points to Asset A, and 10 points to Asset B. In this round, {_R_BASE}. Is there a chance to get 72 dollars?"],
    ("risk", "inverse"): [
        "What is the probability you will get a return from Asset A?",
        f"Suppose that you invest 90 points to Asset A, and 10 points to Asset B. In this round, {_R_INV}. What return will you get?",
        f"Suppose that you invest 90 points to Asset A, and 10 points to Asset B. In this round, {_R_INV}. Is there a chance to get 72 dollars?"],
    ("risk", "discrete"): [
        "What is the probability you will get a return from Asset A?",
        "If you choose the option ($72, $2), what return will you get?",
        "If you choose the option ($72, $2), is there a chance to get 72 dollars?"],
    ("time", "baseline"): [
        f"Suppose that you invest 90 points to today, and 10 points to one month later. In this round, {_T_BASE}. What return will you get?",
        f"Suppose that you invest 90 points to today, and 10 points to one month later. In this round, {_T_BASE}. When can you get just the 2 dollars cash?",
        f"In this round, {_T_BASE}. What is your allocation? Why?"],
    ("time", "inverse"): [
        f"Suppose that you invest 90 points to today, and 10 points to one month later. In this round, {_T_INV}. What return will you get?",
        f"Suppose that you invest 90 points to today, and 10 points to one month later. In this round, {_T_INV}. When can you get just the 2 dollars cash?",
        f"In this round, {_T_INV}. What is your allocation? Why?"],
    ("time", "discrete"): [
        "If you choose the option ($72, $2), what return will you get?",
        "If you choose the option ($72, $2), when can you get just the 2 dollars cash?",
        "If you face the options ($40, $10) and ($72, $2), which option will you select? Why?"],
    ("social", "baseline"): [
        "Suppose that you allocate 90 points to yourself, and 10 points to the other. In this round, allocating every 1 point to yourself returns 0.8 dollars for yourself, and allocating every 1 point to the other returns 0.2 dollars for the other. What return will you get?",
        "Suppose that you allocate 90 points to yourself, and 10 points to the other. In this round, allocating every 1 point for yourself returns 0.8 dollars for yourself, and allocating every 1 point for the other returns 0.2 dollars for the other. Who will get just 2 dollars?",
        "In this round, allocating every 1 point for yourself returns 0.8 dollars for yourself, and allocating every 1 point for the other returns 0.2 dollars for the other. Will you allocate to the other? Why?"],
    ("social", "inverse"): [
        "Suppose that you allocate 90 points to yourself, and 10 points to the other. In this round, every 1.25 points to yourself returns 1 dollar for yourself, allocating every 5 points to the other returns 1 dollar for the other. What return will you get?",
        "Suppose that you allocate 90 points to yourself, and 10 points to the other. In this round, allocating every 1.25 points for yourself returns 1 dollar for yourself, and allocating every 5 points for the other returns 1 dollar for the other. Who will get just 2 dollars?",
        "In this round, allocating every 1.25 points for yourself returns 1 dollar for yourself, and allocating every 5 points for the other returns 1 dollar for the other. Will you allocate to the other? Why?"],
    ("social", "discrete"): [
        "If you choose the option ($72, $2), what return will you get?",
        "If you choose the option ($72, $2), who will get just 2 dollars?",
        "If you face the options ($40, $10) and ($72, $2), which option will you select? Why?"],
    ("food", "baseline"): [
        "What goods can you get from decisions?",
        "Suppose that you spend 90 points to meat, and 10 points to tomato. In this round, spending every 1 point for meat will get 0.8 Kg meat, and spending every 1 point for tomato will get 0.2 Kg tomato, what will you get?",
        "In this round, spending every 1 point for meat will get 0.8 Kg meat, and spending every 1 point for tomato will get 0.2 Kg tomato. What is your allocation? Why?"],
    ("food", "inverse"): [
        "What goods can you get from decisions?",
        "Suppose that you spend 90 points to meat, and 10 points to tomato. In this round, spending every 1.25 point for meat will get 1 Kg meat, and spending every 5 points for tomato will get 1 Kg tomato, what will you get?",
        "In this round, spending every 1.25 points for meat will get 1 Kg meat, and spending every 5 points for tomato will get 1 Kg tomato. What is your allocation? Why?"],
    ("food", "discrete"): [
        "What goods can you get from decisions?",
        "Suppose you choose the option (72 Kg, 2 Kg), what will you get?",
        "Suppose you face the options (40 Kg, 10 Kg) and (72 Kg, 2 Kg), which option will you select? Why?"],
}

# ---------------- decision tasks ----------------
TASK = {
    ("risk", "baseline"): "In this round, investing every 1 point for Asset A returns {m} dollars, and investing every 1 point for Asset B returns {n} dollars. What is your allocation?",
    ("risk", "inverse"): "In this round, investing every {m} points for Asset A returns 1 dollar, and investing every {n} points for Asset B returns 1 dollar. What is your allocation?",
    ("time", "baseline"): "In this round, investing every 1 point for today returns {m} dollars today, and investing every 1 point for one month later returns {n} dollars check which can be cashed in one month later. What is your allocation?",
    ("time", "inverse"): "In this round, investing every {m} points for today returns 1 dollar today, and investing every {n} points for one month later returns 1 dollar check which can be cashed in one month later. What is your allocation?",
    ("social", "baseline"): "In this round, allocating every 1 point for yourself returns {m} dollars for yourself, and allocating every 1 point for the other one returns {n} dollars for him/her. What is your allocation?",
    ("social", "inverse"): "In this round, allocating every {m} points for yourself returns 1 dollar for yourself, and allocating every {n} points for the other one returns 1 dollar for him/her. What is your allocation?",
    ("food", "baseline"): "In this round, spending every 1 point on meat will get {m} Kg meat, and spending every 1 point on tomato will get {n} Kg tomato. What is your allocation?",
    ("food", "inverse"): "In this round, spending every {m} points on meat will get 1 Kg meat, and spending every {n} points on tomato will get 1 Kg tomato. What is your allocation?",
}


def _key(cfg):
    return "discrete" if cfg["choice"] == "discrete" else cfg["framing"]


def opening_messages(domain, cfg):
    return [{"role": "system", "content": SYSTEM.format(who=WHO[cfg["demo"]])},
            {"role": "assistant", "content": ASSISTANT[(domain, cfg["choice"])]}]


def test_questions(domain, cfg):
    return TESTS[(domain, _key(cfg))]


def option_text(domain, xa, xb):
    return f"({xa:.2f} Kg,{xb:.2f} Kg)" if domain == "food" else f"(${xa:.2f},${xb:.2f})"


def round_message(domain, cfg, rnd, m, n):
    if cfg["choice"] == "discrete":
        opts = ", ".join(option_text(domain, o[2], o[3]) for o in discrete_options(m, n))
        return f"In this round, there are 11 options, which are {opts}. Which is the best?"
    if cfg["framing"] == "inverse":                      # "every 1/M points ... returns 1 dollar", 2 decimals
        return TASK[(domain, "inverse")].format(m=f"{1 / m:.2f}", n=f"{1 / n:.2f}")
    return TASK[(domain, "baseline")].format(m=f"{m:.2f}", n=f"{n:.2f}")


def labels(domain):
    return LABELS[domain]
```

```python
"""Prompt builder.

Structure follows the paper (Methods + SI Appendix A): a system message (role), an
"assistant" message that stores the decision format, three comprehension questions, then
25 decision rounds as user messages in one conversation. The wording below is our own
paraphrase of that structure; replace it with the authors' SI text if you have it.
"""
import config as C
from src.prices import discrete_options

# domain -> labels and how a point converts into payoff
DOMAIN = {
    "risk": dict(
        a="Asset A", b="Asset B", unit="dollars",
        setting=("In every round, the decision maker has 100 points to invest between Asset A and "
                 "Asset B. After the decision, one asset is selected: there is a 50% chance the "
                 "return comes from Asset A and a 50% chance it comes from Asset B. The decision "
                 "maker receives only the return of the selected asset."),
        tests=[
            "What is the probability that the return comes from Asset A?",
            "Suppose investing every 1 point for Asset A returns 0.8 dollars and investing every 1 point "
            "for Asset B returns 0.2 dollars. If you put 90 points in Asset A and 10 points in Asset B, "
            "what are the possible returns?",
            "In the situation of the previous question, is it possible to receive 72 dollars?",
        ]),
    "time": dict(
        a="today", b="one month later", unit="dollars",
        setting=("In every round, the decision maker has 100 points to allocate between today and one "
                 "month later. Points allocated to today are paid in cash today. Points allocated to one "
                 "month later are paid by a check that can be cashed one month from today. The decision "
                 "maker receives both payments."),
        tests=[
            "Suppose every 1 point for today pays 0.8 dollars and every 1 point for one month later pays "
            "0.2 dollars. If you allocate 90 points to today and 10 points to one month later, what is the "
            "total amount you receive?",
            "In the situation of the previous question, when can you receive the 2 dollars?",
            "In that situation, what allocation would you choose, and why?",
        ]),
    "social": dict(
        a="yourself", b="the other person", unit="dollars",
        setting=("In every round, the decision maker is randomly matched with a new anonymous subject, "
                 "and there is no feedback across rounds. The decision maker has 100 points to allocate "
                 "between herself or himself and the other person. Both receive their payments."),
        tests=[
            "Suppose every 1 point for yourself pays you 0.8 dollars and every 1 point for the other person "
            "pays the other person 0.2 dollars. If you allocate 90 points to yourself and 10 points to the "
            "other person, how much does each of you receive?",
            "In the situation of the previous question, who receives the 2 dollars?",
            "Will you allocate anything to the other person? Why?",
        ]),
    "food": dict(
        a="ham meat", b="tomato", unit="units",
        setting=("In every round, the decision maker has 100 points that need to be spent between ham meat "
                 "and tomato. The decision maker receives the food bundle that is chosen."),
        tests=[
            "Suppose every 1 point for ham meat buys 0.8 units of ham meat and every 1 point for tomato buys "
            "0.2 units of tomato. If you spend 90 points on ham meat and 10 points on tomato, what do you get?",
            "Can you receive 72 units of ham meat and 2 units of tomato with 100 points in that situation?",
            "What will you do in each round?",
        ]),
}

DEMO_PHRASE = {
    None: "a human decision maker",
    "female": "a female decision maker",
    "male": "a male decision maker",
    "young child": "a young child decision maker",
    "elderly": "an elderly decision maker",
    "elementary_edu": "a decision maker with an elementary school education",
    "college_edu": "a decision maker with a college education",
    "Asian": "an Asian decision maker",
    "African American": "an African American decision maker",
}


def system_message(demo=None) -> str:
    return (f"I want you to act as {DEMO_PHRASE[demo]}. You will make decisions in "
            f"{C.N_ROUNDS} rounds. You should use your best judgment to come up with solutions that you "
            "like most. You must give an answer in every round; a missing answer is treated as a random choice.")


def answer_format(domain: str, choice: str) -> str:
    d = DOMAIN[domain]
    if choice == "discrete":
        return "Please only tell me your best option, in the form: Option <number>."
    return (f"Please only tell me your allocation, in the form: {d['a']}: <points>, {d['b']}: <points>. "
            "The two numbers must add up to 100.")


def assistant_message(domain: str, choice: str) -> str:
    d = DOMAIN[domain]
    return (f"{d['setting']} In each round, the payoff per point for {d['a']} and for {d['b']} changes. "
            f"I will describe the payoffs and you choose. {answer_format(domain, choice)} "
            "I will not ask you to decide yet.")


def _price_text(domain, framing, m, n):
    d = DOMAIN[domain]
    if framing == "baseline":     # "1 point = X units"
        return (f"every 1 point for {d['a']} returns {m:.2f} {d['unit']}, and every 1 point for "
                f"{d['b']} returns {n:.2f} {d['unit']}")
    # inverse framing: "Y points = 1 unit"
    return (f"every {1 / m:.2f} points for {d['a']} return 1 {d['unit'][:-1]}, and every {1 / n:.2f} points "
            f"for {d['b']} return 1 {d['unit'][:-1]}")


def round_message(domain, framing, choice, rnd, m, n) -> str:
    d = DOMAIN[domain]
    if choice == "discrete":
        opts = discrete_options(m, n)
        listing = "; ".join(f"Option {j + 1}: ({d['a']} {o[2]:.2f}, {d['b']} {o[3]:.2f})"
                            for j, o in enumerate(opts))
        return (f"Round {rnd}. In this round, there are {len(opts)} options (amounts in {d['unit']}): "
                f"{listing}. Which is the best? {answer_format(domain, choice)}")
    return (f"Round {rnd}. In this round, {_price_text(domain, framing, m, n)}. "
            f"What is your allocation? {answer_format(domain, choice)}")


def opening_messages(domain, condition_cfg):
    """Messages before the comprehension questions."""
    return [
        {"role": "system", "content": system_message(condition_cfg["demo"])},
        {"role": "assistant", "content": assistant_message(domain, condition_cfg["choice"])},
    ]
```

`src/prompt_api.py` 按 `LLM_PROMPTS` 在两个版本之间切换：

```python
"""One interface to the two prompt sets (LLM_PROMPTS = "paper" or "paraphrase")."""
import config as C
from src import prompts as PARA
from src import prompts_paper as PAPER
from src.prices import discrete_options


def opening_messages(domain, cfg):
    return (PAPER if C.PROMPT_SET == "paper" else PARA).opening_messages(domain, cfg)


def test_questions(domain, cfg):
    if C.PROMPT_SET == "paper":
        return PAPER.test_questions(domain, cfg)
    return PARA.DOMAIN[domain]["tests"]


def round_message(domain, cfg, rnd, m, n):
    if C.PROMPT_SET == "paper":
        return PAPER.round_message(domain, cfg, rnd, m, n)
    return PARA.round_message(domain, cfg["framing"], cfg["choice"], rnd, m, n)


def labels(domain):
    if C.PROMPT_SET == "paper":
        return PAPER.labels(domain)
    return PARA.DOMAIN[domain]["a"], PARA.DOMAIN[domain]["b"]


def option_values(m, n):
    """The 11 options as (xA, xB), rounded as shown to the model."""
    return [(o[2], o[3]) for o in discrete_options(m, n)]
```

### 5.4 `src/parse.py`：回复 → 数字

原文提示词不规定回答格式，所以解析器按三条规则依次尝试：紧跟在两个标签后的数字；带"points"的数字中第一对和为 100 的；所有不超过 100 的数字中第一对和为 100 的。离散条件下，取最后一个结论性表述（"I choose / I would select / the best option is"）之后、与 11 个选项之一完全匹配的数对；没有结论性表述时，只有回复中恰好出现一个选项才算有效，所以在给出选择前被截断的回答会记为无效。有效回答 = 两个和为 100 的非负数（允许 ±1 的误差，然后按比例缩放）；其他情况视为无效并剔除，这与作者处理未作答的方式一致。`01_smoke_test.py` 会打印每一轮的解析结果，方便人工核对。

```python
"""Turn the model's free-text reply into an allocation.

The original prompts do not impose an answer format, so replies vary ("Asset A: 60, Asset B: 40",
"I will invest 60 points in Asset A and 40 points in Asset B, which returns 52.8 dollars...").
Rules, in order (the first that gives two non-negative numbers summing to 100 +/- 1 wins):
  1. numbers right after the two labels;
  2. the first pair of numbers tagged "points" that sums to 100;
  3. the first pair of any numbers in [0, 100] that sums to 100.
"""
import re
import config as C

NUM = r"(\d+(?:\.\d+)?)"


def _ok(x, y):
    return x >= 0 and y >= 0 and abs(x + y - C.ENDOWMENT) <= 1.0


def _first_pair(nums):
    for i in range(len(nums)):
        for j in range(i + 1, len(nums)):
            if _ok(nums[i], nums[j]):
                return nums[i], nums[j]
    return None


def parse_continuous(text: str, label_a: str, label_b: str):
    """Return (a, b, valid)."""
    if not text:
        return None, None, False
    t = text.replace(",", " ").replace("**", "")
    a = re.search(re.escape(label_a) + r"\W{0,3}\s*" + NUM, t, flags=re.I)
    b = re.search(re.escape(label_b) + r"\W{0,3}\s*" + NUM, t, flags=re.I)
    pair = None
    if a and b and _ok(float(a.group(1)), float(b.group(1))):
        pair = float(a.group(1)), float(b.group(1))
    if pair is None:
        pts = [float(v) for v in re.findall(NUM + r"\s*points?\b", t, flags=re.I)]
        pair = _first_pair(pts)
    if pair is None:
        nums = [float(v) for v in re.findall(NUM, t) if float(v) <= C.ENDOWMENT]
        pair = _first_pair(nums)
    if pair is None:
        return None, None, False
    x, y = pair
    s = x + y                                              # rescale tiny rounding gaps to exactly 100
    return x * C.ENDOWMENT / s, y * C.ENDOWMENT / s, True


DECIDE = (r"(\bI(?: would| will|'d|'ll)?(?: still)? (?:choose|chose|select|pick|go with|opt for|recommend|prefer)"
          r"|(?:best|optimal|preferred|recommended|ideal) (?:option|choice)(?: [\w ,]{0,40}?)? (?:is|would be|will be)\b"
          r"|(?:^|\n)\s*(?:the )?(?:best|optimal) (?:option|choice)\s*:"
          r"|my (?:choice|answer|decision|selection|pick)(?: [\w ,]{0,20}?)? (?:is|would be)\b"
          r"|answer is|I would go for|\b(?:select|choose|pick)(?:ing)? the option)")   # a conclusion, not "To determine the best option ..."
SUPERLATIVE = r"\b(best|highest|optimal|maximi[sz]e|most (?:appealing|attractive|favorable|beneficial))"


def parse_discrete(text: str, options=None, allow_option_number=False):
    """Return (option_index 0..10, valid).
    Paraphrased prompts (allow_option_number=True): "Option 7".
    Original prompts: the model names the pair, e.g. "I choose ($52.80, $12.00)". Replies often list
    several options before concluding, so we take the first matching pair after the LAST decision word
    (choose / select / best option ...). Without a decision word, a reply is valid only if it names
    exactly one of the 11 options. A reply cut off before the choice is therefore invalid."""
    if not text:
        return None, False
    if allow_option_number:
        m = re.search(r"option\s*#?\s*(\d+)", text, flags=re.I)
        if m and 1 <= int(m.group(1)) <= C.N_DISCRETE_OPTIONS:
            return int(m.group(1)) - 1, True
    if not options:
        return None, False
    t = text.replace(",", ", ").replace("**", "")
    pat = r"\(\s*\$?\s*" + NUM + r"\s*(?:Kg)?\s*,\s*\$?\s*" + NUM

    def match(xa, xb):
        for j, (oa, ob) in enumerate(options):
            if abs(float(xa) - oa) < 0.011 and abs(float(xb) - ob) < 0.011:
                return j
        return None

    hits = [(mo.start(), match(*mo.groups())) for mo in re.finditer(pat, t, flags=re.I)]
    hits = [(pos, j) for pos, j in hits if j is not None]
    if not hits:
        return None, False
    decide = [mo.start() for mo in re.finditer(DECIDE, t, flags=re.I)]
    if decide:
        after = [j for pos, j in hits if pos > decide[-1]]
        if after:
            return after[0], True
    distinct = {j for _, j in hits}
    if len(distinct) == 1:
        return distinct.pop(), True
    # last resort: the last sentence that praises exactly one option ("... offers the highest return")
    for sent in reversed(re.split(r"(?<=[.!?])\s+|\n+", t)):
        if re.search(SUPERLATIVE, sent, flags=re.I):
            js = {match(*mo.groups()) for mo in re.finditer(pat, sent, flags=re.I)} - {None}
            if len(js) == 1:
                return js.pop(), True
    return None, False
```

### 5.5 `src/llm_client.py`：API 调用

`LLM_KEY_HEADER` 非空时，会把密钥额外放进该名字的请求头（HKUST 网关需要 `api-key`）。直接用 OpenAI 时留空即可。

```python
"""Thin wrapper around the OpenAI Python SDK (works with any OpenAI-compatible endpoint)."""
import time
import config as C


def make_client():
    if C.PROVIDER == "azure":
        from openai import AzureOpenAI
        return AzureOpenAI(api_key=C.API_KEY, azure_endpoint=C.AZURE_ENDPOINT,
                           api_version=C.AZURE_API_VERSION, timeout=60, max_retries=0)
    from openai import OpenAI
    # timeout=60: a hung request fails after 60 s instead of the SDK default of 10 min;
    # max_retries=0: retries are handled (and printed) by chat() below
    kw = {"api_key": C.API_KEY or "not-needed", "timeout": 60, "max_retries": 0}
    if C.BASE_URL:
        kw["base_url"] = C.BASE_URL
    if C.KEY_HEADER:                      # e.g. HKUST GenAI gateway expects header "api-key: <key>"
        kw["default_headers"] = {C.KEY_HEADER: C.API_KEY}
    return OpenAI(**kw)


def chat(client, messages, temperature, model=C.MODEL, max_tokens=C.MAX_TOKENS, retries=8):
    """One chat call with exponential back-off. Returns (text, usage_dict).
    Raises RuntimeError if every retry fails, so the subject is NOT saved and gets rerun later."""
    for attempt in range(retries):
        try:
            kw = {"max_tokens": max_tokens} if max_tokens else {}
            r = client.chat.completions.create(model=model, messages=messages, temperature=temperature, **kw)
            u = getattr(r, "usage", None)
            usage = {"in": getattr(u, "prompt_tokens", 0), "out": getattr(u, "completion_tokens", 0)}
            return (r.choices[0].message.content or "").strip(), usage
        except Exception as e:   # rate limit, timeout, 5xx ...
            wait = min(60, 2 ** attempt)
            print(f"  API error ({type(e).__name__}: {e}); retry in {wait}s")
            time.sleep(wait)
    raise RuntimeError(f"API still failing after {retries} attempts")


def credit_balance():
    """Remaining credit on the HKUST GenAI gateway, or None if not available (other providers)."""
    if not (C.BASE_URL and "hkust-genai" in C.BASE_URL and C.API_KEY):
        return None
    import json, urllib.request
    try:
        req = urllib.request.Request(C.BASE_URL.rstrip("/") + "/balance", headers={"api-key": C.API_KEY})
        with urllib.request.urlopen(req, timeout=30) as r:
            return float(json.loads(r.read().decode())["credit"])
    except Exception:
        return None
```

### 5.6 `src/experiment.py`：一个被试 = 一段对话

`MockClient` 是一个 CES 效用最大化者，让你可以离线跑通整个流程。它**不是** GPT 的模型，只是为了在花钱买 token 之前把 bug 找出来。

价格框架条件下，模型看到的是四舍五入到两位小数的 1/M，所以我们记录它实际看到的**有效**价格（M_eff = 1 / round(1/M, 2)）。否则单是四舍五入就可能制造出与模型无关的微小 GARP 违反。

```python
"""Run one GPT 'subject': opening messages, 3 comprehension questions, 25 decision rounds."""
import re
import numpy as np
import config as C
from src import prompt_api as P
from src.prices import draw_prices, subject_seed, discrete_options
from src.parse import parse_continuous, parse_discrete
from src.llm_client import chat


class MockClient:
    """Offline stand-in for an LLM: a noisy CES utility maximiser. Lets you test the whole
    pipeline without spending API credit. Not a model of GPT. Understands both prompt sets."""

    def __init__(self, alpha=0.6, rho=0.3, noise=0.0, seed=0):
        self.alpha, self.rho, self.noise = alpha, rho, noise
        self.rng = np.random.default_rng(seed)

    def reply(self, messages):
        last = messages[-1]["content"]
        if not ("What is your allocation?" in last or "Which is the best?" in last) or "Suppose" in last \
                or "Why?" in last:
            return "Understood."
        nums = [float(v) for v in re.findall(r"(\d+\.\d+)", last)]
        if "options" in last:   # discrete: option 1 = (0, 100N), option 2 = (10M, 90N)
            pairs = list(zip(nums[0::2], nums[1::2]))
            m, n = pairs[1][0] / 10, pairs[0][1] / 100
            a = self._optimum(m, n)
            j = int(np.argmin([abs(10 * k - a) for k in range(len(pairs))]))
            if "Option 1:" in last:                       # paraphrased prompts
                return f"Option {j + 1}"
            return f"I choose (${pairs[j][0]:.2f}, ${pairs[j][1]:.2f})."
        if " 1 dollar" in last or " 1 Kg" in last:       # inverse framing: numbers are 1/M, 1/N
            m, n = 1 / nums[0], 1 / nums[1]
        else:
            m, n = nums[0], nums[1]
        a = round(self._optimum(m, n))
        return f"I would put {a} points in the first and {100 - a} points in the second."

    def _optimum(self, m, n):
        # share of points on A for CES u = [a xA^r + (1-a) xB^r]^(1/r), prices 1/M, 1/N
        ra = self.rho / (1 - self.rho)
        g = (self.alpha / (1 - self.alpha)) ** (1 / (1 - self.rho))
        share = g / ((n / m) ** ra + g)        # pA/pB = (1/M)/(1/N) = N/M
        share = np.clip(share + self.noise * self.rng.normal(), 0, 1)
        return 100 * share


def _ask(client, messages, temperature):
    if isinstance(client, MockClient):
        return client.reply(messages), {"in": 0, "out": 0}
    return chat(client, messages, temperature)


def run_subject(client, domain, cond_name, rep, keep_transcript=True):
    cfg = C.CONDITIONS[cond_name]
    rng = np.random.default_rng(subject_seed(domain, cond_name, rep))
    prices = draw_prices(rng)
    msgs = P.opening_messages(domain, cfg)
    usage = {"in": 0, "out": 0}
    tests = []
    for q in P.test_questions(domain, cfg):          # comprehension check, kept in the history
        msgs.append({"role": "user", "content": q})
        ans, u = _ask(client, msgs, cfg["temperature"])
        msgs.append({"role": "assistant", "content": ans})
        tests.append(ans)
        usage = {k: usage[k] + u[k] for k in usage}
    rows = []
    lab_a, lab_b = P.labels(domain)
    for r, (m, n) in enumerate(prices, start=1):
        msgs.append({"role": "user", "content": P.round_message(domain, cfg, r, m, n)})
        ans, u = _ask(client, msgs, cfg["temperature"])
        msgs.append({"role": "assistant", "content": ans})
        usage = {k: usage[k] + u[k] for k in usage}
        if cfg["choice"] == "discrete":
            j, ok = parse_discrete(ans, P.option_values(m, n), allow_option_number=(C.PROMPT_SET != "paper"))
            a, b = (discrete_options(m, n)[j][0], discrete_options(m, n)[j][1]) if ok else (None, None)
        else:
            a, b, ok = parse_continuous(ans, lab_a, lab_b)
        if cfg["framing"] == "inverse":   # the model saw 1/M rounded to 2 decimals: use what it saw
            m, n = 1 / round(1 / m, 2), 1 / round(1 / n, 2)
        rows.append(dict(condition=cond_name, domain=domain, rep=rep, round=r, M=m, N=n,
                         points_a=a, points_b=b, valid=bool(ok), reply=ans, prompts=C.PROMPT_SET))
    meta = dict(condition=cond_name, domain=domain, rep=rep, prompts=C.PROMPT_SET, model=C.MODEL,
                usage=usage, tests=tests, transcript=msgs if keep_transcript else None)
    return rows, meta
```

### 5.7 `src/rp.py`：显示偏好引擎

**定义（一个有 N 个选择的被试）。** E[i, j] = p_i · x_j。
- Direct revealed preference (直接显示偏好)：若 E[i,i] ≥ E[i,j]，则 x_i R⁰ x_j（选 x_i 时 x_j 买得起）。
- Strict (严格)：若 E[i,i] > E[i,j]，则 x_i P⁰ x_j。
- R = R⁰ 的 transitive closure (传递闭包)。
- **GARP** (广义显示偏好公理)：不存在 x_i R x_j 且 x_j P⁰ x_i 的一对。
- **Afriat's theorem (Afriat 定理)**：GARP ⇔ 数据可以被一个连续、凹、严格递增的效用函数解释。
- **CCEI** (临界成本效率指数)：把每个预算缩小到 e · E[i,i] 后 GARP 仍成立的最大 e ≤ 1。解读：1 − CCEI 是最严重的不一致所"浪费"的资金比例。

**算法。** 显示偏好关系只在比值 E[i,j]/E[i,i] 处发生变化，所以 CCEI 必然是这些比值之一。GARP_e 关于 e 单调，因此对排序后的候选值做二分查找，并在每个候选值的略下方检验（上确界不一定能取到）。`00_selftest.py` 会把它与精细网格和手算例子对照。

**其他指数（SI 的稳健性检验）。**
- **HMI** (Houtman–Maks 指数)：能同时满足 GARP 的观测所占的最大比例。在涉及违反的观测上做精确搜索（实际很快）；搜索量过大时退回贪心算法，并加以标记。
- **MPI** (money pump index, 货币泵指数)：每个违反循环中套利者能榨取的金额占支出的比例。两种商品时，任何 GARP 违反都意味着存在二元循环违反（Rose 1958，论文引用了这一点），所以我们在违反的二元循环上取平均。这是对一般循环 MPI 的简化，报告中要写明。
- **MCI** (minimum cost index, 最小成本指数; Dean & Martin 2016)：为使剩余关系一致所需删除的显示偏好关系的最小成本，成本 = (E[i,i] − E[i,j]) / Σ E[k,k]。用一个小型 MILP 精确求解。
- **Bronars test (Bronars 检验)**：在每条预算线上均匀随机选点的随机被试的 CCEI。如果几乎都违反 GARP，说明设计有足够的检验效力发现非理性。

```python
"""Revealed-preference toolkit: GARP, CCEI (Afriat), HMI, MPI, MCI, Bronars power test.

Inputs for one subject:
  P : (n, k) prices,  X : (n, k) chosen quantities.
E[i, j] = p_i . x_j  = cost of bundle j at the prices of round i.
x_i is directly revealed preferred to x_j  (x_i R0 x_j)  if  E[i, i] >= E[i, j].
"""
from itertools import combinations
import numpy as np

TOL = 1e-9


def cost_matrix(P, X):
    return np.asarray(P, float) @ np.asarray(X, float).T


def closure(R):
    """Transitive closure (Warshall)."""
    R = R.copy()
    for k in range(R.shape[0]):
        R |= R[:, [k]] & R[[k], :]
    return R


def garp_ok(E, e=1.0, keep=None):
    """True if GARP holds at efficiency e (Afriat: compare e * own expenditure)."""
    own = np.diag(E)[:, None]
    R0 = e * own >= E - TOL          # weak direct revealed preference
    S0 = e * own > E + TOL           # strict direct revealed preference
    if keep is not None:
        R0, S0 = R0[np.ix_(keep, keep)], S0[np.ix_(keep, keep)]
    Rc = closure(R0)
    return not np.any(Rc & S0.T)     # x_i R* x_j and x_j P0 x_i  -> violation


def n_violations(E):
    """Number of ordered pairs (i, j) with x_i R* x_j and x_j P0 x_i."""
    own = np.diag(E)[:, None]
    Rc = closure(own >= E - TOL)
    return int(np.sum(Rc & (own > E + TOL).T))


def ccei(P, X):
    """Critical cost efficiency index in [0, 1] = sup{e : GARP holds at efficiency e}.
    Exact: the relations only change at the ratios E_ij / E_ii, so the sup is one of them
    (or 1). GARP_e is monotone in e, so we binary-search the sorted candidates, testing just
    below each candidate (the sup itself may not be attained)."""
    E = cost_matrix(P, X)
    if garp_ok(E, 1.0):
        return 1.0
    own = np.diag(E)
    ratios = np.unique((E / own[:, None])[~np.eye(len(E), dtype=bool)])
    cand = np.r_[np.sort(ratios[(ratios < 1) & (ratios > 0)]), 1.0]
    lo, hi, best = 0, len(cand) - 1, 0.0
    while lo <= hi:
        mid = (lo + hi) // 2
        if garp_ok(E, cand[mid] * (1 - 1e-9)):
            best, lo = cand[mid], mid + 1
        else:
            hi = mid - 1
    return float(best)


def hmi(P, X, max_checks=2_000_000):
    """Houtman-Maks index: largest share of observations that jointly satisfy GARP.
    Exact search over observations involved in violations; greedy fallback if too many."""
    E = cost_matrix(P, X)
    n = len(E)
    if garp_ok(E):
        return 1.0, True
    own = np.diag(E)[:, None]
    Rc = closure(own >= E - TOL)
    V = Rc & (own > E + TOL).T
    involved = sorted(set(np.where(V)[0]) | set(np.where(V)[1]))
    checks = 0
    for k in range(1, len(involved) + 1):
        for drop in combinations(involved, k):
            checks += 1
            if checks > max_checks:
                return _hmi_greedy(E), False
            keep = [i for i in range(n) if i not in drop]
            if garp_ok(E, 1.0, keep):
                return (n - k) / n, True
    return 1 / n, True


def _hmi_greedy(E):
    keep = list(range(len(E)))
    while not garp_ok(E, 1.0, keep):
        sub = E[np.ix_(keep, keep)]
        own = np.diag(sub)[:, None]
        V = closure(own >= sub - TOL) & (own > sub + TOL).T
        worst = int(np.argmax(V.sum(0) + V.sum(1)))
        keep.pop(worst)
    return len(keep) / len(E)


def mpi(P, X):
    """Money pump index (Echenique, Lee & Shum 2011) over violating 2-cycles.
    With two goods every GARP violation implies a 2-cycle violation (Rose 1958), so 2-cycles suffice
    to detect violations; we report the mean and max MPI over those cycles (0 if none)."""
    E = cost_matrix(P, X)
    own = np.diag(E)
    vals = []
    for i, j in combinations(range(len(E)), 2):
        a = own[i] - E[i, j]          # money saved at prices i by buying x_j instead of x_i
        b = own[j] - E[j, i]
        if (a >= -TOL and b > TOL) or (a > TOL and b >= -TOL):
            vals.append((a + b) / (own[i] + own[j]))
    return (float(np.mean(vals)), float(np.max(vals))) if vals else (0.0, 0.0)


def mci(P, X):
    """Minimum cost index (Dean & Martin 2016): cheapest set of direct revealed-preference relations
    to drop so the rest is GARP-consistent. Cost of dropping x_i R0 x_j = (E_ii - E_ij) / sum_k E_kk.
    Solved as a small MILP with utility levels U (weak edge: U_i >= U_j; strict edge: U_i >= U_j + 1)."""
    from scipy.optimize import milp, LinearConstraint, Bounds
    E = cost_matrix(P, X)
    if garp_ok(E):
        return 0.0
    n = len(E)
    own = np.diag(E)
    edges = [(i, j) for i in range(n) for j in range(n) if i != j and own[i] >= E[i, j] - TOL]
    m = len(edges)
    M = n + 2
    # variables: U_0..U_{n-1} (continuous in [0, n]), b_0..b_{m-1} (binary drop indicators)
    c = np.r_[np.zeros(n), [(own[i] - E[i, j]) / own.sum() for i, j in edges]]
    A = np.zeros((m, n + m))
    lb = np.zeros(m)
    for r, (i, j) in enumerate(edges):
        A[r, i], A[r, j], A[r, n + r] = 1, -1, M          # U_i - U_j + M b >= need
        lb[r] = 1.0 if own[i] > E[i, j] + TOL else 0.0
    res = milp(c, constraints=LinearConstraint(A, lb, np.inf),
               integrality=np.r_[np.zeros(n), np.ones(m)],
               bounds=Bounds(np.r_[np.zeros(n), np.zeros(m)], np.r_[np.full(n, n), np.ones(m)]))
    return float(res.fun) if res.success else np.nan


def bronars(P, rng, n_sim=1000):
    """Random choosers: uniform share of budget on each line (Bronars 1987). Returns CCEI array.
    P are prices with income normalised so that p . x = 100 points."""
    P = np.asarray(P, float)
    out = np.empty(n_sim)
    for s in range(n_sim):
        share = rng.uniform(0, 1, len(P))
        X = np.column_stack([share * 100 / P[:, 0], (1 - share) * 100 / P[:, 1]])
        out[s] = ccei(P, X)
    return out
```

### 5.8 `src/demand.py`：需求向下倾斜

为什么需要它：总是选同一个角点或 50/50 分配的被试也能通过 GARP。如果被试真的在对价格作出反应，ln(xA/xB) 与 ln(pA/pB) 的 Spearman 相关应为负。角点加 0.1 点（预算的 0.1%），使对数有定义。

```python
"""Downward-sloping demand: Spearman correlation of ln(xA/xB) with ln(pA/pB) per subject."""
import numpy as np
from scipy.stats import spearmanr
import config as C


def spearman_subject(points_a, points_b, M, N):
    a = np.maximum(np.asarray(points_a, float), C.CORNER_ADJ_POINTS)   # 0.1% of budget at corners
    b = np.maximum(np.asarray(points_b, float), C.CORNER_ADJ_POINTS)
    M, N = np.asarray(M, float), np.asarray(N, float)
    log_x = np.log((a * M) / (b * N))
    log_p = np.log((1 / M) / (1 / N))
    if np.ptp(log_x) == 0:          # identical choices in every round -> undefined
        return np.nan
    return float(spearmanr(log_x, log_p).statistic)
```

### 5.9 `src/estimate.py`：用 Tobit 估计偏好参数

由各效用函数的一阶条件（论文 Materials and Methods）可得：

share₁ = p₁x₁ / E = g / ((p₁/p₂)^r + g)，其中 r = ρ/(1−ρ)，g = [α/(1−α)]^{1/(1−ρ)}。

- 风险：disappointment aversion (失望厌恶) 形式 U = α u(x_high) + (1−α) u(x_low)，u(z) = z^ρ/ρ（ρ = 0 时为 ln z）。商品 1 = 较大的结果。α = 0.5 即 expected utility (期望效用)；θ = 1 − ρ 是 relative risk aversion (相对风险厌恶)。
- 时间：U = α u(today) + (1−α) u(later)。α > 0.5 表示没耐心。
- 社会、食物：CES 效用 U = [α x₁^ρ + (1−α) x₂^ρ]^{1/ρ}。α = 放在自己（社会）或肉（食物）上的权重；ρ → 1 为完全替代（efficiency-oriented, 效率导向），ρ → 0 为 Cobb–Douglas，ρ → −∞ 为 Leontief（equality-oriented, 平等导向）。

由于以点数计的支出就等于分配的点数，share₁ = 商品 1 上的点数 / 100。角点份额（0 或 1）是截断的，所以使用 **two-limit Tobit** (双边截尾 Tobit) 似然函数。参数化方式：α ∈ (0,1) 用 logit，ρ < 1 用 ρ = 1 − e^θ（论文限定 ρ ≤ 1，因为 ρ > 1 和 ρ = 1 产生相同的角点选择）。先用粗网格选初值，再用 Nelder–Mead 精细优化。

```python
"""Structural estimation of (alpha, rho) by two-limit (nonlinear) Tobit on expenditure shares.

Paper, Materials and Methods: for all four domains the first-order condition gives
    share_1 = p1 x1 / E = g / ((p1/p2)^r + g),   r = rho / (1 - rho),  g = [alpha / (1 - alpha)]^(1/(1 - rho)).
Shares are censored at 0 and 1 (corner choices) -> two-limit Tobit maximum likelihood.
  risk  : good 1 = the better (larger) outcome, alpha = weight on it (disappointment aversion, Gul 1991)
  time  : good 1 = today,     alpha = weight on today
  social: good 1 = self,      alpha = weight on self
  food  : good 1 = ham meat,  alpha = weight on meat
Because the expenditure share in this design equals points/100, share_1 = points on good 1 / 100.
"""
import numpy as np
from scipy.optimize import minimize
from scipy.stats import norm
from scipy.special import expit


def shares_and_prices(domain, points_a, points_b, M, N):
    a = np.asarray(points_a, float) / 100
    M, N = np.asarray(M, float), np.asarray(N, float)
    pa_pb = N / M                                  # (1/M) / (1/N)
    if domain == "risk":                           # reorder: good 1 = larger quantity
        xa, xb = a * 100 * M, (1 - a) * 100 * N
        first_is_a = xa >= xb
        s = np.where(first_is_a, a, 1 - a)
        ratio = np.where(first_is_a, pa_pb, 1 / pa_pb)
    else:
        s, ratio = a, pa_pb
    return s, ratio


def _unpack(theta):
    alpha = 1 / (1 + np.exp(-theta[0]))           # (0, 1)
    rho = 1 - np.exp(theta[1])                    # (-inf, 1)
    sigma = np.exp(theta[2])
    return alpha, rho, sigma


def predicted_share(alpha, rho, ratio):
    """g / (ratio^r + g), computed in logs to avoid overflow: expit(ln g - r ln ratio)."""
    r = rho / (1 - rho)
    log_g = np.log(alpha / (1 - alpha)) / (1 - rho)
    return expit(log_g - r * np.log(ratio))


def negloglik(theta, s, ratio, eps=1e-6):
    alpha, rho, sigma = _unpack(theta)
    mu = predicted_share(alpha, rho, ratio)
    lo, hi = s <= eps, s >= 1 - eps
    mid = ~(lo | hi)
    ll = np.zeros_like(s)
    ll[lo] = norm.logcdf((0 - mu[lo]) / sigma)
    ll[hi] = norm.logsf((1 - mu[hi]) / sigma)
    ll[mid] = norm.logpdf((s[mid] - mu[mid]) / sigma) - np.log(sigma)
    v = -np.sum(ll)
    return v if np.isfinite(v) else 1e12


def fit(s, ratio):
    """Return dict(alpha, rho, sigma, nll, ok).
    A coarse grid over (alpha, rho, sigma) picks the two best starting points; Nelder-Mead refines them."""
    s, ratio = np.asarray(s, float), np.asarray(ratio, float)
    grid = [(a, r, sg) for a in np.linspace(-2.5, 2.5, 11)            # logit(alpha)
            for r in np.log([0.02, 0.1, 0.3, 0.6, 1.0, 1.5, 2.5, 5.0, 10.0])   # rho = 1 - e^r
            for sg in np.log([0.02, 0.1, 0.3])]
    vals = np.array([negloglik(g, s, ratio) for g in grid])
    best = None
    for k in np.argsort(vals)[:2]:
        res = minimize(negloglik, x0=list(grid[k]), args=(s, ratio), method="Nelder-Mead",
                       options={"maxiter": 3000, "xatol": 1e-6, "fatol": 1e-8})
        if best is None or res.fun < best.fun:
            best = res
    alpha, rho, sigma = _unpack(best.x)
    return dict(alpha=alpha, rho=rho, sigma=sigma, nll=best.fun, ok=bool(best.success))
```

### 5.10 `src/stats.py`、`src/dataio.py`

论文只说"two-sided two-sample t-tests"，没说是否假设方差相等。我们用 Welch t 检验（GPT 方差极小，Welch 更保守），并在报告中注明。

```python
"""Tests used in the paper: two-sample and one-sample t-tests, Levene, OLS with robust SE."""
import warnings
import numpy as np
from scipy import stats

warnings.filterwarnings("ignore", category=RuntimeWarning)   # near-constant samples (e.g. all CCEI = 1)


def two_sample(a, b):
    """Two-sided two-sample t-test (Welch; the paper does not say which variant)."""
    a, b = np.asarray(a, float), np.asarray(b, float)
    a, b = a[~np.isnan(a)], b[~np.isnan(b)]
    t = stats.ttest_ind(a, b, equal_var=False)
    return dict(mean_a=a.mean(), mean_b=b.mean(), n_a=len(a), n_b=len(b), t=t.statistic, p=t.pvalue)


def one_sample(a, mu):
    a = np.asarray(a, float)
    a = a[~np.isnan(a)]
    t = stats.ttest_1samp(a, mu)
    return dict(mean=a.mean(), mu=mu, n=len(a), t=t.statistic, p=t.pvalue)


def levene(a, b):
    a, b = np.asarray(a, float), np.asarray(b, float)
    r = stats.levene(a[~np.isnan(a)], b[~np.isnan(b)])
    return dict(sd_a=np.nanstd(a, ddof=1), sd_b=np.nanstd(b, ddof=1), W=r.statistic, p=r.pvalue)


def ols_hc1(y, X, names):
    """OLS with HC1 robust standard errors. X must already include a constant column."""
    y, X = np.asarray(y, float), np.asarray(X, float)
    n, k = X.shape
    XtX_inv = np.linalg.inv(X.T @ X)
    beta = XtX_inv @ X.T @ y
    u = y - X @ beta
    V = XtX_inv @ (X.T * u**2) @ X @ XtX_inv * n / (n - k)
    se = np.sqrt(np.diag(V))
    t = beta / se
    p = 2 * stats.t.sf(np.abs(t), n - k)
    return [dict(term=nm, coef=b, se=s, t=tt, p=pp) for nm, b, s, tt, pp in zip(names, beta, se, t, p)]
```

```python
"""Load choices into one tidy table.

Columns: source (model label / Human), condition, domain, rep (subject id), round, M, N,
         points_a, points_b, valid
GPT choices come from data/raw/*.jsonl (written by scripts/02_run_llm.py).
Human choices (optional) come from data/human.csv with the same columns except source/valid.
"""
import json
import numpy as np
import pandas as pd
import config as C



def read_jsonl(path):
    """Read a .jsonl file, skipping a line cut short by a forced stop (e.g. closing the terminal)."""
    out = []
    with open(path, encoding="utf-8") as fh:
        for line in fh:
            if line.strip():
                try:
                    out.append(json.loads(line))
                except json.JSONDecodeError:
                    print(f"  skipped a broken line in {path.name}")
    return out


def load_gpt():
    """Your model's choices: data/raw (original prompts) and data/raw_paraphrase (paraphrased prompts),
    plus any other models copied to data/extra/<label>/."""
    frames = []
    sets = [(C.DATA / "raw", C.SOURCE_LABEL), (C.DATA / "raw_paraphrase", C.PARA_LABEL)]
    extra = C.DATA / "extra"
    if extra.exists():
        sets += [(d, d.name) for d in sorted(extra.glob("*")) if d.is_dir()]
    for folder, label in sets:
        rows = [r for f in sorted(folder.glob("*.jsonl")) for r in read_jsonl(f)] if folder.exists() else []
        if rows:
            frames.append(pd.DataFrame(rows).assign(source=label))
    return pd.concat(frames, ignore_index=True) if frames else pd.DataFrame()


def load_human():
    f = C.DATA / "human.csv"
    if not f.exists():
        return pd.DataFrame()
    df = pd.read_csv(f)
    df["source"] = "Human"
    df["valid"] = df["points_a"].notna() & df["points_b"].notna()
    return df


def load_all():
    df = pd.concat([load_gpt(), load_human()], ignore_index=True)
    if df.empty:
        raise SystemExit("No choice data found. Run scripts/02_run_llm.py first.")
    return df


def subject_arrays(g):
    """From one subject's valid rows -> (P, X) for revealed-preference tests."""
    g = g[g["valid"]]
    M, N = g["M"].to_numpy(float), g["N"].to_numpy(float)
    P = np.column_stack([1 / M, 1 / N])
    X = np.column_stack([g["points_a"].to_numpy(float) * M, g["points_b"].to_numpy(float) * N])
    return P, X


def append_authors(df, name):
    """Append the authors' subject-level file data/authors_<name>.csv if it exists (07_import_authors.py)."""
    f = C.DATA / f"authors_{name}.csv"
    if not f.exists():
        return df
    return pd.concat([df, pd.read_csv(f)], ignore_index=True)
```

### 5.11 脚本

`scripts/00_selftest.py`：在做任何事情之前先跑它。
```python
"""Check the analysis code before spending any API credit. Run: python scripts/00_selftest.py"""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
import numpy as np
from src import rp
from src.estimate import predicted_share, fit, shares_and_prices
from src.prices import draw_prices
from src.parse import parse_continuous, parse_discrete
from src import prompts as Pm

ok = True


def check(name, cond):
    global ok
    print(("PASS " if cond else "FAIL ") + name)
    ok &= bool(cond)


# 1. textbook GARP violation: two budget lines, each choice affordable and cheaper on the other line
P = np.array([[1, 2], [2, 1.]]); X = np.array([[1, 4], [4, 1.]])
check("CCEI = 2/3 on the two-line example", abs(rp.ccei(P, X) - 2 / 3) < 1e-9)
check("HMI = 1/2", rp.hmi(P, X)[0] == 0.5)
check("MPI = 1/3", abs(rp.mpi(P, X)[0] - 1 / 3) < 1e-9)
check("MCI = 1/6", abs(rp.mci(P, X) - 1 / 6) < 1e-6)

# 2. an exact CES maximiser is perfectly rational
rng = np.random.default_rng(0)
pr = draw_prices(rng); M, N = pr[:, 0], pr[:, 1]
share = predicted_share(0.6, 0.3, N / M)
Pp = np.column_stack([1 / M, 1 / N]); Xp = np.column_stack([share * 100 * M, (1 - share) * 100 * N])
check("CES agent: CCEI = 1, HMI = 1, MCI = 0",
      rp.ccei(Pp, Xp) == 1 and rp.hmi(Pp, Xp)[0] == 1 and rp.mci(Pp, Xp) == 0)

# 3. random choosers usually violate GARP (Bronars power)
viol = np.mean(rp.bronars(Pp, rng, 300) < 1)
check(f"Bronars: {viol:.1%} of random subjects violate GARP (paper: 99.9%)", viol > 0.95)

# 4. Tobit recovers known parameters
pr = np.vstack([draw_prices(rng) for _ in range(40)]); M, N = pr[:, 0], pr[:, 1]
for a0, r0 in [(0.6, 0.3), (0.5, -1.0), (0.75, 0.6)]:
    s = np.clip(predicted_share(a0, r0, N / M) + 0.03 * rng.normal(size=len(M)), 0, 1)
    e = fit(s, N / M)
    check(f"Tobit recovers alpha={a0}, rho={r0} -> {e['alpha']:.3f}, {e['rho']:.3f}",
          abs(e["alpha"] - a0) < 0.03 and abs(e["rho"] - r0) < 0.1)

# 5. parser
check("parse 'Asset A: 30, Asset B: 70'", parse_continuous("Asset A: 30, Asset B: 70", "Asset A", "Asset B")[2])
check("parse 'I choose Option 4.' (paraphrase)", parse_discrete("I choose Option 4.", allow_option_number=True) == (3, True))
check("reject 'A: 80, B: 80'", not parse_continuous("A: 80, B: 80", "A", "B")[2])
r = parse_continuous("I will invest 60 points in Asset A and 40 points in Asset B, which returns 52.8 dollars.", "Asset A", "Asset B")
check("parse free text with dollar amounts -> 60/40", r[2] and round(r[0]) == 60)
r = parse_continuous("Today: 100 points\nOne month later: 0 points", "today", "one month later")
check("parse 'Today: 100 points / One month later: 0 points'", r[2] and round(r[0]) == 100)
from src.prices import discrete_options
opts = [(o[2], o[3]) for o in discrete_options(0.88, 0.30)]
check("parse discrete pair '($52.80, $12.00)' -> option 7", parse_discrete("My best option is ($52.80, $12.00).", opts) == (6, True))
listing = "To determine the best option: 1. ($0.00, $30.00) -> 30 2. ($8.80, $27.00) -> 35.8 ... Therefore, I choose ($88.00, $0.00)."
check("discrete: list of options then choice -> last option", parse_discrete(listing, opts) == (10, True))
check("discrete: 'The best option in this round is (...)' among others",
      parse_discrete("Comparing ($0.00, $30.00) with others, the best option in this round is ($88.00, $0.00).", opts) == (10, True))
check("discrete: superlative sentence fallback",
      parse_discrete("($0.00, $30.00) is safe. However, ($88.00, $0.00) offers the highest potential return.", opts) == (10, True))
check("discrete: list cut off before the choice -> invalid", not parse_discrete("To determine the best option: 1. ($0.00, $30.00) 2. ($8.80, $27.00) 3. ($17", opts)[1])

# 6. prompts render
msg = Pm.round_message("risk", "inverse", "continuous", 1, 0.5, 0.25)
check("inverse framing shows 2.00 and 4.00 points", "2.00 points" in msg and "4.00 points" in msg)
print("\nALL PASSED" if ok else "\nSOME CHECKS FAILED")
```

`scripts/00b_check_api.py`：接通 API 后第一个运行。
```python
"""Check that the API works before running anything: key, model list, credit balance, one call.

  python scripts/00b_check_api.py
"""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
import httpx
import config as C
from src.llm_client import make_client

print(f"provider={C.PROVIDER}  base_url={C.BASE_URL}  model={C.MODEL}  key_header={C.KEY_HEADER or '(Bearer)'}")
if not C.API_KEY or C.API_KEY.startswith("<"):
    sys.exit("LLM_API_KEY is empty: fill in .env first.")
client = make_client()

# 1. which models can this key use?
try:
    names = sorted(m.id for m in client.models.list().data)
    print(f"\n{len(names)} models available:\n  " + "\n  ".join(names))
except Exception as e:
    print(f"\nCould not list models ({type(e).__name__}: {e}).\n"
          "Take model names from your provider's 'supported models' page instead.")

# 2. credit balance (HKUST gateway only)
if C.BASE_URL and "hkust-genai" in C.BASE_URL:
    try:
        r = httpx.get(C.BASE_URL.rstrip("/") + "/balance", headers={"api-key": C.API_KEY}, timeout=30)
        print(f"\nBalance (HTTP {r.status_code}): {r.text[:500]}")
    except Exception as e:
        print(f"\nBalance check failed: {e}")

# 3. one tiny call with temperature 0
try:
    r = client.chat.completions.create(
        model=C.MODEL, temperature=0, max_tokens=20,
        messages=[{"role": "user", "content": "Reply with exactly: Asset A: 30, Asset B: 70"}])
    print(f"\nTest call OK -> {r.choices[0].message.content!r}  usage={r.usage}")
except Exception as e:
    print(f"\nTest call FAILED: {type(e).__name__}: {e}")
```

`scripts/01_smoke_test.py`
```python
"""Run ONE subject per domain, print the whole conversation, and project the full cost.

  python scripts/01_smoke_test.py --mock                     # offline, no API key needed
  python scripts/01_smoke_test.py --condition baseline       # real API, 4 subjects
  python scripts/01_smoke_test.py --price-in 0.15 --price-out 0.60   # USD per 1M tokens
"""
import argparse, sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
import config as C
from src.experiment import run_subject, MockClient
from src.llm_client import make_client

ap = argparse.ArgumentParser()
ap.add_argument("--condition", default="baseline", choices=list(C.CONDITIONS))
ap.add_argument("--mock", action="store_true")
ap.add_argument("--price-in", type=float, default=0.0, help="USD per 1M input tokens")
ap.add_argument("--price-out", type=float, default=0.0, help="USD per 1M output tokens")
args = ap.parse_args()

client = MockClient() if args.mock else make_client()
tot_in = tot_out = 0
for domain in C.DOMAINS:
    rows, meta = run_subject(client, domain, args.condition, rep=0)
    print(f"\n================ {domain} / {args.condition} / prompts={C.PROMPT_SET} ================")
    for m in meta["transcript"]:
        print(f"[{m['role']}] {m['content']}")
    print("--> parsed choices (points A / points B):",
          "; ".join(f"R{r['round']}: {r['points_a']:.0f}/{r['points_b']:.0f}" if r["valid"] else f"R{r['round']}: INVALID"
                    for r in rows))
    ok = sum(r["valid"] for r in rows)
    print(f"--> valid answers: {ok}/{len(rows)}; tokens in={meta['usage']['in']} out={meta['usage']['out']}")
    tot_in += meta["usage"]["in"]
    tot_out += meta["usage"]["out"]

subjects = len(C.DOMAINS) * C.N_REPS
per_in, per_out = tot_in / len(C.DOMAINS), tot_out / len(C.DOMAINS)
print(f"\nOne condition = {subjects} subjects ~ {per_in * subjects / 1e6:.1f}M input + "
      f"{per_out * subjects / 1e6:.2f}M output tokens")
if args.price_in or args.price_out:
    cost = (per_in * args.price_in + per_out * args.price_out) * subjects / 1e6
    print(f"Estimated cost per condition: USD {cost:.2f}; all {len(C.CONDITIONS)} conditions: "
          f"USD {cost * len(C.CONDITIONS):.2f}")
```

`scripts/02_run_llm.py`
```python
"""Collect GPT choices. Resumable: finished (condition, domain, rep) triples are skipped.

  python scripts/02_run_llm.py --conditions baseline                      # 4 x 100 subjects
  python scripts/02_run_llm.py --conditions price_framing discrete --reps 100
  python scripts/02_run_llm.py --conditions female male --reps 30         # cheaper pass
  python scripts/02_run_llm.py --conditions baseline --mock               # offline pipeline test
Output: data/raw/<condition>.jsonl (one line per round) and data/meta/<condition>.jsonl
(one line per subject: token usage, comprehension answers, full transcript).
A subject is written only after all 25 rounds succeed, so stopping at any time is safe.
Ctrl+C stops the run (with --workers > 1, press it once and wait up to ~1 s).
"""
import argparse, json, os, sys
from concurrent.futures import ThreadPoolExecutor, wait, FIRST_COMPLETED
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
import config as C
from src.experiment import run_subject, MockClient
from src.llm_client import make_client, credit_balance
from src.dataio import read_jsonl

ap = argparse.ArgumentParser()
ap.add_argument("--conditions", nargs="+", default=["baseline"], choices=list(C.CONDITIONS))
ap.add_argument("--domains", nargs="+", default=C.DOMAINS, choices=C.DOMAINS)
ap.add_argument("--reps", type=int, default=C.N_REPS)
ap.add_argument("--workers", type=int, default=1, help="parallel conversations (HKUST gateway: 1-2)")
ap.add_argument("--mock", action="store_true")
args = ap.parse_args()

raw_dir, meta_dir = C.RAW_DIR, C.META_DIR
raw_dir.mkdir(parents=True, exist_ok=True)
meta_dir.mkdir(parents=True, exist_ok=True)


def done_set(cond):
    f = meta_dir / f"{cond}.jsonl"
    return {(d["domain"], d["rep"]) for d in read_jsonl(f)} if f.exists() else set()


class Stop(Exception):
    pass


def check_credit():
    """Stop before the HKUST credit runs out (threshold: LLM_MIN_CREDIT in .env, default 30)."""
    c = None if args.mock else credit_balance()
    if c is None:
        return
    print(f"  credit left: {c:.2f}")
    if c < C.MIN_CREDIT:
        raise Stop(f"credit {c:.2f} is below LLM_MIN_CREDIT={C.MIN_CREDIT:.0f}; top up or lower the threshold")


for cond in args.conditions:
    done = done_set(cond)
    todo = [(d, r) for d in args.domains for r in range(args.reps) if (d, r) not in done]
    print(f"[{cond}] prompts={C.PROMPT_SET} model={C.MODEL}: {len(todo)} subjects to run ({len(done)} already done)")
    client = MockClient(noise=0.02, seed=1) if args.mock else make_client()
    state = {"n": 0, "fails": 0}

    with open(raw_dir / f"{cond}.jsonl", "a", encoding="utf-8") as fr, \
         open(meta_dir / f"{cond}.jsonl", "a", encoding="utf-8") as fm:

        def save(key, get_result):
            """Write one finished subject; count failures; raise Stop after 3 in a row."""
            try:
                rows, meta = get_result()
            except Exception as e:                       # API down: do not save, rerun next time
                state["fails"] += 1
                print(f"  subject {key} not saved ({e}); it will be rerun next time")
                if state["fails"] >= 3:
                    raise Stop("3 subjects failed in a row: the API looks down")
                return
            state["fails"] = 0
            for row in rows:                              # rows first, meta last = "subject finished"
                fr.write(json.dumps(row, ensure_ascii=False) + "\n")
            fm.write(json.dumps(meta, ensure_ascii=False) + "\n")
            fr.flush(); fm.flush()
            state["n"] += 1
            if state["n"] % 20 == 0 or state["n"] == len(todo):
                bad = sum(not r["valid"] for r in rows)
                print(f"  {state['n']}/{len(todo)} done (last subject: {bad} invalid answers)")
                check_credit()

        try:
            check_credit()                                # before starting this condition
            if args.workers <= 1 or args.mock:            # plain loop: Ctrl+C works immediately
                for d, r in todo:
                    save((d, r), lambda d=d, r=r: run_subject(client, d, cond, r))
            else:                                         # threads, polled every second so Ctrl+C works
                ex = ThreadPoolExecutor(max_workers=args.workers)
                futs = {ex.submit(run_subject, client, d, cond, r): (d, r) for d, r in todo}
                pending = set(futs)
                try:
                    while pending:
                        finished, pending = wait(pending, timeout=1, return_when=FIRST_COMPLETED)
                        for fut in finished:
                            save(futs[fut], fut.result)
                finally:
                    ex.shutdown(wait=False, cancel_futures=True)
        except (KeyboardInterrupt, Stop) as e:
            fr.flush(); fm.flush()
            print(f"\nStopped ({str(e) or 'Ctrl+C'}). Finished subjects are saved; rerun the same command to continue.")
            os._exit(1)                                   # do not wait for running threads
```

`scripts/03_indices.py`
```python
"""Rationality indices per subject + Bronars random benchmark.

Output: results/indices.csv   (source, condition, domain, rep, n_valid, CCEI, HMI, MPI_mean, MPI_max, MCI, spearman)
        results/bronars.csv   (domain, sim, CCEI)
        results/table_indices.csv (summary like the paper's text)
"""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
import numpy as np
import pandas as pd
import config as C
from src.dataio import load_all, subject_arrays, append_authors
from src import rp
from src.demand import spearman_subject
from src.prices import draw_prices

df = load_all().drop_duplicates(["source", "condition", "domain", "rep", "round"], keep="last")
out = []
for (src, cond, dom, rep), g in df.groupby(["source", "condition", "domain", "rep"]):
    gv = g[g["valid"]]
    rec = dict(source=src, condition=cond, domain=dom, rep=rep, n_valid=len(gv))
    if len(gv) < C.MIN_VALID_ROUNDS:
        out.append(rec)
        continue
    P, X = subject_arrays(gv)
    h, exact = rp.hmi(P, X)
    m_mean, m_max = rp.mpi(P, X)
    rec.update(CCEI=rp.ccei(P, X), HMI=h, HMI_exact=exact, MPI_mean=m_mean, MPI_max=m_max,
               MCI=rp.mci(P, X), GARP_violations=rp.n_violations(rp.cost_matrix(P, X)),
               spearman=spearman_subject(gv["points_a"], gv["points_b"], gv["M"], gv["N"]),
               # share of rounds with the subject's most frequent allocation: flags fixed rules
               # (always the same option / corner) that pass GARP and look price-responsive
               modal_share=gv["points_a"].round().value_counts().iloc[0] / len(gv),
               corner_share=((gv["points_a"] <= 0.5) | (gv["points_b"] <= 0.5)).mean())
    out.append(rec)
ind = append_authors(pd.DataFrame(out), "indices")      # paper's GPT-3.5 and human subjects, if imported
ind.to_csv(C.RESULTS / "indices.csv", index=False)

# Bronars (1987): uniform random choices on the same kind of budget lines
rng = np.random.default_rng(C.SEED_BASE)
br = []
for dom in C.DOMAINS:
    for s in range(C.N_BRONARS):
        pr = draw_prices(rng)
        P = np.column_stack([1 / pr[:, 0], 1 / pr[:, 1]])
        br.append(dict(domain=dom, sim=s, CCEI=rp.bronars(P, rng, 1)[0]))
br = pd.DataFrame(br)
br.to_csv(C.RESULTS / "bronars.csv", index=False)

summ = (ind.dropna(subset=["CCEI"])
        .groupby(["source", "condition", "domain"])
        .agg(n=("CCEI", "size"), CCEI_mean=("CCEI", "mean"),
             share_CCEI_1=("CCEI", lambda s: (s >= 1 - 1e-9).mean()),
             share_CCEI_below_0_9=("CCEI", lambda s: (s < 0.9).mean()),
             HMI_mean=("HMI", "mean"), MPI_mean=("MPI_mean", "mean"), MCI_mean=("MCI", "mean"),
             spearman_mean=("spearman", "mean"),
             share_spearman_neg=("spearman", lambda s: (s < 0).mean()),
             modal_share_mean=("modal_share", "mean"), corner_share_mean=("corner_share", "mean"))
        .reset_index())
summ.to_csv(C.RESULTS / "table_indices.csv", index=False)
viol = br.groupby("domain")["CCEI"].apply(lambda s: (s < 1).mean())
print(summ.round(3).to_string(index=False))
print("\nBronars: share of random subjects violating GARP\n", viol.round(3).to_string())
```

`scripts/04_estimate.py`
```python
"""Preference parameters (alpha, rho): pooled (SI Table S2) and individual (Fig. 3, SI Table S3).

Only subjects with CCEI >= 0.95 are used. The paper does not estimate preferences in the
price-framing and discrete conditions (rationality too low), so those are skipped here too.
Output: results/params_pooled.csv, results/params_individual.csv
"""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
import numpy as np
import pandas as pd
import config as C
from src.dataio import load_all, append_authors
from src.estimate import shares_and_prices, fit

SKIP = {"price_framing", "discrete"}
df = load_all().drop_duplicates(["source", "condition", "domain", "rep", "round"], keep="last")
df = df[df["valid"] & ~df["condition"].isin(SKIP)]
ind = pd.read_csv(C.RESULTS / "indices.csv")
keep = ind[ind["CCEI"] >= C.CCEI_CUTOFF_FOR_ESTIMATION][["source", "condition", "domain", "rep"]]
keep = keep[keep.source.isin(set(df.source))].astype({"rep": int})   # authors' rows are already estimated
df = df.merge(keep, on=["source", "condition", "domain", "rep"])

pooled, indiv = [], []
for (src, cond, dom), g in df.groupby(["source", "condition", "domain"]):
    s, ratio = shares_and_prices(dom, g["points_a"], g["points_b"], g["M"], g["N"])
    est = fit(s, ratio)
    pooled.append(dict(source=src, condition=cond, domain=dom, n_subjects=g["rep"].nunique(), **est))
    for rep, h in g.groupby("rep"):
        s, ratio = shares_and_prices(dom, h["points_a"], h["points_b"], h["M"], h["N"])
        indiv.append(dict(source=src, condition=cond, domain=dom, rep=rep, **fit(s, ratio)))
    print(f"{src:5s} {cond:16s} {dom:6s} alpha={est['alpha']:.3f} rho={est['rho']:.3f}")

pd.DataFrame(pooled).pipe(append_authors, "params_pooled").to_csv(C.RESULTS / "params_pooled.csv", index=False)
ind_df = pd.DataFrame(indiv).pipe(append_authors, "params")
ind_df.to_csv(C.RESULTS / "params_individual.csv", index=False)
print("\nIndividual-level means / SDs (cf. SI Table S3):")
print(ind_df.groupby(["source", "condition", "domain"])[["alpha", "rho"]].agg(["mean", "std"]).round(3))
```

`scripts/05_tests.py`
```python
"""Statistical tests reported in the paper, for every model in the data. Output: results/tests.md

Sources: your model (label = LLM_LABEL / LLM_MODEL), the paper's GPT-3.5 subjects and the human
subjects (both added by 07_import_authors.py). Each test is run for every model present.
"""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
import numpy as np
import pandas as pd
import config as C
from src.stats import two_sample, one_sample, levene, ols_hc1

ind = pd.read_csv(C.RESULTS / "indices.csv").dropna(subset=["CCEI"])
pf = C.RESULTS / "params_individual.csv"
par = pd.read_csv(pf) if pf.exists() else pd.DataFrame(columns=["source", "condition", "domain", "alpha", "rho"])
llms = sorted((s for s in ind.source.unique() if s != "Human"), key=lambda s: s == C.PAPER_LABEL)
lines = ["# Statistical tests\n", f"Models: {', '.join(llms)}" + ("; humans included" if "Human" in set(ind.source) else "")]


def md(df):
    """DataFrame -> Markdown table (no extra package needed)."""
    cols = list(df.columns)
    fmt = lambda v: f"{v:.4g}" if isinstance(v, (float, np.floating)) else str(v)
    out = ["| " + " | ".join(cols) + " |", "|" + "---|" * len(cols)]
    out += ["| " + " | ".join(fmt(v) for v in row) + " |" for row in df.itertuples(index=False)]
    return "\n".join(out)


def table(rows, title):
    if rows:
        lines.append(f"\n## {title}\n")
        lines.append(md(pd.DataFrame(rows)))
        lines.append("")


def sel(df, src, cond, dom):
    return df[(df.source == src) & (df.condition == cond) & (df.domain == dom)]


# 1. each model vs humans, baseline (Fig. 1, Fig. 2, SI Figs. S2-S5)
rows = []
for m in llms:
    for dom in C.DOMAINS:
        for var in ["CCEI", "spearman", "HMI", "MPI_mean", "MCI"]:
            a, b = sel(ind, m, "baseline", dom)[var], sel(ind, "Human", "baseline", dom)[var]
            if a.notna().any() and b.notna().any():
                rows.append(dict(model=m, domain=dom, measure=var, **two_sample(a, b)))
table(rows, "Model (a) vs human subjects (b), baseline: two-sided two-sample t-tests")

# 2. each model vs literature mean CCEI 0.918 (SI Fig. S1)
rows = [dict(model=m, domain=d, **one_sample(sel(ind, m, "baseline", d)["CCEI"], C.LITERATURE_MEAN_CCEI))
        for m in llms for d in C.DOMAINS if len(sel(ind, m, "baseline", d))]
table(rows, "Model baseline CCEI vs literature mean 0.918: one-sample t-tests")

# 3. baseline vs each variation, within model (Fig. 4, SI Fig. S24)
rows = []
for m in llms:
    for cond in [c for c in C.CONDITIONS if c != "baseline"]:
        for dom in C.DOMAINS:
            a, b = sel(ind, m, "baseline", dom), sel(ind, m, cond, dom)
            if len(a) and len(b):
                for var in ["CCEI", "spearman"]:
                    rows.append(dict(model=m, condition=cond, domain=dom, measure=var, **two_sample(a[var], b[var])))
table(rows, "Within model: baseline (a) vs variation (b)")

# 4. model vs model, same condition (model generations; original vs paraphrased prompts)
rows = []
for i, ma in enumerate(llms):
    for mb in llms[i + 1:]:
        for cond in C.CONDITIONS:
            for dom in C.DOMAINS:
                a, b = sel(ind, ma, cond, dom), sel(ind, mb, cond, dom)
                if len(a) and len(b):
                    for var in ["CCEI", "spearman"]:
                        rows.append(dict(model_a=ma, model_b=mb, condition=cond, domain=dom, measure=var,
                                         **two_sample(a[var], b[var])))
table(rows, "Model (a) vs model (b), same condition")

# 5. heterogeneity of individual parameters (Levene)
rows = []
for m in llms:
    for cond in ["temp_0.5", "temp_1"]:
        for dom in C.DOMAINS:
            for var in ["alpha", "rho"]:
                a, b = sel(par, m, "baseline", dom)[var], sel(par, m, cond, dom)[var]
                if len(a) > 2 and len(b) > 2:
                    rows.append(dict(model=m, comparison=f"baseline vs {cond}", domain=dom, param=var, **levene(a, b)))
    for dom in C.DOMAINS:
        for var in ["alpha", "rho"]:
            a, b = sel(par, m, "baseline", dom)[var], sel(par, "Human", "baseline", dom)[var]
            if len(a) > 2 and len(b) > 2:
                rows.append(dict(model=m, comparison="model vs Human", domain=dom, param=var, **levene(a, b)))
table(rows, "Heterogeneity of individual parameters: Levene tests (sd_a vs sd_b)")

# 6. difference-in-differences (SI Table S4): is the model's drop larger than the humans' drop?
for m in llms:
    for treat in ["price_framing", "discrete"]:
        rows = []
        for dom in C.DOMAINS:
            d = ind[(ind.domain == dom) & ind.condition.isin(["baseline", treat]) & ind.source.isin([m, "Human"])]
            if len(d.groupby(["source", "condition"]).size()) < 4:
                continue
            is_m, is_t = (d.source == m).astype(float), (d.condition == treat).astype(float)
            X = np.column_stack([np.ones(len(d)), is_m, is_t, is_m * is_t])
            for r in ols_hc1(d["CCEI"], X, ["const", "model", treat, f"model x {treat}"]):
                rows.append(dict(domain=dom, **r))
        table(rows, f"{m}: OLS of CCEI on model, {treat}, interaction (HC1 SE)")

(C.RESULTS / "tests.md").write_text("\n".join(lines), encoding="utf-8")
print("\n".join(lines))
```

`scripts/06_figures.py`
```python
"""Figures 1-4 of the paper, with every model in the data. Output: results/fig1_ccei_cdf.png ... fig4_conditions.png"""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
import numpy as np
import pandas as pd
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import config as C

ind = pd.read_csv(C.RESULTS / "indices.csv").dropna(subset=["CCEI"])
br = pd.read_csv(C.RESULTS / "bronars.csv")
TITLES = {"risk": "Risk", "time": "Time", "social": "Social", "food": "Food"}
llms = sorted((s for s in ind.source.unique() if s != "Human"), key=lambda s: s == C.PAPER_LABEL)
PALETTE = ["#1F4E8C", "#2C7A4B", "#5B47B8"]
STYLE = {m: dict(color=("#8A949E" if m == C.PAPER_LABEL else PALETTE[i % 3]), lw=2) for i, m in enumerate(llms)}
STYLE["Human"] = dict(color="#B42318", ls="--", lw=1.6)


def cdf(ax, x, **kw):
    x = np.sort(np.asarray(x, float))
    x = x[~np.isnan(x)]
    if len(x):
        ax.step(np.r_[x[0], x], np.r_[0, np.arange(1, len(x) + 1) / len(x)], where="post", **kw)


def four_panels(var, fname, xlabel, with_random=False):
    fig, axes = plt.subplots(2, 2, figsize=(9, 7), sharey=True)
    for ax, dom in zip(axes.flat, C.DOMAINS):
        base = ind[(ind.condition == "baseline") & (ind.domain == dom)]
        if with_random:
            cdf(ax, br[br.domain == dom][var], color="#BCC5C3", ls=":", lw=1.6, label="Simulated (Bronars)")
        for src in ["Human"] + llms:
            cdf(ax, base[base.source == src][var], label=src, **STYLE[src])
        ax.set_title(TITLES[dom]); ax.set_xlabel(xlabel); ax.grid(alpha=.3)
    axes[0, 0].set_ylabel("Cumulative share"); axes[1, 0].set_ylabel("Cumulative share")
    axes[0, 0].legend(frameon=False, fontsize=8)
    fig.tight_layout(); fig.savefig(C.RESULTS / fname, dpi=160); plt.close(fig)


four_panels("CCEI", "fig1_ccei_cdf.png", "CCEI", with_random=True)
four_panels("spearman", "fig2_spearman_cdf.png", "Spearman corr. of ln(xA/xB) and ln(pA/pB)")

# Fig. 3: individual parameters, baseline
pf = C.RESULTS / "params_individual.csv"
if pf.exists():
    par = pd.read_csv(pf)
    par = par[par.condition == "baseline"]
    fig, axes = plt.subplots(2, 2, figsize=(9, 7))
    for ax, dom in zip(axes.flat, C.DOMAINS):
        for src in ["Human"] + llms:
            d = par[(par.source == src) & (par.domain == dom)]
            col = STYLE[src]["color"]
            ax.scatter(d["alpha"], d["rho"].clip(lower=-3), marker="o" if src == "Human" else "s", s=20, alpha=.7,
                       facecolors="none" if src == "Human" else col, edgecolors=col, label=src)
        ax.set_title(TITLES[dom]); ax.set_xlabel("alpha"); ax.set_ylabel("rho (clipped at -3)")
        ax.set_xlim(0, 1); ax.grid(alpha=.3)
    axes[0, 0].legend(frameon=False, fontsize=8)
    fig.tight_layout(); fig.savefig(C.RESULTS / "fig3_params.png", dpi=160); plt.close(fig)

# Fig. 4: mean CCEI and 95% CI by condition, one marker per model
conds = [c for c in C.CONDITIONS if c in set(ind[ind.source != "Human"].condition)]
fig, axes = plt.subplots(1, 4, figsize=(15, 4.8), sharey=True)
off = np.linspace(-0.18, 0.18, len(llms)) if len(llms) > 1 else [0.0]
for ax, dom in zip(axes, C.DOMAINS):
    for k, m in enumerate(llms):
        xs, ms, es = [], [], []
        for j, c in enumerate(conds):
            x = ind[(ind.source == m) & (ind.condition == c) & (ind.domain == dom)]["CCEI"]
            if len(x):
                xs.append(j + off[k]); ms.append(x.mean())
                es.append(1.96 * x.std(ddof=1) / np.sqrt(len(x)) if len(x) > 1 else 0)
        lo = [min(e, mm) for e, mm in zip(es, ms)]
        hi = [min(e, 1 - mm) for e, mm in zip(es, ms)]          # CCEI cannot exceed 1
        ax.errorbar(xs, ms, yerr=[lo, hi], fmt="s" if m != C.PAPER_LABEL else "o",
                    color=STYLE[m]["color"], capsize=3, label=m)
    ax.set_xticks(range(len(conds))); ax.set_xticklabels(conds, rotation=70, fontsize=8)
    ax.set_title(TITLES[dom]); ax.grid(alpha=.3)
axes[0].set_ylabel("Mean CCEI (95% CI)"); axes[0].legend(frameon=False, fontsize=8)
fig.tight_layout(); fig.savefig(C.RESULTS / "fig4_conditions.png", dpi=160); plt.close(fig)
print("Figures written to", C.RESULTS)
```

`scripts/09_progress.py`：查看每个条件、每个领域完成了多少被试，以及剩余额度。
```python
"""Show progress: finished subjects per condition and domain, invalid-answer rate, credit left.

  python scripts/09_progress.py
"""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
import pandas as pd
import config as C
from src.dataio import read_jsonl
from src.llm_client import credit_balance

meta_dir, raw_dir = C.META_DIR, C.RAW_DIR
print(f"Prompt set: {C.PROMPT_SET}  (folders: {raw_dir.name}, {meta_dir.name})  model: {C.MODEL}\n")
rows = []
for f in sorted(meta_dir.glob("*.jsonl")):
    m = pd.DataFrame(read_jsonl(f))
    r = pd.DataFrame(read_jsonl(raw_dir / f.name)) if (raw_dir / f.name).exists() else pd.DataFrame()
    for dom in C.DOMAINS:
        n = int((m["domain"] == dom).sum()) if len(m) else 0
        bad = (1 - r.loc[r["domain"] == dom, "valid"].mean()) if len(r) and (r["domain"] == dom).any() else float("nan")
        rows.append(dict(condition=f.stem, domain=dom, finished=n, invalid_rate=round(bad, 4)))
if not rows:
    print("No finished subjects yet for this prompt set.")
else:
  print(pd.DataFrame(rows).pivot(index="condition", columns="domain", values="finished")
      .reindex(columns=C.DOMAINS).fillna(0).astype(int).to_string())
  print("\nInvalid-answer rate:")
  print(pd.DataFrame(rows).pivot(index="condition", columns="domain", values="invalid_rate").reindex(columns=C.DOMAINS).to_string())
c = credit_balance()
print(f"\nCredit left: {c:.2f}" if c is not None else "\nCredit: not available for this provider")
```

`scripts/10_show_invalid.py`：列出无法解析的回复，用于检查和扩展解析规则。
```python
"""List the replies that could not be parsed, so the parsing rules can be checked or extended.

  python scripts/10_show_invalid.py                 # summary + up to 15 examples
  python scripts/10_show_invalid.py --all > invalid.txt
"""
import argparse, sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
import pandas as pd
import config as C
from src.dataio import read_jsonl

ap = argparse.ArgumentParser()
ap.add_argument("--all", action="store_true")
args = ap.parse_args()

rows = [r for f in sorted(C.RAW_DIR.glob("*.jsonl")) for r in read_jsonl(f)]
df = pd.DataFrame(rows)
bad = df[~df["valid"]]
print(f"Prompt set: {C.PROMPT_SET}. Invalid rounds: {len(bad)} of {len(df)}\n")
print(bad.groupby(["condition", "domain"]).size().rename("invalid_rounds").to_string())
per_subj = df.groupby(["condition", "domain", "rep"])["valid"].sum()
print(f"\nSubjects with fewer than {C.MIN_VALID_ROUNDS} valid rounds (dropped from analysis): "
      f"{int((per_subj < C.MIN_VALID_ROUNDS).sum())}")
show = bad if args.all else bad.sample(min(15, len(bad)), random_state=0) if len(bad) else bad
for _, r in show.iterrows():
    print(f"\n--- {r['condition']} / {r['domain']} / rep {r['rep']} / round {r['round']}  (M={r['M']:.2f}, N={r['N']:.2f})")
    print(str(r["reply"])[-600:])
```

`scripts/11_reparse.py`：解析规则改进后，对已保存的回复重新解析（不调用 API）。
```python
"""Re-apply the current parsing rules to replies already collected (no API calls).
Use after src/parse.py is improved. Originals are backed up as *.jsonl.bak.

  python scripts/11_reparse.py
"""
import json, shutil, sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
import config as C
from src import prompt_api as P
from src.dataio import read_jsonl
from src.parse import parse_continuous, parse_discrete
from src.prices import discrete_options

for f in sorted(C.RAW_DIR.glob("*.jsonl")):
    rows = read_jsonl(f)
    before = sum(r["valid"] for r in rows)
    for r in rows:
        cfg = C.CONDITIONS[r["condition"]]
        if cfg["choice"] == "discrete":
            opts = discrete_options(r["M"], r["N"])
            j, ok = parse_discrete(r["reply"], [(o[2], o[3]) for o in opts],
                                   allow_option_number=(C.PROMPT_SET != "paper"))
            r["points_a"], r["points_b"] = (opts[j][0], opts[j][1]) if ok else (None, None)
        else:
            a, b, ok = parse_continuous(r["reply"], *P.labels(r["domain"]))
            r["points_a"], r["points_b"] = a, b
        r["valid"] = bool(ok)
    shutil.copy(f, f.with_suffix(".jsonl.bak"))
    with open(f, "w", encoding="utf-8") as fh:
        for r in rows:
            fh.write(json.dumps(r, ensure_ascii=False) + "\n")
    print(f"{f.name}: valid rounds {before} -> {sum(r['valid'] for r in rows)} of {len(rows)}")
```

`scripts/12_offmenu.py`：离散条件中"菜单外"选择的比例，以及三种处理规则下的指数（稳健性检验）。
```python
"""Discrete condition: choices that are NOT on the menu ("off-menu"), and how much they matter.

With the original prompts the model sometimes names a pair that is not among the 11 options, e.g. it
answers ($93.00, $0.00) when the menu contains ($0.00, $93.00) but only ($64.00, $0.00) as the A corner:
it keeps the larger amount but moves it to the first slot. Such a reply is not a feasible choice, so the
main analysis treats it as invalid (rule "strict"). This script reports how often it happens and
recomputes the indices under three rules:
  strict : off-menu rounds dropped; subjects need >= 20 valid rounds (as in 03_indices.py)
  amount : off-menu pair mapped to the menu option with the same two amounts in swapped order
           (the model got the amount right and the slot wrong)
  slot   : (X, 0) mapped to the A corner, (0, X) to the B corner
           (the model got the slot right - "from Asset A", "for me", "today" - and the amount wrong)
Output: results/offmenu_rates.csv, results/offmenu_robustness.csv

  python scripts/12_offmenu.py
"""
import re, sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
import numpy as np
import pandas as pd
import config as C
from src import rp
from src.dataio import load_gpt, subject_arrays
from src.demand import spearman_subject
from src.parse import DECIDE, NUM
from src.prices import discrete_options

PAIR = r"\(\s*\$?\s*" + NUM + r"\s*(?:Kg)?\s*,\s*\$?\s*" + NUM


def stated_pair(text):
    """The pair the reply settles on: first pair after the last decision phrase, else the only pair."""
    t = str(text).replace(",", ", ").replace("**", "")
    pairs = [(mo.start(), float(mo.group(1)), float(mo.group(2))) for mo in re.finditer(PAIR, t, flags=re.I)]
    if not pairs:
        return None
    decide = [mo.start() for mo in re.finditer(DECIDE, t, flags=re.I)]
    if decide:
        after = [p for p in pairs if p[0] > decide[-1]]
        if after:
            return after[0][1:]
    distinct = {(a, b) for _, a, b in pairs}
    return distinct.pop() if len(distinct) == 1 else None


def find(opts, a, b):
    for j, (oa, ob) in enumerate(opts):
        if abs(a - oa) < 0.011 and abs(b - ob) < 0.011:
            return j
    return None


df = load_gpt()
df = df[df["condition"] == "discrete"].copy()
if df.empty:
    sys.exit("No discrete-condition data found.")
df["offmenu"] = False
df["pa_amount"], df["pa_slot"] = df["points_a"], df["points_a"]
for i, r in df[~df["valid"]].iterrows():
    opts_full = discrete_options(r["M"], r["N"])
    opts = [(o[2], o[3]) for o in opts_full]
    sp = stated_pair(r["reply"])
    if sp is None or find(opts, *sp) is not None:
        continue
    df.at[i, "offmenu"] = True
    j = find(opts, sp[1], sp[0])                       # swapped order
    if j is not None:
        df.at[i, "pa_amount"] = opts_full[j][0]
    if sp[1] < 0.011:                                  # (X, 0): slot A
        df.at[i, "pa_slot"] = C.ENDOWMENT
    elif sp[0] < 0.011:                                # (0, X): slot B
        df.at[i, "pa_slot"] = 0.0

rates = (df.groupby(["source", "domain"])
         .agg(rounds=("valid", "size"), invalid=("valid", lambda s: (~s).sum()), offmenu=("offmenu", "sum"))
         .assign(offmenu_rate=lambda d: d["offmenu"] / d["rounds"]).reset_index())
rates.to_csv(C.RESULTS / "offmenu_rates.csv", index=False)
print("Off-menu choices in the discrete condition:\n", rates.round(3).to_string(index=False))

out = []
for rule, col in [("strict", "points_a"), ("amount", "pa_amount"), ("slot", "pa_slot")]:
    for (src, dom, rep), g in df.groupby(["source", "domain", "rep"]):
        gv = g[g[col].notna()].copy()
        if len(gv) < C.MIN_VALID_ROUNDS:
            continue
        gv["points_a"], gv["points_b"] = gv[col], C.ENDOWMENT - gv[col]
        gv["valid"] = True
        P, X = subject_arrays(gv)
        out.append(dict(rule=rule, source=src, domain=dom, rep=rep, n_valid=len(gv), CCEI=rp.ccei(P, X),
                        spearman=spearman_subject(gv["points_a"], gv["points_b"], gv["M"], gv["N"]),
                        modal_share=gv["points_a"].round().value_counts().iloc[0] / len(gv)))
res = pd.DataFrame(out)
summ = (res.groupby(["source", "domain", "rule"])
        .agg(n_subjects=("CCEI", "size"), CCEI_mean=("CCEI", "mean"),
             share_CCEI_below_0_9=("CCEI", lambda s: (s < 0.9).mean()),
             spearman_mean=("spearman", "mean"), modal_share_mean=("modal_share", "mean"))
        .reset_index())
summ.to_csv(C.RESULTS / "offmenu_robustness.csv", index=False)
print("\nIndices under the three rules:\n", summ.round(3).to_string(index=False))
```

`scripts/08_clean_failed.py`：删除含 API 失败（空回复）或未跑完的被试，让 `02_run_llm.py` 重跑它们；也能跳过强制关闭时写坏的半行。
```python
"""Remove subjects that contain API failures (empty replies) or never finished, so that
scripts/02_run_llm.py reruns them. Genuine invalid answers (non-empty text) are kept.
Originals are backed up as *.jsonl.bak.

  python scripts/08_clean_failed.py
"""
import json, shutil, sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
import config as C
from src.dataio import read_jsonl

pairs = [(C.DATA / "raw", C.DATA / "meta"), (C.DATA / "raw_paraphrase", C.DATA / "meta_paraphrase")]
for raw, meta_dir in [(f, m) for r, m in pairs if r.exists() for f in sorted(r.glob("*.jsonl"))]:
    meta = meta_dir / raw.name
    rows = read_jsonl(raw)
    bad = {(r["domain"], r["rep"]) for r in rows if not (r.get("reply") or "").strip()}
    done = {(m["domain"], m["rep"]) for m in (read_jsonl(meta) if meta.exists() else [])}
    bad |= {(r["domain"], r["rep"]) for r in rows} - done      # rows of a subject that never finished
    if not bad:
        print(f"{raw.parent.name}/{raw.stem}: no API failures")
        continue
    metas = read_jsonl(meta) if meta.exists() else []
    for f in (raw, meta):
        if f.exists():
            shutil.copy(f, f.with_suffix(".jsonl.bak"))
    with open(raw, "w", encoding="utf-8") as fh:
        for r in rows:
            if (r["domain"], r["rep"]) not in bad:
                fh.write(json.dumps(r, ensure_ascii=False) + "\n")
    with open(meta, "w", encoding="utf-8") as fh:
        for m in metas:
            if (m["domain"], m["rep"]) not in bad:
                fh.write(json.dumps(m, ensure_ascii=False) + "\n")
    print(f"{raw.parent.name}/{raw.stem}: removed {len(bad)} failed/unfinished subjects: {sorted(bad)}")
```

---

## 6. 运行顺序与检查点

| 步骤 | 命令 | 应该看到什么 | 耗时 |
|---|---|---|---|
| 1 | `python scripts/00_selftest.py` | `ALL PASSED`（教科书例子 CCEI 2/3、HMI 1/2、MPI 1/3、MCI 1/6；Tobit 还原 α、ρ） | 几秒 |
| 1b | `python scripts/00b_check_api.py` | 列出模型、显示余额、`Test call OK` | 几秒 |
| 2 | `python scripts/02_run_llm.py --mock --conditions baseline price_framing --reps 10`，然后执行第 5–8 步 | 整个流程离线跑通；mock 的 CCEI 约为 1。**然后删除 `data/raw`、`data/meta`、`results`** | 1 分钟 |
| 3 | `python scripts/01_smoke_test.py --price-in X --price-out Y` | 逐条阅读对话记录。理解测试题答对了吗？回答格式对吗？每个条件的成本是多少？ | 1–2 分钟 |
| 4 | `python scripts/02_run_llm.py --conditions baseline --workers 1` | 400 个被试；中断后可续跑 | HKUST 网关约 3–4 小时 |
| 5 | `python scripts/03_indices.py` | `results/indices.csv`、`table_indices.csv`；Bronars 约 99.9% 违反 | 1–3 分钟 |
| 6 | `python scripts/04_estimate.py` | `params_pooled.csv`、`params_individual.csv` | 全部条件 5–10 分钟 |
| 7 | `python scripts/05_tests.py` | `results/tests.md` | 几秒 |
| 8 | `python scripts/06_figures.py` | `fig1`–`fig4` PNG | 几秒 |

之后按档位对其他条件重复第 4 步，再重跑第 5–8 步。

**第 3 步之后的检查点（最重要）：** 如果模型答错理解测试题、用整段文字作答，或者拒答（"As an AI, I don't have preferences…"），现在就修改提示词。后面所有数字都依赖于这一步。把对话记录留作证据。

---

## 7. 作者数据：人类被试与 GPT-3.5

论文 "Data, Materials, and Software Availability" 部分的 Dropbox 链接（参考文献 79）里有一个 `data.csv`。它**不是原始选择**，而是**被试层面的汇总数据** (subject-level data)：每行一个被试，指数和估计都已经算好。

| 列 | 含义 |
|---|---|
| `label` | `GPT_<领域>_<条件>`（GPT-3.5，每组 100 个）或 `Human_<条件>`（347 人：baseline 115、priceframing 111、discrete 121；每人一行包含四个领域） |
| `ccei_ / hmi_ / mpi_ / mci_ / spearman_<领域>` | 各理性指数与需求检验 |
| `alpha_ / rho_<领域>` | 个体层面的偏好估计 |
| `<参数>_<领域>_agg`、`*_se_*_agg` | 合并估计及其标准误（SI 表 S2） |
| `ccei_<领域>_sim` | 作者的 Bronars 模拟值 |
| `Q366`–`Q370` | 人类被试的人口统计问题（编码方式未说明，所以暂不使用） |

条件名对应关系：`priceframing` → `price_framing`，`temp5` → `temp_0.5`，`temp1` → `temp_1`，`kid` → `young_child`，`elder` → `elderly`，`low_edu` → `elementary_edu`，`high_edu` → `college_edu`，`black` → `african_american`。

**这意味着：**人类组和 GPT-3.5 组的**指数计算**无法从原始选择重做，但所有**统计比较**（GPT 与人类、模型代际、价格框架和离散选择的交互项、Levene 检验）以及图 1–4 都能完整复现。论文正文的全部关键数字都能从这个文件中逐一核对出来。

**用法：**把文件放到 `data/data.csv`，然后：
```powershell
python scripts/07_import_authors.py data/data.csv
python scripts/03_indices.py; python scripts/04_estimate.py; python scripts/05_tests.py; python scripts/06_figures.py
```
`07` 会写出 `data/authors_indices.csv`、`authors_params.csv`、`authors_params_pooled.csv`，并打印一张核对表。`03`、`04` 会自动把它们并入结果，来源分别标为 `Human` 和 `gpt-3.5-turbo (paper)`；你自己的模型则标为 `.env` 里的 `LLM_LABEL`（默认等于模型名）。

**核对目标（导入后应完全一致）：**GPT baseline 中 CCEI = 1 的人数为 95 / 89 / 81 / 92；人类平均 CCEI 为 0.980 / 0.985 / 0.967 / 0.963；人类 Spearman 均值为 −0.826 / −0.788 / −0.681 / −0.673；价格框架与离散条件的 GPT 均值见 0.2 节。

`scripts/07_import_authors.py`
```python
"""Import the authors' subject-level data (data.csv from the paper's Dropbox folder).

The file has one row per subject with indices already computed (no raw choices):
  label = GPT_<domain>_<condition> (100 GPT-3.5 subjects each) or Human_<condition> (347 people,
  each with all four domains in one row). Columns ccei_/hmi_/mpi_/mci_/spearman_/alpha_/rho_<domain>,
  aggregate estimates <param>_<domain>_agg, and Q366-Q370 (human demographics, coding not documented).

  python scripts/07_import_authors.py data/data.csv
Writes data/authors_indices.csv, data/authors_params.csv, data/authors_params_pooled.csv; these are
appended automatically by 03_indices.py and 04_estimate.py. Then rerun 03-06.
"""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
import pandas as pd
import config as C

COND = {"baseline": "baseline", "priceframing": "price_framing", "discrete": "discrete",
        "temp5": "temp_0.5", "temp1": "temp_1", "female": "female", "male": "male",
        "kid": "young_child", "elder": "elderly", "low_edu": "elementary_edu",
        "high_edu": "college_edu", "asian": "asian", "black": "african_american"}

src = Path(sys.argv[1] if len(sys.argv) > 1 else C.DATA / "data.csv")
raw = pd.read_csv(src)
# human ids in the file are platform participant ids: replace them with neutral codes H001, H002, ...
hid = {v: f"H{i + 1:03d}" for i, v in enumerate(raw.loc[raw["label"].str.startswith("Human"), "id"].unique())}
raw["id"] = [hid.get(v, v) for v in raw["id"]]
ind, par, pooled = [], [], []
for _, row in raw.iterrows():
    parts = row["label"].split("_")
    if parts[0] == "GPT":
        source, domains, cond = C.PAPER_LABEL, [parts[1]], COND["_".join(parts[2:])]
    else:
        source, domains, cond = "Human", C.DOMAINS, COND["_".join(parts[1:])]
    for dom in domains:
        if pd.isna(row[f"ccei_{dom}"]):
            continue
        ind.append(dict(source=source, condition=cond, domain=dom, rep=str(row["id"]), n_valid=C.N_ROUNDS,
                        CCEI=row[f"ccei_{dom}"], HMI=row[f"hmi_{dom}"], MPI_mean=row[f"mpi_{dom}"],
                        MCI=row[f"mci_{dom}"], spearman=row[f"spearman_{dom}"]))
        if pd.notna(row[f"alpha_{dom}"]):
            par.append(dict(source=source, condition=cond, domain=dom, rep=str(row["id"]),
                            alpha=row[f"alpha_{dom}"], rho=row[f"rho_{dom}"]))
        if pd.notna(row.get(f"alpha_{dom}_agg")):
            pooled.append(dict(source=source, condition=cond, domain=dom,
                               alpha=row[f"alpha_{dom}_agg"], rho=row[f"rho_{dom}_agg"],
                               alpha_se=row[f"alpha_se_{dom}_agg"], rho_se=row[f"rho_se_{dom}_agg"]))

ind, par = pd.DataFrame(ind), pd.DataFrame(par)
pooled = pd.DataFrame(pooled).drop_duplicates(["source", "condition", "domain"])
ind.to_csv(C.DATA / "authors_indices.csv", index=False)
par.to_csv(C.DATA / "authors_params.csv", index=False)
pooled.to_csv(C.DATA / "authors_params_pooled.csv", index=False)

# check against the numbers printed in the paper
chk = (ind[ind.condition.isin(["baseline", "price_framing", "discrete"])]
       .groupby(["source", "condition", "domain"])
       .agg(n=("CCEI", "size"), CCEI_mean=("CCEI", "mean"), CCEI_eq_1=("CCEI", lambda s: (s >= 1 - 1e-9).sum()),
            below_0_9=("CCEI", lambda s: (s < 0.9).mean()), spearman_mean=("spearman", "mean")).round(3))
print(chk.to_string())
print(f"\nWrote {len(ind)} subject-domain rows, {len(par)} individual estimates, {len(pooled)} pooled estimates.")
print("Paper: GPT baseline CCEI=1 counts 95/89/81/92; human mean CCEI 0.980/0.985/0.967/0.963.")
```

---

## 8. 输出与论文的对应关系

| 论文中的内容 | 你的文件 | 列 / 说明 |
|---|---|---|
| 图 1：CCEI 累积分布（GPT、人类、模拟） | `results/fig1_ccei_cdf.png` | |
| "100 个中有 95、89、81、92 个 CCEI = 1" | `table_indices.csv` | `share_CCEI_1` × n |
| 平均 CCEI，GPT 对人类，t 检验 | `table_indices.csv`、`tests.md` 第 1 部分 | `CCEI_mean` |
| GPT 对文献均值 0.918 | `tests.md` 第 2 部分 | |
| SI 图 S2–S5（HMI、MPI、MCI） | `indices.csv` | `HMI`、`MPI_mean`、`MCI` |
| 图 2：Spearman 累积分布；GPT"全部为负" | `fig2_spearman_cdf.png`、`table_indices.csv` | `spearman_mean`、`share_spearman_neg` |
| SI 表 S2：合并估计 (α, ρ) | `params_pooled.csv` | |
| 图 3 / SI 表 S3：个体估计 (α, ρ) | `fig3_params.png`、`params_individual.csv` | |
| 图 4：各条件平均 CCEI | `fig4_conditions.png` | |
| 价格框架 / 离散："34% 低于 0.9"等 | `table_indices.csv` | `share_CCEI_below_0_9` |
| SI 表 S4（GPT 的下降是否大于人类？） | `tests.md` 最后几部分 | `model x price_framing` 系数，每个模型一张表 |
| 温度提高 ρ 的标准差（Levene） | `tests.md` 的 Levene 部分 | |
| 模型代际：你的模型 vs GPT-3.5 | `tests.md` "Your model vs gpt-3.5-turbo (paper)" | 每个条件、每个领域 |
| 无效回答率 4.7% / 9.8% | `data/raw/*.jsonl` | `valid == false` 的比例 |

各条件的无效回答率：
```python
import pandas as pd, json, glob
rows = [json.loads(l) for f in glob.glob("data/raw/*.jsonl") for l in open(f, encoding="utf-8")]
d = pd.DataFrame(rows); print(1 - d.groupby("condition")["valid"].mean())
```

---

## 9. 什么算复现成功

| 论文的结论 | 用你的模型，满足以下条件即算"复现" |
|---|---|
| GPT 在四个领域都高度理性 | 平均 CCEI ≥ 约 0.99，大多数被试 CCEI = 1 |
| GPT 高于人类 | GPT 的 CCEI 显著高于人类（作者数据）且高于 0.918 |
| 选择对价格有反应（不是聚集在角点） | 平均 Spearman 明显为负，几乎所有被试为负 |
| 对温度、人设不敏感 | 与基准相比 CCEI 无显著差异 |
| **对价格框架和离散选择敏感** | CCEI 和 Spearman 显著下降；下降幅度超过人类（交互项系数） |
| GPT 的偏好更同质 | 个体 α、ρ 的标准差远低于人类 |

新模型可能*无法*复现框架效应（它们也许能正确换算"Y 点 = 1 单位"）。这是一个实质性发现，而不是复现失败：报告为"GPT-3.5 上记录的这一局限在模型 X 上不复存在"。

需要避免的解读陷阱：
1. **100 个 GPT"被试"不是 100 个人。** 温度为 0 时它们只因价格不同而不同。它们方差小，既反映模型，也反映设计；t 检验却把它们当作独立的样本。
2. **对话记忆。** 模型在同一段对话中能看到自己之前的回答，一致性可能部分来自于此。扩展 E2 检验这一点。
3. **简单规则也能得到 CCEI = 1。** 一定要把 CCEI 和 Spearman 放在一起看。

---

## 10. 常见问题

| 现象 | 原因 | 处理 |
|---|---|---|
| `ModuleNotFoundError: src` | 在错误的文件夹运行 | 在项目根目录运行：`python scripts/03_indices.py` |
| `ImportError: cannot import name 'milp'` | SciPy 版本太旧 | `pip install -U "scipy>=1.11"` |
| `openai.NotFoundError` / model not found | 模型或 deployment 名称错误，或模型已下线 | 在服务商的模型列表中核对名称；不要用 `gpt-3.5-turbo`（已下线） |
| `RateLimitError` 反复出现 | 并发数太多（HKUST 网关每分钟 60 次） | `--workers 1`；客户端已经会自动退避 |
| 401 / Access denied | 密钥错误或缺少 `api-key` 请求头 | 检查 `.env` 中的 `LLM_API_KEY` 与 `LLM_KEY_HEADER` |
| 502 / 503 / 504 反复出现 | 网关或上游服务暂时故障 | 客户端重试 8 次（约 4 分钟）；仍失败则该被试不保存，连续 3 个失败就自动停止。稍后重跑同一条命令；旧版代码跑过的数据先运行 `08_clean_failed.py` |
| 按 Ctrl+C 停不下来 | 旧版代码在线程里等待，Windows 下无法中断；SDK 默认超时长达 10 分钟 | 新版：`--workers 1` 时直接按 Ctrl+C；多线程时按一次、等约 1 秒。请求超时改为 60 秒。实在不行就关闭终端，已完成的被试不受影响 |
| 大量 `valid == false` | 模型用整段文字或百分比作答 | 查看 `data/raw/*.jsonl` 里的 `reply`；收紧格式要求，或扩展 `parse.py` |
| `temperature` 报错 | 推理模型固定了温度 | 该模型跳过温度条件；在报告中说明 |
| 模型拒答（"I am an AI…"） | 安全对齐 | 保留"act as a human decision maker"的角色设定；若仍拒答，计为无效并报告比例 |
| 离散条件下 mock 的 CCEI 全为 1 | 正常：mock 选的是最近的选项 | 只有真实模型的结果有意义 |
| 程序崩溃后出现重复行 | 崩溃前写入了部分被试 | 脚本会按 (condition, domain, rep, round) 去重 |
| `04_estimate.py` 很慢 | 条件多 × 每个 100 个被试 | 正常：每个被试约 1 秒；跑一次即可，结果存在 CSV 里 |
| PowerShell 用 `>` 输出的文件 pandas 读不了 | 默认 UTF-16 编码 | 用 `Out-File -Encoding utf8`，或让脚本自己写文件 |

---

## 11. 扩展：从复现走向论文

| # | 扩展 | 改动 | 问题 |
|---|---|---|---|
| E1 | 模型代际 | 在 3–4 个模型上跑基准 + 框架 + 离散 | 理性在提高吗？框架脆弱性消失了吗？ |
| E2 | 记忆 vs 推理 | 每一轮都在**新的**对话中进行（没有历史） | 一致性是不是看到过去答案的产物？ |
| E3 | Chain-of-thought (思维链) | 先要求推理，再作答 | 深思熟虑能修复框架错误吗？ |
| E4 | 语言框架 | 用中文做同样的任务 | 理性是否依赖于提示词的语言？ |
| E5 | 三种商品 | k = 3 的预算集 | 更难的检验：两商品时 WARP = SARP 不再成立 |
| E6 | 中点启发式 | 统计恰好 50/50 和第一个 / 最后一个选项的比例 | 直接检验论文的"语料启发式"解释 |
| E7 | 人设异质性 | 带有明确偏好特征的人设 | LLM 能否模拟人类的*异质性*，而不只是理性？（参见 Horton 2023） |
| E8 | 金融 / 会计情境 | 股票与债券之间的组合；经理分配预算 | 换成领域术语后理性还在吗？把 LLM 主体与投资者行为研究连起来 |

**多个模型放在一起分析：**每个模型在自己的项目副本里运行（各自的 `.env` 填不同模型），跑完后把副本里的 `data\raw\*.jsonl` 复制到主项目的 `data\extra\<模型名>\`。`03`–`06` 会自动把它当作另一个模型来源，检验和图里会并列显示。

---

## 12. 假设记录（写进报告）

| # | 论文没有说明的地方 | 本复现的做法 |
|---|---|---|
| A1 | 每次重复用相同还是新的价格 | 每次重复用新的带种子价格；各条件之间相同（配对） |
| A2 | 提示词原文 | 主分析用附录 A 原文；改写版作为提示词敏感性检验 |
| A2b | 离散选项公式 | 附录中 Ni 的公式为笔误，按预算线取值 |
| A3 | 回复如何解析 | 正则表达式；和必须为 100 ± 1；无效回答剔除 |
| A4 | 部分轮次无效的被试 | 25 轮中 ≥ 20 轮有效则保留，用有效轮次计算指数 |
| A5 | Welch 还是合并方差 t 检验 | Welch |
| A6 | MPI 基于哪些循环 | 违反的二元循环（两种商品时已足够） |
| A7 | 估计时风险领域的排序 | 商品 1 = 所选组合中数量较大的一个，价格比相应调换 |
| A8 | 模型 | 当前模型 X（gpt-3.5-turbo 已于 2026-10-23 下线） |
| A9 | 价格框架的四舍五入 | 有效价格 = 显示的 1/M（两位小数） |
| A11 | 离散条件中模型说出的选项不在菜单里 | 主分析记为无效；`12_offmenu.py` 按"金额正确"和"位置正确"两种映射做稳健性检验 |
| A10 | 回复长度上限 (max_tokens) | 不设上限，与论文"其余参数保持默认"一致；改写版运行时设为 200 |

---

## 参考文献（核心）

- Afriat, S. N. (1967). The construction of utility functions from expenditure data. *International Economic Review*, 8, 67–77.
- Afriat, S. N. (1972). Efficiency estimation of production functions. *International Economic Review*, 13, 568–598.
- Andreoni, J., & Miller, J. (2002). Giving according to GARP. *Econometrica*, 70, 737–753.
- Andreoni, J., & Sprenger, C. (2012). Estimating time preferences from convex budgets. *AER*, 102, 3333–3356.
- Bronars, S. G. (1987). The power of nonparametric tests of preference maximization. *Econometrica*, 55, 693–698.
- Choi, S., Fisman, R., Gale, D., & Kariv, S. (2007). Consistency and heterogeneity of individual behavior under uncertainty. *AER*, 97, 1921–1938.
- Choi, S., Kariv, S., Müller, W., & Silverman, D. (2014). Who is (more) rational? *AER*, 104, 1518–1550.
- Dean, M., & Martin, D. (2016). Measuring rationality with the minimum cost of revealed preference violations. *REStat*, 98, 524–534.
- Echenique, F., Lee, S., & Shum, M. (2011). The money pump as a measure of revealed preference violations. *JPE*, 119, 1201–1223.
- Fisman, R., Kariv, S., & Markovits, D. (2007). Individual preferences for giving. *AER*, 97, 1858–1876.
- Gul, F. (1991). A theory of disappointment aversion. *Econometrica*, 59, 667–686.
- Harbaugh, W. T., Krause, K., & Berry, T. R. (2001). GARP for kids. *AER*, 91, 1539–1545.
- Horton, J. J. (2023). Large language models as simulated economic agents: What can we learn from homo silicus? NBER Working Paper.
- Houtman, M., & Maks, J. (1985). Determining all maximal data subsets consistent with revealed preference. *Kwantitatieve Methoden*, 19, 89–104.
- Rose, H. (1958). Consistency of preference: The two-commodity case. *REStud*, 25, 124–125.
- Varian, H. R. (1982). The nonparametric approach to demand analysis. *Econometrica*, 50, 945–973.
- Varian, H. R. (1990). Goodness-of-fit in optimizing models. *Journal of Econometrics*, 46, 125–140.
