#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Validation Engine（验证战役引擎）V1.0
======================================
GPT 工业化清单 Sprint 5：90-Day Battle Plan
从"建议30天验证"升级为结构化验证战役。

结构（Schema V2.0 validation_plan）:
  Day 0-30   验证"有没有需求"  指标: 客流/转化/复购
  Day 31-60  验证"能不能赚钱"  指标: 毛利/人效/损耗
  Day 61-90  验证"能不能复制"  指标: SOP/人员替代/稳定性

每个阶段输出: 关键假设 / 验证方法 / 通过条件 / 失败条件 / 下一动作
"""
import json, datetime


class ValidationEngine:
    def __init__(self, category_config=None):
        self.category_config = category_config or {}

    def build_plan(self, project_id, category, business_model=None):
        """生成 90 天验证战役计划"""
        bm = business_model or {}
        return {
            "project_id": project_id,
            "category": category,
            "duration_days": 90,
            "phases": {
                "phase1": self._phase1(),
                "phase2": self._phase2(bm),
                "phase3": self._phase3(bm),
            },
            "principles": [
                "先验证需求，再验证盈利，最后验证复制",
                "每阶段有明确通过/失败条件，不模糊",
                "失败条件触发 → 进入 Kill Criteria（不硬撑）",
            ],
        }

    def _phase1(self):
        """Day 0-30: 验证需求"""
        return {
            "days": "0-30",
            "goal": "验证有没有需求（不是你以为的需求）",
            "key_assumption": "目标客群在目标价位有真实购买行为",
            "validation_methods": [
                "冷启动试卖（不装修不挂牌先测）",
                "现场转化率观察（路过→进店→购买漏斗）",
                "周边竞品客流时段记录",
            ],
            "metrics": ["客流", "转化率", "首单复购率"],
            "pass_criteria": ["日均客流≥X", "转化率≥Y%", "复购率≥Z%"],
            "fail_criteria": ["连续2周客流低于基线", "试卖期间日均亏损超上限"],
            "next_action": "通过→进入盈利验证；失败→触发 Kill Criteria",
        }

    def _phase2(self, bm):
        """Day 31-60: 验证盈利"""
        return {
            "days": "31-60",
            "goal": "验证能不能赚钱（单店经济模型成立）",
            "key_assumption": "毛利结构+固定成本支撑盈亏平衡（当前假设区间）",
            "validation_methods": [
                "完整记账（收入/成本/损耗分日）",
                "SKU 毛利实测（哪些赚钱哪些白干）",
                "人效测算（单人产能上限）",
            ],
            "metrics": ["毛利率", "人效", "损耗率", "日订单量"],
            "pass_criteria": ["毛利率≥X%", "日单量达到盈亏平衡点", "损耗率≤Y%"],
            "fail_criteria": ["毛利率持续低于假设", "日单量2周未达盈亏平衡的80%"],
            "next_action": "通过→进入复制验证；失败→收缩规模或退出",
        }

    def _phase3(self, bm):
        """Day 61-90: 验证复制"""
        return {
            "days": "61-90",
            "goal": "验证能不能复制（SOP 稳定+人员可替代）",
            "key_assumption": "经营可标准化，不依赖创始人个人在场",
            "validation_methods": [
                "SOP 文档化（每个岗位的操作标准）",
                "人员轮换测试（请假/换人仍能稳定出品）",
                "供应链压力测试（物料断供时有无替代）",
            ],
            "metrics": ["出品一致性", "人员替代天数", "SOP 覆盖率", "供应链稳定性"],
            "pass_criteria": ["SOP 覆盖核心岗位100%", "新人3天内可独立上岗", "出品波动率<5%"],
            "fail_criteria": ["依赖创始人个人技能无法替代", "核心物料无第二供应商"],
            "next_action": "通过→决定复制/扩店；失败→维持单店（不扩）",
        }

    def build_kill_criteria(self, budget, monthly_fixed_cost, survival_months=3):
        """Kill Criteria（Schema V2.0 kill_criteria：先定义退出条件再入场）"""
        return {
            "financial_stop": {
                "trigger": f"累计亏损达预算50%（{budget*0.5:.0f}元）",
                "action": "立即退出，不追加投资",
            },
            "monthly_loss_stop": {
                "trigger": f"单月亏损超 {monthly_fixed_cost*0.8:.0f} 元持续2个月",
                "action": "触发复核（收缩 or 退出）",
            },
            "validation_fail_stop": {
                "trigger": "任一阶段失败条件触发",
                "action": "按阶段 plan 的 next_action 执行",
            },
            "survival_floor": {
                "trigger": f"现金低于 {survival_months} 个月运营成本",
                "action": "停止投入（不硬撑到破产）",
            },
            "principle": "90天验证期是'验证'不是'赌博'——不达标即退",
        }


if __name__ == "__main__":
    print("=== Validation Engine V1.0 自检 ===")
    ve = ValidationEngine()
    plan = ve.build_plan("FDR-ZZ-FRIED-001", "炸鸡", {"model": "生炸档口"})

    print("\n[90天验证战役]")
    for phase, data in plan["phases"].items():
        print(f"\n  {data['days']} {data['goal']}")
        print(f"    关键假设: {data['key_assumption']}")
        print(f"    指标: {', '.join(data['metrics'])}")
        print(f"    通过: {'; '.join(data['pass_criteria'])}")
        print(f"    失败: {'; '.join(data['fail_criteria'])}")

    print("\n[Kill Criteria]")
    kill = ve.build_kill_criteria(200000, 15000)
    for k, v in kill.items():
        if isinstance(v, dict):
            print(f"  {k}: {v['trigger']} → {v['action']}")
        else:
            print(f"  {k}: {v}")
