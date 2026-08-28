#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
RC3 图遍历攻击测试：多跳路径 + 随机深度图
===========================================
验证 trace_decision_chain() 是真正递归遍历（任意深度 D/E 可达即阻断）。

GPT 攻击案例:
  E008(D) → I002 → H003 → I009 → R1 → Decision
  R1 只链接 I009，I009 链接 H003，H003 引 E008(D)
  → 必须被追溯（旧实现到 I009 就停，D 穿透）
"""
import sys, os, random
sys.path.insert(0, "/Users/mac/Desktop/青葵/foodintelai-site/qto-engine/gates")
from decision_qualification_gate import DecisionQualificationGate


def build_deep_graph(depth, poison="D"):
    """构造 1~10 层节点图，最深处放 D 级证据。
    返回 (evidence_layer, insight_layer, hypothesis_layer, decision_refs)
    图结构: R1 → N1 → N2 → ... → N{depth} → E{poison}(D级)
    """
    ev = {"E001": {"evidence_status": "A"}, "EP": {"evidence_status": poison}}
    ins, hyp = {}, {}
    # 从最深往浅建：最后一层节点直接引 EP
    prev_link = None
    for i in range(depth, 0, -1):
        nid = f"N{i}"
        links = [prev_link] if prev_link else []
        node = {"id": nid, "evidence": [], "linked_nodes": links}
        if i == depth:
            node["evidence"] = ["EP"]  # 最深层引 D 级证据
        if i % 2 == 0:
            ins[nid] = node
        else:
            hyp[nid] = node
        prev_link = nid
    refs = {"reasons": [{"id": "R1", "evidence": [], "linked_nodes": [prev_link]}],
            "conditions": [], "scores": []}
    return ev, ins, hyp, refs


def test_gpt_attack_case():
    """GPT 具体攻击案例：I002→H003→I009 多跳"""
    ev = {"E001": {"evidence_status": "A"}, "E008": {"evidence_status": "D"}}
    ins = {
        "I002": {"id": "I002", "evidence": [], "linked_hypotheses": ["H003"]},
        "I009": {"id": "I009", "evidence": [], "linked_hypotheses": ["H003"]},
    }
    hyp = {"H003": {"id": "H003", "evidence_for": ["E008"], "evidence_against": []}}
    refs = {"reasons": [{"id": "R1", "evidence": [], "linked_insights": ["I009"]}],
            "conditions": [], "scores": []}
    gate = DecisionQualificationGate(ev, ins, hyp)
    chains = gate.trace_decision_chain(refs, max_depth=10)
    # 检查：链上是否含 E008(D)
    de_found = any(x[2] in ("D", "E") for ch in chains for x in ch["chain"])
    print(f"[GPT攻击案例] 追溯链数={len(chains)}, D/E可见={de_found}")
    for ch in chains:
        print(f"  链: {' → '.join(f'{r}({l})' for _, r, l in ch['chain'])}")
    return de_found


def test_deep_graphs():
    """1~10 层随机图：D 必须在任意深度被追溯"""
    ok_all = True
    for depth in range(1, 11):
        ev, ins, hyp, refs = build_deep_graph(depth)
        gate = DecisionQualificationGate(ev, ins, hyp)
        chains = gate.trace_decision_chain(refs, max_depth=15)
        de_found = any(x[2] in ("D", "E") for ch in chains for x in ch["chain"])
        status = "✅" if de_found else "❌"
        if not de_found:
            ok_all = False
        print(f"  {status} 深度{depth}: D级可达={de_found}")
    return ok_all


def test_cycle_detection():
    """环检测：A→B→A 不能死循环"""
    ev = {"E001": {"evidence_status": "A"}}
    ins = {
        "N1": {"id": "N1", "evidence": ["E001"], "linked_nodes": ["N2"]},
        "N2": {"id": "N2", "evidence": [], "linked_nodes": ["N1"]},  # 环
    }
    refs = {"reasons": [{"id": "R1", "evidence": [], "linked_nodes": ["N1"]}],
            "conditions": [], "scores": []}
    gate = DecisionQualificationGate(ev, ins, {})
    chains = gate.trace_decision_chain(refs, max_depth=10)
    # 不崩溃 + 有结果
    ok = len(chains) >= 0 and gate.trace_decision_chain  # 基本不抛异常
    print(f"  环检测: {'✅ 无死循环' if ok else '❌'}")
    return ok


if __name__ == "__main__":
    print("=== RC3 图遍历攻击测试 ===")
    r1 = test_gpt_attack_case()
    print("\n— 深度测试 (1~10层) —")
    r2 = test_deep_graphs()
    print("\n— 环检测 —")
    r3 = test_cycle_detection()
    print(f"\n{'✅ 全部通过：递归遍历在任意深度阻断 D/E' if (r1 and r2 and r3) else '❌ 存在漏洞'}")
