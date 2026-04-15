# CSIRO — Image2Biomass Prediction — 赛题规格与评测说明

> 与 Kaggle **Overview / Data / Evaluation** 官方说明一致；若有冲突以官网为准。

来源：[竞赛 Overview](https://www.kaggle.com/competitions/csiro-biomass/overview) | [Data](https://www.kaggle.com/competitions/csiro-biomass/data) | [Evaluation](https://www.kaggle.com/competitions/csiro-biomass/overview/evaluation)

## 赛题定位

- **任务类型**：**回归**——根据牧场 **RGB 图像**（及附带的表格元数据）预测多种 **干物质生物量**（单位：克等，以数据说明为准）。
- **一句话目标**：在隐藏测试集上最大化 **全局加权 R²**（见下文）。
- **提交**：赛题要求通过 **Kaggle Notebook** 提交（「Submit」可用性等以当前规则页为准）；预测文件格式为 **CSV**（`sample_id`, `target`），与 `sample_submission.csv` 一致。

## 数据（`train.csv` / `test.csv`）

### `train.csv`（训练）

典型列（以当前数据包为准）：

| 列名 | 说明 |
|------|------|
| `sample_id` | 唯一行 ID，格式如 `IDxxxx__Dry_Total_g` |
| `image_path` | 图像相对路径，如 `train/IDxxxx.jpg` |
| `Sampling_Date` | 采样日期 |
| `State` | 州/区域 |
| `Species` | 草场/物种类型 |
| `Pre_GSHH_NDVI` | 预计算的 NDVI 等指数 |
| `Height_Ave_cm` | 平均株高（厘米） |
| `target_name` | 目标名：`Dry_Green_g`、`Dry_Dead_g`、`Dry_Clover_g`、`GDM_g`、`Dry_Total_g` |
| `target` | 回归标签（连续值） |

**结构**：同一 `image_path` 通常对应 **5 行**（5 个 `target_name`）。本仓库当前 `data/train.csv` 快照：**357** 张图、**1785** 行；完整图像与 Kaggle 隐藏测试集以 [Data 页](https://www.kaggle.com/competitions/csiro-biomass/data) 下载为准。

### `test.csv`（测试）

含 `sample_id`, `image_path`, `target_name` 等；**无 `target`**。公开样本行数较少，正式评测为隐藏集。

### `sample_submission.csv`

提交需包含至少：`sample_id`, `target`（预测值）。

## 评价指标（Evaluation）

### 加权 R²（全局）

对所有 **(图像, target) 行** 一起计算 **一个** 加权决定系数 **R²_w**，而不是先按 target 分别算 R² 再平均。

**行权重**（按 `target_name`）：

| `target_name` | 权重 |
|---------------|------|
| `Dry_Green_g` | 0.1 |
| `Dry_Dead_g` | 0.1 |
| `Dry_Clover_g` | 0.1 |
| `GDM_g` | 0.2 |
| `Dry_Total_g` | 0.5 |

**公式**：

\[
R^2_w = 1 - \frac{\sum_j w_j (y_j - \hat{y}_j)^2}{\sum_j w_j (y_j - \bar{y}_w)^2}
\]

其中 \(\bar{y}_w = \frac{\sum_j w_j y_j}{\sum_j w_j}\) 为真实标签的加权均值；\(w_j\) 为第 \(j\) 行对应 target 的权重；\(y_j\)、\(\hat{y}_j\) 为真值与预测值。

**含义**：`Dry_Total_g` 在评测中占比最大（0.5），优化时需整体权衡各 target。

## 提交方式（Submitting）

- 输出 **CSV**：列与 `sample_submission.csv` 对齐；`sample_id` 行集合与评测集一致。
- **Notebook 提交**：以 Kaggle 竞赛页 **Rules / Submission** 当前说明为准（如需联网、运行时间限制等）。

## 与本仓库的关系

- 本地 **`data/*.csv`** 用于对齐列名与 EDA；**训练图像**若在本地未下载，以 Kaggle `input/` 路径为准。
- 验证集划分建议 **按图像聚合** 再切分，避免同一图的多行同时出现在 train 与 val。

## 奖励与规模（仅供参考）

奖金池 **$75,000** 及奖牌积分等以 Overview 实时显示为准。

---

**结论**：赛题核心是 **图像（+可选表格特征）→ 多目标生物量回归**，优化目标是 **单行加权的全局 R²_w**；`Dry_Total_g` 权重最高。
