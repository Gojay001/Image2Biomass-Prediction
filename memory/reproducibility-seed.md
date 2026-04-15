# 训练与实验固定随机种子（Seed）

本文档约定 Kaggle 训练 notebook 中应如何设置 **seed**，使实验可对比。**完全 bitwise 复现在分布式 / 混合精度下通常不保证**，目标为「同环境、同依赖下尽量可重复」。

---

## 1. 统一常量

- 定义 **`SEED = 42`**（或项目约定单一整数）。
- **数据划分、KFold、shuffle** 均使用该 seed（勿在多处写不同魔法数）。

---

## 2. 常见入口（在训练开始前）

1. **`random.seed(SEED)`**
2. **`numpy.random.seed(SEED)`**（若使用 NumPy）
3. **`torch.manual_seed(SEED)`**
4. **`torch.cuda.manual_seed_all(SEED)`**（若使用 CUDA）
5. 使用 PyTorch Lightning / HF Trainer 时在其参数中传入 **`seed`** / **`pl.seed_everything(SEED)`** 等（以所用库为准）

可选（更强确定性，可能略慢）：

- `torch.backends.cudnn.deterministic = True`
- `torch.backends.cudnn.benchmark = False`

---

## 3. 数据加载

- `DataLoader` 的 **`generator=torch.Generator().manual_seed(SEED)`**（若需）
- 多进程 `num_workers>0` 可能引入残余差异；追求可复现时可在调试阶段用 `num_workers=0`

---

## 4. 与实验解读的关系

- **小幅度 LB 波动** 可能与 seed / 增强 / 环境噪声同量级；**架构与数据策略** 仍是主要依据。
- 固定 seed 用于**减少无关变量**，而非消除所有评测噪声。

---

更新日期：2026-04-15
