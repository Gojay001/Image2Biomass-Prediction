# TASKS.md — 实验方向与进度追踪

## 文档维护

- 本文件为**实验主记录**（版本表、Public Score、`EXP-xxx` 日志）。
- **新增或更新实验**、或**仓库目录/数据文件有变**时，应同步更新：
  - **`README.md`**：项目结构树与入口说明；
  - **`AGENTS.md`**：项目结构、协作步骤、禁止事项；
  - **本文件**：表格、`当前最优` 摘要、关键结论与交叉引用。
- 详见 [AGENTS.md](AGENTS.md) 工作流第 6 步（文档同步）。

---

## 竞赛目标

在官方评测下最大化 **加权决定系数 R²_w**（对所有 `(image, target)` 行统一计算，行权因 `target_name` 而异）。公式与权重见 [docs/competition-spec.md](docs/competition-spec.md)。

---

## 当前状态

| 版本 | 描述 | Public Score | 状态 |
|------|------|--------------|------|
| v3.0-siglip+dinov3 | 双路：SigLIP 嵌入 + 树模型 与 DINOv3 Large 推理融合 + 质量平衡（见「EXP-003」） | **~0.72**（notebook 文件名 LB；以 Kaggle 为准） | 已入库：`notebooks/v3.0-siglip+dinov3-lb-0.72.ipynb` |
| v2.0-dinov3 | 单路 DINOv3 Huge+ 基线：左右半图 + fusion neck + 5-fold 推理（见「EXP-002」） | **~0.70** | 已入库：`notebooks/v2.0-dinov3-lb-0.70.ipynb` |
| v1.0-ensemble4 | 四路子预测加权融合（见「EXP-001」） | **~0.69** | 已入库：`notebooks/v1.0-ensemble4-lb-0.69.ipynb` |

**当前最优**：**v3.0-siglip+dinov3**（`notebooks/v3.0-siglip+dinov3-lb-0.72.ipynb`，Public LB 约 **0.72**）。

---

## 优化方向（待讨论）

### 方向 1：验证策略

- 训练表为**多行/图**：划分时宜 **按 `image_path` 或图像 ID 分组**，避免同一图泄漏到训练与验证
- 与加权 R² 对齐的本地近似：按行权重的加权 MSE 或官方公式复现

### 方向 2：特征与模型

- 预训练视觉骨干（CNN / ViT）+ 多目标回归头（5 个 target 可共享骨干、独立头或联合建模）
- 利用 `Pre_GSHH_NDVI`、`Height_Ave_cm` 等元数据（注意测试阶段可用列以赛题为准）

### 方向 3：损失与后处理

- 直接优化 MSE 时，可考虑与 **评测权重** 对齐的 sample_weight
- 检查 `target` 分布、异常值与量纲

### 方向 4：数据与增强

- 光照、颜色、几何增强；按草场类型 / 州分层抽样

---

## 实验日志

### EXP-003: v3.0 SigLIP + DINOv3 双路融合

- **Notebook**：[notebooks/v3.0-siglip+dinov3-lb-0.72.ipynb](notebooks/v3.0-siglip+dinov3-lb-0.72.ipynb)（致谢：Eng Adam Al mohammedi、Baidalin、Adilzhan、CigarCat、Mattia Angeli、Khoa、samu2505 等）。
- **Public LB**：文件名标注 **~0.72**（以 Kaggle Leaderboard 为准）。
- **流程概要**（多 cell / 子进程顺序）：
  1. **`submission_siglip.csv`（Cell 1：SigLIP + 表格 ML）**  
     读 **`csiro-datasplit/csiro_data_split.csv`** 与 **`test.csv`** 宽表；**SigLIP SO400M** 图像嵌入（大图 **520×520 滑窗 patch**，overlap=16，patch 特征 **mean**）；**`generate_semantic_features`** 文本概念相似度 + ratio 特征；**`SupervisedEmbeddingEngine`**（Scaler / PCA / PLS / GMM + 语义）；**按 `fold` 的 5 折**：**HistGB、GradientBoosting、CatBoost、LGBM** 各预测测试集，**四模型算术平均**；**`Dry_Clover_g` 在折内恒为 0**（不单独拟合）；**`post_process_biomass`**（固定三叶草为 0、由分量推 **GDM** / **Total**）→ **`melt_table`** → **`submission_siglip.csv`**。
  2. **`submission_dinov2026.csv`（Cell 2–3：`csiro_infer.py`）**  
     **`vit_large_patch16_dinov3_qkvb`** + **FiLM** 调制左右特征、三 **Softplus** 头（green / clover / dead）；**`MODELS_DIR`**（如 **`modelv3/.../models_retrained`**）下 **多个 `*.pth`** 各推理后 **模型维 mean**；**TTA**（原图 / 水平翻 / 垂直翻）；阈值与小规则后处理 → **`submission_dinov2026.csv`**。
  3. **`submission72.csv`（Cell 4：`robust_ensemble`）**  
     读入上述两 CSV，**`Dry_Clover_g` 仅用 DINO 分支**；其余目标 **`target = 0.65 * dino + 0.35 * siglip`**（`W_DINO` / `W_SIGLIP`）；宽表后 **`enforce_mass_balance(..., fixed_clover=True)`**：固定三叶草、令 **GDM = Green + Clover**、**Total = GDM + Dead**，非负 clip → **`submission72.csv`** 作为最终融合提交。
- **依赖**：**`csiro-biomass`**、**`google-siglip-so400m-patch14-384`**、**`csiro-datasplit`**、**`modelv3`**（或 ipynb 内当前 `CFG` 路径）等；以 notebook 与 Kaggle **Rules** 为准。
- **说明**：与 **EXP-001** 四路大集成不同，本版为 **两路**（嵌入+树 vs. 端到端 DINO）+ **物理解析重算**，工程与算量相对集中。

### EXP-002: v2.0 DINOv3 单模基线（Huge+）

- **Notebook**：[notebooks/v2.0-dinov3-lb-0.70.ipynb](notebooks/v2.0-dinov3-lb-0.70.ipynb)（致谢 / 上游：[Khoa 的 Kaggle baseline](https://www.kaggle.com/code/llkh0a/cisro-baseline-train-infer-21-12-dinov3-siglip) 的「已训练推理」版思路）。
- **Public LB**：文件名标注 **~0.70**（以 Kaggle Leaderboard 为准）。
- **模型**：`timm` **`vit_huge_plus_patch16_dinov3.lvd1689m`**，输入 **512**；左右半图各自过 ViT（`global_pool=''` 保留 patch token），**序列维拼接** 后经 **`LocalMambaBlock`×2** 做轻量跨半图混合，再 **AdaptiveAvgPool1d** 与 **多回归头**（`Softplus` 保证非负）；**`GDM_g` / `Dry_Total_g`** 由 green、clover、dead **加和约束**得到（与 v1.0 单路 notebook 同构）。
- **数据预处理**：BGR→RGB；**`clean_image`**（裁底 10%、HSV 抠橙区 **inpaint**）；**Albumentations**（训练增广 / 验证 / TTA）；**ImageNet normalize**。
- **推理**：默认 **`CREATE_SUBMISSION=True`**，从 **`MODEL_DIR`** 加载各折 **`best_model_fold{k}.pth`**（配置中为 Kaggle Dataset **`baseline-dinov3`**），**多折预测平均**；可选 **TTA**；长表 **merge** `test.csv` 生成提交。
- **训练**：主训练循环在 notebook 内为**注释块**；完整训练需解冻/冻结策略、**EMA**、**AdamW 分组 lr**、**warmup + 余弦**、**StratifiedGroupKFold** 等与 v1.0 同系列说明一致。
- **依赖**：竞赛 **`csiro-biomass`**、权重 Dataset（如 **`vit-huge-plus-patch16-dinov3-lvd1689m`**、`baseline-dinov3`）等，路径以 ipynb 内 `CFG` 为准。

### EXP-001: v1.0 四路集成（ensemble4）

- **Notebook**：[notebooks/v1.0-ensemble4-lb-0.69.ipynb](notebooks/v1.0-ensemble4-lb-0.69.ipynb)（致谢：Chika Komari、seddik turki、samu2505 等社区基线）。
- **Public LB**：文件名标注 **~0.69**（以 Kaggle Leaderboard 为准）。
- **流程概要**（下列 **1–4 为四条子流水线**；**代码执行顺序**为：1 → 3 → 2 → 4 → 融合）：
  1. **`submission1.csv`（SigLIP + 表格/嵌入）**  
     `test.csv` → 宽表；**SigLIP** 图像嵌入 + 可选 **语义文本特征**；**`SupervisedEmbeddingEngine`**（Scaler / PCA / PLS / GMM + 语义）；**5 折 CV** 下 **HistGB、Sklearn GB、CatBoost、LGBM** 各训预测，**四模型测试预测算术平均**；**`post_process_biomass`**；**`melt_table`** 生成 `sample_id,target`。训练侧使用 **`csiro_data_split`** 等 Kaggle 附加数据（以赛题 Rules 为准）。
  2. **`submission3.csv`（CrossPVT / T2T / Mamba + DINO）**  
     **`run_dino_inference()`**：`vit_*` 结构 **`CrossPVT_T2T_MambaDINO`**，**5 个 fold** 的 `best_wr2.pt` 在 batch 内前向取 **mean**；可选 **TTA**；宽表 melt 后与 `test.csv` **merge** 对齐 `sample_id`。
  3. **`submission2.csv`（MVP 多 DINO checkpoint）**  
     **`run_mvp_inference()`**：`csiro-mvp-models` 下 **model1…10** 分两堆（各 5 个），组内 **TTA + 平均**，组间 **`0.95 * pred_A + 0.075 * pred_B`**；**`create_submission_mvp`** 中 **GDM / Total 与分量一致** 后写 CSV。
  4. **`submission4.csv`（EVA02）**  
     **`run_eva()`**：单 checkpoint（如 `best_model_fold_4.pth`），左右半图 + **TTA**；**clover/dead** 由 total/gdm/green **差分 + clip/阈值** 规则化；逐图写长表。
  5. **`submission.csv`（最终提交）**  
     按 **`sample_id` merge** 上述四文件，**`target = 0.4*t1 + 0.25*t2 + 0.25*t3 + 0.1*t4`**（注释：**siglip / mvp dino / cross dino / eva**）。
- **依赖**：需在 Kaggle Notebook 中挂载竞赛 **`csiro-biomass`** 及 notebook 内硬编码的 **Models / Datasets / Kernel 输出**（路径以该 ipynb 为准）；**联网与外部数据**以竞赛当前 Rules 为准。
- **与赛题对齐**：输出均为官方要求的 **`sample_id`, `target`** 长表；本地 **`competition_metric`** 使用的权重数值与 [docs/competition-spec.md](docs/competition-spec.md) 一致，**是否与官方全局 R² 逐行等价**以官网 Evaluation 为准。

### EXP-000: 项目初始化

- **说明**：按 `Nvidia-Nemotron/` 目录与流程初始化；`data/` 含 `train.csv` / `test.csv` / `sample_submission.csv`。
- **本地 CSV 快照**：`train.csv` **1785** 行、**357** 张唯一图（每图 5 行 target）；`test.csv` 公开 **5** 行（1 张图 × 5 target）。图像文件需从 Kaggle Data 挂载或下载。
- **后续**：双路 SigLIP+DINO 见 **EXP-003**；单模 Huge+ 见 **EXP-002**；四路大集成见 **EXP-001**。
