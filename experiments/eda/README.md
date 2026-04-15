# EDA：`train.csv` 分析

## 脚本

| 文件 | 说明 |
|------|------|
| `analyze_train_csv.py` | 只读统计行数、列、`target_name` 分布、按图聚合行数、`target` 简单分位数 |

## 运行

在项目根目录执行（Python 3.9+，**仅标准库**）：

```bash
python experiments/eda/analyze_train_csv.py
```

指定路径或输出报告：

```bash
python experiments/eda/analyze_train_csv.py --csv data/train.csv
python experiments/eda/analyze_train_csv.py --output experiments/eda/output/train_report.txt
```

## 约定

- **不修改** `data/` 下原始文件（见 `AGENTS.md`）。
- 生成报告放在 `experiments/eda/output/`（默认 gitignore）。
