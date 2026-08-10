#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Decision Transfer Test（决策迁移测试）
========================================
GPT Phase 4 隐藏测试：同一个决策引擎换场景，决策逻辑是否稳定。

不要测试"能不能分析 20 个行业"。
测试：不同商业模型，Decision Graph 是否自动切换推导逻辑。

案例对（GPT 原话）:
  郑州炸鸡店 → 高频消费/低客单/标准化/适合复制
  洗车店     → 高频服务/位置依赖/设备资产/人工效率

验收：
  1. 两个输入都能跑（已有）
  2. 输出的 Business DNA / Decision Graph 反映不同商业结构（关键！）
  3. 不是"换汤不换药"——决策依据必须随商业模型切换
"""
import sys, os

ROOT = os.path.dirname(os.path.abspath(__file__))
for sub in ["ontology", "business-twin", "validation", "fde", "pipeline"]:
    sys.path.insert(0, os.path.join(ROOT, sub))
sys.path.insert(0, os.path.join(ROOT, "pipeline"))
from pipeline.ontology_decision_pipeline import Pipeline
from renderer.fdr_renderer_v2 import FDRRendererV2
from business_twin_engine import BusinessTwinEngine


def main():
    pipe = Pipeline()
    twin = BusinessTwinEngine()
    print("=== Decision Transfer Test：同引擎，不同商业模型 ===\n")

    cases = [
        ("炸鸡店", {"category": "炸鸡", "process": "生炸", "product_form": "整只/大件",
                    "price_band": [15, 20], "business_model": "堂食+外卖", "style": "中式"},
         dict(budget=200000, avg_order_value=18, gross_margin=0.55, monthly_fixed_cost=15000,
              daily_orders=(30, 60, 100))),
        ("洗车店", {"category": "洗车店", "process": "冲调/预制", "product_form": "预包装/即食",
                    "price_band": [25, 60], "business_model": "夫妻店", "style": "服务"},
         dict(budget=150000, avg_order_value=40, gross_margin=0.60, monthly_fixed_cost=12000,
              daily_orders=(15, 25, 40))),
        ("快递驿站", {"category": "快递驿站", "process": "预包装", "product_form": "预包装/即食",
                      "price_band": [3, 5], "business_model": "夫妻店", "style": "社区"},
         dict(budget=80000, avg_order_value=4, gross_margin=0.40, monthly_fixed_cost=6000,
              daily_orders=(150, 250, 400))),
    ]

    results = {}
    for name, inputs, twin_args in cases:
        r = pipe.run(inputs, budget=twin_args["budget"])
        tw = twin.run(**twin_args)
        r["twin_investment"] = tw["investment"]
        r["evidence_count"] = 13
        results[name] = r
        op = r["ontology_node"]["operation_profile"]
        dna = {
            "复制难度": op["replication_difficulty"],
            "风险": op["risk_level"],
            "技能依赖": op["skill_dependency"],
            "投资": op["investment_level"],
            "人工强度": op["labor_intensity"],
        }
        print(f"■ {name}")
        print(f"  Business DNA: {dna}")
        print(f"  决策: {r['decision_node']['decision']}")
        print(f"  理由1: {r['reason_node'][0]['text'][:50]}")
        print(f"  理由2: {r['reason_node'][1]['text'][:50]}")
        print()

    # ============ 验收：决策逻辑是否随商业模型切换 ============
    print("=== 迁移验证 ===")
    checks = []

    # 1. 炸鸡 vs 洗车：复制难度/技能依赖应不同（不同商业结构）
    zj, xc = results["炸鸡店"], results["洗车店"]
    if zj["ontology_node"]["operation_profile"]["replication_difficulty"] != xc["ontology_node"]["operation_profile"]["replication_difficulty"]:
        checks.append(("炸鸡 vs 洗车：复制难度不同（商业结构切换）", True))
    else:
        checks.append(("炸鸡 vs 洗车：复制难度不同", False))

    # 2. 决策理由文本应不同（不是模板复制）
    zj_r, xc_r = zj["reason_node"], xc["reason_node"]
    if zj_r[0]["text"] != xc_r[0]["text"]:
        checks.append(("决策理由随模型切换（非固定模板）", True))
    else:
        checks.append(("决策理由随模型切换", False))

    # 3. 洗车店：位置依赖应体现（投资高=设备资产）
    if xc["ontology_node"]["operation_profile"]["investment_level"] > 50:
        checks.append(("洗车店投资门槛被识别（设备资产）", True))
    else:
        checks.append(("洗车店投资门槛识别", False))

    # 4. 快递驿站：低技能高标准化（易复制）
    yd = results["快递驿站"]["ontology_node"]["operation_profile"]
    if yd["skill_dependency"] < 30 and yd["replication_difficulty"] < 30:
        checks.append(("快递驿站：低技能+易复制（服务型结构识别）", True))
    else:
        checks.append(("快递驿站结构识别", False))

    all_pass = all(c[1] for c in checks)
    for name, ok in checks:
        print(f"  {'✅' if ok else '❌'} {name}")
    print(f"\n{'🎉 Decision Transfer Test 通过——引擎随商业模型切换逻辑' if all_pass else '❌ 有迁移失败'}")
    return 0 if all_pass else 1


if __name__ == "__main__":
    sys.exit(main())
