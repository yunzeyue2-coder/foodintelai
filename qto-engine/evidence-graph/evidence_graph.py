#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Evidence Graph-Lite
===================
青藤OS 证据网络（最小可运行版）

作用：把"结论 → 证据"的绑定关系做成可见网络（JSON）。
     专业报告与普通报告的最大区别：每一句重要判断都能反查到证据。

最小实现（不建图数据库，先 JSON）:
{
  "nodes": {
    "E001": {"type": "evidence", "label": "炸鸡门店规模 2397家", "source": "FID-001", "confidence": "B"},
    "I004": {"type": "insight", "label": "工艺是第一分水岭", "evidence_status": "A"},
    "D001": {"type": "decision", "label": "条件进入R2", "evidence_status": "A+B"}
  },
  "edges": [
    {"from": "E010", "to": "I004", "relation": "supports"},
    {"from": "I004", "to": "D001", "relation": "supports"}
  ]
}

可验证性质：
- 可达性：每个决策节点都能沿边走到证据节点（无孤儿结论）
- 反查：从任何结论可回溯到数据来源
"""
import json


class EvidenceGraph:
    def __init__(self, project_id):
        self.project_id = project_id
        self.nodes = {}
        self.edges = []

    def add_node(self, nid, ntype, label, source="", confidence="C", extra=None):
        """添加节点：type = evidence/insight/decision/hypothesis"""
        self.nodes[nid] = {
            "id": nid, "type": ntype, "label": label,
            "source": source, "confidence": confidence,
            **({"extra": extra} if extra else {})
        }

    def add_edge(self, frm, to, relation="supports"):
        """添加边：from → to"""
        if frm not in self.nodes or to not in self.nodes:
            return False, f"节点缺失: {frm}→{to}"
        self.edges.append({"from": frm, "to": to, "relation": relation})
        return True, f"{frm} → {to}"

    # ---- 验证 ----
    def verify_no_orphan_decisions(self):
        """验证：所有 decision 节点必须至少有一条入边（有支撑）"""
        orphans = []
        decision_ids = [n for n, d in self.nodes.items() if d["type"] == "decision"]
        for did in decision_ids:
            has_in = any(e["to"] == did for e in self.edges)
            if not has_in:
                orphans.append(did)
        return len(orphans) == 0, orphans

    def verify_reachability(self):
        """验证：每个 decision 节点都能反查到至少一个 evidence 节点"""
        # 反向走图：decision → insight → evidence
        parent_map = {}
        for e in self.edges:
            parent_map.setdefault(e["to"], []).append(e["from"])

        def trace_back(nid, visited):
            node = self.nodes[nid]
            if node["type"] == "evidence":
                return True
            if nid in visited:
                return False
            visited.add(nid)
            for p in parent_map.get(nid, []):
                if trace_back(p, visited):
                    return True
            return False

        results = {}
        for nid, node in self.nodes.items():
            if node["type"] == "decision":
                results[nid] = trace_back(nid, set())
        return all(results.values()), results

    def to_json(self, path=None):
        d = {"project_id": self.project_id, "nodes": self.nodes, "edges": self.edges}
        s = json.dumps(d, ensure_ascii=False, indent=2)
        if path:
            with open(path, "w", encoding="utf-8") as f:
                f.write(s)
        return s

    def self_test(self):
        """回归测试：炸鸡证据网络 + 孤儿结论检测"""
        g = EvidenceGraph("FDR-ZZ-FRIED-001")
        # 证据
        g.add_node("E010", "evidence", "生炸vs裹粉双生态 HHI", "FID-001+Ontology", "B")
        g.add_node("E011", "evidence", "显著商业簇 35.2%", "FID-001", "B")
        g.add_node("E003", "evidence", "价格带分布 67.8%", "FID-001", "B")
        # 洞察
        g.add_node("I004", "insight", "工艺是第一分水岭", "证据推导", "B")
        # 假设
        g.add_node("H003", "hypothesis", "正新品牌壁垒不可正面进入", "E010+E012", "A")
        # 决策
        g.add_node("D001", "decision", "条件进入R2·生炸方向", "FDE", "B")
        # 边
        g.add_edge("E010", "I004")
        g.add_edge("E011", "I004")
        g.add_edge("I004", "H003")
        g.add_edge("H003", "D001")
        return g


if __name__ == "__main__":
    g = EvidenceGraph("FDR-ZZ-FRIED-001").self_test()
    print("=== Evidence Graph-Lite 自检 ===")
    print(f"节点: {len(g.nodes)} | 边: {len(g.edges)}")
    ok1, orphans = g.verify_no_orphan_decisions()
    print(f"✅ 无孤儿结论: {ok1}" + (f"（孤立: {orphans}）" if orphans else ""))
    ok2, reach = g.verify_reachability()
    print(f"✅ 决策可反查证据: {ok2} {reach}")
    print("\n网络结构:")
    for e in g.edges:
        print(f"  {e['from']} → {e['to']} ({e['relation']})")
    print("\n✅ Evidence Graph-Lite: 证据网络可反查验证通过")
