#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
RC4 Attack 矩阵：GPT 第三轮审计要求的 5 组攻击测试
===================================================
Attack A: D → Insight → Hypothesis → Score → Decision   → BLOCKED/REJECTED
Attack B: D → Insight → Narrative → Decision            → BLOCKED/REJECTED
Attack C: D → Condition → FDE Score → Decision          → BLOCKED/REJECTED
Attack D: D → Node × 11层 → Decision                    → BLOCKED（深度超限 Fail-closed）
Attack E: A → 10层 → Decision                           → QUALIFIED（安全路径放行）

验证核心：
1. 任意节点类型（Score/Narrative/Condition/FDE）都在注册表 → 不会被截断
2. 深度超限 = Fail-closed（BLOCKED 不是静默放行）
3. 环可见（cycles 记录）
4. Authority Ceiling 传播正确
"""
import sys
sys.path.insert(0, "/Users/mac/Desktop/青葵/foodintelai-site/qto-engine/gates")
from decision_graph import DecisionGraph

PROV = {"source": "FID_PIPELINE"}


def build_chain(node_types, evidence_level="D"):
    """按节点类型链建图。node_types: ["insight","hypothesis","score"] 表示
    D → insight → hypothesis → score → Decision（链上最后一个接 Decision）"""
    g = DecisionGraph()
    g.evidence_levels = {"EP": evidence_level}
    g.register_node("EP", "evidence", provenance=PROV)
    prev = "EP"
    nid = 1
    for t in node_types:
        n = f"N{nid}"
        g.register_node(n, t, evidence_refs=[prev] if t != "evidence" else [], links=[], provenance=PROV)
        # 上一节点链接到当前（证据是叶子，其余链式）
        if prev != "EP":
            g.nodes[prev]["links"].append(n)
        else:
            # EP 是证据，让第一个非证据节点引用它（通过 evidence_refs 而非 links）
            g.nodes[n]["evidence_refs"] = ["EP"]
        prev = n
        nid += 1
    # Decision 链接最后一个节点
    g.register_node("D", "decision", links=[prev], provenance=PROV)
    return g


def attack_a():
    """D → Insight → Hypothesis → Score → Decision"""
    g = DecisionGraph()
    g.evidence_levels = {"E008": "D"}
    g.register_node("E008", "evidence", provenance=PROV)
    g.register_node("I001", "insight", evidence_refs=["E008"], provenance=PROV)
    g.register_node("H001", "hypothesis", links=["I001"], provenance=PROV)
    g.register_node("S001", "score", links=["H001"], provenance=PROV)
    g.register_node("D", "decision", links=["S001"], provenance=PROV)
    return g.qualify("D")


def attack_b():
    """D → Insight → Narrative → Decision"""
    g = DecisionGraph()
    g.evidence_levels = {"E008": "D"}
    g.register_node("E008", "evidence", provenance=PROV)
    g.register_node("I001", "insight", evidence_refs=["E008"], provenance=PROV)
    g.register_node("N001", "narrative", links=["I001"], provenance=PROV)
    g.register_node("D", "decision", links=["N001"], provenance=PROV)
    return g.qualify("D")


def attack_c():
    """D → Condition → FDE Score → Decision"""
    g = DecisionGraph()
    g.evidence_levels = {"E008": "D"}
    g.register_node("E008", "evidence", provenance=PROV)
    g.register_node("C001", "condition", evidence_refs=["E008"], provenance=PROV)
    g.register_node("F001", "fde", links=["C001"], provenance=PROV)
    g.register_node("D", "decision", links=["F001"], provenance=PROV)
    return g.qualify("D")


def attack_d():
    """D → Node × 11层 → Decision（深度超限 Fail-closed）"""
    g = DecisionGraph()
    g.evidence_levels = {"E008": "D"}
    g.register_node("E008", "evidence", provenance=PROV)
    # 链头 N1 引 E008(D)，然后 N1→N2→...→N11 链式
    prev = None
    head = None
    for i in range(11):
        n = f"N{i+1}"
        t = "insight" if i % 2 == 0 else "hypothesis"
        ev_refs = ["E008"] if i == 0 else []
        g.register_node(n, t, evidence_refs=ev_refs, provenance=PROV)
        if prev:
            g.nodes[prev]["links"].append(n)
        else:
            head = n
        prev = n
    # D 链接链头 N1 → 深度 = 11 层
    g.register_node("D", "decision", links=[head], provenance=PROV)
    return g.qualify("D")


def attack_e():
    """A → 10层 → Decision（安全路径应 QUALIFIED）"""
    g = DecisionGraph()
    g.evidence_levels = {"E001": "A"}
    g.register_node("E001", "evidence", provenance=PROV)
    prev = None
    head = None
    for i in range(10):
        n = f"N{i+1}"
        t = "insight" if i % 2 == 0 else "hypothesis"
        ev_refs = ["E001"] if i == 0 else []
        g.register_node(n, t, evidence_refs=ev_refs, provenance=PROV)
        if prev:
            g.nodes[prev]["links"].append(n)
        else:
            head = n
        prev = n
    g.register_node("D", "decision", links=[head], provenance=PROV)
    return g.qualify("D")


def attack_f():
    """环检测：A→B→A 环必须可见（cycles 记录）"""
    g = DecisionGraph()
    g.evidence_levels = {"E001": "A"}
    g.register_node("E001", "evidence", provenance=PROV)
    g.register_node("N1", "insight", evidence_refs=["E001"], links=["N2"], provenance=PROV)
    g.register_node("N2", "insight", links=["N1"], provenance=PROV)  # 环 N1↔N2
    g.register_node("D", "decision", links=["N1"], provenance=PROV)
    return g.qualify("D")


if __name__ == "__main__":
    print("=== RC4 Attack 矩阵 ===")
    tests = [
        ("A: D→Insight→Hypothesis→Score→Decision", attack_a, "REJECTED"),
        ("B: D→Insight→Narrative→Decision", attack_b, "REJECTED"),
        ("C: D→Condition→FDE→Decision", attack_c, "REJECTED"),
        ("D: D→Node×11层→Decision（超限）", attack_d, "BLOCKED"),
        ("E: A→10层→Decision（安全）", attack_e, "QUALIFIED"),
        ("F: 环 A→B→A（可见）", attack_f, "BLOCKED"),
    ]
    all_ok = True
    for name, fn, expect in tests:
        r = fn()
        ok = r["qualification"] == expect
        all_ok = all_ok and ok
        extra = ""
        if "Attack D" in name or "深度超限" in name:
            extra = f" | depth_exceeded={r['depth_exceeded']}"
        if "环" in name:
            extra = f" | cycles={r['cycles']}"
        print(f"  {'✅' if ok else '❌'} {name}: {r['qualification']} (期望 {expect}){extra}")
        if not ok:
            print(f"      原因: {r['reason']}")

    print(f"\n{'✅ RC4 Attack 矩阵全部通过' if all_ok else '❌ 存在失败'}")
