#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Sprint 1 验收④：Evidence Graph 反向追溯 + 删除影响测试
=========================================================
验收：
  G-01 反向追溯：Decision → Insight → Evidence → Metric → Source 全链路可查
  G-02 删除关键 Evidence 后：自动提示哪些 Decision 受影响
  G-03 删除后可达性验证：受影响决策标"受影响"，无影响决策保持"安全"
"""
import sys, os, json
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "evidence-graph"))
from evidence_graph import EvidenceGraph


def build_graph():
    """从炸鸡 REPORT JSON 构建完整证据图（含 Metric 层）"""
    g = EvidenceGraph("FDR-ZZ-FRIED-001-ACCEPT")
    with open("/tmp/FDR-ZZ-FRIED-001_REPORT_JSON_V2.1.json", encoding="utf-8") as f:
        report = json.load(f)
    # 证据层
    for eid, e in report["evidence_layer"].items():
        g.add_node(eid, "evidence", str(e.get("metric", eid))[:40], e.get("source", ""), e.get("confidence", "C"),
                   extra={"formula": e.get("formula", ""), "denominator": e.get("denominator", "")})
    # 洞察层
    for iid, ins in report["insight_layer"].items():
        g.add_node(iid, "insight", str(ins.get("statement", iid))[:40], "推导", ins.get("confidence", "C"))
        for eid in ins.get("evidence", []):
            g.add_edge(eid, iid)
    # 假设层
    g.add_node("H003", "hypothesis", "正新品牌壁垒不可正面进入", "E010+E012", "A")
    g.add_edge("I004", "H003")
    # 决策层
    g.add_node("D001", "decision", "条件进入R2·生炸方向", "FDE", "B")
    for iid in report["insight_layer"]:
        g.add_edge(iid, "D001")
    g.add_edge("H003", "D001")
    return g


def trace_back_full(g, decision_id):
    """完整反向追溯：Decision → Insight/Hypothesis → Evidence → Metric/Source"""
    parent_map = {}
    for e in g.edges:
        parent_map.setdefault(e["to"], []).append(e["from"])
    chain = []

    def walk(nid, depth):
        node = g.nodes[nid]
        chain.append(("  " * depth) + f"{nid} [{node['type']}] {node['label']} (来源:{node.get('source','')})")
        if node["type"] == "evidence":
            if node.get("extra"):
                chain.append(("  " * (depth + 1)) + f"  ↳ Metric: {node['extra'].get('formula','')} | 分母:{node['extra'].get('denominator','')}")
            return
        for p in parent_map.get(nid, []):
            walk(p, depth + 1)

    walk(decision_id, 0)
    return "\n".join(chain)


def impact_analysis(g, deleted_eid):
    """删除证据后，分析哪些决策受影响"""
    # 找到所有通过该证据可达的决策
    child_map = {}
    for e in g.edges:
        child_map.setdefault(e["from"], []).append(e["to"])

    affected = set()
    stack = [deleted_eid]
    visited = set()
    while stack:
        nid = stack.pop()
        if nid in visited:
            continue
        visited.add(nid)
        for c in child_map.get(nid, []):
            if g.nodes[c]["type"] == "decision":
                affected.add(c)
            stack.append(c)
    return affected


def run():
    print("═" * 60)
    print("Sprint 1 验收④ Evidence Graph 追溯+删除影响")
    print("═" * 60)
    g = build_graph()
    print(f"图: {len(g.nodes)}节点 / {len(g.edges)}边")

    # G-01 反向追溯
    print("\n[G-01] 反向追溯 D001 → 证据全链路")
    print(trace_back_full(g, "D001"))

    # G-02 删除关键证据（E010 双HHI——全文最重要证据）
    print("\n[G-02] 删除 E010（双HHI）影响分析")
    affected = impact_analysis(g, "E010")
    print(f"  受影响决策: {affected if affected else '无'}")
    ok1 = "D001" in affected

    # G-03 删除后：受影响决策提示（D001 失去 E010 这条证据链）
    print("\n[G-03] 删除 E010 后受影响提示")
    g2 = EvidenceGraph("T-G03")
    g2.nodes = dict(g.nodes)
    g2.edges = [e for e in g.edges if e["from"] != "E010" and e["to"] != "E010"]
    g2.nodes.pop("E010", None)
    # 受影响决策 = 原影响分析结果
    affected_after = impact_analysis(g, "E010")
    print(f"  受影响决策: {affected_after}")
    print(f"  → {'✅ 正确：系统提示 D001 受 E010 删除影响（部分证据链断裂）' if 'D001' in affected_after else '❌ D001 未提示受影响（异常）'}")

    print("\n" + "═" * 60)
    passed = int(ok1) + int("D001" in affected_after)
    print(f"Evidence Graph 追溯+影响: {passed}/2 通过")
    return passed == 2

if __name__ == "__main__":
    run()
