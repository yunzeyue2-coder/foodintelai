#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Ontology → DecisionGraph 流水线（Pipeline Wiring）
===================================================
GPT 工业化加固 P1：让 Decision Graph 全面接入 Ontology。

流水线（GPT 原话）:
  用户输入 → Ontology Parser → Entity Profile → Decision Engine
           → Evidence Engine → FDR Renderer → PDF

本文件: Ontology → Decision Engine 的接线
  Ontology Node（画像）
      ↓
  Reason Node（规则推导理由）
      ↓
  Decision Node（Gate 裁决）
      ↓
  Action Node（90天计划 + Kill Criteria）

关键: 整个链路不依赖品类名——Ontology 输出属性，规则读属性。
"""
import sys, os, json

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))  # qto-engine
for sub in ["ontology", "business-twin", "validation", "fde", "site"]:
    sys.path.insert(0, os.path.join(ROOT, sub))
from ontology_v04 import FoodBusinessOntology
from business_twin_engine import BusinessTwinEngine
from validation_engine import ValidationEngine
from fde_veto_gate import FDEVetoGate


class Pipeline:
    """Ontology → DecisionGraph 流水线（品类无关）"""

    def __init__(self):
        self.ontology = FoodBusinessOntology()
        self.twin = BusinessTwinEngine()
        self.validation = ValidationEngine()
        self.veto = FDEVetoGate()

    def run(self, inputs, budget, experience_years=0):
        """完整流水线：
        输入: {category, process, product_form, price_band, business_model, style}
        输出: 决策链（Ontology Node → Reason Node → Decision Node → Action Node）
        """
        # ============ 1. Ontology Node：三画像 ============
        profile = self.ontology.build_profiles(inputs)
        rep = self.ontology.replication_path(inputs)
        op = profile["operation_profile"]

        # ============ 2. Reason Node：规则推导理由 ============
        reasons = self._build_reasons(inputs, op, rep)

        # ============ 2.5 Unknowns：诚实边界（GPT P2）============
        # 未知行业/未匹配规则 → 指出缺失数据，不假装分析
        unknowns = []
        if inputs.get("process") not in self.ontology.PROCESS_RULES:
            unknowns.append(f"工艺'{inputs.get('process')}'无匹配规则——属性为默认近似值，需人工校准")
        if inputs.get("product_form") not in self.ontology.PRODUCT_RULES:
            unknowns.append(f"产品形态'{inputs.get('product_form')}'无匹配规则——损耗/出品速度未校准")
        if not inputs.get("price_band") or inputs["price_band"][1] > 5000:
            unknowns.append("价格带异常或缺失——投资/利润空间推导不可靠")
        # 推理置信度（规则覆盖度）
        rule_coverage = sum(1 for k in ["process", "product_form", "price_band", "business_model"]
                            if k in inputs and (k != "process" or inputs[k] in self.ontology.PROCESS_RULES)
                            and (k != "product_form" or inputs[k] in self.ontology.PRODUCT_RULES))
        confidence = min(0.95, 0.4 + rule_coverage * 0.15)

        # ============ 3. Decision Node：Gate 裁决 ============
        skill_score = 100 - op["skill_dependency"]
        exp_gap = 0.9 if experience_years < 1 else (0.6 if experience_years < 3 else 0.2)
        v = self.veto.decide(base_score=self._base_score(op), profile={
            "skill_gap": skill_score,
            "capital_gap": 100 - op["investment_level"],
            "survival_months_low": 5.0,
            "experience_gap": exp_gap,
            "competition_pressure": 0.5,
            "data_uncertainty": 0.4,
        })

        # ============ 4. Action Node：验证计划 + Kill Criteria ============
        avg_price = sum(inputs.get("price_band", [10, 15])) / 2
        plan = self.validation.build_plan(f"PROJ-{inputs['category']}", inputs["category"])
        kill = self.validation.build_kill_criteria(budget, max(6000, int(avg_price * 350)))

        return {
            "inputs": inputs,
            "ontology_node": profile,
            "reason_node": reasons,
            "unknowns": unknowns,
            "inference_confidence": round(confidence, 2),
            "decision_node": v,
            "action_node": {"validation_plan": plan, "kill_criteria": kill},
        }

    def _build_reasons(self, inputs, op, rep):
        """规则推导理由（不依赖品类名）"""
        reasons = []
        # 复制难度分档：<35 易复制 / 35-55 中等 / >55 难复制
        if op["replication_difficulty"] < 35:
            reasons.append({
                "text": f"复制难度{op['replication_difficulty']}/100——模型高度标准化，具备连锁复制潜力",
                "evidence_level": "B", "source": "ontology_rules"})
        elif op["replication_difficulty"] < 55:
            reasons.append({
                "text": f"复制难度{op['replication_difficulty']}/100——中等，技能依赖{op['skill_dependency']}，需验证标准化后扩张",
                "evidence_level": "B", "source": "ontology_rules"})
        else:
            reasons.append({
                "text": f"复制难度{op['replication_difficulty']}/100——技能依赖{op['skill_dependency']}，适合单店深耕",
                "evidence_level": "B", "source": "ontology_rules"})
        if op["risk_level"] < 35:
            reasons.append({
                "text": f"风险等级{op['risk_level']}/100——损耗/依赖结构可控",
                "evidence_level": "C", "source": "ontology_rules"})
        else:
            reasons.append({
                "text": f"风险等级{op['risk_level']}/100——需重点验证损耗与供应链",
                "evidence_level": "C", "source": "ontology_rules"})
        reasons.append({
            "text": f"投资水平{op['investment_level']}/100、人工强度{op['labor_intensity']}/100——进入门槛与运营强度已量化",
            "evidence_level": "B", "source": "ontology_rules"})
        return reasons

    def _base_score(self, op):
        """基础分（规则：低风险+低复制难度 → 高分）"""
        return max(40, min(85, 85 - op["risk_level"] * 0.3 - op["replication_difficulty"] * 0.3))


if __name__ == "__main__":
    print("=== Ontology → DecisionGraph 流水线自检 ===")
    pipe = Pipeline()

    # 案例1: 奶茶（标准化高）
    r1 = pipe.run({"category": "奶茶", "process": "冲调/预制", "product_form": "杯装/便携",
                   "price_band": [12, 20], "business_model": "堂食+外卖", "style": "新式"},
                  budget=300000)
    print(f"\n■ {r1['inputs']['category']}")
    print(f"  [Reason]")
    for r in r1["reason_node"]:
        print(f"    {r['text'][:60]}")
    print(f"  [Decision] {r1['decision_node']['decision']} | {r1['decision_node']['reason'][:50]}")
    print(f"  [Action] {len(r1['action_node']['validation_plan']['phases'])}阶段 + Kill {len(r1['action_node']['kill_criteria'])}条")

    # 案例2: 火锅（重资产高技能）
    r2 = pipe.run({"category": "火锅", "process": "现煮", "product_form": "现煮类",
                   "price_band": [60, 90], "business_model": "堂食", "style": "川渝"},
                  budget=600000)
    print(f"\n■ {r2['inputs']['category']}")
    print(f"  [Reason]")
    for r in r2["reason_node"]:
        print(f"    {r['text'][:60]}")
    print(f"  [Decision] {r2['decision_node']['decision']} | {r2['decision_node']['reason'][:50]}")

    # 案例3: 无人宠物墓园（GPT P2 未知行业）
    r3 = pipe.run({"category": "无人宠物墓园", "process": "预包装", "product_form": "预包装/即食",
                   "price_band": [300, 800], "business_model": "连锁标准", "style": "服务"},
                  budget=150000)
    print(f"\n■ {r3['inputs']['category']}（未知行业）")
    print(f"  [Reason]")
    for r in r3["reason_node"]:
        print(f"    {r['text'][:60]}")
    print(f"  [Unknowns] 推理置信度 {r3['inference_confidence']}")
    for u in r3["unknowns"]:
        print(f"    ⚠️ {u}")
    print(f"  [Decision] {r3['decision_node']['decision']} | {r3['decision_node']['reason'][:50]}")
    print(f"\n  ✅ 未知行业同样走完整决策链（Ontology→Reason→Decision→Action）+ 诚实标注缺失数据")
