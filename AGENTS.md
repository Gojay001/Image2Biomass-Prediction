# AGENTS.md — AI 协作规则

## 项目定位

Kaggle 竞赛 **CSIRO - Image2Biomass Prediction** 的本地工作区。训练与提交在 **Kaggle 平台**（GPU / Notebook）完成；本地仓库用于：

- 讨论与规划建模与验证策略
- 记录实验结果与分析
- 管理 notebook 版本
- 数据探索与轻量 EDA 脚本
- 存档可复用代码片段

## 工作流

```
讨论方案 → 用户确认 → 修改 notebooks/*.ipynb → 用户本地按需 git commit → Kaggle 运行与提交
```

### 每轮迭代步骤

1. **讨论**：AI 提出方向 + 具体方案，等待用户确认
2. **确认**：用户明确同意后，AI 修改对应 `.ipynb` 文件
3. **Git**：默认由用户在本地自行 `git add` / `git commit`；**仅当用户在本轮对话中明确要求 AI 代为提交时**，AI 才可执行 commit，并沿用下方前缀与消息格式
4. **上传**：用户在 Kaggle 运行 notebook、按赛规提交预测或 Notebook 输出
5. **记录**：AI 将实验结果更新到 `TASKS.md`
6. **文档同步**：目录结构变更，或**新增/更新实验记录**时，同步检查并更新 **`AGENTS.md`**（本文件：目录树与规则）、**`README.md`**（概览与项目结构）、**`TASKS.md`**（实验表、EXP 日志、当前最优摘要）

### 禁止事项

- **未经用户明确要求，AI 不得执行 `git commit`（禁止自动提交）**
- 未经用户确认不得修改 notebook
- 不在本地假定具备与 Kaggle 相同的 GPU / 全量图像路径；大规模训练以 Kaggle 为准
- 不修改 `data/` 中**竞赛官方**原始文件（如 `train.csv` / `test.csv` / `sample_submission.csv`）；衍生特征或中间表须在文档中说明来源与用途

## Git 规范

### 提交前缀

| 前缀 | 用途 | 示例 |
|------|------|------|
| `feat:` | 新功能/新策略 | `feat: add ViT regression head` |
| `fix:` | 修复 bug | `fix: correct image path join` |
| `refactor:` | 重构（不改行为） | `refactor: extract dataset class` |
| `data:` | 数据处理相关 | `data: add fold by image id` |
| `exp:` | 实验记录更新 | `exp: record v01 public LB` |
| `docs:` | 文档更新 | `docs: update competition spec` |
| `chore:` | 杂项 | `chore: update .gitignore` |

### 提交消息格式

```
<prefix> <简要描述>

<可选正文>
```

## Notebook 命名

```
notebooks/v<版本号>-<简短描述>.ipynb
```

示例：

- `v01-baseline-cnn.ipynb` — 简单 CNN / 预训练骨干回归 baseline
- `v02-kfold-image.ipynb` — 按图像 GroupKFold 交叉验证

每个版本对应一个独立实验方向；小改动可在同版本内迭代。

## 项目结构

```
├── AGENTS.md                 # 本文件
├── TASKS.md                  # 实验方向、进度、Leaderboard、EXP 日志
├── README.md                 # 项目概览
├── .gitignore
├── data/
│   ├── train.csv             # 官方训练表（勿改）
│   ├── test.csv              # 公开测试行（勿改）
│   └── sample_submission.csv # 提交格式样例（勿改）
├── docs/
│   ├── competition-spec.md   # 赛题规格
│   └── superpowers/plans/    # 规划类文档（可选）
├── memory/
│   ├── reproducibility-seed.md
│   └── data-split-train-val.md
├── notebooks/                # Kaggle 用 notebook
└── experiments/
    └── eda/                  # 本地 EDA（勿与 Kaggle 环境混用依赖）
        ├── README.md
        └── analyze_train_csv.py
```

说明：`experiments/eda/output/` 为生成报告目录，默认 **gitignore**。

## 沟通语言

所有回复使用**中文**。代码注释与 commit 消息可混用中英文。
