#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Decision Qualification Gate（决策资格闸门）V2.3-RC2
====================================================
GPT 红队审计（P0-1/P0-2/P0-3 + P1-1/P1-2）修复后的组合引擎。

核心变化：从"字段级防火墙"升级为"Decision Graph 防火墙"。

P0-1 Graph-level Authority Propagation：
  建立 Decision → Reason/Score/Condition → Insight/Hypothesis → Evidence 反向追溯
  链路最低 Authority = 整条链最高可用 Authority Ceiling（向上继承）

P0-2 Indirect Bypass Block：
  任何 D/E → Insight/Hypothesis/Score/Condition/Narrative → Final Decision 路径必须阻断

P0-3 Qualification Orchestrator：
  Evidence Authority PASS AND Sample Coverage PASS/downgrade → Qualification
  调用方不能只跑一个 Gate

P1-1 UNKNOWN Evidence → FAIL/BLOCKED（不得 PASS）

P1-2 参数 provenance：Gate 参数必须有独立来源声明（provenance），
     不能由被审计的推理节点自评（AI 自评 bias=0.95 路径被标记）
"""
import json, datetime
from collections import defaultdict


class DecisionQualificationGate:
    """组合闸门：Evidence Graph 反向追溯 + Authority 传播 + 双 Gate AND 裁决"""

    # 等级强度（用于传播与比较）
    LEVEL_ORDER = {"A": 5, "B": 4, "C": 3, "D": 2, "E": 1, "UNKNOWN": 0}

    def __init__(self, evidence_layer=None, insight_layer=None, hypothesis_layer=None,
                 score_engine=None, coverage_params=None, provenance=None):
        self.evidence_layer = evidence_layer or {}
        self.insight_layer = insight_layer or {}
        self.hypothesis_layer = hypothesis_layer or {}
        self.score_engine = score_engine or {}
        self.coverage_params = coverage_params or {}
        # P1-2: provenance 记录（参数来源，不能由被审计节点自评）
        self.provenance = provenance or {}
        self.findings = []

    # ============ P0-1: Authority Propagation（图级追溯）============

    def resolve_evidence_level(self, eid):
        """取证据等级（UNKNOWN 时返回 UNKNOWN 而非默认）"""
        e = self.evidence_layer.get(eid, {})
        level = (e.get("evidence_status") or e.get("evidence_level") or "").upper()
        return level if level in self.LEVEL_ORDER else "UNKNOWN"

    def node_authority(self, node):
        """计算某节点的 Authority Ceiling = 其直接引用的最低证据等级"""
        ev_ids = node.get("evidence", []) if isinstance(node, dict) else []
        if not ev_ids:
            return "UNKNOWN", []
        levels = [self.resolve_evidence_level(e) for e in ev_ids]
        # 最低等级（保守）
        min_level = min(levels, key=lambda x: self.LEVEL_ORDER.get(x, 0))
        return min_level, levels

    def trace_decision_chain(self, decision_refs):
        """反向追溯: Decision → Reason/Score/Condition → Insight/Hypothesis → Evidence
        decision_refs: {"reasons": [...], "score": {...}, "conditions": [...]}
        返回每条链的节点序列 + 最低 Authority"""
        chains = []

        def walk(node_id, role, depth=0):
            """递归向上：node -> evidence（含间接 insight/hypothesis）"""
            chain = []

            def _trace(obj, role, seen):
                if id(obj) in seen:
                    return []
                seen = seen | {id(obj)}
                ev_ids = obj.get("evidence", []) if isinstance(obj, dict) else []
                direct = [("evidence", e, self.resolve_evidence_level(e)) for e in ev_ids]
                # 间接引用：insight/hypothesis 作为中介
                indirect = []
                for lid in obj.get("linked_insights", []) if isinstance(obj, dict) else []:
                    if lid in self.insight_layer:
                        sub = self._trace(self.insight_layer[lid], "insight", seen)
                        indirect.extend(sub)
                for hid in obj.get("linked_hypotheses", []) if isinstance(obj, dict) else []:
                    if hid in self.hypothesis_layer:
                        sub = self._trace(self.hypothesis_layer[hid], "hypothesis", seen)
                        indirect.extend(sub)
                return direct + indirect

            # 决策引用 -> 追溯
            return _trace({"evidence": decision_refs}, "decision", set())

        # 简化：收集所有决策引用的证据（含间接层）
        all_refs = []
        for r in decision_refs.get("reasons", []):
            all_refs.append(("reason", r.get("id", "?"), r.get("evidence", []), r.get("linked_insights", []), r.get("linked_hypotheses", [])))
        for c in decision_refs.get("conditions", []):
            all_refs.append(("condition", c.get("id", "?"), c.get("evidence", []), c.get("linked_insights", []), c.get("linked_hypotheses", [])))
        for s in decision_refs.get("scores", []):
            all_refs.append(("score", s.get("id", "?"), s.get("evidence", []), s.get("linked_insights", []), s.get("linked_hypotheses", [])))

        # 逐链展开（含间接层）
        for role, rid, ev_ids, li, lh in all_refs:
            chain = []
            for e in ev_ids:
                chain.append(("evidence", e, self.resolve_evidence_level(e)))
            for iid in li:
                if iid in self.insight_layer:
                    ins = self.insight_layer[iid]
                    chain.append(("insight", iid, self.node_authority(ins)[0]))
                    for e in ins.get("evidence", []):
                        chain.append(("evidence", e, self.resolve_evidence_level(e)))
            for hid in lh:
                if hid in self.hypothesis_layer:
                    hyp = self.hypothesis_layer[hid]
                    chain.append(("hypothesis", hid, self.node_authority(hyp)[0]))
                    for e in hyp.get("evidence_for", []) + hyp.get("evidence_against", []):
                        chain.append(("evidence", e, self.resolve_evidence_level(e)))
            if chain:
                # 链路最低 Authority = 整条链最高可用上限
                min_level = min((x[2] for x in chain), key=lambda x: self.LEVEL_ORDER.get(x, 0))
                chains.append({
                    "role": role, "ref_id": rid, "chain": chain,
                    "chain_min_authority": min_level,
                })
        return chains

    # ============ P0-2: Indirect Bypass Block ============

    def check_indirect_bypass(self, chains):
        """检查任何链路上是否有 D/E 证据（含间接 Insight/Hypothesis 路径）。
        Negative Evidence 原则（GPT 审计第③点）：
          - reasons / scores：D/E 严禁（支撑决策的依据必须有资格）
          - conditions：允许 D/E（低权限≠没用——可作验证条件/Unknown，
            但不能升级成事实判断）
        """
        violations = []
        for ch in chains:
            if ch["role"] == "condition":
                continue  # condition 允许 D/E（Negative Evidence 语义）
            has_de = [x for x in ch["chain"] if x[2] in ("D", "E")]
            if has_de:
                path = " → ".join(f"{r}({l})" for _, r, l in has_de)
                violations.append({
                    "ref": f"{ch['role']}:{ch['ref_id']}",
                    "issue": f"间接路径含 D/E 证据: {path}",
                    "level": "VIOLATION",
                })
        return violations

    # ============ P0-3: Qualification Orchestrator ============

    def qualify(self, decision_refs, coverage_result=None, strict=True):
        """组合裁决: Evidence Authority AND Sample Coverage → Qualification"""
        from evidence_authority_gate import EvidenceAuthorityGate
        from sample_coverage_gate import SampleCoverageGate

        # 1. Evidence Authority（直连 Reason 检查，复用原 Gate）
        auth_gate = EvidenceAuthorityGate(self.evidence_layer)
        reasons = decision_refs.get("reasons", [])
        auth_result = auth_gate.check_reasons(reasons)

        # 2. 图级传播 + 间接阻断（P0-1 + P0-2）
        chains = self.trace_decision_chain(decision_refs)
        bypass = self.check_indirect_bypass(chains)
        if bypass:
            auth_result["violations"].extend(bypass)
            auth_result["status"] = "FAIL"

        # 3. UNKNOWN 不得 PASS（P1-1）——但 condition 链允许（Negative Evidence）
        unknown_refs = []
        for ch in chains:
            if ch["role"] == "condition":
                continue  # condition 允许 UNKNOWN（待验证项）
            for role, rid, level in ch["chain"]:
                if level == "UNKNOWN":
                    unknown_refs.append(f"{role}:{rid}")
        if unknown_refs:
            auth_result["violations"].append({
                "reason": "UNKNOWN evidence",
                "issue": f"UNKNOWN 等级证据不得 PASS: {unknown_refs}",
                "level": "VIOLATION",
            })
            auth_result["status"] = "FAIL"

        # 4. Sample Coverage（P0-3: 强制组合）
        coverage_gate = SampleCoverageGate()
        cov = coverage_result or coverage_gate.evaluate(self.coverage_params)

        # 5. P1-2: provenance 检查（参数不能由被审计节点自评）
        prov_issues = []
        if self.coverage_params:
            for k in ["coverage", "bias", "geographic", "category_penetration", "completeness", "temporal"]:
                p = self.provenance.get(k, {})
                source = p.get("source", "UNSPECIFIED")
                if source in ("AI_SELF", "UNSPECIFIED", ""):
                    prov_issues.append(f"{k}: 参数来源={source}（需独立 provenance，不能由被审计节点自评）")

        # 6. 组合裁决（AND）
        auth_pass = auth_result["status"] == "PASS"
        cov_blocked = cov["decision_scope"] in ("INSUFFICIENT",)
        # Coverage 允许降级（LOCAL/REGIONAL）但不能拒绝
        cov_ok = not cov_blocked

        if not auth_pass:
            qualification = "REJECTED"
            reason = f"Evidence Authority FAIL（{len(auth_result['violations'])} 违规）"
        elif not cov_ok:
            qualification = "REJECTED"
            reason = f"Sample Coverage INSUFFICIENT（{cov['decision_scope']}）"
        elif prov_issues:
            qualification = "CONDITIONAL"
            reason = f"provenance 缺失（{len(prov_issues)} 项参数来源不明）"
        else:
            qualification = "QUALIFIED"
            reason = f"Authority PASS + Coverage {cov['decision_scope']}（降级适用）"

        result = {
            "qualification": qualification,
            "reason": reason,
            "evidence_authority": auth_result["status"],
            "coverage_scope": cov["decision_scope"],
            "coverage_score": cov["scope_score"],
            "chains_traced": len(chains),
            "bypass_violations": len(bypass),
            "unknown_refs": unknown_refs,
            "provenance_issues": prov_issues,
            "violations": auth_result["violations"],
            "status": qualification,
        }
        return result

    def self_test(self):
        """回归测试：全路径验证"""
        ev = {
            "E001": {"evidence_status": "A", "metric": "m1"},
            "E002": {"evidence_status": "B", "metric": "m2"},
            "E008": {"evidence_status": "D", "metric": "m8"},
            "E999": {"metric": "no-level"},  # UNKNOWN
        }
        ins = {
            "I001": {"evidence": ["E001"], "statement": "A级洞察"},
            "I005": {"evidence": ["E008"], "statement": "D级洞察"},  # 受 D 污染
        }
        hyp = {
            "H003": {"evidence_for": ["E008"], "evidence_against": [], "statement": "基于D的假设"},
        }
        cov = {"coverage": 0.92, "bias": 0.9, "geographic": 1.0,
               "category_penetration": 0.85, "completeness": 0.9, "temporal": 0.6}
        prov = {"coverage": {"source": "FID_PIPELINE"}, "bias": {"source": "FID_PIPELINE"},
                "geographic": {"source": "FID_PIPELINE"}, "category_penetration": {"source": "FID_PIPELINE"},
                "completeness": {"source": "FID_PIPELINE"}, "temporal": {"source": "FID_PIPELINE"}}

        gate = DecisionQualificationGate(ev, ins, hyp, None, cov, prov)

        # 干净案例（全部 A/B，间接层干净）
        clean = {
            "reasons": [{"id": "R1", "text": "干净", "evidence": ["E001"], "linked_insights": ["I001"]}],
            "conditions": [], "scores": [],
        }
        r1 = gate.qualify(clean)
        # 绕过案例（Reason 直连 E001，但 linked_insight I005 受 D 污染）
        bypass = {
            "reasons": [{"id": "R2", "text": "表面干净", "evidence": ["E001"], "linked_insights": ["I005"]}],
            "conditions": [], "scores": [],
        }
        r2 = gate.qualify(bypass)
        # UNKNOWN 案例
        unknown = {
            "reasons": [{"id": "R3", "text": "未知等级", "evidence": ["E999"]}],
            "conditions": [], "scores": [],
        }
        r3 = gate.qualify(unknown)
        # provenance 缺失案例
        gate2 = DecisionQualificationGate(ev, ins, hyp, None, cov, {})
        r4 = gate2.qualify(clean)

        return {"clean": r1, "bypass": r2, "unknown": r3, "no_prov": r4}


if __name__ == "__main__":
    g = DecisionQualificationGate()
    r = g.self_test()
    print("=== Decision Qualification Gate 自检（V2.3-RC2）===")
    names = {"clean": "干净案例(全A/B)", "bypass": "间接绕过(D藏Insight)", "unknown": "UNKNOWN证据", "no_prov": "provenance缺失"}
    for k, v in r.items():
        status = v["status"]
        mark = "✅" if status == "QUALIFIED" else ("🟡" if status == "CONDITIONAL" else "❌")
        print(f"  {mark} [{names[k]}] {status}")
        print(f"     原因: {v['reason']}")
        if k == "bypass":
            print(f"     阻断: {v['bypass_violations']} 条间接路径违规")
        if k == "unknown":
            print(f"     UNKNOWN引用: {v['unknown_refs']}")
        if k == "no_prov":
            print(f"     provenance问题: {len(v['provenance_issues'])} 项")
