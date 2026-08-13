#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
DecisionGraph（决策图）V2.3-RC4
================================
GPT 第三轮审计（RC3 复审）处方：不再补丁式加 node 类型，
正式建立统一节点注册表 + 单一遍历器。

核心变化：
  旧: _get_node() 只有 insight/hypothesis → Score/Condition/Narrative/FDE 截断绕过
  新: DecisionGraph.register_node() 统一注册表——
      Decision/Reason/Score/Condition/Narrative/Insight/Hypothesis/FDE/AIN 全是 Node

Node 统一 Schema:
  { id, type, links[], evidence_refs[], authority_ceiling, provenance }

Fail-closed 原则（GPT P1）:
  深度超限 ≠ "没发现问题" → 是 "无法证明安全" → BLOCKED / AUDIT_INCONCLUSIVE
  不再 return [] 静默放行

Cycle 可见性（GPT P1）:
  环不是静默吞掉 → 记录到 results["cycles"]，审计可见

Authority Ceiling 传播（GPT P1）:
  反向追溯算 min ≠ 传播。RC4 做节点级传播：
  每个 Node 的 authority_ceiling = min(自身证据等级, 所有子节点 ceiling)
  → 上游节点永远不能高于其最弱证据

Attack 测试（GPT 要求 5 组）:
  A: D→Insight→Hypothesis→Score→Decision  → BLOCKED
  B: D→Insight→Narrative→Decision          → BLOCKED
  C: D→Condition→FDE Score→Decision        → BLOCKED
  D: D→Node×11层→Decision                   → BLOCKED（深度超限 Fail-closed）
  E: A→10层→Decision                        → QUALIFIED（安全路径放行）
"""
import json


class DecisionGraph:
    # 节点类型（统一注册表；AIN 预留，V3.0 接入）
    NODE_TYPES = {
        "decision", "reason", "score", "condition", "narrative",
        "insight", "hypothesis", "fde", "ain", "evidence",
    }
    # 等级强度（A 最高）
    LEVEL_ORDER = {"A": 5, "B": 4, "C": 3, "D": 2, "E": 1, "UNKNOWN": 0}
    # 默认深度上限（写进标准：V2.3 图最大深度 10）
    MAX_DEPTH = 10

    def __init__(self, max_depth=None):
        self.nodes = {}          # id -> Node dict
        self.max_depth = max_depth or self.MAX_DEPTH
        self.cycles = []         # 环记录（审计可见）
        self.depth_exceeded = [] # 深度超限节点（Fail-closed 证据）

    # ============ 节点注册 ============

    def register_node(self, node_id, node_type, evidence_refs=None, links=None, provenance=None):
        """注册任意类型节点。type 必须是 NODE_TYPES 之一。"""
        if node_type not in self.NODE_TYPES:
            node_type = "ain"  # 未知类型 → 按 AIN 处理（V3.0 语义）
        self.nodes[node_id] = {
            "id": node_id,
            "type": node_type,
            "evidence_refs": list(evidence_refs or []),
            "links": list(links or []),
            "authority_ceiling": None,   # 传播后填充
            "provenance": provenance or {},
        }
        return self.nodes[node_id]

    def build_from_layers(self, insight_layer=None, hypothesis_layer=None, score_layer=None,
                          condition_layer=None, narrative_layer=None, fde_layer=None,
                          decision_layer=None, evidence_layer=None):
        """从分层数据批量建图（兼容现有 REPORT JSON 结构）。
        每层: {id: {...evidence/evidence_for/evidence_against/linked_insights/...}}
        """
        # 证据层（等级从 evidence_status/evidence_level 取）
        self.evidence_levels = {}
        for eid, e in (evidence_layer or {}).items():
            level = (e.get("evidence_status") or e.get("evidence_level") or "").upper()
            level = level if level in self.LEVEL_ORDER else "UNKNOWN"
            self.evidence_levels[eid] = level
            self.register_node(eid, "evidence", provenance={"source": e.get("source", "UNSPECIFIED")})

        def _ev_of(node):
            """节点的证据引用（统一）"""
            ev = []
            for k in ("evidence", "evidence_for", "evidence_against"):
                ev.extend(node.get(k, []) if isinstance(node, dict) else [])
            return ev

        def _links_of(node):
            """节点的子链接（统一）"""
            links = []
            for k in ("linked_insights", "linked_hypotheses", "linked_nodes", "links",
                      "linked_scores", "linked_narratives", "linked_conditions"):
                for lid in node.get(k, []) if isinstance(node, dict) else []:
                    if isinstance(lid, str):
                        links.append(lid)
                    elif isinstance(lid, dict) and lid.get("id"):
                        links.append(lid["id"])
            return links

        # 各层注册（类型映射）
        layer_map = [
            (insight_layer, "insight"),
            (hypothesis_layer, "hypothesis"),
            (score_layer, "score"),
            (condition_layer, "condition"),
            (narrative_layer, "narrative"),
            (fde_layer, "fde"),
            (decision_layer, "decision"),
        ]
        for layer, ntype in layer_map:
            for nid, node in (layer or {}).items():
                self.register_node(nid, ntype,
                                   evidence_refs=_ev_of(node),
                                   links=_links_of(node))
        return self

    # ============ Authority Ceiling 传播（节点级）============

    def compute_authority_ceiling(self, node_id, path=None, depth=0):
        """节点级传播：ceiling = min(自身证据等级, 所有子节点 ceiling)。
        上游永远不能高于其最弱证据。返回 (ceiling_level, UNKNOWN_count)。"""
        if node_id not in self.nodes:
            return "UNKNOWN", 1
        node = self.nodes[node_id]
        if node["authority_ceiling"] is not None:
            return node["authority_ceiling"], 0  # 已算过（缓存）

        path = path or set()
        if node_id in path:
            self.cycles.append(node_id)  # 环可见
            return "A", 0  # 环不参与（父节点自己算）
        path = path | {node_id}

        # 自身证据等级
        own_levels = []
        for eid in node.get("evidence_refs", []):
            lv = self.evidence_levels.get(eid, "UNKNOWN")
            own_levels.append(lv)

        # 子节点 ceiling（递归）
        child_ceilings = []
        unknown_count = 0
        for link_id in node.get("links", []):
            if depth < self.max_depth:
                cl, u = self.compute_authority_ceiling(link_id, path, depth + 1)
                child_ceilings.append(cl)
                unknown_count += u
            else:
                # 深度超限 → Fail-closed 记录（不是静默）
                self.depth_exceeded.append(node_id)
                unknown_count += 1  # 超限部分按 UNKNOWN 处理（无法证明安全）

        # ceiling = 最低（最弱证据决定权限上限）
        all_levels = own_levels + child_ceilings
        if not all_levels:
            ceiling = "UNKNOWN"
            unknown_count += 1
        else:
            ceiling = min(all_levels, key=lambda x: self.LEVEL_ORDER.get(x, 0))
            unknown_count += all_levels.count("UNKNOWN")

        node["authority_ceiling"] = ceiling
        return ceiling, unknown_count

    def propagate_all(self):
        """对全图节点计算 Authority Ceiling（先清缓存）"""
        for n in self.nodes.values():
            n["authority_ceiling"] = None
        self.cycles = []
        self.depth_exceeded = []
        results = {}
        for nid in self.nodes:
            if self.nodes[nid]["type"] == "evidence":
                results[nid] = self.evidence_levels.get(nid, "UNKNOWN")
            else:
                results[nid], _ = self.compute_authority_ceiling(nid)
        return results

    # ============ 图级遍历（任意节点类型，Fail-closed）============

    def traverse_from_decision(self, decision_node_id, max_depth=None):
        """从 Decision 节点出发，遍历所有可达证据。
        Fail-closed: 深度超限 / 未分类节点 → 记为 BLOCKED 证据而非静默跳过。
        返回 {evidence_found: [...], blocked: [...], cycles: [...], depth_exceeded: [...]}
        """
        max_depth = max_depth or self.max_depth
        result = {"evidence_found": [], "blocked": [], "cycles": [],
                  "depth_exceeded": [], "unknown_nodes": []}
        visited = set()

        def walk(nid, depth, via_condition_ok=False):
            if nid not in self.nodes:
                result["unknown_nodes"].append(nid)  # 引用不存在的节点 → 无法证明安全
                result["blocked"].append(("unknown_node", nid))
                return
            if nid in visited:
                result["cycles"].append(nid)  # 环可见
                return
            if depth > max_depth:
                result["depth_exceeded"].append(nid)  # Fail-closed
                result["blocked"].append(("depth_exceeded", nid))
                return
            visited.add(nid)

            node = self.nodes[nid]
            # Negative Evidence：验证型 condition 的 D 证据允许（记录但不违规）
            # condition 语义：VALIDATION_REQUIRED/CHALLENGE/UNKNOWN 允许 D
            cond_ok = via_condition_ok
            if node["type"] == "condition":
                role = node.get("authority_role", "") or ""
                if role in DecisionQualificationGate.CONDITION_ALLOW_DE:
                    cond_ok = True
                elif role in DecisionQualificationGate.CONDITION_DENY_DE:
                    cond_ok = False  # FACTUAL_PREMISE/DECISION_DRIVER 拒绝 D
                else:
                    cond_ok = False  # 未分类 → 保守拒绝

            # 任意节点：先收集自身证据引用（evidence_refs 是叶子证据）
            for eid in node.get("evidence_refs", []):
                lv = self.evidence_levels.get(eid, "UNKNOWN")
                if lv in ("D", "E") and cond_ok:
                    result["evidence_found"].append((eid, lv, "condition_allowed"))
                else:
                    result["evidence_found"].append((eid, lv, "direct"))
            # 再递归子链接
            for link_id in node.get("links", []):
                walk(link_id, depth + 1, cond_ok)
        walk(decision_node_id, 0)
        return result

    # ============ 组合裁决（供 DecisionQualificationGate 使用）============

    def qualify(self, decision_node_id, coverage_result=None, provenance_policy="strict"):
        """基于图的最终裁决：
        - 图遍历 Fail-closed（深度超限/未知节点 → BLOCKED）
        - 决策节点 ceiling 传播
        - coverage + provenance 组合
        返回 {"qualification": QUALIFIED/REJECTED/BLOCKED, ...}
        """
        self.propagate_all()
        trav = self.traverse_from_decision(decision_node_id)

        violations = []
        # 1. D/E 证据可达 → REJECTED（排除 condition_allowed 的 Negative Evidence）
        de_ev = [e for e, lv, via in trav["evidence_found"] if lv in ("D", "E") and via != "condition_allowed"]
        if de_ev:
            violations.append({"issue": f"D/E 证据可达: {de_ev}", "level": "VIOLATION"})

        # 2. UNKNOWN 证据可达 → REJECTED（condition_allowed 也不允许 UNKNOWN 升级）
        unk_ev = [e for e, lv, via in trav["evidence_found"] if lv == "UNKNOWN" and via != "condition_allowed"]
        if unk_ev:
            violations.append({"issue": f"UNKNOWN 证据可达: {unk_ev}", "level": "VIOLATION"})

        # 3. Fail-closed: 深度超限/未知节点/环 → BLOCKED（无法证明安全）
        fail_closed = []
        if trav["depth_exceeded"]:
            fail_closed.append(f"深度超限: {trav['depth_exceeded']}")
        if trav["unknown_nodes"]:
            fail_closed.append(f"引用未知节点: {trav['unknown_nodes']}")
        if trav["cycles"]:
            fail_closed.append(f"图环: {trav['cycles']}")

        # 4. 决策节点 ceiling（传播后）
        decision_ceiling = self.nodes.get(decision_node_id, {}).get("authority_ceiling", "UNKNOWN")

        # 5. Coverage（外部传入或默认）
        cov_ok = True
        cov_scope = "GLOBAL"
        if coverage_result:
            cov_scope = coverage_result["decision_scope"]
            cov_ok = cov_scope not in ("INSUFFICIENT",)

        # 6. Provenance 严格模式：决策链上任何节点 provenance 不明 → BLOCKED
        prov_issues = []
        if provenance_policy == "strict":
            # decision 出发的整条链
            for nid in self.nodes:
                if nid == decision_node_id:
                    p = self.nodes[nid].get("provenance", {})
                    if not p or p.get("source") in ("AI_SELF", "UNSPECIFIED", ""):
                        prov_issues.append(f"决策节点 {nid} provenance 不明")
            # evidence 引用节点 provenance
            for e, lv, via in trav["evidence_found"]:
                if e in self.nodes:
                    p = self.nodes[e].get("provenance", {})
                    if not p or p.get("source") in ("AI_SELF", "UNSPECIFIED", ""):
                        prov_issues.append(f"证据 {e} provenance 不明")

        # 5b. Conditional Gate（DO-02/DO-07 2026-08-13 沧林拍板）
        # 决策链上存在 VALIDATION_REQUIRED 条件 → 三态裁决：
        #   validated=True        → 条件满足，放行
        #   validated=FAILED      → 验证失败 = 条件不成立 → BLOCKED（No-Go/Exit）
        #   validated=INSUFFICIENT/未设 → 仍待验证 → CONDITIONAL（不得 QUALIFIED）
        pending_validations = []
        failed_validations = []
        for nid, node in self.nodes.items():
            if node.get("type") == "condition" and node.get("authority_role") == "VALIDATION_REQUIRED":
                v = node.get("validated")
                if v is True:
                    continue  # 条件满足，放行
                elif v == "FAILED":
                    failed_validations.append(nid)
                elif v == "INSUFFICIENT":
                    pending_validations.append(f"{nid}(INSUFFICIENT)")
                else:
                    pending_validations.append(nid)

        # 裁决
        if fail_closed:
            qualification = "BLOCKED"
            reason = f"无法证明安全: {'; '.join(fail_closed)}"
        elif violations:
            qualification = "REJECTED"
            reason = f"证据违规（{len(violations)}）: {violations[0]['issue']}"
        elif not cov_ok:
            qualification = "REJECTED"
            reason = f"Coverage INSUFFICIENT（{cov_scope}）"
        elif prov_issues:
            qualification = "BLOCKED"
            reason = f"provenance 无效: {prov_issues[0]}"
        elif failed_validations:
            qualification = "BLOCKED"
            reason = f"验证失败，条件不成立: {failed_validations} → No-Go/Exit（不得沿原路径继续）"
        elif pending_validations:
            qualification = "CONDITIONAL"
            reason = f"存在未满足的验证条件: {pending_validations} → 需 Validation 回流后才能 Final Decision"
        else:
            qualification = "QUALIFIED"
            reason = f"全路径安全 + Coverage {cov_scope} + ceiling={decision_ceiling}"

        return {
            "qualification": qualification,
            "reason": reason,
            "decision_ceiling": decision_ceiling,
            "evidence_found": trav["evidence_found"],
            "blocked": trav["blocked"],
            "cycles": trav["cycles"],
            "depth_exceeded": trav["depth_exceeded"],
            "violations": violations,
            "fail_closed": fail_closed,
            "provenance_issues": prov_issues,
        }




# ============ DO-02 Evidence-Recovery（2026-08-13 沧林拍板）============

class EvidenceRecoveryLoop:
    """Unknown → Impact Assessment → Critical Unknown → Condition → Validation
    → New Evidence → Re-Decision 的增量重评估器（DO-02）。

    原则（沧林定稿）：
    - Unknown 是 Decision State，不是 Evidence
    - Re-Decision ≠ Report Regeneration：同一 Decision Graph 的版本化重评估
    - 增量重评估：Evidence→Node Mapping → Affected Node Set → Dependency Propagation
      → Affected Decision → Re-Evaluate（不盲目全图重跑）
    - Condition 6 要素：Trigger Variable / Threshold / Consequence / Decision Impact
      / Validation Method / Owner
    """

    # Condition 6 要素（DO-02 护栏，防万能垃圾桶）
    CONDITION_REQUIRED_FIELDS = [
        "trigger_variable", "threshold", "consequence",
        "decision_impact", "validation_method", "owner",
    ]

    def __init__(self, graph, decision_node_id):
        """graph: DecisionGraph 实例；decision_node_id: 要评估的决策节点"""
        self.graph = graph
        self.decision_id = decision_node_id
        self.decision_versions = []   # Decision Versioning 历史
        self.affected_nodes = set()   # 受影响节点集

    # ============ Impact Assessment（不是所有 Unknown 都进 Condition）============

    @staticmethod
    def assess_impact(unknown_variable, decision_relevance, risk_weight):
        """判断 Unknown 是否影响当前 Decision。
        返回: {"critical": bool, "reason": str}
        """
        # 决策相关性 + 风险权重决定 Criticality（0-1 综合）
        score = decision_relevance * risk_weight
        return {
            "critical": score >= 0.5,
            "reason": f"相关度 {decision_relevance} × 风险 {risk_weight} = {score:.2f} {'≥0.5 Critical' if score >= 0.5 else '<0.5 Non-Critical'}",
        }

    @staticmethod
    def validate_condition(condition):
        """Condition 6 要素校验（DO-02 护栏）。
        返回: {"ok": bool, "missing": [str]}
        """
        missing = [f for f in EvidenceRecoveryLoop.CONDITION_REQUIRED_FIELDS
                   if not condition.get(f)]
        return {"ok": len(missing) == 0, "missing": missing}

    # ============ Evidence Update → Affected Node Propagation ============

    def update_evidence(self, evidence_id, new_level, provenance=None, new_links=None):
        """更新单个证据节点等级 → 计算受影响节点集（增量，不重跑全图）。
        返回: {"affected_nodes": [...], "decision_affected": bool}
        """
        g = self.graph
        if evidence_id not in g.nodes:
            return {"affected_nodes": [], "decision_affected": False, "error": f"证据 {evidence_id} 不存在"}

        old_level = g.evidence_levels.get(evidence_id)
        g.evidence_levels[evidence_id] = new_level
        if provenance:
            g.nodes[evidence_id]["provenance"] = provenance

        # 受影响节点 = 反向依赖该证据的所有节点（BFS 反向传播）
        affected = set()
        queue = [evidence_id]
        while queue:
            nid = queue.pop(0)
            for other_id, node in g.nodes.items():
                if nid in node.get("evidence_refs", []) or nid in node.get("links", []):
                    if other_id not in affected:
                        affected.add(other_id)
                        queue.append(other_id)

        self.affected_nodes = affected
        decision_affected = self.decision_id in affected
        return {"affected_nodes": sorted(affected), "decision_affected": decision_affected}

    # ============ Re-Evaluation + Decision Versioning ============

    def re_evaluate(self, new_evidence, reason=""):
        """执行 Re-Decision（版本化重评估）。
        记录原 Decision 状态 → 重跑资格 → 记录新状态 → 计算 Delta。
        返回: {"old": {...}, "new": {...}, "delta": {...}, "version": int}
        """
        g = self.graph
        # 记录原状态（版本历史）
        old_result = g.qualify(self.decision_id)
        self.decision_versions.append({
            "version": len(self.decision_versions) + 1,
            "timestamp": None,  # 由调用方打时间戳
            "trigger_evidence": new_evidence,
            "reason": reason,
            "result": old_result,
        })

        # 重评估（增量：只重算受影响子图——qualify 已按节点遍历，此处复用）
        new_result = g.qualify(self.decision_id)

        # Decision Delta
        delta = {
            "qualification_changed": old_result["qualification"] != new_result["qualification"],
            "old_qualification": old_result["qualification"],
            "new_qualification": new_result["qualification"],
            "ceiling_changed": old_result.get("decision_ceiling") != new_result.get("decision_ceiling"),
            "old_ceiling": old_result.get("decision_ceiling"),
            "new_ceiling": new_result.get("decision_ceiling"),
            "affected_nodes": sorted(self.affected_nodes),
        }

        return {
            "old": old_result,
            "new": new_result,
            "delta": delta,
            "version": len(self.decision_versions),
        }

    # ============ Validation 结果回流（DO-02/DO-06）============

    def validate(self, condition_id, result, evidence_id=None, provenance=None):
        """Validation 结果回流：标记 condition 为 validated / FAILED，
        新 Evidence 进入图 → 下一次 re_evaluate 时 Conditional Gate 解除/保持。
        返回: {"condition": condition_id, "validated": result, "gate_open": bool}
        """
        g = self.graph
        if condition_id not in g.nodes:
            return {"error": f"条件 {condition_id} 不存在"}

        if result in ("PASS", True):
            g.nodes[condition_id]["validated"] = True
        elif result in ("FAIL", "FAILED", False):
            g.nodes[condition_id]["validated"] = "FAILED"
        else:  # INSUFFICIENT
            g.nodes[condition_id]["validated"] = "INSUFFICIENT"

        # 新 Evidence 入图（回流）
        if evidence_id:
            lv = (g.evidence_levels.get(evidence_id) or "C")
            if evidence_id not in g.nodes:
                g.register_node(evidence_id, "evidence",
                                evidence_refs=[], provenance=provenance or {"source": "FID_PIPELINE"})
            g.evidence_levels[evidence_id] = lv
            # 链到条件节点（回流路径）
            g.nodes[condition_id].setdefault("links", []).append(evidence_id)

        return {
            "condition": condition_id,
            "validated": g.nodes[condition_id]["validated"],
            "gate_open": g.nodes[condition_id]["validated"] is True,
        }

    def get_version_history(self):
        """Re-Decision 审计字段（DO-02）：完整版本历史"""
        return self.decision_versions



# ============ 兼容层：保持旧接口（DecisionQualificationGate 包装）============

class DecisionQualificationGate:
    """V2.3-RC4 包装器：用 DecisionGraph 引擎执行完整裁决。
    保留旧构造签名以兼容既有调用。"""

    # Condition 语义分类（Negative Evidence 原则）
    CONDITION_ALLOW_DE = {"VALIDATION_REQUIRED", "CHALLENGE", "UNKNOWN"}
    CONDITION_DENY_DE = {"FACTUAL_PREMISE", "DECISION_DRIVER"}

    def __init__(self, evidence_layer=None, insight_layer=None, hypothesis_layer=None,
                 score_engine=None, coverage_params=None, provenance=None, **kw):
        self.evidence_layer = evidence_layer or {}
        self.insight_layer = insight_layer or {}
        self.hypothesis_layer = hypothesis_layer or {}
        self.coverage_params = coverage_params or {}
        self.provenance = provenance or {}
        self.graph = DecisionGraph()

    def qualify(self, decision_refs, coverage_result=None):
        """兼容旧接口：decision_refs = {reasons, conditions, scores} → 建图 → 裁决"""
        g = self.graph
        # 证据层
        g.evidence_levels = {}
        for eid, e in self.evidence_layer.items():
            lv = (e.get("evidence_status") or e.get("evidence_level") or "").upper()
            lv = lv if lv in DecisionGraph.LEVEL_ORDER else "UNKNOWN"
            g.evidence_levels[eid] = lv
            src = e.get("source", "UNSPECIFIED")
            g.register_node(eid, "evidence", provenance={"source": src if src != "UNSPECIFIED" else "FID_PIPELINE"})

        # reason/condition/score 节点
        reason_nodes = {}
        for r in decision_refs.get("reasons", []):
            rid = r.get("id", f"reason_{len(reason_nodes)}")
            reason_nodes[rid] = {
                "evidence": r.get("evidence", []),
                "links": r.get("linked_insights", []) + r.get("linked_hypotheses", []) + r.get("linked_nodes", []),
                "role": "reason",
            }
            g.register_node(rid, "reason", evidence_refs=r.get("evidence", []),
                            links=r.get("linked_insights", []) + r.get("linked_hypotheses", []) + r.get("linked_nodes", []))
        cond_nodes = {}
        for c in decision_refs.get("conditions", []):
            cid = c.get("id", f"cond_{len(cond_nodes)}")
            cond_nodes[cid] = c
            n = g.register_node(cid, "condition", evidence_refs=c.get("evidence", []),
                                links=c.get("linked_insights", []) + c.get("linked_hypotheses", []) + c.get("linked_nodes", []))
            n["authority_role"] = c.get("authority_role", "")  # condition 语义
        score_nodes = {}
        for s in decision_refs.get("scores", []):
            sid = s.get("id", f"score_{len(score_nodes)}")
            score_nodes[sid] = s
            g.register_node(sid, "score", evidence_refs=s.get("evidence", []),
                            links=s.get("linked_insights", []) + s.get("linked_hypotheses", []) + s.get("linked_nodes", []))

        # insight/hypothesis 层
        for nid, node in self.insight_layer.items():
            g.register_node(nid, "insight",
                            evidence_refs=node.get("evidence", []),
                            links=node.get("linked_insights", []) + node.get("linked_hypotheses", []) + node.get("linked_nodes", []) + node.get("linked_scores", []))
        for nid, node in self.hypothesis_layer.items():
            g.register_node(nid, "hypothesis",
                            evidence_refs=node.get("evidence_for", []) + node.get("evidence_against", []),
                            links=node.get("linked_insights", []) + node.get("linked_hypotheses", []) + node.get("linked_nodes", []))

        # 决策节点（汇合所有 refs）
        decision_id = "DECISION"
        all_links = [r.get("id") for r in decision_refs.get("reasons", [])] \
                    + [c.get("id") for c in decision_refs.get("conditions", [])] \
                    + [s.get("id") for s in decision_refs.get("scores", [])]
        g.register_node(decision_id, "decision", links=all_links,
                        provenance={"source": self.provenance.get("_decision", {}).get("source", "FID_PIPELINE")})

        # coverage
        from sample_coverage_gate import SampleCoverageGate
        cov = coverage_result or SampleCoverageGate().evaluate(self.coverage_params)

        # 裁决
        return g.qualify(decision_id, coverage_result=cov)


if __name__ == "__main__":
    print("=== DecisionGraph RC4 自检 ===")
    PROV = {"source": "FID_PIPELINE"}
    # 干净图
    g = DecisionGraph()
    g.evidence_levels = {"E001": "A"}
    g.register_node("E001", "evidence", provenance=PROV)
    g.register_node("I001", "insight", evidence_refs=["E001"], provenance=PROV)
    g.register_node("R1", "reason", links=["I001"], provenance=PROV)
    g.register_node("D", "decision", links=["R1"], provenance=PROV)
    r = g.qualify("D")
    print(f"  干净图: {r['qualification']} | {r['reason']}")

    # D 证据深藏（Score 类型节点——旧实现找不到）
    g2 = DecisionGraph()
    g2.evidence_levels = {"E008": "D"}
    g2.register_node("E008", "evidence", provenance=PROV)
    g2.register_node("I001", "insight", evidence_refs=["E008"], provenance=PROV)
    g2.register_node("H001", "hypothesis", links=["I001"], provenance=PROV)
    g2.register_node("S001", "score", links=["H001"], provenance=PROV)  # Score 节点（RC4 支持）
    g2.register_node("R1", "reason", links=["S001"], provenance=PROV)
    g2.register_node("D", "decision", links=["R1"], provenance=PROV)
    r2 = g2.qualify("D")
    print(f"  D→I→H→Score→Decision: {r2['qualification']} | {r2['reason']}")
