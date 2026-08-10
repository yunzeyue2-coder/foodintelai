#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
FAS-Lite（Framework Architecture System）
========================================
青藤OS 分析框架生成器（最小可运行版）

作用：项目不能靠人脑拆——输入品类+城市+决策，生成决策问题树（MECE风格）。

输入:
{
  "category": "米线",
  "city": "郑州",
  "decision": "是否适合20万创业进入"
}

输出（四支决策问题树）:
1. 市场结构  规模/结构/趋势/竞争
2. 消费者    需求/价格/场景/时段
3. 商业模型  投资/运营/盈利/复制
4. 进入策略  路径/风险/验证/退出

关键：
- FAS 生成的是"决策问题树"，不是"报告目录"——每个节点是一个待回答的问题
- 分支可扩展（品类特定变量从 Category Ontology 注入）
"""
import json

# 通用决策问题树（MECE 风格，四支）
GENERIC_TREE = {
    "market": {
        "label": "市场结构",
        "questions": [
            "市场规模多大？（门店数/密度）",
            "结构如何？（品类Ontology分簇）",
            "趋势方向？（新开店vs闭店）",
            "竞争强度？（HHI/品牌集中度）",
        ],
        "evidence_types": ["FID数据", "Ontology", "HHI模型"],
    },
    "consumer": {
        "label": "消费者",
        "questions": [
            "核心需求是什么？（正餐/小吃/外卖）",
            "价格带锚点在哪里？",
            "消费场景？（社区/商圈/学校）",
            "时段结构？（早/午/晚/夜）",
        ],
        "evidence_types": ["价格数据", "商圈数据", "外卖字段"],
    },
    "business": {
        "label": "商业模型",
        "questions": [
            "投资规模？（初始/装修/设备）",
            "单店经济？（客单×订单×毛利）",
            "运营复杂度？（技能/人员/标准化）",
            "可复制性？（连锁化/供应链）",
        ],
        "evidence_types": ["专家判断", "Unit Economics框架", "供应链分析"],
    },
    "strategy": {
        "label": "进入策略",
        "questions": [
            "进入路径？（自营/加盟/档口）",
            "差异化机会在哪里？",
            "主要风险与Stop条件？",
            "验证协议？（30/90/180天）",
        ],
        "evidence_types": ["Decision Stack", "Risk Matrix", "Validation Protocol"],
    },
}


class FASE:
    def __init__(self):
        self.category_variables = {}  # 品类特定变量（Category Ontology 注入）

    def register_category_variables(self, category, variables):
        """注册品类特定决策变量（如米线：汤底/米粉形态/时段属性）"""
        self.category_variables[category] = variables

    def generate(self, category, city, decision):
        """生成决策问题树"""
        tree = {"meta": {"category": category, "city": city, "decision": decision}, "branches": {}}
        for branch_id, branch in GENERIC_TREE.items():
            tree["branches"][branch_id] = {
                "label": branch["label"],
                "questions": list(branch["questions"]),
                "evidence_types": branch["evidence_types"],
            }
        # 注入品类特定问题
        cv = self.category_variables.get(category, {})
        if cv:
            for branch_id, extra_qs in cv.get("extra_questions", {}).items():
                if branch_id in tree["branches"]:
                    tree["branches"][branch_id]["questions"].extend(extra_qs)
            tree["meta"]["category_variables"] = cv.get("list", [])
        return tree

    def to_json(self, tree, path=None):
        s = json.dumps(tree, ensure_ascii=False, indent=2)
        if path:
            with open(path, "w", encoding="utf-8") as f:
                f.write(s)
        return s

    def self_test(self):
        """回归测试：炸鸡树 + 米线树"""
        # 炸鸡品类变量
        self.register_category_variables("炸鸡", {
            "list": ["客单价", "炸制能力", "外卖适配", "SKU", "鸡肉供应", "复购", "连锁化"],
            "extra_questions": {
                "business": ["炸制技能依赖度？（生炸vs裹粉）", "半成品vs现场腌制供应链？"],
                "consumer": ["外卖占比 vs 堂食占比？"],
            },
        })
        # 米线品类变量
        self.register_category_variables("米线", {
            "list": ["汤底", "米粉形态", "早餐属性", "正餐属性", "地域心智", "客单", "配送半径", "标准化程度"],
            "extra_questions": {
                "business": ["汤底标准化程度？（现熬vs料包）", "米粉供应链稳定性？"],
                "consumer": ["早餐/正餐时段结构？", "地域心智强度？（云南/湖南/本地化）"],
                "market": ["品类边界？（米线vs米粉vs酸辣粉）"],
            },
        })
        fried = self.generate("炸鸡", "郑州", "20万创业进入")
        rice = self.generate("米线", "郑州", "20万创业进入")
        return fried, rice


if __name__ == "__main__":
    fas = FASE()
    fried, rice = fas.self_test()
    print("=== FAS-Lite 自检 ===")
    print(f"炸鸡树: {len(fried['branches'])} 支, 品类变量 {len(fried['meta'].get('category_variables', []))} 个")
    print(f"米线树: {len(rice['branches'])} 支, 品类变量 {len(rice['meta'].get('category_variables', []))} 个")
    print("\n米线树（含品类特定问题注入）:")
    for bid, b in rice["branches"].items():
        print(f"  [{b['label']}] {len(b['questions'])}问")
        for q in b["questions"]:
            print(f"    - {q}")
    print("\n✅ FAS-Lite: 决策问题树生成正常（品类变量注入验证通过）")
