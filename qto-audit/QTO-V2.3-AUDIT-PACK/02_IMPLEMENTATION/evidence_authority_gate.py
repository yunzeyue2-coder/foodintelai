#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Evidence Authority Gate（证据资格闸门）V2.3
============================================
把 Decision Authority 从"文档规范"变成"机器约束"。

问题（米线 PORT-001 复核⑤暴露）：
  Reason #1 → A级证据
  Reason #2 → A级证据
  Reason #3 → C级证据   ← 与 A 级并列进入同一层级，违反 Authority
  Reason #4 → A级证据

规则（沧林 2026-08-10 拍板）：
  Evidence等级  可承担角色
  A            主决策理由（Primary）
  B            主理由，但需注明限制（Primary + caveat）
  C            只能作为条件/假设/待验证项（Conditional）
  D/E          不得进入正式决策依据（Rejected）

输出结构：
  DECISION REASONS
  ├── Primary Evidence    A / A / B（带caveat）
  └── Conditional Evidence C → 仅支持条件，不得独立形成方向

用法:
  from evidence_authority_gate import EvidenceAuthorityGate, check_reasons
  gate = EvidenceAuthorityGate(evidence_layer)
  result = check_reasons(reasons, evidence_layer)
"""
import json

# 等级 -> 允许角色
ROLE_MAP = {
    "A": "primary",
    "B": "primary_caveat",
    "C": "conditional",
    "D": "rejected",
    "E": "rejected",
}


class EvidenceAuthorityGate:
    def __init__(self, evidence_layer=None):
        self.evidence_layer = evidence_layer or {}

    def get_evidence_level(self, eid):
        """取证据等级（兼容 evidence_status / evidence_level / confidence 字段）"""
        e = self.evidence_layer.get(eid, {})
        level = e.get("evidence_status") or e.get("evidence_level") or ""
        return level.upper() if level else "UNKNOWN"

    def classify(self, eid):
        """分类单个证据的角色"""
        level = self.get_evidence_level(eid)
        role = ROLE_MAP.get(level, "unknown")
        return {"evidence_id": eid, "level": level, "role": role}

    def check_reasons(self, reasons, allow_conditional=True):
        """检查整组决策理由。
        reasons: [{"text": "...", "evidence": ["E001", ...]}]
        返回: 分级后的结构 + 违规清单
        """
        primary = []
        conditional = []
        rejected = []
        violations = []

        for i, r in enumerate(reasons, 1):
            ev_ids = r.get("evidence", [])
            r_id = r.get("id", f"R{i}")
            text = r.get("text", "")

            # 无证据理由
            if not ev_ids:
                violations.append({"reason": r_id, "issue": "无证据绑定", "level": "VIOLATION"})
                continue

            # 取该理由引用的最低等级（保守）
            levels = [self.get_evidence_level(e) for e in ev_ids]
            min_level = min(levels, key=lambda x: list(ROLE_MAP.keys()).index(x) if x in ROLE_MAP else 99)
            role = ROLE_MAP.get(min_level, "unknown")

            entry = {
                "id": r_id, "text": text, "evidence": ev_ids,
                "evidence_levels": levels, "min_level": min_level, "role": role,
            }

            if role == "primary" or role == "primary_caveat":
                primary.append(entry)
            elif role == "conditional":
                conditional.append(entry)
                if not allow_conditional:
                    violations.append({"reason": r_id, "issue": f"C级证据({min_level})作为决策理由（当不允许条件理由时）", "level": "VIOLATION"})
            elif role == "rejected":
                rejected.append(entry)
                violations.append({"reason": r_id, "issue": f"D/E级证据({min_level})不得进入正式决策依据", "level": "VIOLATION"})
            else:
                violations.append({"reason": r_id, "issue": f"未知证据等级({min_level})", "level": "WARNING"})

        result = {
            "primary_reasons": primary,
            "conditional_reasons": conditional,
            "rejected": rejected,
            "violations": violations,
            "status": "PASS" if not any(v["level"] == "VIOLATION" for v in violations) else "FAIL",
        }
        return result

    def self_test(self):
        """回归测试：A/B 主理由 + C 条件 + D/E 拒绝"""
        ev = {
            "E001": {"evidence_status": "A"},
            "E002": {"evidence_status": "B"},
            "E003": {"evidence_status": "C"},
            "E004": {"evidence_status": "D"},
            "E005": {"evidence_status": "E"},
        }
        gate = EvidenceAuthorityGate(ev)
        reasons = [
            {"id": "R1", "text": "A级主理由", "evidence": ["E001"]},
            {"id": "R2", "text": "B级主理由", "evidence": ["E002"]},
            {"id": "R3", "text": "C级条件理由", "evidence": ["E003"]},
            {"id": "R4", "text": "D级应被拒", "evidence": ["E004"]},
            {"id": "R5", "text": "E级应被拒", "evidence": ["E005"]},
        ]
        return gate.check_reasons(reasons)


if __name__ == "__main__":
    r = EvidenceAuthorityGate().self_test()
    print("=== Evidence Authority Gate 自检 ===")
    print(f"主理由({len(r['primary_reasons'])}): {[x['id'] for x in r['primary_reasons']]}")
    print(f"条件理由({len(r['conditional_reasons'])}): {[x['id'] for x in r['conditional_reasons']]}")
    print(f"被拒({len(r['rejected'])}): {[x['id'] for x in r['rejected']]}")
    print(f"违规({len(r['violations'])}):")
    for v in r["violations"]:
        print(f"  ❌ {v['reason']}: {v['issue']}")
    print(f"\n状态: {r['status']}（应 FAIL——D/E 被拒）")
