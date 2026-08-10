#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Sprint 1 验收③：FAS 品类无关性测试
====================================
FAS 的价值不是生成炸鸡框架，而是生成品类无关的决策树。
验收：炸鸡/米线/卤味/饮品/早餐 五品类，决策树都能生成且品类变量正确注入。
"""
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "fas"))
from fas_engine import FASE

# 五个品类的品类变量（Category Ontology 视角）
CATEGORIES = {
    "炸鸡": {
        "list": ["客单价", "炸制能力", "外卖适配", "SKU", "鸡肉供应", "复购", "连锁化"],
        "extra_questions": {
            "business": ["炸制技能依赖度？（生炸vs裹粉）", "半成品vs现场腌制供应链？"],
            "consumer": ["外卖占比 vs 堂食占比？"],
        },
    },
    "米线": {
        "list": ["汤底", "米粉形态", "早餐属性", "正餐属性", "地域心智", "客单", "配送半径", "标准化程度"],
        "extra_questions": {
            "business": ["汤底标准化程度？（现熬vs料包）", "米粉供应链稳定性？"],
            "consumer": ["早餐/正餐时段结构？", "地域心智强度？（云南/湖南/本地化）"],
            "market": ["品类边界？（米线vs米粉vs酸辣粉）"],
        },
    },
    "卤味": {
        "list": ["卤汤", "非遗属性", "锁鲜包装", "零售/堂食", "供应链", "复购", "区域心智"],
        "extra_questions": {
            "business": ["卤汤老卤资产价值？", "锁鲜包装成本结构？"],
            "consumer": ["零售带走 vs 堂食比例？", "卤味配酒/配饭场景？"],
            "market": ["品类边界？（卤味vs卤货vs凉菜）"],
        },
    },
    "饮品": {
        "list": ["季节波动", "原料成本", "出品速度", "杯型毛利", "连锁化", "外卖适配", "复购"],
        "extra_questions": {
            "business": ["季节SKU切换成本？", "原料冷链要求？"],
            "consumer": ["季节需求波动？（夏季冰饮/冬季热饮）", "价格敏感度？"],
            "market": ["品类边界？（奶茶vs果茶vs咖啡）"],
        },
    },
    "早餐": {
        "list": ["出餐速度", "时段集中", "客流峰谷", "卫生许可", "供应链", "复购", "外卖适配"],
        "extra_questions": {
            "business": ["早高峰出餐速度能否达标？", "宵夜/下午茶时段能否延伸？"],
            "consumer": ["通勤带走的场景占比？", "价格带锚点？（5-10元）"],
            "market": ["品类边界？（包子vs豆浆油条vs煎饼）"],
        },
    },
}

def run():
    print("═" * 60)
    print("Sprint 1 验收③ FAS 品类无关性测试（5品类）")
    print("═" * 60)
    fas = FASE()
    for cat, vars in CATEGORIES.items():
        fas.register_category_variables(cat, vars)

    results = []
    for cat in CATEGORIES:
        tree = fas.generate(cat, "郑州", "20万创业进入")
        branches = len(tree["branches"])
        q_total = sum(len(b["questions"]) for b in tree["branches"].values())
        cv = len(tree["meta"].get("category_variables", []))
        ok = branches == 4 and q_total >= 12 and cv >= 4
        results.append(ok)
        print(f"  {'✅' if ok else '❌'} {cat}: {branches}支 / {q_total}问 / 品类变量{cv}个")
        if not ok:
            for bid, b in tree["branches"].items():
                print(f"       [{b['label']}] {len(b['questions'])}问")

    print("\n" + "═" * 60)
    passed = sum(results)
    print(f"FAS 品类无关性: {passed}/5 通过")
    if passed == 5:
        print("→ 决策树生成与品类变量注入在 5 个品类上全部通用")
    else:
        print("→ 存在品类无法生成完整决策树，需检查变量注入")
    return passed == 5

if __name__ == "__main__":
    run()
