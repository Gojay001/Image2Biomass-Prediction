#!/usr/bin/env python3
"""只读分析 CSIRO biomass train.csv：行数、列、target 与图像聚合统计。"""

from __future__ import annotations

import argparse
import csv
import math
import sys
from collections import Counter, defaultdict
from pathlib import Path


def _quantiles(sorted_vals: list[float], qs: tuple[float, ...]) -> dict[float, float]:
    if not sorted_vals:
        return {q: float("nan") for q in qs}
    n = len(sorted_vals)
    out: dict[float, float] = {}
    for q in qs:
        if n == 1:
            out[q] = sorted_vals[0]
            continue
        pos = q * (n - 1)
        lo = int(math.floor(pos))
        hi = int(math.ceil(pos))
        if lo == hi:
            out[q] = sorted_vals[lo]
        else:
            t = pos - lo
            out[q] = sorted_vals[lo] * (1 - t) + sorted_vals[hi] * t
    return out


def analyze(path: Path) -> str:
    lines: list[str] = []
    with path.open(newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        if not reader.fieldnames:
            return "错误：CSV 无表头\n"
        fieldnames = list(reader.fieldnames)
        rows = list(reader)

    n = len(rows)
    lines.append(f"文件: {path}")
    lines.append(f"行数（不含表头）: {n}")
    lines.append(f"列: {', '.join(fieldnames)}")

    # target_name 分布
    if "target_name" in fieldnames:
        c = Counter(r.get("target_name", "") for r in rows)
        lines.append("\n[target_name] 计数:")
        for k, v in sorted(c.items(), key=lambda x: (-x[1], x[0])):
            lines.append(f"  {k}: {v}")

    # 每图行数
    if "image_path" in fieldnames:
        per_image: dict[str, int] = defaultdict(int)
        for r in rows:
            per_image[r.get("image_path", "")] += 1
        counts = sorted(per_image.values())
        lines.append("\n[按 image_path] 每张图行数:")
        lines.append(f"  唯一图像数: {len(per_image)}")
        if counts:
            lines.append(f"  每图行数 min/max: {min(counts)} / {max(counts)}")
            qc = _quantiles(counts, (0.0, 0.5, 1.0))
            lines.append(
                f"  每图行数 p0/p50/p100: {qc[0.0]:.0f} / {qc[0.5]:.1f} / {qc[1.0]:.0f}"
            )

    # target 数值
    if "target" in fieldnames:
        vals: list[float] = []
        bad = 0
        for r in rows:
            s = (r.get("target") or "").strip()
            if s == "":
                bad += 1
                continue
            try:
                vals.append(float(s))
            except ValueError:
                bad += 1
        vals.sort()
        lines.append("\n[target] 统计:")
        lines.append(f"  可解析: {len(vals)}, 无效/空: {bad}")
        if vals:
            q = _quantiles(vals, (0.0, 0.05, 0.25, 0.5, 0.75, 0.95, 1.0))
            lines.append(
                "  分位数 p0/p5/p25/p50/p75/p95/p100: "
                f"{q[0.0]:.4f} / {q[0.05]:.4f} / {q[0.25]:.4f} / "
                f"{q[0.5]:.4f} / {q[0.75]:.4f} / {q[0.95]:.4f} / {q[1.0]:.4f}"
            )

    # State / Species 基数
    for col in ("State", "Species"):
        if col in fieldnames:
            u = {r.get(col, "") for r in rows}
            lines.append(f"\n[{col}] 唯一值数量: {len(u)}")

    lines.append("")
    return "\n".join(lines)


def main() -> int:
    p = argparse.ArgumentParser(description="Analyze CSIRO train.csv (stdlib only).")
    p.add_argument("--csv", type=Path, default=Path("data/train.csv"), help="Path to train.csv")
    p.add_argument("--output", type=Path, default=None, help="Write report to file")
    args = p.parse_args()

    if not args.csv.is_file():
        print(f"找不到文件: {args.csv}", file=sys.stderr)
        return 1

    report = analyze(args.csv)
    if args.output:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(report, encoding="utf-8")
        print(f"已写入: {args.output}")
    else:
        print(report, end="")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
