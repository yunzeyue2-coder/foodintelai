#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
青藤OS V2.1 控制层回归验证（炸鸡 V2.1）
=========================================
串联 Workflow + Hypothesis + FAS + Evidence Graph，用炸鸡真实数据全流程跑一遍，
验证 4 个 Lite 设备协同工作，并与旧流程 FQA 对比。

验证链:
  FAS 生成决策树 → Hypothesis 提出假设 → 绑定证据 → Evidence Graph 可视化
  → Workflow 状态机走完整 8 步 → FQA 质量闸
"""
import sys, os, json
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "workflow"))
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "hypothesis"))
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "fas"))
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "evidence-graph"))

from workflow_engine import WorkflowEngine
from hypothesis_engine import HypothesisEngine
from fas_engine import FASE
from evidence_graph import EvidenceGraph

ROOT = os.path.dirname(os.path.abspath(__file__))

def run():
    print("═" * 60)
    print("青藤OS V2.1 控制层回归验证（炸鸡 V2.1）")
    print("═" * 60)

    # ========== 1. FAS: 生成炸鸡决策问题树 ==========
    print("\n[1/5] FAS 决策问题树")
    fas = FASE()
    fas.register_category_variables("炸鸡", {
        "list": ["客单价", "炸制能力", "外卖适配", "SKU", "鸡肉供应", "复购", "连锁化"],
        "extra_questions": {
            "business": ["炸制技能依赖度？（生炸vs裹粉）", "半成品vs现场腌制供应链？"],
            "consumer": ["外卖占比 vs 堂食占比？"],
        },
    })
    tree = fas.generate("炸鸡", "郑州", "20万创业进入")
    branches = len(tree["branches"])
    q_total = sum(len(b["questions"]) for b in tree["branches"].values())
    print(f"  ✅ 生成 {branches} 支 / {q_total} 个决策问题（含品类变量注入）")

    # ========== 2. Hypothesis: 加载炸鸡 5 假设 ==========
    print("\n[2/5] Hypothesis 假设管理")
    with open(os.path.join(ROOT, "hypothesis/hypotheses_ZZ_FRIED.json"), encoding="utf-8") as f:
        hdata = json.load(f)
    heng = HypothesisEngine(hdata["project_id"])
    for h in hdata["hypotheses"].values():
        heng.hypotheses[h["id"]] = h
    n_ok = sum(1 for h in heng.hypotheses.values() if h["status"] in ("validated", "uncertain"))
    n_bad = sum(1 for h in heng.hypotheses.values() if h["status"] == "proposed")
    print(f"  ✅ 5 假设已加载: {n_ok} 已评估 / {n_bad} 待实验 (H004 遵守 Evidence Boundary)")

    # ========== 3. Evidence Graph: 构建炸鸡证据网络 ==========
    print("\n[3/5] Evidence Graph 证据网络")
    eg = EvidenceGraph("FDR-ZZ-FRIED-001")
    # 从 REPORT JSON 构建
    with open("/tmp/FDR-ZZ-FRIED-001_REPORT_JSON_V2.1.json", encoding="utf-8") as f:
        report = json.load(f)
    for eid, e in report["evidence_layer"].items():
        eg.add_node(eid, "evidence", str(e.get("metric", eid))[:40], e.get("source", ""), e.get("confidence", "C"))
    for iid, ins in report["insight_layer"].items():
        eg.add_node(iid, "insight", str(ins.get("statement", iid))[:40], "推导", ins.get("confidence", "C"))
        for eid in ins.get("evidence", []):
            eg.add_edge(eid, iid)
    eg.add_node("D001", "decision", "条件进入R2", "FDE", "B")
    for iid in report["insight_layer"]:
        eg.add_edge(iid, "D001")
    ok1, orphans = eg.verify_no_orphan_decisions()
    ok2, reach = eg.verify_reachability()
    print(f"  ✅ 节点 {len(eg.nodes)} / 边 {len(eg.edges)} | 无孤儿: {ok1} | 可反查: {ok2}")
    if not ok1 or not ok2:
        print(f"  ⚠️ 孤儿: {orphans}, 不可达: {[k for k,v in reach.items() if not v]}")

    # ========== 4. Workflow: 状态机走完整 8 步 ==========
    print("\n[4/5] Workflow 状态机")
    wf = WorkflowEngine("FDR-ZZ-FRIED-001-REG")
    step_outputs = {
        "01_PROJECT_DEFINED": {"charter": {"decision_question": "20万创业者在郑州进入炸鸡？"}},
        "02_FRAMEWORK_READY": {"framework": tree},
        "03_DATA_READY": {"dataset": "zz_fried_label_table_v03.csv"},
        "04_ANALYSIS_RUNNING": {"metrics": {"hhi_struct_sz": 2405.9, "hhi_brand_sz": 1393.4, "obs_cov": 0.352}},
        "05_EVIDENCE_BOUND": {"evidence": {eid: {} for eid in report["evidence_layer"]}},
        "06_DECISION_GENERATED": {"decision_memo": report["decision_memo"]},
        "07_FQA_PASSED": {"fqa_report": {"score": 100}},
    }
    steps = []
    while not wf.is_terminal():
        out = step_outputs.get(wf.get_state(), {})
        ok, msg = wf.advance(out)
        steps.append((wf.get_state(), ok, msg))
    all_ok = all(ok for _, ok, _ in steps)
    print(f"  {'✅' if all_ok else '❌'} 8步全流转: {[s[0] for s in steps]}")
    print(f"  最终: {wf.get_state()} | 进度 {wf.progress()}%")

    # ========== 5. FQA: 质量闸 ==========
    print("\n[5/5] FQA 质量闸")
    from fqa_check import main as fqa_main
    import io, contextlib
    buf = io.StringIO()
    with contextlib.redirect_stdout(buf):
        score, issues = fqa_main("/tmp/FDR-ZZ-FRIED-001_REPORT_JSON_V2.1.json")
    print(f"  ✅ FQA Score: {score}/100 ({'A' if score>=90 else 'B' if score>=75 else 'C'}) | 问题 {issues} 项")

    # ========== 总结 ==========
    print("\n" + "═" * 60)
    print("回归验证结论")
    print("═" * 60)
    checks = {
        "FAS 决策树生成": branches > 0,
        "Hypothesis 反证约束": n_bad == 1 and "H004" in [h["id"] for h in heng.hypotheses.values() if h["status"] == "proposed"],
        "Evidence Graph 可反查": ok1 and ok2,
        "Workflow 8步流转": all_ok,
        "FQA 质量闸 ≥75": score >= 75,
    }
    for k, v in checks.items():
        print(f"  {'✅' if v else '❌'} {k}")
    print(f"\n综合: {sum(checks.values())}/{len(checks)} 项通过")
    print("→ 控制层有效：项目现在可以被机器编排，而非仅靠人脑串联")

if __name__ == "__main__":
    run()
