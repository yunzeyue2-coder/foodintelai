#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Sprint 1 验收②：Hypothesis Engine 强制约束测试
================================================
专业咨询不是证明观点，而是管理不确定性。
验收：
  H-01 假设必须有证据（proposed 状态必须有绑定的 for/against，否则提示）
  H-02 结论必须关闭假设（validated/rejected 必须有证据支撑）
  H-03 允许 Unknown（无数据时 status=uncertain/proposed 合法）
  H-04 反证约束（evidence_against 必须可用，不能只"证明自己"）
  H-05 置信度必须标注（A/B/C/D，不能空）
"""
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "hypothesis"))
from hypothesis_engine import HypothesisEngine

def run():
    print("═" * 60)
    print("Sprint 1 验收② Hypothesis 强制约束测试")
    print("═" * 60)
    results = []
    eng = HypothesisEngine("ACCEPT-TEST")

    # H-01 假设必须有证据
    def h01():
        eng2 = HypothesisEngine("H01")
        eng2.propose("H1", "测试假设", "market", "测试", "support_entry")
        ev = eng2.evaluate("H1")
        return ev["verdict"] == "insufficient", f"无证据假设评估={ev['verdict']} (应 insufficient)"
    results.append(h01())

    # H-02 结论必须关闭假设：validated 必须有支持证据
    def h02():
        eng3 = HypothesisEngine("H02")
        eng3.propose("H2", "有证据假设", "market", "测试", "support_entry")
        eng3.add_evidence("H2", "E001", "for")
        ok, msg = eng3.update_status("H2", "validated", "A")
        ev = eng3.evaluate("H2")
        return ok and ev["verdict"] == "supported", f"validated 有证据: {ev['verdict']}"
    results.append(h02())

    # H-03 允许 Unknown：无数据 → proposed/uncertain 合法
    def h03():
        eng4 = HypothesisEngine("H03")
        eng4.propose("H3", "无数据假设", "business", "框架", "neutral")
        st = eng4.hypotheses["H3"]["status"]
        return st == "proposed", f"无数据假设 status={st} (应 proposed)"
    results.append(h03())

    # H-04 反证约束：可以添加 against 证据
    def h04():
        eng5 = HypothesisEngine("H04")
        eng5.propose("H4", "有反证假设", "market", "测试", "support_entry")
        eng5.add_evidence("H4", "E001", "for")
        eng5.add_evidence("H4", "E002", "against")
        ev = eng5.evaluate("H4")
        return ev["verdict"] == "uncertain", f"正反冲突 → {ev['verdict']} (应 uncertain)"
    results.append(h04())

    # H-05 置信度必须标注
    def h05():
        eng6 = HypothesisEngine("H05")
        eng6.propose("H5", "置信度测试", "risk", "测试", "support_avoid")
        conf = eng6.hypotheses["H5"]["confidence"]
        return conf in ("A", "B", "C", "D"), f"置信度={conf} (有效)"
    results.append(h05())

    for i, (ok, msg) in enumerate(results, 1):
        print(f"  {'✅' if ok else '❌'} H-0{i}: {msg}")

    print("\n" + "═" * 60)
    passed = sum(r[0] if isinstance(r, tuple) else r for r in results)
    print(f"Hypothesis 强制约束测试: {passed}/5 通过")
    return passed == 5

if __name__ == "__main__":
    run()
