#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Sample Coverage Gate（样本覆盖闸门）V2.3
==========================================
Decision Confidence Downgrade——样本少允许分析，但系统自动限制结论外推范围。

核心原则（沧林 2026-08-10 拍板）：
  数据存在 ≠ 数据足够 ≠ 可以推导全局结论
  样本少 → Decision Scope 自动收缩 → Local Direction / Hypothesis
  样本足 → 正常决策（Global Direction）

关键：不写死单一阈值（不是 coverage < 30% → 降级），
而是多变量综合评估：
  Sample Coverage     采样覆盖率（采样/总体估计）
  Sample Selection Bias 选择偏差（是否有系统性偏差）
  Geographic Scope    地理覆盖（单区 vs 全城 vs 全省）
  Category Penetration 品类渗透（识别率/命中率）
  Data Completeness   数据完整度（缺失字段率）
  Temporal Coverage   时间覆盖（单日快照 vs 时序）

输出 Decision Scope 等级：
  GLOBAL    → 城市/品类级结论，可独立决策
  REGIONAL  → 区域/样本级结论，方向待全量验证
  LOCAL     → 仅样本区域初步信号，不得外推
  INSUFFICIENT → 不足以形成方向，仅记录
"""
import json, math

# Decision Scope 判定矩阵（多变量加权，非单阈值）
SCOPE_WEIGHTS = {
    "coverage": 0.25,        # 采样覆盖率
    "bias": 0.20,            # 选择偏差（1=无偏差）
    "geographic": 0.20,      # 地理覆盖（1=全城）
    "category_penetration": 0.15,  # 品类识别渗透（1=高）
    "completeness": 0.10,    # 数据完整度（1=完整）
    "temporal": 0.10,        # 时间覆盖（1=时序完整）
}

SCOPE_THRESHOLDS = [
    (0.75, "GLOBAL", "覆盖充分，可输出城市/品类级结论"),
    (0.55, "REGIONAL", "覆盖不足，Decision Scope 收缩为区域方向，需全量验证"),
    (0.35, "LOCAL", "仅样本区域初步信号，不得外推全局"),
    (0.0, "INSUFFICIENT", "数据不足，仅记录，不形成方向"),
]


class SampleCoverageGate:
    def __init__(self):
        pass

    def evaluate(self, params):
        """params: {coverage, bias, geographic, category_penetration, completeness, temporal}
        各项 0-1（1=最好）。coverage = 采样数/总体估计。"""
        # 归一化校验
        score = 0
        for k, w in SCOPE_WEIGHTS.items():
            v = params.get(k, 0)
            v = max(0.0, min(1.0, float(v)))
            score += v * w

        for threshold, scope, note in SCOPE_THRESHOLDS:
            if score >= threshold:
                break

        result = {
            "scope_score": round(score, 3),
            "decision_scope": scope,
            "scope_note": note,
            "params": params,
        }
        return result

    def downgrade_decision(self, original_decision, scope_result):
        """根据 Scope 对决策降级"""
        scope = scope_result["decision_scope"]
        if scope == "GLOBAL":
            return {"status": "CONFIRMED", "decision": original_decision,
                    "message": "决策范围充分，维持原结论"}
        if scope == "REGIONAL":
            return {"status": "DOWNGRADED", "decision": f"区域性方向（{original_decision}）",
                    "message": "样本覆盖不足：决策收缩为区域方向，全城验证后升级"}
        if scope == "LOCAL":
            return {"status": "DOWNGRADED", "decision": "样本区域初步信号",
                    "message": f"仅样本区域存在该方向初步信号（{original_decision}），证据不足以支持全城决策，需扩大样本验证"}
        return {"status": "BLOCKED", "decision": "不形成方向",
                "message": "数据不足，仅记录，不形成决策"}

    def self_test(self):
        """回归测试：三种场景"""
        results = {}
        # 场景1：充分覆盖（全城 2397 家）
        results["full"] = self.evaluate({
            "coverage": 0.95, "bias": 0.9, "geographic": 1.0,
            "category_penetration": 0.85, "completeness": 0.9, "temporal": 0.5,
        })
        # 场景2：单区（金水区 200 家 vs 全城估计）
        results["regional"] = self.evaluate({
            "coverage": 0.35, "bias": 0.7, "geographic": 0.25,
            "category_penetration": 0.6, "completeness": 0.8, "temporal": 0.2,
        })
        # 场景3：极端（10000 家采样 50 家）
        results["extreme"] = self.evaluate({
            "coverage": 0.005, "bias": 0.5, "geographic": 0.1,
            "category_penetration": 0.4, "completeness": 0.6, "temporal": 0.1,
        })
        return results


if __name__ == "__main__":
    gate = SampleCoverageGate()
    results = gate.self_test()
    print("=== Sample Coverage Gate 自检 ===")
    for name, r in results.items():
        print(f"\n[{name}] scope_score={r['scope_score']} → {r['decision_scope']}")
        print(f"  {r['scope_note']}")
        d = gate.downgrade_decision("郑州米线应开社区店", r)
        print(f"  降级结果: [{d['status']}] {d['decision']}")
        print(f"  → {d['message']}")
