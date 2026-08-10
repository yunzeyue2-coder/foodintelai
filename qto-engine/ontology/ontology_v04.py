#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Food Business Ontology V0.5（规则推导引擎，非品类套模板）
===========================================================
沧林修正（2026-08-10）：不要品类套模板，要所有品类思维。

旧（错误）: CATEGORY_BASE = {"炸鸡": {...}, "米线": {...}} —— 预设表，新品类要登记
新（正确）: 规则推导 —— 输入任意品类的基础属性（工艺/产品形态/价格带/经营模型），
           自动推导 消费画像+经营画像+供应链画像。炸鸡/米线只是输入样例。

推导规则（不是查找表）：
  工艺       → 技能依赖/设备依赖/标准化/风险
  产品形态   → 加工复杂度/出品速度/损耗敏感性
  价格带     → 投资水平/利润空间
  经营模型   → 人工强度/租金敏感/外卖依赖

验收: 任意新品类（如"烤冷面""螺蛳粉""炸串"）无需登记，输入基础属性即出画像。
"""
import json


class FoodBusinessOntology:
    # ============ 推导规则（工艺 → 工程属性）============
    PROCESS_RULES = {
        "生炸":     {"skill": 30, "equipment": 20, "standard": -20, "risk": 25},
        "裹粉":     {"skill": 15, "equipment": 25, "standard": 10,  "risk": 15},
        "现卤":     {"skill": 40, "equipment": 30, "standard": -30, "risk": 35},
        "小锅现煮": {"skill": 35, "equipment": 25, "standard": -25, "risk": 30},
        "烤制":     {"skill": 25, "equipment": 35, "standard": -10, "risk": 20},
        "炸串":     {"skill": 20, "equipment": 15, "standard": 5,   "risk": 18},
        "冲调/预制": {"skill": 5,  "equipment": 10, "standard": 40, "risk": 5},
        "预包装":   {"skill": 10, "equipment": 15, "standard": 35,  "risk": 10},
        "汤粉现煮": {"skill": 30, "equipment": 20, "standard": -15, "risk": 25},
        "拌粉/冷食": {"skill": 15, "equipment": 10, "standard": 20, "risk": 12},
        "烘焙":     {"skill": 45, "equipment": 40, "standard": -35, "risk": 30},
    }

    # ============ 推导规则（产品形态 → 加工复杂度/损耗）============
    PRODUCT_RULES = {
        "整只/大件":  {"processing": 40, "speed": 30, "loss": 35, "note": "备料耗时，损耗中等"},
        "切件/小块":  {"processing": 25, "speed": 45, "loss": 30, "note": "出品快，损耗中"},
        "汤粉类":     {"processing": 30, "speed": 35, "loss": 50, "note": "汤底保鲜，损耗高"},
        "拌粉/干拌":  {"processing": 20, "speed": 50, "loss": 25, "note": "出品快，损耗低"},
        "现煮类":     {"processing": 35, "speed": 25, "loss": 45, "note": "翻台慢，损耗高"},
        "预包装/即食": {"processing": 10, "speed": 60, "loss": 15, "note": "标准化高，损耗低"},
        "烤制类":     {"processing": 45, "speed": 20, "loss": 30, "note": "烤制耗时，翻台慢"},
        "炸制类":     {"processing": 25, "speed": 40, "loss": 28, "note": "现炸出品快"},
        "卤制类":     {"processing": 30, "speed": 35, "loss": 20, "note": "可批量预制，损耗低"},
        "饮品/杯装":  {"processing": 15, "speed": 55, "loss": 10, "note": "标准化高，损耗低"},
        "烤冷面/手抓饼": {"processing": 20, "speed": 50, "loss": 20, "note": "档口快出品"},
    }

    # ============ 推导规则（价格带 → 投资/利润空间）============
    def price_profile(self, price_low, price_high):
        """价格带 → 投资水平/利润空间（连续函数，不是查表）"""
        avg = (price_low + price_high) / 2
        return {
            "investment_level": max(10, min(90, avg * 3)),           # 客单价越高启动投入越高
            "margin_space": max(10, min(90, avg * 2.5)),              # 客单价越高毛利空间越大
            "price_position": "低客单" if avg < 12 else ("中客单" if avg < 25 else "高客单"),
        }

    # ============ 推导规则（经营模型 → 人工/租金/外卖）============
    def model_profile(self, business_model):
        """经营模型 → 人工强度/租金敏感/外卖依赖"""
        base = {"labor": 55, "rent_sensitive": 50, "delivery_depend": 40}
        modifiers = {
            "档口":   {"labor": -20, "rent_sensitive": -15, "delivery_depend": 20},
            "堂食":   {"labor": 15,  "rent_sensitive": 25,  "delivery_depend": -15},
            "堂食+外卖": {"labor": 10, "rent_sensitive": 15, "delivery_depend": 20},
            "外卖专营": {"labor": 0,  "rent_sensitive": -25, "delivery_depend": 55},
            "夫妻店": {"labor": -10, "rent_sensitive": 5,   "delivery_depend": 10},
            "连锁标准": {"labor": 20, "rent_sensitive": 10,  "delivery_depend": 15},
        }
        m = modifiers.get(business_model, {})
        return {
            "labor_intensity": max(10, min(90, base["labor"] + m.get("labor", 0))),
            "rent_sensitivity": max(10, min(90, base["rent_sensitive"] + m.get("rent_sensitive", 0))),
            "delivery_dependency": max(10, min(90, base["delivery_depend"] + m.get("delivery_depend", 0))),
        }

    # ============ 推导（核心：输入基础属性 → 三画像）============

    def build_profiles(self, inputs):
        """输入任意品类的基础属性 → 消费画像+经营画像+供应链画像。
        inputs: {
          category: "炸鸡"（仅标签，不参与推导——验证品类无关）
          process: "生炸" | "小锅现煮" | ...（工艺规则推导）
          product_form: "整只/大件" | "汤粉类" | ...（产品形态规则）
          price_band: [15, 20]（价格区间）
          business_model: "堂食+外卖" | "档口" | ...（经营模型）
          style: "中式"（可选，消费画像）
        }
        任何新品类：换 inputs 即可，无需登记。
        """
        process = inputs.get("process", "冲调/预制")
        product = inputs.get("product_form", "预包装/即食")
        price = inputs.get("price_band", [10, 15])
        model = inputs.get("business_model", "档口")

        pp = self.PROCESS_RULES.get(process, {"skill": 20, "equipment": 20, "standard": 0, "risk": 15})
        pr = self.PRODUCT_RULES.get(product, {"processing": 25, "speed": 40, "loss": 30, "note": ""})
        pc = self.price_profile(*price)
        mp = self.model_profile(model)

        # ---- 经营画像（规则组合，非查表）----
        skill = pp["skill"] + pr["processing"] * 0.4 + mp["labor_intensity"] * 0.2
        equipment = pp["equipment"] + (10 if pr["processing"] >= 35 else 0)
        standard = pp["standard"] + (30 if pr["speed"] >= 50 else 0) - pr["processing"] * 0.3
        loss = pr["loss"] + pc["investment_level"] * 0.05
        replication = pp["skill"] * 0.6 + pr["processing"] * 0.4 + mp["labor_intensity"] * 0.2
        risk = pp["risk"] + pr["loss"] * 0.3 + mp["delivery_dependency"] * 0.1

        operation = {
            "skill_dependency": round(max(5, min(95, skill))),
            "equipment_dependency": round(max(5, min(95, equipment))),
            "standardization_level": round(max(0, min(90, standard))),
            "investment_level": round(pc["investment_level"]),
            "labor_intensity": round(mp["labor_intensity"]),
            "loss_sensitivity": round(max(10, min(90, loss))),
            "replication_difficulty": round(max(10, min(95, replication))),
            "risk_level": round(max(5, min(95, risk))),
            "margin_space": round(pc["margin_space"]),
        }

        # ---- 供应链画像（规则推导）----
        supply = {
            "supply_complexity": "高" if equipment >= 30 else ("中" if equipment >= 20 else "低"),
            "material_perishability": "高" if pr["loss"] >= 40 else ("中" if pr["loss"] >= 25 else "低"),
            "supplier_dependency": "单源风险" if skill >= 35 else "多源可行",
            "product_speed_note": pr["note"],
        }

        # ---- 消费画像（标签化）----
        consumer = {
            "category": inputs.get("category", "未知"),
            "style": inputs.get("style", "未知"),
            "process": process,
            "product_form": product,
            "price_band": f"{price[0]}-{price[1]}元",
            "price_position": pc["price_position"],
        }

        return {
            "inputs": inputs,
            "consumer_profile": consumer,
            "operation_profile": operation,
            "supply_chain_profile": supply,
        }

    # ============ 复制路径（GPT 例子：工艺→设备→技能→标准化→复制难度→风险）============

    def replication_path(self, inputs):
        """输出复制难度 + 连锁化路径判断"""
        p = self.build_profiles(inputs)
        op = p["operation_profile"]
        chain = [
            ("工艺", inputs.get("process", "?")),
            ("设备依赖", f"{op['equipment_dependency']}/100"),
            ("技能依赖", f"{op['skill_dependency']}/100"),
            ("标准化程度", f"{op['standardization_level']}/100"),
            ("复制难度", f"{op['replication_difficulty']}/100"),
            ("创业风险", f"{op['risk_level']}/100"),
        ]
        verdict = "易复制（可连锁）" if op["replication_difficulty"] < 50 and op["skill_dependency"] < 40 else "难复制（适合单店/师徒制）"
        return {"path": chain, "verdict": verdict, "operation": op}


if __name__ == "__main__":
    print("=== Food Business Ontology V0.5（规则推导引擎）自检 ===")
    o = FoodBusinessOntology()

    # 验收1: 任意品类——炸鸡（生炸/整只/15-20元/堂食+外卖）
    print("\n[炸鸡·生炸]（输入样例）")
    r = o.replication_path({"category": "炸鸡", "process": "生炸", "product_form": "整只/大件",
                            "price_band": [15, 20], "business_model": "堂食+外卖", "style": "中式"})
    for step in r["path"]:
        print(f"  {step[0]}: {step[1]}")
    print(f"  → {r['verdict']}")

    # 验收2: 换品类——烤冷面（根本没登记过）
    print("\n[烤冷面]（未登记品类，直接推导）")
    r2 = o.replication_path({"category": "烤冷面", "process": "烤制", "product_form": "烤冷面/手抓饼",
                             "price_band": [8, 12], "business_model": "档口", "style": "东北"})
    for step in r2["path"]:
        print(f"  {step[0]}: {step[1]}")
    print(f"  → {r2['verdict']}")

    # 验收3: 换品类——螺蛳粉（汤粉类）
    print("\n[螺蛳粉·汤粉现煮]（未登记品类）")
    r3 = o.replication_path({"category": "螺蛳粉", "process": "汤粉现煮", "product_form": "汤粉类",
                             "price_band": [12, 18], "business_model": "堂食", "style": "广西"})
    for step in r3["path"]:
        print(f"  {step[0]}: {step[1]}")
    print(f"  → {r3['verdict']}")

    # 验收4: 三画像完整生成
    print("\n[三画像验证·烤冷面]")
    p = o.build_profiles({"category": "烤冷面", "process": "烤制", "product_form": "烤冷面/手抓饼",
                          "price_band": [8, 12], "business_model": "档口", "style": "东北"})
    print(f"  消费: {p['consumer_profile']}")
    print(f"  经营: {json.dumps(p['operation_profile'], ensure_ascii=False)}")
    print(f"  供应链: {p['supply_chain_profile']}")
    print(f"\n  ✅ 品类无关：烤冷面/螺蛳粉无需登记，规则直接推导")
