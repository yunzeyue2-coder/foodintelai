#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
行业插件协议（Industry Plugin Protocol）V1.0
=============================================
GPT 质量框架（2026-08-11）：青藤OS 不是一个大 Prompt，而是
  通用决策引擎（怎么判断） + 行业Ontology插件（判断什么）

通用引擎: Ontology规则推导 + DecisionGraph + Gates + Business Twin（品类无关）
行业插件: 定义该行业"关注什么变量"——餐饮/制造/零售/服务各有侧重

协议（插件 = JSON 配置，不是代码）:
{
  "plugin_id": "...",
  "industry": "餐饮/制造/零售/服务",
  "focus_variables": [...],      # 这个行业判断什么
  "weight_profile": {...},       # 变量权重
  "evidence_requirements": {...} # 该行业证据要求
}
"""
import json, os, sys


class IndustryPluginRegistry:
    """行业插件注册表——插件是 JSON 配置，引擎读取属性"""

    BUILTIN = {
        "餐饮": {
            "industry": "餐饮",
            "keywords": ["快餐", "小吃", "甜品", "咖啡", "火锅", "烧烤", "茶饮", "奶茶", "外卖"],
            "focus_variables": ["需求频率", "客单价", "坪效", "供应链", "人工", "复购", "标准化"],
            "weights": {"需求频率": 0.2, "客单价": 0.15, "坪效": 0.15, "供应链": 0.15,
                        "人工": 0.1, "复购": 0.15, "标准化": 0.1},
            "evidence_requirements": {
                "必查": ["周边竞品密度", "价格带分布", "商圈人流"],
                "可推理": ["复购率（无数据时用品类基准区间）"],
                "禁止": ["跨区域外推全局结论（无全量数据时）"],
            },
        },
        "制造": {
            "industry": "制造",
            "keywords": ["工厂", "加工", "生产", "供应链制造", "代工"],
            "focus_variables": ["产能", "设备", "良率", "订单", "库存", "现金流"],
            "weights": {"产能": 0.2, "设备": 0.15, "良率": 0.2, "订单": 0.15, "库存": 0.15, "现金流": 0.15},
            "evidence_requirements": {
                "必查": ["产能利用率", "良率基线", "订单能见度"],
                "可推理": ["设备折旧（区间）"],
                "禁止": ["用零售逻辑推导制造（坪效不适配）"],
            },
        },
        "零售": {
            "industry": "零售",
            "keywords": ["便利店", "超市", "专卖", "商超", "门店零售"],
            "focus_variables": ["选址", "周转", "SKU", "库存", "毛利"],
            "weights": {"选址": 0.25, "周转": 0.2, "SKU": 0.15, "库存": 0.2, "毛利": 0.2},
            "evidence_requirements": {
                "必查": ["选址评分", "SKU 周转天数", "毛利结构"],
                "可推理": ["损耗率区间"],
                "禁止": ["无库存数据推导周转"],
            },
        },
        "服务": {
            "industry": "服务",
            "keywords": ["洗车", "美容", "理发", "洗护", "健身", "托管", "驿站", "维修"],
            "focus_variables": ["位置依赖", "人工效率", "服务标准化", "复购频率", "资产强度"],
            "weights": {"位置依赖": 0.25, "人工效率": 0.2, "服务标准化": 0.2, "复购频率": 0.2, "资产强度": 0.15},
            "evidence_requirements": {
                "必查": ["位置流量", "单人产能", "服务时长"],
                "可推理": ["坪效区间"],
                "禁止": ["无位置数据推导选址"],
            },
        },
    }

    def __init__(self, plugin_dir=None):
        self.plugin_dir = plugin_dir
        self.plugins = dict(self.BUILTIN)

    def register(self, plugin_json):
        """注册自定义插件（JSON 配置）"""
        pid = plugin_json.get("plugin_id")
        if not pid:
            raise ValueError("插件必须含 plugin_id")
        self.plugins[pid] = plugin_json
        return pid

    def get(self, industry):
        """取行业插件（精确 + 模糊 + 关键词匹配）"""
        if industry in self.plugins:
            return self.plugins[industry]
        for pid, plug in self.plugins.items():
            plug_industry = plug.get("industry", pid)
            # 包含匹配
            if plug_industry in industry or industry in plug_industry:
                return plug
            # 关键词匹配
            for kw in plug.get("keywords", []):
                if kw in industry:
                    return plug
        return None

    def validate(self, industry):
        """校验行业是否可判断：有插件 = 有判断框架；无插件 = Unknown 诚实标注"""
        plug = self.get(industry)
        if plug:
            return {"ok": True, "plugin": plug["plugin_id"] if "plugin_id" in plug else list(self.plugins.keys())[0] if False else None,
                    "focus": plug["focus_variables"]}
        return {"ok": False, "reason": f"行业'{industry}'无插件——用通用引擎近似推导+标注 Unknowns"}


if __name__ == "__main__":
    print("=== 行业插件协议 V1.0 自检 ===")
    reg = IndustryPluginRegistry()

    # 1. 内置四行业
    for ind in ["餐饮", "制造", "零售", "服务"]:
        v = reg.validate(ind)
        plug = reg.get(ind)
        print(f"\n[{ind} 插件]")
        print(f"  关注: {plug['focus_variables']}")
        print(f"  权重: {plug['weights']}")

    # 2. 未登记行业 → 诚实标注
    print("\n[未知行业: 高炉炼钢]")
    v = reg.validate("高炉炼钢")
    print(f"  {'✅ 有插件' if v['ok'] else '⚠️ ' + v['reason']}")

    # 3. 自定义插件注册
    print("\n[注册自定义插件: 宠物服务]")
    custom = {
        "plugin_id": "PET_SERVICE",
        "industry": "宠物服务",
        "focus_variables": ["服务时长", "复购", "位置", "技能要求", "客单价"],
        "weights": {"服务时长": 0.2, "复购": 0.25, "位置": 0.2, "技能要求": 0.2, "客单价": 0.15},
        "evidence_requirements": {"必查": ["周边宠物密度", "服务价格带"]},
    }
    pid = reg.register(custom)
    print(f"  注册: {pid}")
    v = reg.validate("宠物洗护")
    print(f"  校验宠物洗护: {'✅ 有插件' if v['ok'] else '⚠️ ' + v['reason']}")
