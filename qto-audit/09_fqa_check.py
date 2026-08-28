#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
FQA 质量审查机器人（Food Quality Assurance）
=============================================
把 FDR 四层 QC 变成可执行检查清单。
输入: FDR REPORT JSON
输出: FQA Score + 问题清单

三组检查:
  逻辑组  结论是否超过证据/因果倒置/样本不足
  商业组  是否有收入模型/成本模型/风险模型
  咨询组  Executive Summary/Key Findings/Recommendation/Action Plan 是否齐全
"""
import json, sys, re

def load_report(path):
    with open(path, encoding="utf-8") as f:
        return json.load(f)

def check_logic(R):
    """逻辑检查：结论超过证据/因果倒置/样本不足"""
    issues, passed = [], []

    # 1. 每个 Insight 必须有 evidence 绑定
    for iid, ins in R.get("insight_layer", {}).items():
        evs = ins.get("evidence", [])
        if not evs:
            issues.append(f"{iid}: 无证据绑定")
        else:
            missing = [e for e in evs if e not in R.get("evidence_layer", {})]
            if missing:
                issues.append(f"{iid}: 绑定缺失 {missing}")
            else:
                passed.append(f"{iid}: 证据绑定完整 ({len(evs)}项)")

    # 2. 证据等级限制结论强度
    for iid, ins in R.get("insight_layer", {}).items():
        status = ins.get("evidence_status", "")
        authority = ins.get("decision_authority", "")
        if status == "A" and authority not in ("direct",):
            issues.append(f"{iid}: A级应可direct决策，但authority={authority}")
        elif status in ("C", "D") and authority == "direct":
            issues.append(f"{iid}: {status}级不应direct决策! (违反Decision Authority)")

    # 3. Unknown 不形成确定性判断
    for eid, e in R.get("evidence_layer", {}).items():
        if e.get("evidence_status") == "D":
            val = e.get("value", "")
            if val and "无法判断" not in str(val) and isinstance(val, str) and len(val) > 30:
                issues.append(f"{eid}: D级但给了较长value (可能越界)")

    return issues, passed

def check_business(R):
    """商业检查：收入/成本/风险模型"""
    issues, passed = [], []

    # 1. 风险模型
    risks = R.get("risk_layer", [])
    if risks:
        passed.append(f"风险模型: {len(risks)}项")
    else:
        issues.append("缺风险模型 (risk_layer)")

    # 2. 停止条件
    actions = R.get("action_layer", [])
    has_stop = any("stop_condition" in a or "stop" in str(a).lower() for a in actions)
    if has_stop:
        passed.append("停止条件: 存在")
    else:
        issues.append("缺停止条件")

    # 3. 收入/成本框架（允许 Framework-only）
    bm = R.get("business_model_archetypes", {})
    has_framework = any("Framework" in str(b.get("evidence_status", "")) for b in bm.values())
    if has_framework:
        passed.append("单店经济框架: 存在 (Evidence Boundary 合规)")
    else:
        issues.append("缺单店经济框架")

    return issues, passed

def check_consulting(R):
    """咨询检查：咨询交付要素"""
    issues, passed = [], []
    memo = R.get("decision_memo", {})

    # 1. Executive Summary
    if R.get("executive_summary") or R.get("summary"):
        passed.append("Executive Summary: 存在")
    else:
        issues.append("缺 Executive Summary")

    # 2. 明确决策
    if memo.get("decision"):
        passed.append(f"Decision: {memo['decision']}")
    else:
        issues.append("缺 Decision 结论")

    # 3. 推荐方向
    if memo.get("recommended_direction"):
        passed.append("Recommendation: 存在")
    else:
        issues.append("缺 Recommendation")

    # 4. 行动方案
    if memo.get("action_30days") or actions_exists(R):
        passed.append("Action Plan: 存在")
    else:
        issues.append("缺 Action Plan")

    # 5. 停止条件
    if memo.get("conditions"):
        passed.append(f"Conditions: {len(memo['conditions'])}项")
    else:
        issues.append("缺 Conditions")

    # 6. 决策过程透明度 (reasons)
    if memo.get("reasons"):
        passed.append(f"Decision Trace: {len(memo['reasons'])}条理由")
    else:
        issues.append("缺 Decision Trace (reasons)")

    return issues, passed

def actions_exists(R):
    return bool(R.get("action_layer"))

def main(path):
    R = load_report(path)
    print(f"=== FQA 质量审查: {R.get('report_metadata', {}).get('report_id', '?')} {R.get('report_metadata', {}).get('version', '?')} ===\n")

    total_issues = 0
    total_passed = 0
    groups = []

    for name, fn in [("逻辑组", check_logic), ("商业组", check_business), ("咨询组", check_consulting)]:
        issues, passed = fn(R)
        groups.append((name, issues, passed))
        print(f"── {name} ──")
        for p in passed:
            print(f"  ✅ {p}")
        for i in issues:
            print(f"  ❌ {i}")
        total_issues += len(issues)
        total_passed += len(passed)
        print()

    # FQA Score
    total = total_passed + total_issues
    score = round(total_passed / total * 100) if total else 0
    grade = "A" if score >= 90 else "B" if score >= 75 else "C" if score >= 60 else "D"
    print(f"=== FQA Score: {score}/100 ({grade}) ===")
    print(f"   通过 {total_passed} 项 / 问题 {total_issues} 项")

    return score, total_issues

if __name__ == "__main__":
    path = sys.argv[1] if len(sys.argv) > 1 else "/tmp/FDR-ZZ-FRIED-001_REPORT_JSON_V2.1.json"
    main(path)
