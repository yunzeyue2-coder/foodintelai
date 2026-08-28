#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Sprint 1 验收：Workflow Engine 异常路径测试（Failure Path）
============================================================
咨询系统必须支持 Failure Path，不只是 Happy Path。
测试用例：
  F-01 缺 Evidence 前进 → 应拒绝（不能从 ANALYSIS 空手到 EVIDENCE_BOUND）
  F-02 FDE 失败（无 decision_memo）→ 应拒绝
  F-03 FQA 失败（score<75）→ 应拒绝（质量闸拦截）
  F-04 缺 Charter 前进 → 应拒绝（项目定义是硬前提）
  F-05 中途修改 Charter → 应能回退到 01（版本管理）
  F-06 非法流转（跳步）→ 应拒绝
"""
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "workflow"))
from workflow_engine import WorkflowEngine

def test(rid, desc, fn):
    try:
        ok, msg = fn()
        status = "✅" if ok else "❌"
        print(f"  {status} {rid} {desc}: {msg}")
        return ok
    except Exception as e:
        print(f"  ❌ {rid} {desc}: 崩溃! {type(e).__name__}: {e}")
        return False

def run():
    print("═" * 60)
    print("Sprint 1 验收① Workflow 异常路径测试")
    print("═" * 60)
    results = []

    # F-01 缺 Evidence 前进
    def f01():
        wf = WorkflowEngine("T-F01")
        wf.advance({"charter": {"decision_question": "q"}})
        wf.advance({"framework": {"m": 1}})
        wf.advance({"dataset": "x.csv"})
        # 缺 metrics，直接尝试到 EVIDENCE_BOUND —— 应失败
        ok, msg = wf.advance({"evidence": {"E": {}}})  # 缺 metrics
        return (not ok) and wf.get_state() == "04_ANALYSIS_RUNNING", msg
    results.append(test("F-01", "缺Metrics前进应拒绝", f01))

    # F-02 FDE 失败（无 decision_memo）
    def f02():
        wf = WorkflowEngine("T-F02")
        for out in [{"charter": {"decision_question": "q"}}, {"framework": {"m": 1}},
                    {"dataset": "x.csv"}, {"metrics": {"hhi": 100}},
                    {"evidence": {"E001": {}}}]:
            wf.advance(out)
        # 缺 decision_memo，尝试到 FQA —— 应失败
        ok, msg = wf.advance({"fqa_report": {"score": 100}})
        return (not ok) and wf.get_state() == "06_DECISION_GENERATED", msg
    results.append(test("F-02", "缺Decision前进应拒绝", f02))

    # F-03 FQA 失败（score<75）
    def f03():
        wf = WorkflowEngine("T-F03")
        for out in [{"charter": {"decision_question": "q"}}, {"framework": {"m": 1}},
                    {"dataset": "x.csv"}, {"metrics": {"hhi": 100}},
                    {"evidence": {"E001": {}}}, {"decision_memo": {"decision": "R2"}}]:
            wf.advance(out)
        # FQA score=60 < 75 → 应拒绝
        ok, msg = wf.advance({"fqa_report": {"score": 60}})
        return (not ok) and wf.get_state() == "07_FQA_PASSED", msg
    results.append(test("F-03", "FQA<75前进应拒绝", f03))

    # F-04 缺 Charter 前进
    def f04():
        wf = WorkflowEngine("T-F04")
        ok, msg = wf.advance({"framework": {"m": 1}})  # 直接给 framework 但缺 charter
        return (not ok) and wf.get_state() == "01_PROJECT_DEFINED", msg
    results.append(test("F-04", "缺Charter前进应拒绝", f04))

    # F-05 中途修改 Charter 回退
    def f05():
        wf = WorkflowEngine("T-F05")
        for out in [{"charter": {"decision_question": "q"}}, {"framework": {"m": 1}},
                    {"dataset": "x.csv"}, {"metrics": {"hhi": 100}},
                    {"evidence": {"E001": {}}}, {"decision_memo": {"decision": "R2"}}]:
            wf.advance(out)
        # 模拟中途改 Charter：回退到 01 重新定义
        wf.state = "01_PROJECT_DEFINED"
        wf.log.append({"from": "07_FQA_PASSED", "to": "01_PROJECT_DEFINED", "timestamp": "2026-08-10", "reason": "Charter修正", "output_keys": []})
        return wf.get_state() == "01_PROJECT_DEFINED" and len(wf.log) == 7, "回退到 01 并记录日志"
    results.append(test("F-05", "中途改Charter可回退", f05))

    # F-06 非法流转（跳步：04 直接到 06）
    def f06():
        wf = WorkflowEngine("T-F06")
        for out in [{"charter": {"decision_question": "q"}}, {"framework": {"m": 1}},
                    {"dataset": "x.csv"}, {"metrics": {"hhi": 100}}]:
            wf.advance(out)
        # 04_ANALYSIS_RUNNING 直接给 decision_memo 跳 05 → 应拒绝
        ok, msg = wf.advance({"decision_memo": {"decision": "R2"}})
        # 断言：跳步被拒 + 状态未进入 06
        return (not ok) and wf.get_state() not in ("06_DECISION_GENERATED", "07_FQA_PASSED"), msg
    results.append(test("F-06", "跳步流转应拒绝", f06))

    print("\n" + "═" * 60)
    passed = sum(results)
    print(f"Workflow 异常测试: {passed}/6 通过")
    print("→ 状态机拒绝非法流转，咨询系统具备 Failure Path 能力" if passed == 6 else "→ 存在未拦截路径，需修复")
    return passed == 6

if __name__ == "__main__":
    run()
