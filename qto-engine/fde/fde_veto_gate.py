#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
FDE Veto Gate（决策否决闸门）V1.0
=================================
GPT 工业化清单 Sprint 2 / 沧林 Schema V2.0 risk_gate：
从"线性评分"升级为"Gate Check → Risk Penalty → Decision"。

旧: Score(Market×0.7 + Match×0.3) → Decision（机会可以掩盖能力不足）
新: Score → Hard Gate(硬约束) → Penalty(风险扣分) → Decision

核心能力：
1. Hard Constraints（Veto）：skill_gap<30 → REJECT / capital_gap<40 → WARNING
2. Risk Penalty：软风险按权重扣分，不直接否决
3. 输出决策：GO / CONDITIONAL_GO / REVISED_ENTRY / WAIT / NOT_RECOMMENDED
4. GPT 验收案例：20万+无餐饮经验+生炸 → 不能输出 R2(GO/CONDITIONAL_GO)
"""
import json


class FDEVetoGate:
    # 决策档位（对齐 Schema V2.0 final_decision）
    DECISIONS = ["GO", "CONDITIONAL_GO", "REVISED_ENTRY", "WAIT", "NOT_RECOMMENDED"]

    # 默认硬约束（可被项目 config 覆盖）
    DEFAULT_HARD_CONSTRAINTS = [
        {"name": "skill_gap", "threshold": 30, "action": "reject",
         "reason": "工艺/运营技能不足，无法独立运营"},
        {"name": "capital_gap", "threshold": 40, "action": "warning",
         "reason": "预算与品类启动成本差距较大"},
        {"name": "survival_gap", "threshold": 3, "action": "reject",
         "reason": "生存压力测试撑不过3个月（低场景）"},
    ]

    # 默认软风险扣分（可覆盖）
    DEFAULT_PENALTIES = [
        {"name": "experience_gap", "weight": 0.15, "note": "无行业经验"},
        {"name": "competition_pressure", "weight": 0.10, "note": "竞争密度高"},
        {"name": "data_uncertainty", "weight": 0.05, "note": "数据覆盖不足"},
    ]

    def __init__(self, hard_constraints=None, penalties=None):
        self.hard_constraints = hard_constraints or self.DEFAULT_HARD_CONSTRAINTS
        self.penalties = penalties or self.DEFAULT_PENALTIES

    # ============ 1. Hard Gate（Veto）============

    def check_hard_gate(self, profile):
        """硬约束检查：返回 violations（触发 veto 的约束）
        profile: {skill_score, capital_score, survival_months_low, ...}
        """
        violations = []
        for c in self.hard_constraints:
            val = profile.get(c["name"])
            if val is None:
                continue  # 无数据不触发（保守：不因缺数据误杀）
            if c["action"] == "reject" and val < c["threshold"]:
                violations.append({**c, "value": val, "severity": "VETO"})
            elif c["action"] == "warning" and val < c["threshold"]:
                violations.append({**c, "value": val, "severity": "WARNING"})
        return violations

    # ============ 2. Risk Penalty ============

    def apply_penalty(self, base_score, profile):
        """软风险扣分：base_score * (1 - Σweight_i) 当对应风险存在"""
        total_penalty = 0.0
        applied = []
        for p in self.penalties:
            key = p["name"]
            # 风险值 > 阈值（0-1，越高风险越大）则扣分
            risk_val = profile.get(key, 0)
            if risk_val and risk_val > 0.3:
                total_penalty += p["weight"]
                applied.append({**p, "risk_value": risk_val})
        penalized = base_score * (1 - min(total_penalty, 0.5))  # 扣分上限50%
        return round(penalized), applied, round(total_penalty, 2)

    # ============ 3. 决策裁决 ============

    def decide(self, base_score, profile):
        """完整裁决：Hard Gate → Penalty → Decision"""
        violations = self.check_hard_gate(profile)

        # Veto：存在 REJECT 级违规 → 直接 NOT_RECOMMENDED
        vetoes = [v for v in violations if v["severity"] == "VETO"]
        if vetoes:
            return {
                "decision": "NOT_RECOMMENDED",
                "reason": f"硬约束否决: {vetoes[0]['reason']}（{vetoes[0]['name']}={vetoes[0]['value']} < {vetoes[0]['threshold']}）",
                "base_score": base_score,
                "final_score": 0,
                "veto_triggers": vetoes,
                "warnings": [v for v in violations if v["severity"] == "WARNING"],
                "penalty_applied": [],
                "penalty_total": 0,
            }

        # Penalty
        final_score, applied, penalty_total = self.apply_penalty(base_score, profile)
        warnings = [v for v in violations if v["severity"] == "WARNING"]

        # 分档
        if final_score >= 75:
            decision = "GO"
        elif final_score >= 60:
            decision = "CONDITIONAL_GO"
        elif final_score >= 45:
            decision = "REVISED_ENTRY"
        elif final_score >= 30:
            decision = "WAIT"
        else:
            decision = "NOT_RECOMMENDED"

        # WARNING 级硬约束降档
        if warnings and decision in ("GO", "CONDITIONAL_GO"):
            decision = "REVISED_ENTRY" if decision == "GO" else "CONDITIONAL_GO"

        return {
            "decision": decision,
            "reason": f"评分 {base_score} → 风险扣分{penalty_total:.0%} → {final_score}",
            "base_score": base_score,
            "final_score": final_score,
            "veto_triggers": vetoes,
            "warnings": warnings,
            "penalty_applied": applied,
            "penalty_total": penalty_total,
        }


if __name__ == "__main__":
    print("=== FDE Veto Gate V1.0 自检 ===")
    gate = FDEVetoGate()

    # 场景1: GPT 验收案例——20万+无经验+生炸 → 必须 NOT_RECOMMENDED
    print("\n[场景1] 20万+无餐饮经验+生炸整鸡")
    r1 = gate.decide(base_score=80, profile={
        "skill_gap": 25,           # 技能25 < 30 → VETO
        "capital_gap": 55,
        "survival_months_low": 3.1,
        "experience_gap": 0.9,
        "competition_pressure": 0.6,
        "data_uncertainty": 0.3,
    })
    print(f"  决策: {r1['decision']} {'✅ 被否决' if r1['decision']=='NOT_RECOMMENDED' else '❌ 未拦截'}")
    print(f"  原因: {r1['reason']}")

    # 场景2: 技能达标但经验缺 → CONDITIONAL_GO 带警告
    print("\n[场景2] 技能65+经验缺 → 降档")
    r2 = gate.decide(base_score=80, profile={
        "skill_gap": 65,
        "capital_gap": 55,
        "survival_months_low": 5.3,
        "experience_gap": 0.9,
        "competition_pressure": 0.6,
        "data_uncertainty": 0.3,
    })
    print(f"  决策: {r2['decision']} | 评分 {r2['base_score']} → {r2['final_score']}")
    print(f"  原因: {r2['reason']}")

    # 场景3: 全绿 → GO
    print("\n[场景3] 技能80+经验0.2+资金足 → GO")
    r3 = gate.decide(base_score=82, profile={
        "skill_gap": 80, "capital_gap": 70, "survival_months_low": 8.0,
        "experience_gap": 0.2, "competition_pressure": 0.3, "data_uncertainty": 0.2,
    })
    print(f"  决策: {r3['decision']} | 评分 {r3['base_score']} → {r3['final_score']}")
