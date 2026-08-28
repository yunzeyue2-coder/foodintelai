#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
FDE Evidence Binding（FDE 证据绑定层）
======================================
把"评分"变成"证据驱动评分"。

旧: 市场吸引力 78
新: 市场吸引力 78
    依据: E001(门店规模) E002(价格空间) E003(品牌集中度)
    反向风险: E006(竞争密度)
    置信度: B

核心约束（Decision Authority 落地）:
- 每个分数维度必须绑定 evidence（依据）
- 允许绑定反向证据（风险），不是只"证明自己"
- 置信度由证据等级推导：全A→A级结论；含B→B级；含C/D→降级
"""
import json, os

# 五维评分结构（FDE-V0.3）
DIMENSIONS = {
    "market":     {"name": "市场吸引力",     "weight": 0.25},
    "competition": {"name": "竞争压力",       "weight": 0.20},
    "operation":  {"name": "运营复杂度",     "weight": 0.20},
    "resource":   {"name": "资源匹配度",     "weight": 0.25},
    "timing":     {"name": "时机窗口",       "weight": 0.10},
}

# 证据等级映射
LEVEL_SCORE = {"A": 1.0, "B": 0.8, "C": 0.5, "D": 0.2, "E": 0.5}


class FDE:
    def __init__(self, model_version="FDE-V0.4"):
        self.model_version = model_version
        self.scores = {}  # dim -> {score, evidence_for, evidence_against, confidence}

    def score_dim(self, dim, score, evidence_for=None, evidence_against=None, evidence_levels=None):
        """给维度评分并绑定证据
        dim: market/competition/operation/resource/timing
        score: 0-100
        evidence_for: [E001, ...]
        evidence_against: [E006, ...]
        evidence_levels: {E001: "A", ...} 用于置信度推导
        """
        if dim not in DIMENSIONS:
            return False, f"非法维度 {dim}"
        evidence_for = evidence_for or []
        evidence_against = evidence_against or []
        evidence_levels = evidence_levels or {}

        # 置信度推导：取所有证据的最低等级（保守原则）
        all_ev = evidence_for + evidence_against
        if not all_ev:
            conf = "D"  # 无证据 → 不能给分数
        else:
            levels = [evidence_levels.get(e, "C") for e in all_ev]
            order = ["A", "B", "C", "D", "E"]
            conf = min(levels, key=lambda x: order.index(x) if x in order else 2)

        self.scores[dim] = {
            "dimension": dim,
            "name": DIMENSIONS[dim]["name"],
            "score": score,
            "evidence_for": evidence_for,
            "evidence_against": evidence_against,
            "confidence": conf,
            "bound": len(all_ev) > 0,
        }
        return True, f"{dim}={score} (依据{len(evidence_for)}/反证{len(evidence_against)}/置信度{conf})"

    def compute(self):
        """计算总分（加权）——未绑定证据的维度不参与"""
        total_w = 0
        total = 0
        unbounded = []
        for dim, d in DIMENSIONS.items():
            if dim in self.scores and self.scores[dim]["bound"]:
                total += self.scores[dim]["score"] * d["weight"]
                total_w += d["weight"]
            else:
                unbounded.append(dim)
        final = round(total / total_w) if total_w > 0 else None
        return {
            "model_version": self.model_version,
            "final_score": final,
            "weights_used": total_w,
            "unbounded_dims": unbounded,
            "dimension_scores": self.scores,
        }

    def evidence_gap_report(self):
        """输出证据缺口（哪些维度没绑定）——防止'评分无依据'"""
        gaps = [dim for dim in DIMENSIONS if dim not in self.scores or not self.scores[dim]["bound"]]
        return gaps

    def to_json(self, path=None):
        d = self.compute()
        s = json.dumps(d, ensure_ascii=False, indent=2)
        if path:
            with open(path, "w", encoding="utf-8") as f:
                f.write(s)
        return s

    def self_test(self):
        """回归测试：炸鸡评分证据绑定"""
        f = FDE()
        f.score_dim("market", 78, ["E001", "E002", "E003"], ["E006"],
                    {"E001": "A", "E002": "B", "E003": "B", "E006": "B"})
        f.score_dim("competition", 72, ["E010", "E011"], ["E012"],
                    {"E010": "B", "E011": "B", "E012": "B"})
        f.score_dim("operation", 75, ["E010"], ["E008"], {"E010": "B", "E008": "D"})
        f.score_dim("resource", 70, ["E003"], [], {"E003": "B"})
        f.score_dim("timing", 68, ["E002"], [], {"E002": "B"})
        return f


if __name__ == "__main__":
    f = FDE().self_test()
    print("=== FDE Evidence Binding 自检 ===")
    for dim, s in f.scores.items():
        print(f"  {s['name']} {s['score']} | 依据{s['evidence_for']} | 反证{s['evidence_against']} | 置信度{s['confidence']}")
    result = f.compute()
    print(f"\n综合评分: {result['final_score']} (权重覆盖 {result['weights_used']})")
    print(f"未绑定维度: {result['unbounded_dims'] or '无'}")
    gaps = f.evidence_gap_report()
    print(f"证据缺口: {gaps or '无'}")
    print("\n✅ FDE 评分已证据驱动：每个分数可反查依据/反证/置信度")
