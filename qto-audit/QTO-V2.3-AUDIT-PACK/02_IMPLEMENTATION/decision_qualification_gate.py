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

    # ============ P0-RC3: 通用递归 Graph Traversal ============

    def resolve_evidence_level(self, eid):
        """取证据等级（UNKNOWN 时返回 UNKNOWN 而非默认）"""
        e = self.evidence_layer.get(eid, {})
        level = (e.get("evidence_status") or e.get("evidence_level") or "").upper()
        return level if level in self.LEVEL_ORDER else "UNKNOWN"

    def _get_node(self, node_id):
        """按 id 取任意类型节点（insight/hypothesis/score/condition 统一注册表）"""
        if node_id in self.insight_layer:
            return ("insight", self.insight_layer[node_id])
        if node_id in self.hypothesis_layer:
            return ("hypothesis", self.hypothesis_layer[node_id])
        return (None, None)

    def _links_of(self, node):
        """节点的下一跳链接（统一取 linked_insights/linked_hypotheses/linked_nodes）"""
        links = []
        for k in ("linked_insights", "linked_hypotheses", "linked_nodes", "links"):
            for lid in node.get(k, []) if isinstance(node, dict) else []:
                if isinstance(lid, str):
                    links.append(lid)
                elif isinstance(lid, dict) and lid.get("id"):
                    links.append(lid["id"])
        return links

    def _evidence_of(self, node):
        """节点的直接证据引用（统一取 evidence/evidence_for/evidence_against）"""
        ev = []
        for k in ("evidence", "evidence_for", "evidence_against"):
            ev.extend(node.get(k, []) if isinstance(node, dict) else [])
        return ev

    def trace_decision_chain(self, decision_refs, max_depth=10):
        """通用递归图遍历（DFS + visited + cycle detection + max depth）。
        Decision → 任意节点（Insight/Hypothesis/...）→ ... → Evidence。
        任意深度：D/E 无论藏在图多深，都能被追溯到。

        decision_refs: {"reasons": [...], "conditions": [...], "scores": [...]}
        每个 ref: {id, evidence[], linked_insights[], linked_hypotheses[], linked_nodes[]}
        """
        chains = []
        seen_global = set()  # 全局 visited（防跨链重复）
        CYCLES = []  # 环记录（cycle detection）

        def dfs(node_id, role, depth, path):
            """返回该节点可达的所有证据（递归）"""
            if depth > max_depth:
                return []  # 深度上限保护
            if node_id in seen_global:
                return []  # visited（防环/防重复）
            seen_global.add(node_id)

            t, node = self._get_node(node_id)
            if node is None:
                return []

            # 环检测：路径上重复
            if node_id in path:
                CYCLES.append(node_id)
                return []

            ev_ids = self._evidence_of(node)
            result = [("evidence", e, self.resolve_evidence_level(e)) for e in ev_ids]

            # 递归展开子链接（任意深度）
            for link_id in self._links_of(node):
                sub = dfs(link_id, t, depth + 1, path | {node_id})
                result.extend(sub)
            return result

        # 收集决策引用
        all_refs = []
        for r in decision_refs.get("reasons", []):
            all_refs.append(("reason", r))
        for c in decision_refs.get("conditions", []):
            all_refs.append(("condition", c))
        for s in decision_refs.get("scores", []):
            all_refs.append(("score", s))

        # 每个 ref：直接证据 + 递归子图
        for role, ref in all_refs:
            rid = ref.get("id", "?")
            chain = []

            # 直接证据
            for e in self._evidence_of(ref):
                chain.append(("evidence", e, self.resolve_evidence_level(e)))

            # 递归展开链接
            for link_id in self._links_of(ref):
                seen_global = set()  # 每条链独立 visited
                sub = dfs(link_id, "linked", 0, set())
                chain.extend(sub)

            if chain:
                min_level = min((x[2] for x in chain), key=lambda x: self.LEVEL_ORDER.get(x, 0))
                chains.append({
                    "role": role, "ref_id": rid, "chain": chain,
                    "chain_min_authority": min_level,
                    "authority_role": ref.get("authority_role", ""),
                })
        return chains

    # ============ P0-2: Indirect Bypass Block ============

    # Condition 语义分类（GPT RC2 审计 P1）：
    # 允许 D/E 的 role：VALIDATION_REQUIRED / CHALLENGE / UNKNOWN
    # 拒绝 D/E 的 role：FACTUAL_PREMISE / DECISION_DRIVER / 未分类(空)
    # 未分类条件含 D → 保守拒绝（不能默认放行，否则 AI 可写无 role 条件藏 D）
    CONDITION_ALLOW_DE = {"VALIDATION_REQUIRED", "CHALLENGE", "UNKNOWN"}
    CONDITION_DENY_DE = {"FACTUAL_PREMISE", "DECISION_DRIVER"}

    def check_indirect_bypass(self, chains):
        """检查任何链路上是否有 D/E 证据（含间接 Insight/Hypothesis 路径）。
        Negative Evidence 原则（GPT 审计第③点）：
          - reasons / scores：D/E 严禁（支撑决策的依据必须有资格）
          - conditions：按语义分类——
            VALIDATION_REQUIRED/CHALLENGE/UNKNOWN 允许 D（验证条件）
            FACTUAL_PREMISE/DECISION_DRIVER 拒绝 D（当作事实/决策驱动）
        """
        violations = []
        for ch in chains:
            if ch["role"] == "condition":
                role_tag = ch.get("authority_role", "") or ""
                if role_tag in self.CONDITION_ALLOW_DE:
                    continue  # 验证型条件允许 D/E
                if role_tag in self.CONDITION_DENY_DE:
                    has_de = [x for x in ch["chain"] if x[2] in ("D", "E")]
                    if has_de:
                        path = " → ".join(f"{r}({l})" for _, r, l in has_de)
                        violations.append({
                            "ref": f"condition:{ch['ref_id']}",
                            "issue": f"DECISION_DRIVER/FACTUAL_PREMISE 条件含 D/E 证据: {path}",
                            "level": "VIOLATION",
                        })
                    continue
                # 未知 role：保守处理——reasons 语义（不允许 D 藏条件）
                has_de = [x for x in ch["chain"] if x[2] in ("D", "E")]
                if has_de:
                    path = " → ".join(f"{r}({l})" for _, r, l in has_de)
                    violations.append({
                        "ref": f"condition:{ch['ref_id']}",
                        "issue": f"未分类条件含 D/E 证据: {path}",
                        "level": "VIOLATION",
                    })
                continue
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
        #    RC3: PROVENANCE_INVALID → BLOCKED（不是 CONDITIONAL）
        #    理由：不能证明来源 = 不能作为正式决策依据（V2.3 核心原则）
        prov_issues = []
        prov_blocked = False
        if self.coverage_params:
            for k in ["coverage", "bias", "geographic", "category_penetration", "completeness", "temporal"]:
                p = self.provenance.get(k, {})
                source = p.get("source", "UNSPECIFIED")
                if source in ("AI_SELF", "UNSPECIFIED", ""):
                    prov_issues.append(f"{k}: 参数来源={source}（需独立 provenance，不能由被审计节点自评）")
                    prov_blocked = True

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
        elif prov_blocked:
            # RC3 升级：provenance 无效 → BLOCKED（调用方不得把 AI 自评数据带进 Decision）
            qualification = "BLOCKED"
            reason = f"provenance 无效（{len(prov_issues)} 项参数来源不明/AI自评，不能作为正式决策依据）"
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
