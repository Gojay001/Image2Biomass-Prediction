# CSIRO — Image2Biomass Prediction

[Kaggle 竞赛页](https://www.kaggle.com/competitions/csiro-biomass/overview) | 奖金池 $75,000（以官网为准）

## 竞赛时间与成绩

- **赛程**：**2025-10-29** — **2026-01-29**（以 Kaggle 竞赛页为准）。
- **排名**：**第 326 名** / 共 **3805** 支参赛队伍（约 **Top 9%**）。
- **奖牌**：**单人铜牌**（Solo Bronze；以 Kaggle 官方榜单与奖牌规则为准）。

## 任务

从牧场 **RGB 航拍图** 预测多种 **干物质生物量** 指标（`Dry_Green_g`、`Dry_Dead_g` 等）。训练表为「每张图 × 每个 target」多行；评测为 **全局加权 R²**（见 [docs/competition-spec.md](docs/competition-spec.md)）。

## 工作流

```
本地讨论方案 → 确认 → 修改 notebook → git commit → Kaggle Notebook 训练与提交 → 反馈结果
```

- **训练与提交**：本赛题需在 **Kaggle Notebook** 中完成（启用 Submit 后提交预测；以官网规则为准）
- **本地**：方案讨论、版本管理、EDA、实验记录

详见 [AGENTS.md](AGENTS.md) 了解 AI 协作规则、git 规范与**文档同步**约定。

## 项目结构

```
├── AGENTS.md                    # AI 协作规则 & git 规范
├── TASKS.md                     # 实验进度、分数、EXP 日志（主记录）
├── README.md                    # 本文件
├── data/
│   ├── train.csv                # 竞赛官方训练表（含 image_path、元数据、target）
│   ├── test.csv                 # 公开测试样本行（正式评测为隐藏集）
│   └── sample_submission.csv    # 提交列名样例
├── docs/
│   ├── competition-spec.md      # 赛题规格与评测
│   └── superpowers/plans/       # 功能/分析规划（可选）
├── memory/                      # 约定备忘：seed、按图像划分等
├── notebooks/                   # Kaggle 训练 notebook（v01… 版本化命名）
└── experiments/eda/             # 本地 EDA 脚本（analyze_train_csv.py）
```

**文档同步**：新增实验或变更目录时，请同步更新 [TASKS.md](TASKS.md)、本文件与 [AGENTS.md](AGENTS.md)（见 AGENTS 工作流第 6 步）。

## 赛题要点

- **数据**：`image_path` 指向 `train/`、`test/` 下图像（完整数据包以 Kaggle Data 页为准）；`train.csv` 含 `State`、`Species`、`Pre_GSHH_NDVI`、`Height_Ave_cm` 等辅助列
- **标签**：`target_name` + `target`（连续值）；每张图对应 **5 行**（5 个 target）
- **指标**：加权 **R²_w**（各 target 行权不同，`Dry_Total_g` 权重最高）

详见 [docs/competition-spec.md](docs/competition-spec.md)。
